#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import random
import os
import os.path


logging.basicConfig(level=logging.INFO, format="%(message)s")
NUM_POINTS = 30
DATA_DIR = 'data'
UNLABELED_FILE = os.path.join(DATA_DIR, 'unlabeled.dat')
LABELED_FILE = os.path.join(DATA_DIR, 'labeled.dat')


def main():

    # Generate random points
    # Label as '1' if above the line y=x, and '0' if below
    points = []
    for _ in range(NUM_POINTS):
        point = {
            'x': random.random(),
            'y': random.random(),
        }
        point['label'] = 1 if point['y'] > point['x'] else 0
        points.append(point)

    # Make data dir
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Write out two data files: one unlabeled and one labeled
    with open(UNLABELED_FILE, 'w') as ufile, open(LABELED_FILE, 'w') as lfile:
        for i, p in enumerate(points):
            unlabeled_line = "'pt{idx} | x:{x:.2f} y:{y:.2f}\n".format(idx=i, x=p['x'], y=p['y'])
            labeled_line = '{label} {rest}'.format(label=p['label'], rest=unlabeled_line)
            ufile.write(unlabeled_line)
            lfile.write(labeled_line)


if __name__ == '__main__':
    main()
