#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import sqlite3
import json
import os.path
import codecs


logging.basicConfig(level=logging.INFO, format="%(message)s")
QUESTION_FILE = os.path.join('data', 'answers.tsv')
BEST_FILE = os.path.join('data', 'best.tsv')
FINAL_BEST_FILE = os.path.join('data', 'final_best.tsv')
POINTS_FILE = os.path.join('data', 'points.tsv')
BASE_QUERY = 'SELECT * FROM image_discovery WHERE codeversion=3.0 AND workerId NOT LIKE "debug%"'
tsv = lambda *args: '\t'.join([str(a) for a in args]) + '\n'


# REUSE: from http://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


# Initialize the database cursor
conn = sqlite3.connect('participants.db')
conn.row_factory = dict_factory
c = conn.cursor()


def write_question_data():
    c.execute(BASE_QUERY)
    with codecs.open(QUESTION_FILE, 'w', encoding='utf8') as outfile:
        outfile.write(tsv("Worker", "Condition", "Counterbalance", "Key", "Value"))
        for r in c.fetchall():
            if r['datastring'] is not None:
                user_data = json.loads(r['datastring'])
                question_data = user_data['questiondata']
                for k, v in question_data.items():
                    outfile.write(tsv(r['workerid'], r['cond'], r['counterbalance'], k, v))


def write_simplex_final_best_data(file_, r, task_data):
    final_trials = filter(
        lambda task: task['trialdata']['phase'] in
        ["Simplex::Forced End", "Simplex::Success"],
        task_data)
    for trial in final_trials:
        best_trial = filter(lambda p: p['rank'] == 1, trial['trialdata']['points']['points'])[0]
        best = best_trial['value']
        file_.write(tsv(
            r['workerid'], r['cond'], r['counterbalance'],
            trial['trialdata']['phase'], best[0], best[1], best[2]
        ))


def write_simplex_best_data(file_, r, task_data):
    trials = filter(lambda task: task['trialdata']['phase'] == "Simplex::Choice", task_data)
    sorted_trials = sorted(trials, key=lambda t: t['current_trial'])
    for iteration, trial in enumerate(sorted_trials):
        best_trial = filter(lambda p: p['rank'] == 1, trial['trialdata']['points'])[0]
        best = best_trial['value']
        file_.write(tsv(
            r['workerid'], r['cond'], r['counterbalance'], trial['trialdata']['phase'],
            iteration, best[0], best[1], best[2]
        ))


def write_bayesopt_final_best_data(file_, r, task_data):
    trials = filter(
        lambda task: task['trialdata']['phase'] == "BayesOpt::Choice",
        task_data)
    if len(trials) >= 1:
        last_trial = sorted(trials, key=lambda t: t['current_trial'])[-1]
        last_choice = last_trial['trialdata']['data']['xBetter']['value']
        file_.write(tsv(
            r['workerid'], r['cond'], r['counterbalance'],
            last_trial['trialdata']['phase'], last_choice[0], last_choice[1], last_choice[2]
        ))


def write_bayesopt_best_data(file_, r, task_data):
    trials = filter(lambda task: task['trialdata']['phase'] == "BayesOpt::Choice", task_data)
    sorted_trials = sorted(trials, key=lambda t: t['current_trial'])
    for iteration, trial in enumerate(sorted_trials):
        choice = trial['trialdata']['data']['xBetter']['value']
        file_.write(tsv(
            r['workerid'], r['cond'], r['counterbalance'], trial['trialdata']['phase'],
            iteration, choice[0], choice[1], choice[2]
        ))


def write_final_best_data():
    c.execute(BASE_QUERY)
    with codecs.open(FINAL_BEST_FILE, 'w', encoding='utf8') as outfile:
        outfile.write(tsv("Worker", "Condition", "Counterbalance", "Phase", 'x1', 'x2', 'x3'))
        for r in c.fetchall():
            if r['datastring'] is not None:
                user_data = json.loads(r['datastring'])
                task_data = user_data['data']
                write_simplex_final_best_data(outfile, r, task_data)
                write_bayesopt_final_best_data(outfile, r, task_data)


def write_best_data():
    c.execute(BASE_QUERY)
    with codecs.open(BEST_FILE, 'w', encoding='utf8') as outfile:
        outfile.write(tsv(
            "Worker", "Condition", "Counterbalance", "Phase", "Iteration", 'x1', 'x2', 'x3'))
        for r in c.fetchall():
            if r['datastring'] is not None:
                user_data = json.loads(r['datastring'])
                task_data = user_data['data']
                write_simplex_best_data(outfile, r, task_data)
                write_bayesopt_best_data(outfile, r, task_data)


def write_simplex_points(file_, r, task_data):
    trials = filter(lambda task: task['trialdata']['phase'] == "Simplex::Choice", task_data)
    sorted_trials = sorted(trials, key=lambda t: t['current_trial'])
    indices_seen = []
    for trial in sorted_trials:
        points = trial['trialdata']['points']
        for p in points:
            index = p['index']
            value = p['value']
            if index not in indices_seen:
                indices_seen.append(index)
                file_.write(tsv(
                    r['workerid'], r['cond'], r['counterbalance'], trial['trialdata']['phase'],
                    index, value[0], value[1], value[2]
                ))


def write_bayesopt_points(file_, r, task_data):
    trials = filter(lambda task: task['trialdata']['phase'] == "BayesOpt::Choice", task_data)
    if len(trials) >= 1:
        last_trial = sorted(trials, key=lambda t: t['current_trial'])[-1]
        X = last_trial['trialdata']['data']['x']
        for i, x in enumerate(X):
            file_.write(tsv(
                r['workerid'], r['cond'], r['counterbalance'],
                last_trial['trialdata']['phase'], i, x[0], x[1], x[2]
            ))


def write_points():
    c.execute(BASE_QUERY)
    with codecs.open(POINTS_FILE, 'w', encoding='utf8') as outfile:
        outfile.write(tsv(
            "Worker", "Condition", "Counterbalance", "Phase", "Index", 'x1', 'x2', 'x3'))
        for r in c.fetchall():
            if r['datastring'] is not None:
                user_data = json.loads(r['datastring'])
                task_data = user_data['data']
                write_simplex_points(outfile, r, task_data)
                write_bayesopt_points(outfile, r, task_data)


def main():
    write_question_data()
    write_final_best_data()
    write_best_data()
    write_points()


if __name__ == '__main__':
    main()
