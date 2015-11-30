#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import unittest

from algorithms.simplex import Simplex


logging.basicConfig(level=logging.INFO, format="%(message)s")


class StepTest(unittest.TestCase):

    def setUp(self):
        self.simplex = Simplex()

    def test_step_to_get_reflect_when_only_vertexes_given(self):
        points = [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [3.0, 0], 'rank': 3, 'type': 'vertex'},
        ]
        new_points = self.simplex.step(points)
        self.assertEqual(new_points, [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [3.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [1.0, 0], 'type': 'reflection'},
        ])

    def test_reflect_when_better_than_second_worst(self):
        points = [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [1.0, 0], 'rank': 2, 'type': 'reflection'},
            {'value': [2.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [3.0, 0], 'rank': 4, 'type': 'vertex'},
        ]
        new_points = self.simplex.step(points)
        self.assertEqual(new_points, [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [1.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [0.66667, 0], 'type': 'reflection'},
        ])

    def test_get_expansion_when_reflection_is_best(self):
        points = [
            {'value': [1.0, 0], 'rank': 1, 'type': 'reflection'},
            {'value': [1.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [3.0, 0], 'rank': 4, 'type': 'vertex'},
        ]
        new_points = self.simplex.step(points)
        self.assertEqual(new_points, [
            {'value': [1.0, 0], 'rank': 1, 'type': 'reflection'},
            {'value': [1.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [3.0, 0], 'rank': 4, 'type': 'vertex'},
            {'value': [0.0, 0], 'type': 'expansion'},
        ])

    def test_expand_when_expansion_is_best(self):
        points = [
            {'value': [0.0, 0], 'rank': 1, 'type': 'expansion'},
            {'value': [1.0, 0], 'rank': 2, 'type': 'reflection'},
            {'value': [1.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 4, 'type': 'vertex'},
            {'value': [3.0, 0], 'rank': 5, 'type': 'vertex'},
        ]
        new_points = self.simplex.step(points)
        self.assertEqual(new_points, [
            {'value': [0.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [1.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [0.0, 0], 'type': 'reflection'},
        ])

    def test_reflect_when_reflection_better_than_expansion(self):
        points = [
            {'value': [1.0, 0], 'rank': 1, 'type': 'reflection'},
            {'value': [0.0, 0], 'rank': 2, 'type': 'expansion'},
            {'value': [1.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 4, 'type': 'vertex'},
            {'value': [3.0, 0], 'rank': 5, 'type': 'vertex'},
        ]
        new_points = self.simplex.step(points)
        self.assertEqual(new_points, [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [1.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [0.66667, 0], 'type': 'reflection'},
        ])

    def test_get_contraction_when_reflection_is_worst(self):
        points = [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [3.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [1.0, 0], 'rank': 4, 'type': 'reflection'},
        ]
        new_points = self.simplex.step(points)
        self.assertEqual(new_points, [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [3.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [2.5, 0], 'type': 'contraction'},
        ])

    def test_contract_when_contraction_is_better_than_worst(self):
        points = [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [2.5, 0], 'rank': 3, 'type': 'contraction'},
            {'value': [3.0, 0], 'rank': 4, 'type': 'vertex'},
        ]
        new_points = self.simplex.step(points)
        self.assertEqual(new_points, [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [2.5, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [1.16667, 0], 'type': 'reflection'},
        ])

    def test_reduce_when_contraction_is_worst(self):
        points = [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [2.0, 0], 'rank': 2, 'type': 'vertex'},
            {'value': [3.0, 0], 'rank': 3, 'type': 'vertex'},
            {'value': [2.5, 0], 'rank': 4, 'type': 'contraction'},
        ]
        new_points = self.simplex.step(points)
        self.assertEqual(new_points, [
            {'value': [1.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [1.5, 0], 'type': 'vertex'},
            {'value': [2.0, 0], 'type': 'vertex'},
        ])

    def test_skip_out_of_bounds_points_reflection_and_expansion(self):
        points = [
            {'value': [0.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [0.0, 2.0], 'rank': 2, 'type': 'vertex'},
            {'value': [1.0, 1.0], 'rank': 3, 'type': 'vertex'},
        ]
        new_points = self.simplex.step(points, bounds=[[0, 1], [0, 1]])
        self.assertEqual(new_points, [
            {'value': [0.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [0.0, 2.0], 'rank': 2, 'type': 'vertex'},
            {'value': [1.0, 1.0], 'rank': 3, 'type': 'vertex'},
            {'value': [0.66667, 1.0], 'type': 'contraction'},
        ])

    def test_skip_out_of_bounds_points_expansion_only(self):
        points = [
            {'value': [0.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [0.0, 2.0], 'rank': 2, 'type': 'vertex'},
            {'value': [1.0, 1.0], 'rank': 3, 'type': 'vertex'},
            {'value': [-0.33333, 1.0], 'rank': 4, 'type': 'reflection'},
        ]
        new_points = self.simplex.step(points, bounds=[[-0.5, 1], [0, 1]])
        self.assertEqual(new_points, [
            {'value': [0.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [0.0, 2.0], 'rank': 2, 'type': 'vertex'},
            {'value': [1.0, 1.0], 'rank': 3, 'type': 'vertex'},
            {'value': [0.66667, 1.0], 'type': 'contraction'},
        ])

    def test_normal_behavior_if_no_bounds(self):
        points = [
            {'value': [0.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [0.0, 2.0], 'rank': 2, 'type': 'vertex'},
            {'value': [1.0, 1.0], 'rank': 3, 'type': 'vertex'},
        ]
        new_points = self.simplex.step(points)
        self.assertEqual(new_points, [
            {'value': [0.0, 0], 'rank': 1, 'type': 'vertex'},
            {'value': [0.0, 2.0], 'rank': 2, 'type': 'vertex'},
            {'value': [1.0, 1.0], 'rank': 3, 'type': 'vertex'},
            {'value': [-0.33333, 1.0], 'type': 'reflection'},
        ])
