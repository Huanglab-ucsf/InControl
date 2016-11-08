#!/usr/bin/python
#
# Coherent OBIS laser control
#

import inLib
import time


class Control(inLib.Device):
    def __init__(self, settings):

        ports = settings['ports']

        inLib.Device.__init__(self, 'coherent.RS232_test', settings, ports)

        self.num_ports = len(ports)

        self.laser_lines = []
        self.power_range = []

        if not(len(self._api.tty) == self.num_ports):
            print "Not all lasers available..."

        for i in range(0,self.num_ports):
            laser_wavelength = self.getWavelength(i)
            self.laser_lines.append(laser_wavelength)
            pow_range = self.getPowerRange(i)
            self.power_range.append(pow_range)
            

    def setCDRHDelay(self, port, state):
        if state==0:
            self._api.sendCommand(port, "SYST:CDRH OFF")
            self._api.waitResponse(port)
        elif state==1:
            self._api.sendCommand(port, "SYST:CDRH ON")
            self._api.waitResponse(port)

    def getOperatingMode(self, port):
        self._api.sendCommand(port, "SOUR:AM:SOUR?")
        resp = self._api.waitResponse(port).rsplit('\r\n')
        return resp[0]

    def getWavelength(self, port):
        self._api.sendCommand(port, "SYST:INF:WAV?")
        resp = self._api.waitResponse(port).rsplit('\r\n')
        return int(resp[0])

    def getBaseTemperature(self, port):
        self._api.sendCommand(port, "SOUR:TEMP:BAS?")
        resp = self._api.waitResponse(port).rsplit('\r\n')
        return float(resp[0])

    def getEmissionOnOff(self, port):
        self._api.sendCommand(port, "SOUR:AM:STAT?")
        resp = self._api.waitResponse().rsplit('\r\n')
        if resp[0] == 'ON':
            return 1
        else:
            return 0
        
    def getPowerRange(self, port):
        self._api.sendCommand(port, "SOUR:POW:LIM:HIGH?")
        resp = self._api.waitResponse(port).rsplit('\r\n')
        pmax = float(resp[0])
        self._api.sendCommand(port, "SOUR:POW:LIM:LOW?")
        resp = self._api.waitResponse(port).rsplit('\r\n')
        pmin = float(resp[0])
        return [pmin, pmax]

    def getPower(self):
        self._api.sendCommand(port, "SYST:POW:LEV:IMM:AMPL?")
        power_string = self._api.waitResponse(port).rsplit('\r\n')
        return float(power_string[0])

    def setExtControl(self, port, mode):
        '''
        Mode can be DIG (digital modulation), ANAL (analog),
        or MIX (analog plus digital)
        '''
        if mode == "DIG" or mode == "ANAL" or mode == "MIX":
            self._api.sendCommand(port, "SOUR:AM:EXT " + mode)
        self._api.waitResponse(port)

    def setInternalCW(self,port):
        self._api.sendCommand(port, "SOUR:AM:INT CWP")
        self._api.waitResponse(port)

    def setLaserOnOff(self, port, on):
        if on:
            self._api.sendCommand(port, "SOUR:AM:STAT ON")
            self._api.waitResponse(port)
        if (not on):
            self._api.sendCommand(port, "SOUR:AM:STAT OFF")
            self._api.waitResponse(port)

    def setPower(self, port, power_in_mw):
        if power_in_mw > self.power_range[port][1]:
            power_in_mw = self.power_range[port][1]
        self._api.sendCommand(port, "SOUR:POW:LEV:IMM:AMPL " + str(power_in_mw))
        self._api.waitResponse(port)

    def _powerInMW(self, port, powerFraction):
        powerRange = self.power_range[port][1] - self.power_range[port][0]
        return (powerFraction*powerRange)+self.power_range[port][0]

    def shutDown(self):
        for i in range(0,self.num_ports):
            self.setLaserOnOff(i, False)
            self.setInternalCW(i)

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

