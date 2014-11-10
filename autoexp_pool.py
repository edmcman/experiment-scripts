#!/usr/bin/env python

from multiprocessing import Pool
import autoexp
import sys

pool = Pool()

# By specifying a timeout, keyboard interrupts are processed.
# See http://stackoverflow.com/a/1408476/670527
pool.map_async(autoexp.run_and_process, autoexp.inputs).get(sys.maxint)

