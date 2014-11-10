#!/usr/bin/python
# Example experiment script that generates random data representing
# the time it takes to type a particular word.  The results are
# uploaded to a google docs spreadsheet.

# Authors: Ed Schwartz and Thanassis Avgerinos

import csv
import gdata.spreadsheet.text_db
import os
import random
import string
import subprocess
import sys
import time

from subprocess import Popen, PIPE

# Redo entries already in sheet?
redo = False

trials = 20

names = ["ed", "thanassis"]
inputs = reduce(list.__add__, map(lambda n: map(lambda num: {"name": n, "num": num}, xrange(trials)), names))
print inputs

# Input columns
ids = ["name", "num"]
# Measurement (output) columns
measured = ["time"]

from password import key, user, password

# Change this to the name of the worksheet you want to use
dbname="paper"

client = gdata.spreadsheet.text_db.DatabaseClient(username=user, password=password)

db = client.GetDatabases(spreadsheet_key=key)[0]
tables = db.GetTables(name=dbname)
if len(tables) == 1:
    table = tables[0]
else:
    table = db.CreateTable(dbname, ids + measured)

def timeit(cmd):
    stime = time.time()
    p = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    duration = time.time() - stime
    return_code = p.returncode

    if return_code != 0:
        duration = -1

    return duration, stderr

def quote_if_needed(x):
    x = str(x)
    if x.isdigit():
        return x
    else:
        return "\"" + x + "\""

def run_experiment(inputs):

    # Check for existing rows
    query_strs = map(lambda column: column + " == " + quote_if_needed(inputs[column]), ids)
    query_str = string.join(query_strs, " and ")
    #print query_str

    records = table.FindRecords(query_str)
    #print records

    if redo:
        for row in records:
            row.Delete()
            go = True
    else:
        go = len(records) == 0

    if go:
        runtime, out = timeit("sleep " + str(random.normalvariate(len(inputs["name"]), 1.0)))

        measurements = {"time": runtime}

        # Add input columns
        m = map(lambda column: (column, str(inputs[column])), ids)
        # Add measurement columns
        m = m + map(lambda column: (column, str(measurements[column])), measured)
        d = dict(m)

        process_results(d)

    else:
         # Don't make Google too mad.
         print "Skipping", inputs
         sys.stdout.flush()
         time.sleep(1)

def process_results(d):
    ## Try a couple times to add the data
    for i in xrange(10):
        try:
            print "adding", d
            table.AddRecord(d)
            break
        except:
            print "Unexpected error:", sys.exc_info()[0]
            time.sleep(i*10)
