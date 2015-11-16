#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from django.shortcuts import render


logging.basicConfig(level=logging.INFO, format="%(message)s")


def home(request):
    return render(request, 'fabexample/taskpicker.html', {})


def wait(request):
    return render(request, 'fabexample/wait.html', {})


def rate(request):
    return render(request, 'fabexample/rate.html', {})


def accept(request):
    return render(request, 'fabexample/accept.html', {})
