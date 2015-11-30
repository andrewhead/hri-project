#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import numpy as np


logging.basicConfig(level=logging.INFO, format="%(message)s")


class Simplex(object):
    ''' Nelder-Mead method for numerically determining the optimum. '''

    def step(self, points, bounds=None):

        vertices = [p for p in points if p['type'] == 'vertex']
        sorted_vertices = sorted(vertices, key=lambda p: p['rank'])
        ranks = [p['rank'] for p in points]

        def add_point(type, value):
            points.append({
                'type': type,
                'value': np.round(value, 5).tolist(),
            })

        def replace_worst(new):
            points.remove(new)
            worst_index = points.index(sorted_vertices[-1])
            points[worst_index] = new
            new['type'] = 'vertex'

        if any([p['type'] == 'expansion' for p in points]):
            ref = [p for p in points if p['type'] == 'reflection'][0]
            exp = [p for p in points if p['type'] == 'expansion'][0]
            if exp['rank'] < ref['rank']:
                replace_worst(exp)
                points.remove(ref)
            else:
                replace_worst(ref)
                points.remove(exp)

        elif any([p['type'] == 'contraction' for p in points]):
            con = [p for p in points if p['type'] == 'contraction'][0]
            if con['rank'] < sorted_vertices[-1]['rank']:
                replace_worst(con)
            else:
                for v in sorted_vertices[1:]:
                    new_value = self.reduce(
                        np.array(sorted_vertices[0]['value']),
                        np.array(v['value'])
                    ).tolist()
                    v.clear()
                    v['type'] = 'vertex'
                    v['value'] = new_value
                points.remove(con)

        elif any([p['type'] == 'reflection' for p in points]):
            ref = [p for p in points if p['type'] == 'reflection'][0]
            if ref['rank'] == min(ranks):
                add_point('expansion', self.compute_expansion(vertices))
            elif ref['rank'] < sorted_vertices[-2]['rank']:
                replace_worst(ref)
            else:
                add_point('contraction', self.compute_contraction(vertices))
                points.remove(ref)

        if all([p['type'] == 'vertex' for p in points]) and \
                all(['rank' in p for p in points]):
            add_point('reflection', self.compute_reflection(points))

        sorted_points = sorted(
            [p for p in points if 'rank' in p],
            key=lambda p: p['rank']
            ) + [p for p in points if 'rank' not in p]

        known_rank = 1
        for p in sorted_points:
            if 'rank' in p:
                p['rank'] = known_rank
                known_rank += 1

        if bounds is not None:
            out_of_bounds = False
            for i, p in enumerate(sorted_points):
                for ai, axis in enumerate(bounds):
                    if 'rank' not in p:
                        value = p['value']
                        if value[ai] < axis[0] or value[ai] > axis[1]:
                            out_of_bounds = True
                            p['rank'] = i
            if out_of_bounds:
                sorted_points = self.step(sorted_points, bounds)

        return sorted_points

    def centroid(self, points):
        return np.average(points, axis=0)

    def reflect(self, worst, centroid, alpha=1):
        return centroid + (centroid - worst) * alpha

    def expand(self, worst, centroid, gamma=2):
        return centroid + (centroid - worst) * gamma

    def contract(self, worst, centroid, rho=-.5):
        return centroid + (centroid - worst) * rho

    def reduce(self, best, other, sigma=.5):
        return best + (other - best) * sigma

    def compute_reflection(self, vertices):
        return self.compute_next(
            np.array([v['value'] for v in vertices], dtype=np.float),
            [v['rank'] for v in vertices],
        )[0]

    def compute_expansion(self, vertices):
        return self.compute_next(
            np.array([v['value'] for v in vertices], dtype=np.float),
            [v['rank'] for v in vertices],
        )[1]

    def compute_contraction(self, vertices):
        return self.compute_next(
            np.array([v['value'] for v in vertices], dtype=np.float),
            [v['rank'] for v in vertices],
        )[2]

    def compute_next(self, vertices, vertex_ranks):

        worst_index = np.argmax(vertex_ranks)
        worst = vertices[worst_index]
        cent = self.centroid(vertices)

        reflection = self.reflect(worst, cent)
        expansion = self.expand(worst, cent)
        contraction = self.contract(worst, cent)
        return reflection, expansion, contraction, worst_index
