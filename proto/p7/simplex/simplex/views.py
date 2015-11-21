#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.http import HttpResponse
from django.shortcuts import render


logging.basicConfig(level=logging.INFO, format="%(message)s")


def home(request):
    return render(request, 'simplex/home.html', {})


def update_vertices(request):
    return HttpResponse("Hello world!")


def get_next(request):
    return HttpResponse("Hello world!")
