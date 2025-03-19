#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
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

import sys, os, time
import datetime as dt
from work_sheet import WorkSheet, readFile
from activity import Activity, TagError

filename = os.getenv('HOME')+"/.activity"
partition = os.getenv('HOME')+"/.activity-partition"

if __name__ == '__main__':
    now = dt.datetime.now()
    w = readFile (filename, partition)
    if len(w) == 0:
        raise RuntimeError(".activity file is empty.")
    aOld = w[-1]
    if aOld.endTime:
        #No pending activity, resume lattest one
        aNew = Activity()
        aNew.startTime = now
        aNew.description = aOld.description
        aNew.instanceTags = aOld.instanceTags
        print ("Resume %s" % aNew.description)
    else:
        aOld.endTime = now
        print ("Finished: %s" % aOld.description)
        print ("Previous activities:")
        for a in w[-3:]:
            print(a)
        print("Starting new activity.")
        aNew = Activity()
        aNew.startTime = now
        print("Please write description:")
        aNew.description = sys.stdin.readline()[:-1]
        tagInput = True
        print("Do you want to add a tag ? (y/n) ")
        while sys.stdin.readline() == 'y\n':
            tag = sys.stdin.readline()[:-1]
            try :
                aNew.addTag(tag)
            except TagError as exc:
                print("This tag is new. Confirm ? (y/n)")
                if sys.stdin.readline() == 'y\n':
                    aNew.addNewTag(tag)
            print("Do you want to add a tag ? (y/n) ")
    w.add(aNew)
    w.write(filename)
    time.sleep(2.)
