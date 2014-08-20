#!/usr/bin/env python

import sys
import glob
import yaml
from analyser.source import dbreader as src
from analyser.experiment import *
from analyser.configuration import *

def runExperiments(db, table, field, experiment):
    dbreader = src.SqliteDBReader(db)
    data = dbreader.read(field, table, experiment)

    print 'Run experiments ...'
    for experiment in Experiment.getAll():
        experiment.execute(data)


if len(sys.argv) < 2 or sys.argv[1] == '--help':
    print "usage: %s [--default | --help | --scenario  <scenario-file> ]" % sys.argv[0]
    sys.exit()

if sys.argv[1] == '--default':
    db = 'resources/scout-monitor.db'
    table = 'scout_telemetry'
    fields = ['actual_joint_current_4']
    experiments = [ '9c9b041e-0f7e-4d26-8ea8-12c95ff5ff77' ]
    resultdir = "results"

elif sys.argv[1] == '--scenario':
    config = Configuration(sys.argv[2])
    # Since paths can be relative in the files
    db = config.db
    table = config.table
    fields = config.fields
    experiments = config.experiments
    resultdir = config.resultDir
else:
    print "usage: %s [--default | --help | --scenario  <scenario-file> ]" % sys.argv[0]
    sys.exit()

print 'Select analysis experiments ...'
Experiment.load()

for experiment in experiments:
    for field in fields:
        labels = [ experiment, field ]
        Experiment.setOutputDirectory(resultdir, labels)
        runExperiments(db, table, field, experiment)