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
        pass
            

    def runForward(self, num):
        if num==0:
            outputRun = self._api.commWithResp('RUN')
            print('00RUN ' + str(outputRun))
        elif num==1:
            outputRun = self._api.commWithResp('02RUN')
            print('02RUN ' + str(outputRun))
        time.sleep(self.sleeptime)

    def runReverse(self, num):
        if num==0:
            outputRRun = self._api.commWithResp('RUNW')
            print('00RUN ' + outputRRun)
        elif num==1:
            outputRRun1 = self._api.commWithResp('02RUNW')
            print('02RUN ' + outputRRun1)
        time.sleep(self.sleeptime)

    def stop(self, num):
        if num==0:
            outputSTP = self._api.commWithResp('STP')
            print('00STP ' + str(outputSTP))
        elif num==1:
            outputSTP1 = self._api.commWithResp('02STP')
            print('02STP ' + str(outputSTP1))
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

    def setForwardRate(self, num, flowrate, units):
        commands = ['ULH', 'ULM', 'MLM']
        if num==1:
            num=2
        num_str = '0'+str(num)
        #rateOutput = self._api.commWithResp(num_str + commands[units] + ' ' + str(flowrate))
        rateOutput = self._api.commWithResp(commands[units] + ' ' + str(flowrate))
        print(num_str + commands[units] + ' ' + str(flowrate) + ' ' + str(rateOutput))
        time.sleep(self.sleeptime)

    def setReverseRate(self, num, flowrate, units):
        commands = ['ULHW', 'ULMW', 'MLMW']
        if num==1:
            num=2
        num_str = '0'+str(num)
        rRateOutput = self._api.commWithResp(num_str + commands[units] + ' ' + str(flowrate))
        print(num_str + commands[units] + ' ' + str(flowrate) + ' ' + str(rRateOutput))
        time.sleep(self.sleeptime)

    def setSyringeDiameter(self, num, diam):
        commands = [4.78, 8.66, 12.06, 14.50, 19.13, 21.7, 26.7]
        if num==1:
            num=2
        num_str = '0'+str(num)
        diamOutput = self._api.commWithResp(num_str + 'MMD ' + str(commands[diam]))
        print(num_str + 'MMD ' + str(commands[diam]) + str(diamOutput))
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

