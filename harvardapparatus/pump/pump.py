#!/usr/bin/python
#
# RJM 7/24/2012
#

import inLib
import time


class Control(inLib.Device):
    def __init__(self, settings):

        port = settings['port']

        inLib.Device.__init__(self, 'harvardapparatus.RS232_API', settings, port)

        time.sleep(1.5)

        self.sleeptime = 1.0

        #oldRate keeps track of the last flowrate used, first value being pump 0, second being pump 1, etc.
        self.oldRate = 0

    def findPump(self):
        '''
        Send a query command to the terminal
        '''
        ver = self._api.commWithResp('VER') 
        print(ver)
        return ver
            

    def run(self, direction):
        '''
        Updated
        '''
        command_str = ['RUN', 'RUNW']
        outputRun = self._api.commWithResp(command_str[direction])
        time.sleep(self.sleeptime)
        print(outputRun)


    def stop(self):
        '''
        Updated
        '''
        outputSTP = self._api.commWithResp('STP')
        print(outputSTP)
        time.sleep(self.sleeptime)

    def setMaxForwardRate(self, num):
        if num==0:
            outputMAX = self._api.commWithResp('MAX')
            print('00MAX ' + outputMAX)
        elif num==1:
            self._api.commWithResp('02MAX')
            print('02MAX ' + outputMAX)
        time.sleep(self.sleeptime)

    def setMaxReverseRate(self, num):
        if num==0:
            outputMAXW = self._api.commWithResp('MAXW')
            print('00MAXW ' + outputMAXW)
        elif num==1:
            outputMAXW1self._api.commWithResp('02MAXW')
            print('02MAXW ' + outputMAXW)
        time.sleep(self.sleeptime)

    def setRate(self, rate, units, direction):
        '''
        Updated
        '''
        if direction == 0:
            d_str = units + ' '
        else:
            d_str = units + 'W '
        ser_command = d_str + str(rate)
        print(ser_command)
        rateOutput = self._api.commWithResp(ser_command) 
        print(rateOutput)
        time.sleep(self.sleeptime)

    def setVolume(self, vol, direction):
        '''
        Updated
        '''
        if direction == 0:
            ser_command = 'ULT ' + str(vol)
        else:
            ser_command = 'ULTW ' + str(vol) 
        rateOutput = self._api.commWithResp(ser_command) 
        print(rateOutput)

    def setDiameter(self, diam_text):
        '''
        Updated
        '''
        ser_command = 'MMD '+diam_text
        diamOutput = self._api.commWithResp(ser_command)
        print(diamOutput)
        time.sleep(self.sleeptime)

    def clearForwardRate(self, num):
        if num==0:
            outputCLT = self._api.commWithResp('00CLT')
            print('00CLT ' + outputCLT)
        elif num==1:
            otuputCLT1 = self._api.commWithResp('02CLT')
            print('02CLT ' + outputCLT1)
        time.sleep(self.sleeptime)

    def clearReverseRate(self, num):
        if num==0:
            outputCLTW = self._api.commWithResp('00CLTW')
            print('00CLTW ' + outputCLTW)
        elif num==1:
            outputCLTW1 = self._api.commWithResp('02CLTW')
            print('02CLTW ' + outputCLTW1)
        time.sleep(self.sleeptime)

    def setAndRun(self, num, flowrate, units):
        if num==1:
            num=2
        num_str = '0'+str(num)
        commands = ['ULH', 'ULM', 'MLM']
        
        if flowrate != self.oldRate:
            if flowrate == 0:
                outputSTP = self._api.commWithResp(num_str + 'STP')
                print(num_str + 'STP' + str(outputSTP))
                self.oldRate = flowrate
                time.sleep(self.sleeptime)
            else:
                rateOutput = self._api.commWithResp(num_str + commands[units] + ' ' + str(flowrate))
                print(num_str + commands[units] + ' ' + str(flowrate) + ' ' + str(rateOutput))
                time.sleep(self.sleeptime)
                outputRun = self._api.commWithResp(num_str + 'RUN')
                print(num_str +'RUN' + str(outputRun))
                self.oldRate = flowrate
                time.sleep(self.sleeptime)

    def shutDown(self):
        outputRun = self._api.commWithResp('00STP')
        print('00STP ' + str(outputRun))
        outputRun = self._api.commWithResp('02STP')
        print('02STP ' + str(outputRun))
                
'''
ULM: uL per minute
MLM: mL per minute
ULH: uL per hour
'''
   
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

