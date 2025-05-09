#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010, 2011 CNRS
# Author: Florent Lamiraux
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:

# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os, sys, time
import datetime as dt
from work_sheet import WorkSheet, readFile, workToday, workThisWeek
from activity import Activity, TagError

def displayStatistics(w):
    """
    Display statistics

      Input: a WorkSheet object
    """
    total = w.totalTime
    print ("Total time: %f" % total)
    for p in Activity.partition:
        try:
            t = w.extractUnion([p,]).totalTime
            line = "  " + p + ":" + (30 - len (p))*" " + "\t" + "%.2f"%t +\
                "\t" + "%.2f"%(t/total*100) + "%"
            print (line)
        except:
            pass

if __name__ == '__main__':
    filename = os.getenv ('HOME') + "/.activity"
    partition = filename + "-partition"
    w = readFile(filename, partition)
    displayStatistics(w)
    print ("")
    print ("Today: %f" % workToday(filename, partition).totalTime)
    print ("This week: %f" % workThisWeek(filename, partition).totalTime)
