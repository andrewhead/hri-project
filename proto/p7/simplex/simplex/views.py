#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.http import HttpResponse


logging.basicConfig(level=logging.INFO, format="%(message)s")


def home(request):
    return HttpResponse("At home")


def update_vertices(request):
    return HttpResponse("Hello world!")


def get_next(request):
    return HttpResponse("Hello world!")
