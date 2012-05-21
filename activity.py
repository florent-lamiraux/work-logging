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

import datetime as dt

class TagError (BaseException) :
    pass

class Activity (object):
    """
    Atomic activity with a time and a list of tags that will enable users to
    sum up the time spent for given tags.
    An activity is included in a unique day
    """
    tags = set([])
    """
    The list of tags this activity is related to
    """
    startTime = None
    """
    Starting time of the activity: a datetime.datetime object
    """
    endTime = None
    """
    Ending time of the activity
    """
    description = ""

    nbMembers = 4
    """
    Number of members written in file for each activity
    """
    @staticmethod
    def listToDatetime (strDateAndTime) :
        if strDateAndTime == 'None':
            return None
        # parse starting time
        dateAndTime = strDateAndTime.split(' ')
        if len(dateAndTime) != 2 :
            raise (IOError("wrong starting date or time."))
        # parse date
        initList = map(int, dateAndTime[0].split('-'))
        if len(initList) != 3 :
            raise (IOError("wrong starting date."))
        #parse time
        listTime = map(int, dateAndTime[1].split(":")[:2])
        initList.extend(listTime)
        return dt.datetime(*initList)
    
    @staticmethod
    def fromList (l) :
        """
        Create an instance from a list of string
        """
        if len (l) != Activity.nbMembers :
            raise (IOError ("expect %d element, got %d."%
                            (Activity.nbMembers, len(l))))
        startTime = Activity.listToDatetime (l[0])
        endTime = Activity.listToDatetime (l[1])
        description = l[2]
        instanceTags = l[3].split('" "')
        instanceTags = map(lambda s : s.strip('"'), instanceTags)
        a = Activity()
        a.startTime = startTime
        a.endTime = endTime
        a.description = description
        for t in instanceTags:
            a.addNewTag(t)
        return a

    def __init__(self) :
        """
        Initialize starting time with current time
        """
        self.startTime = dt.datetime.now()
        self.instanceTags = set()
        
    def addTag(self, tag) :
        """
        Add a tag for this activity

          Tag must already be referenced in class set.
        """
        if tag not in Activity.tags :
            raise TagError\
                ("tag %s is unknown. Use addNewTag method for new tags"%tag)
        self.instanceTags.add (tag)
        
    def addNewTag(self, tag) :
        self.instanceTags.add (tag)
        Activity.tags.add(tag)

    def __str__(self) :
        string = "%s;%s;%s;"% (str(self.startTime), str(self.endTime),
                               self.description)
        for t in self.instanceTags :
            string += '"%s" '%t
        string = string[:-1:]
        return string

    def __le__(self, other) :
        return self.startTime <= other.startTime

    def __ge__(self, other) :
        return self.startTime >= other.startTime

    def __lt__(self, other) :
        return self.startTime < other.startTime

    def __gt__(self, other) :
        return self.startTime > other.startTime

    def write(self, f) :
        """
        Write in a file
        """
        f.write (str(self))

    @property
    def duration(self) :
        """
        Compute and return the duration of the activity
        """
        if self.endTime:
            result = self.endTime - self.startTime
        else:
            result = dt.timedelta(0)
        return result
