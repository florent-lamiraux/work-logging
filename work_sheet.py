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

import sys, time
import csv
import datetime as dt
from activity import Activity, TagError

class CsvDialectComma (csv.Dialect) :
    def __init__(self):
        self.quotechar = '#'
        self.delimiter = ','
        self.quoting = csv.QUOTE_NONE
        self.lineterminator = '\n'
        csv.Dialect.__init__(self)

class CsvDialectSemiColon (csv.Dialect) :
    def __init__(self):
        self.quotechar = '#'
        self.delimiter = ';'
        self.quoting = csv.QUOTE_NONE
        self.lineterminator = '\n'
        csv.Dialect.__init__(self)

class WorkSheet (object) :
    """
    List of activities
    """
    
    def __init__ (self) :
        self.activities = []

    def add(self, activity) :
        """
        Add an activity to the time sheet
        """
        if not isinstance(activity, Activity) :
            raise TypeError("expecting an object of type Activity: got %s"%
                            repr(activity))
        if len (activity.instanceTags.intersection (Activity.partition)) != 1:
            raise RuntimeError ("activity should contain one and only one " +
                                "element of partition.")
        self.activities.append(activity)

    def write(self, filename) :
        """
        Write the work sheet in a file
        """
        self.sort()
        with open(filename, 'w') as f :
            f.write(str(self))

    def read(self, filename) :
        """
        Read a work sheet in a file
        """
        
        with open(filename, 'rb') as f :
            reader = csv.reader(f, dialect = CsvDialectSemiColon())
            ln = 0
            for row in reader :
                ln += 1
                try:
                    a = Activity.fromList(row)
                    self.add(a)
                except Exception as exc:
                    raise IOError("error at line %d: %s"%(ln,str(exc)))

    def sort(self) :
        self.activities.sort()
        
    def __add__ (self, other):
        res = WorkSheet ()
        res.activities = self.activities + other.activities
        return res

    def __str__(self) :
        string = ""
        for a in self.activities :
            string += str(a)+'\n'
        return string

    def __getitem__(self, key) :
        return self.activities[key]
    
    def __len__(self) :
        return len(self.activities)

    def checkTags(self, tagSet) :
        """
        Check that given set of tags is included in class set
        """
        if not isinstance(tagSet, set):
            raise TagError("%s is not a set." % tagSet)
        for tag in tagSet :
            if tag not in Activity.tags:
                raise TagError("'%s' is not a known tag." % tag)

    def extractUnion(self, tags) :
        """
        Extract activities related to given set of tags.
        
          Return a work sheet containing the selected activities
          """
        tagSet = set(tags)
        self.checkTags(tagSet)
        w = WorkSheet()
        w.activities = filter(lambda x : 
                              not tagSet.isdisjoint(x.instanceTags) and
                              not x.endTime is None,
                              self.activities)
        return w

    def extractInter(self, tags) :
        """
        Extract activities related to all tags in a given set.

          Return a work sheet containing the selected activities.
        """
        tagSet = set(tags)
        self.checkTags(tagSet)
        self.checkTags(tagSet)
        w = WorkSheet()
        w.activities = filter(lambda x :
                                  tagSet.issubset(x.instanceTags) and
                              not x.endTime is None,
                              self.activities)
        return w


    @property
    def totalTime(self):
        """
        Return total time in hours
        """
        time = reduce(lambda x,y: x+y.duration, self.activities,
                        dt.timedelta(0))
        return time.days*24 + time.seconds/3600.

    def extract(self, predicate) :
        """
        Return a new worksheet containing activities satisfying a predicate

          Input:
            - a predicate.
        """
        w = WorkSheet()
        w.activities = filter(predicate, self.activities)
        return w

    def extractBetween(self, start, end) :
        """
        Extract activities starting between two datetime objects
        """
        return self.extract(lambda x : start <= x.startTime <= end)

    def extractDay(self, year, month, day) :
        """
        Extract activities starting a given day
        """
        init = dt.datetime(year = year, month = month, day = day)
        end = init + dt.timedelta(days=1)
        predicate = lambda x: init <= x.startTime <= end
        return self.extract(predicate)

    def extractMonth(self, year, month) :
        """
        Extract activities starting a given month

          Input:
            - year:  integer
            - month: integer between 1 and 12.
        """
        init = dt.datetime(year = year, month = month, day=1)
        if month < 12:
            end = dt.datetime(year = year, month = month + 1, day=1)
        else:
            end = dt.datetime(year = year+1, month = 1, day=1)
        predicate = lambda x: init <= x.startTime <= end
        return self.extract(predicate)

    def totalTimeByTag(self):
        result = {}
        tags = set()
        for a in self.activities:
            tags = tags.union(a.instanceTags)
        for t in tags:
            result[t] = self.extractInter(set([t])).totalTime
        return result

    def check (self):
        for a1, a2 in zip (self.activities, self.activities [1:]):
            if (a1.endTime > a2.startTime or
                a1.duration < dt.timedelta(0,0) or
                a1.duration > dt.timedelta(1, 0)):
                print ("{0}:\t {1}".format (a1.startTime, a1.description))

def readFile (filename, partition) :
    """
    Read $HOME/.activity file and return the correponding work sheet
    """
    Activity.readPartition (partition)
    w = WorkSheet()
    w.read(filename)
    return w

def workToday(filename, partition) :
    w = readFile(filename, partition)
    now = dt.datetime.now()
    if w[-1].endTime is None:
        w[-1].endTime = now
    return w.extractDay(year = now.year, month = now.month, day = now.day)

def workThisWeek(filename, partition) :
    w = readFile(filename, partition)
    now = dt.datetime.now()
    if w[-1].endTime is None:
        w[-1].endTime = now
    thisMorning = dt.datetime(year = now.year,
                              month = now.month,
                              day = now.day,
                              hour=0, minute=0, second=0, microsecond=0)
    mondayMorning = thisMorning + dt.timedelta(days=-now.weekday())
    return w.extractBetween(mondayMorning, now)

def workThisMonth(filename, partition) :
    w = readFile(filename, partition)
    now = dt.datetime.now()
    if w[-1].endTime is None:
        w[-1].endTime = now
    beginning = dt.datetime(year = now.year,
                            month = now.month,
                            day = 1,
                            hour=0, minute=0, second=0, microsecond=0)
    return w.extractBetween(beginning, now)
