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


        # =================================== query functions ===============================


    def _parse_commoutput_(self, output_comm):
        '''
        parse output command.
        '''

    def findPump(self):
        '''
        Send a query command to the terminal
        '''
        ver = self._api.commWithResp('VER') 
        return ver
            
    def getStatus(self):
        dia_str = self._api.commWithResp('DIA')
        print(dia_str)
        time.sleep(self.sleeptime)
        rat_str = self._api.commWithResp('RAT')
        print(rat_str)
        raw_str = self._api.commWithResp('RAT W')
        print(raw_str)
        vol_str = self._api.commWithResp('RAT')
        print(vol_str)
        status_raw = ''.join([dia_str, rat_str, raw_str, vol_str])
        status = ''.join(status_raw.split(':'))
        return status

        


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

    def setMax(self, direction):
        if direction ==0:
            outputMAX = self._api.commWithResp('MAX')
        elif direction ==1:
            self._api.commWithResp('MAXW')
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
        if '(' in diam_text:
            diam_num = diam_text.split('(')[1].split(')')[0]
            ser_command = 'MMD '+ diam_num

        else:
            ser_command = 'MMD '+diam_text
        diamOutput = self._api.commWithResp(ser_command)
        print(diamOutput)
        time.sleep(self.sleeptime)

    def clearTarget(self, direction):
        if direction ==0:
            outputCLT = self._api.commWithResp('CLT')
        else:
            outputCLT = self._api.commWithResp('CLTW')
        time.sleep(self.sleeptime)
        print(outputCLT)


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

