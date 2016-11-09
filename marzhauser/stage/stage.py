#!/usr/bin/python
#
# RJM 7/31/2012
#

import inLib
import time
from PyQt4 import QtCore


class Control(inLib.Device):
    def __init__(self, settings):

        inLib.Device.__init__(self, 'marzhauser.stage.marzhauser', settings)

        self.storedLocations = []
        self.maxLocations = 10
        self.waitTime = 30

        self._goAbsThread = None

    def addLocation(self):
        xpos,ypos = self.whereStage()
        self.storedLocations.append((xpos,ypos))
        if len(self.storedLocations)>self.maxLocations:
            self.storedLocations = self.storedLocations[1:]
        return self.storedLocations

    def setWaitTime(self, wtime):
        self.waitTime = wtime

    def clearLocations(self):
        self.storedLocations = []

    def goToLocations(self, num):
        if num<len(self.storedLocations):
            xpos,ypos = self.storedLocations[num]
            self.goAbsoluteXY(xpos, ypos)

    def goAbsolute(self, x, y):
        #self._api.goAbsolute(x,y)
        self._goAbsThread = GoAbs(self._api, x, y)
        self._goAbsThread.start()

    def goAbsoluteXY(self, x, y):
        self.goAbsolute(x,y)

    def goRelative(self, dx, dy):
        self._api.goRelative(dx,dy)

    def position(self):
        x,y,z = self._api.position()
        return [x,y,z]

    def whereStage(self):
        x,y,z = self.position()
        return x,y

    def sawtooth(self, xy, movement, repeats, timedelay):
        if xy=='x':
            y = 0
            x = movement
        elif xy=='y':
            y = movement
            x = 0
        for i in range(repeats):
            self.goRelative(x,y)
            time.sleep(timedelay/1000.0)
            self.goRelative(-1*x,-1*y)
            time.sleep(timedelay/1000.0)

    def getSpeed(self):
        vx,vy,vz = self._api.velocity()
        return vx,vy

    def setSpeed(self, axis, speed):
        if axis=='x' or axis=='y':
            self._api.setVelocity(axis, speed)
        elif axis=='xy':
            self._api.setVelocity('x', speed)
            self._api.setVelocity('y', speed)

    def halt(self):
        self._api.stopAxes()

    def getStatus(self):
        stat = self.getStatusAxis()
        return stat

    def getStatusAxis(self):
        stat = self._api.getStatusAxis()
        return stat

    def shutDown(self):
        self._api.shutDown()

class GoAbs(QtCore.QThread):
    def __init__(self, api, xpos, ypos):
        QtCore.QThread.__init__(self)

        self.api = api
        self.xpos = xpos
        self.ypos = ypos

    def run(self):
        self.api.goAbsolute(self.xpos,self.ypos)
   
#
# Testing
#

#
# The MIT License
#
# Copyright (c) 2009 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

