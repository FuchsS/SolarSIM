#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Time conversion

Author: Stefan Fuchs
Website: 
Last modified: April 2017
'''

# A class to handle the time ranges
class timeHoursSeconds(object):
    def __init__(self, s, h, d, y):
        self.s = s
        self.h = h
        self.d = d
        self.y = y
    def secondsToHours(self):
        h = self.s/60/60
        return h
    def secondsToDays(self):
        d = self.s/60/60/24
        return d
    def secondsToYears(self):
        y = self.s/60/60/24/365
        return y
    def daysToSeconds(self):
        s = self.d*24*60*60
        return s
    def daysToHours(self):
        h = self.d * 24
        return h
    def daysToYears(self):
        y = self.d/365
        return y
    def yearsToSeconds(self):
        s = self.y*365*24*60*60
        return s
    def yearsToHours(self):
        h = self.y*365*24
        return h
