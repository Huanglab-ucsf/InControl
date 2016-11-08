#!/usr/bin/python
#
# ASI Stage Control (MS-2000)
#

import inLib
import time
import numpy as np

class Control(inLib.Device):
    def __init__(self, settings):

        port = settings['port']

        timeout=None
        baudrate=settings['baudrate']
        end_of_line = "\r"
        wait_time = 0.05

        apiSettings = {'port': port,
                       'timeout': timeout,
                       'baudrate': baudrate,
                       'eol': end_of_line,
                       'wt': wait_time}

        inLib.Device.__init__(self, 'asi.RS232', settings, apiSettings)

        self._api.sendCommand("BU X")
        resp = self._api.waitResponse()
        print "resp bu: ", resp

        self.storedLocations = []
        self.maxLocations = 10

        self.waitTime = 30

    def addLocation(self):
        xpos, ypos = self.whereStage()
        self.storedLocations.append((xpos,ypos))
        if len(self.storedLocations)>self.maxLocations:
            self.storedLocations = self.storedLocations[1:]
        return self.storedLocations

    def setWaitTime(self, wtime):
        self.waitTime = wtime

    def saveLocations(self, filename):
        np.savetxt(filename, self.storedLocations)

    def loadLocations(self, filename):
        #print "Loading locations from ", filename
        locations = np.loadtxt(filename)
        #print "Read locations: ", locations
        self.storedLocations = locations[:self.maxLocations]
        #print "Returning storedLocations: ", self.storedLocations
        return self.storedLocations

    def returnWaitTime(self):
        return self.waitTime

    def clearLocations(self):
        self.storedLocations = []

    def goToLocations(self, num):
        if num<len(self.storedLocations):
            xpos,ypos = self.storedLocations[num]
            self.goAbsoluteXY(xpos, ypos)
        

    def whereStage(self):
        self._api.sendCommand("W X Y")
        resp = self._api.waitResponse()
        resp_split = resp.split(' ')
        #print "resp_split: ", resp_split
        if len(resp_split)==4:
            xpos = resp_split[1]
            ypos = resp_split[2].rstrip('\n')
            return float(xpos),float(ypos)
        else:
            return 0,0

    def getStatus(self):
        self._api.sendCommand("/")
        resp = self._api.waitResponse()
        #print "get status: ", resp
        return resp.rstrip('\n').lstrip(' ')

    def goAbsolute(self, axis, value):
        if axis=='x':
            self._api.sendCommand("M X=%.2f" % value)
            resp = self._api.waitResponse()
        elif axis=='y':
            self._api.sendCommand("M Y=%.2f" % value)
            resp = self._api.waitResponse()

    def goAbsoluteXY(self, xval, yval):
        self._api.sendCommand("M X=%.2f Y=%.2f" % (xval, yval))
        resp = self._api.waitResponse()
        

    def goRelative(self, axis, value):
        if axis=='x':
            self._api.sendCommand("R X=%.2f" % value)
            resp = self._api.waitResponse()
        if axis=='y':
            self._api.sendCommand("R Y=%.2f" % value)
            resp = self._api.waitResponse()

    def getSpeed(self):
        self._api.sendCommand("S X? Y?")
        resp = self._api.waitResponse()
        print "resp: ", resp
        resp_split = resp.split(' ')
        print "resp_split: ", resp_split
        if len(resp_split)==4:
            xspeed = resp_split[1].lstrip('X=')
            yspeed = resp_split[2].lstrip('Y=')
            return float(xspeed), float(yspeed)
        else:
            return 0,0

    def setSpeed(self, axis, speed):
        if axis=='x':
            self._api.sendCommand("S X=%.2f" % speed)
        elif axis=='y':
            self._api.sendCommand("S Y=%.2f" % speed)
        elif axis=='xy':
            self._api.sendCommand("S X=%.2f Y=%.2f" % (speed,speed))
        resp=self._api.waitResponse()
        #print "Set speed response: ", resp

    def setRScan(self, start, stop):
        self._api.sendCommand("NR X=%.2f Y=%.2f" % (start, stop))
        self._api.waitResponse()

    def setVScan(self, start, stop, lines):
        self._api.sendCommand("NV X=%.2f Y=%.2f Z=%.2f" % (start, stop, lines))
        self._api.waitResponse()

    def startScan(self, xscan, yscan, fpattern):
        if (xscan is None )and (yscan is None):
            self._api.sendCommand("SN")
        elif fpattern is None:
            self._api.sendCommand("SN X=%i Y=%i" % (xscan, yscan))
        else:
            self._api.sendCommand("SN X=%i Y=%i F=%i" % (xscan, yscan, fpattern))
        self._api.waitResponse()

    def halt(self):
        self._api.sendCommand("HALT")
        resp = self._api.waitResponse()

    def shutDown(self):
        print "Shutting down..."

#
# Testing
#

if __name__ == "__main__":
    cube = Cube405()
    if cube.getStatus():
        print cube.getPowerRange()
        print cube.getLaserOnOff()
        power = 2.0
        while power < 3.0:
            cube.setPower(power)
            time.sleep(0.5)
            print cube.getPower()
            power += 0.1


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

