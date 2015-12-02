# this file imports custom routes into the experiment server

from flask import Blueprint, render_template, request, jsonify, abort, current_app

from psiturk.psiturk_config import PsiturkConfig
from psiturk.experiment_errors import ExperimentError
from psiturk.user_utils import PsiTurkAuthorization

# # Database setup
from psiturk.db import db_session
from psiturk.models import Participant
from json import loads
from functools import partial
import numpy as np
import cProfile
import itertools

from algorithms.simplex import Simplex
from algorithms.bayesopt import newton_rhapson, acquire, default_kernel, compute_H, compute_g


# load the configuration options
config = PsiturkConfig()
config.load_config()
myauth = PsiTurkAuthorization(config)  # if you want to add a password protect route use this

# explore the Blueprint
custom_code = Blueprint(
    'custom_code',
    __name__,
    template_folder='templates',
    static_folder='static'
)


@custom_code.route('/bayesopt', methods=['GET'])
def bayesopt():

    # The caller is responsible with updating comparisons.
    # They should be able to just upload the x and f as they were provided by the last
    # call to this URL.
    f = np.array(loads(request.args.get('f', '[]')), dtype=np.float)
    x = np.array(loads(request.args.get('x', '[]')), dtype=np.float)
    comparisons = np.array(loads(request.args.get('comparisons', '[]')), dtype=np.int)

    SIGMA = 10.0
    BOUNDS = np.array([
        [0.0, 4.0],
        [0.0, 4.0],
        [0.0, 4.0],
    ])
    KERNELFUNC = partial(default_kernel, a=-1)

    # Create extra bounds to rule out configurations that burned
    within_bounds = {}
    BURNING_CONFIGURATIONS = [
        (4, 0, 0),
        (4, 1, 0),
        (4, 0, 1),
        (4, 1, 1),
        (4, 1, 1),
        (3, 0, 2),
        (4, 0, 2),
        (4, 1, 2),
        (3, 0, 3),
        (4, 0, 3),
        (4, 1, 3),
        (3, 0, 4),
        (4, 0, 4),
        (4, 1, 4),
    ]
    keys = [_ for _ in itertools.product(range(5), range(5), range(5))]
    for k in keys:
        within_bounds[k] = (k not in BURNING_CONFIGURATIONS)

    def extrabounds(p):
        rounded = np.round(p).astype('int')
        rounded_key = tuple(rounded)
        return within_bounds[rounded_key]

    # If no parameters are given, initialize the data
    if f.shape == (0,):
        x = np.array([
            [1.0, 1.0, 1.0],
        ])
        f = np.array([
            [0.0],
        ])
        comparisons = np.array([])
        best_f_i = 0
        xbest = x[0]
        xnew = np.array([3.0, 3.0, 3.0])
    # Predict the next point for comparison
    else:
        prof = cProfile.Profile()
        f, Cmap = prof.runcall(
            newton_rhapson, x, f, comparisons, KERNELFUNC,
            compute_H, compute_g, SIGMA, maxiter=10)
        prof.dump_stats('code.profile')
        xnew = acquire(x, f, Cmap, BOUNDS, KERNELFUNC, extrabounds)
        best_f_i = np.argmax(f)
        xbest = x[best_f_i]

    # Add newest points to x and f
    x = np.array(x.tolist() + [xnew])
    f = np.array(f.tolist() + [[0.0]])

    return jsonify(**{
        'x': x.tolist(),
        'f': f.tolist(),
        'xbest': {
            'value': xbest.tolist(),
            'img': get_cut_image_name(*(xbest.tolist())),
            'index': best_f_i,
        },
        'xnew': {
            'value': xnew.tolist(),
            'img': get_cut_image_name(*(xnew.tolist())),
            'index': len(f) - 1,
        },
        'comparisons': comparisons.tolist()
    })


def get_cut_image_name(power, speed, ppi):

    SPEED_LEVEL_COUNT = 5
    PPI_LEVELS = [10, 32, 100, 316, 1000]

    row = int(round(power))
    col = int(round(speed))
    index = row * (SPEED_LEVEL_COUNT) + col

    basename = "{ppi}ppi_{index:02}.png".format(
        ppi=PPI_LEVELS[int(round(ppi))],
        index=index
    )
    path = "/static/images/cuts/" + basename
    return path


@custom_code.route('/rank', methods=['GET'])
def home():
    exemplar_index = int(request.args.get('exemplar', 1))
    ppi = exemplar_index / 25
    power = (exemplar_index - (ppi * 25)) / 5
    speed = exemplar_index % 5
    return render_template('rank.html', img=get_cut_image_name(power, speed, ppi))


@custom_code.route('/step', methods=['GET'])
def step():

    points = loads(request.args['points'])
    bounds_json = request.args.get('bounds', None)
    bounds = loads(bounds_json) if bounds_json is not None else None
    get_images = bool(request.args.get('get_images', None))

    if len(points) > 0:
        simplex = Simplex()
        new_points = simplex.step(points, bounds)
    else:
        new_points = [
            {'value': [0, 0, 0], 'type': 'vertex'},
            {'value': [0, 0, 4], 'type': 'vertex'},
            {'value': [0, 4, 0], 'type': 'vertex'},
            {'value': [4, 0, 0], 'type': 'vertex'},
        ]

    for p in new_points:
        if get_images and 'img' not in p:
            p['img'] = get_cut_image_name(*p['value'])

    return jsonify(**{'points': new_points})


'''
# example computing bonus
'''


@custom_code.route('/compute_bonus', methods=['GET'])
def compute_bonus():
    # check that user provided the correct keys
    # errors will not be that gracefull here if being
    # accessed by the Javascrip client
    if 'uniqueId' not in request.args:
        raise ExperimentError('improper_inputs')  # original author wants to change this line
    uniqueId = request.args['uniqueId']

    try:
        # lookup user in database
        user = Participant.query\
            .filter(Participant.uniqueid == uniqueId)\
            .one()
        user_data = loads(user.datastring)  # load datastring from JSON
        bonus = 0

        for record in user_data['data']:  # for line in data file
            trial = record['trialdata']
            if trial['phase'] == 'TEST':
                if trial['hit'] is True:
                    bonus += 0.02
        user.bonus = bonus
        db_session.add(user)
        db_session.commit()
        resp = {"bonusComputed": "success"}
        return jsonify(**resp)
    except Exception as e:
        current_app.logger.info("Error: %s", repr(e))
        abort(404)  # again, bad to display HTML, but...
