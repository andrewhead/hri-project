# this file imports custom routes into the experiment server

from flask import Blueprint, render_template, request, jsonify, abort, current_app
from jinja2 import TemplateNotFound
# from flask import Response
# from functools import wraps
# from sqlalchemy import or_

from psiturk.psiturk_config import PsiturkConfig
from psiturk.experiment_errors import ExperimentError
from psiturk.user_utils import PsiTurkAuthorization
# from psiturk.user_utils import nocache

# # Database setup
from psiturk.db import db_session
from psiturk.models import Participant
from json import loads
# from psiturk.db import init_db
# from json import dumps

from algorithms.simplex import Simplex

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


###########################################################
#  serving warm, fresh, & sweet custom, user-provided routes
#  add them here
###########################################################


'''
# example custom route
'''


@custom_code.route('/my_custom_view')
def my_custom_view():
    current_app.logger.info("Reached /my_custom_view")  # Print message to server.log for debugging
    try:
        return render_template('custom.html')
    except TemplateNotFound:
        abort(404)


'''
# example using HTTP authentication
'''


@custom_code.route('/my_password_protected_route')
@myauth.requires_auth
def my_password_protected_route():
    try:
        return render_template('custom.html')
    except TemplateNotFound:
        abort(404)


'''
# example accessing data
'''


@custom_code.route('/view_data')
@myauth.requires_auth
def list_my_data():
    users = Participant.query.all()
    try:
        return render_template('list.html', participants=users)
    except TemplateNotFound:
        abort(404)


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
    path = "static/images/cuts/" + basename
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
