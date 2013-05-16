#!/usr/bin/python

import csv
import gdata.spreadsheet.text_db
import os
import subprocess
import sys
import time
from multiprocessing import Pool

from subprocess import Popen, PIPE

# Redo entries already in sheet?
redo = False

problems = [1, 2, 3, 4, 5]

key="0Au4zXzOoce8JdGFjZ0JBVTIxRmgzeEpZN0VFRVktb0E"

from password import user, password

dbname="paper"

client = gdata.spreadsheet.text_db.DatabaseClient(username=user, password=password)

db = client.GetDatabases(spreadsheet_key=key)[0]
tables = db.GetTables(name=dbname)
if len(tables) == 1:
    table = tables[0]
else:
    table = db.CreateTable(dbname, ['x', 'time'])

def timeit(cmd):
    stime = time.time()
    p = subprocess.Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    duration = time.time() - stime
    return_code = p.returncode

    if return_code != 0:
        duration = -1

    return duration, stderr

def run_method(x):

    print x

    # Delete any existing row
    qstr = "x==" + str(x)
    records = table.FindRecords(qstr)

    if redo:
        for row in records:
            row.Delete()
            go = True
    else:
        go = len(records) == 0

    if go:
        print "going"
        runtime, out = timeit("sleep " + str(x))
        print "aight"

        d = {'x': str(x), 'time': str(runtime)}
        ## Try a couple times to add the data
        for i in xrange(10):
             try:
                 print "adding", d
                 table.AddRecord(d)
                 break
             except:
                 print "Unexpected error:", sys.exc_info()[0]
                 time.sleep(i*10)

    else:
         # Don't make Google too mad.
         print "Skipping", x
         sys.stdout.flush()
         time.sleep(1)

pool = Pool()

pool.map(run_method, problems)


