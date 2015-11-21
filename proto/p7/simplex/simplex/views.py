#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.http import JsonResponse
from django.shortcuts import render
import numpy as np
import json

from simplex import SimplexExecutor


logging.basicConfig(level=logging.INFO, format="%(message)s")
simplex_executor = SimplexExecutor()


def home(request):
    return render(request, 'simplex/home.html', {})


def update_vertices(request):
    print request.GET
    print np.array(json.loads(request.GET.get('vertices'))),
    print np.array(request.GET.getlist('vertex_ranks[]')),
    print request.GET.get('reflection_rank'),
    print request.GET.get('expansion_rank'),
    print request.GET.get('contraction_rank'),
    updated_vertices = simplex_executor.update_points(
        np.array(json.loads(request.GET.get('vertices'))),
        np.array([int(_) for _ in request.GET.getlist('vertex_ranks[]')]),
        int(request.GET.get('reflection_rank')),
        int(request.GET.get('expansion_rank')),
        int(request.GET.get('contraction_rank')),
    )
    return JsonResponse({
        'vertices': updated_vertices.tolist(),
    })


def get_next(request):
    vertices = json.loads(request.GET.get('vertices'))
    vertex_ranks = request.GET.getlist('vertex_ranks[]')
    reflection, expansion, contraction = simplex_executor.get_next_points(
        np.array(vertices),
        np.array(vertex_ranks),
    )
    return JsonResponse({
        'reflection': reflection.tolist(),
        'expansion': expansion.tolist(),
        'contraction': contraction.tolist(),
    })
