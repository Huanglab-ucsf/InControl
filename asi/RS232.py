#!/usr/bin/python
#
# Wraps the uspp library for RS232 communication.
#
# Hazen 3/09
#

import uspp.uspp as uspp
import time

class API():
    def __init__(self, apiSettings):
        print "apiSettings: ", apiSettings
        try:
            self.tty = uspp.SerialPort(apiSettings['port'],
                                       apiSettings['timeout'],
                                       apiSettings['baudrate'])
            self.tty.flush()
            self.end_of_line = apiSettings['eol']
            self.wait_time = apiSettings['wt']
            self.live = 1
            time.sleep(self.wait_time)
        except:
            self.live = 0
            print "Unable to connect to ASI stage..."

    def commWithResp(self, command):
        self.tty.flush()
        self.tty.write(command + self.end_of_line)
        time.sleep(10 * self.wait_time)
        response = ""
        response_len = self.tty.inWaiting()
        while response_len:
            response += self.tty.read(response_len)
            time.sleep(self.wait_time)
            response_len = self.tty.inWaiting()
        if len(response) > 0:
            return response

    def sendCommand(self, command):
        self.tty.flush()
        self.tty.write(command + self.end_of_line)

    def shutDown(self):
        print "RS232 shutDown"
        del(self.tty)

    def getResponse(self):
        response = ""
        response_len = self.tty.inWaiting()
        while response_len:
            response += self.tty.read(response_len)
            time.sleep(self.wait_time)
            response_len = self.tty.inWaiting()
        if len(response) > 0:
            return response

    def getStatus(self):
        return self.live

    def waitResponse(self, end_of_response = 0, max_attempts = 200):
        if not end_of_response:
            end_of_response = str(self.end_of_line)
        attempts = 0
        response = ""
        index = -1
        while (index == -1) and (attempts < max_attempts):
            response_len = self.tty.inWaiting()
            if response_len > 0:
                response += self.tty.read(response_len)
            time.sleep(0.1 * self.wait_time)
            index = response.find(end_of_response)
            attempts += 1
        return response


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

