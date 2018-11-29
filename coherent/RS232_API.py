#!/usr/bin/python
#
# Hazen 3/09
# edited by Dan on 06/04/18, replaced uspp with the more up-to-date serial library.

#import uspp.uspp as uspp
import time
import serial


class API():
    def __init__(self, ports, timeout=None,
                 baudrate=19200, end_of_line="\r", wait_time=0.05):
        self.tty = []
        self.live = []
        num_of_ports = len(ports)
        print("Ports:", ports)
        self.end_of_line = end_of_line
        for i in range(0,num_of_ports):
            print(ports[i])
            try:
                print("import new laser:")
                ser = serial.Serial(ports[i], baudrate, timeout=timeout) 
                print("new port:", ser)
                self.tty.append(ser)
                #self.tty.append(uspp.SerialPort(ports[i], timeout, baudrate))
                self.wait_time = wait_time
                time.sleep(self.wait_time)
                #self.tty[i].flush()
                time.sleep(self.wait_time)
                self.live.append(1)
            except:
                print("Error importing laser:", ports[i])
                self.live.append(0)

    def commWithResp(self, port_num, command):
        print(port_num)
        self.tty[port_num].flush()
        self.tty[port_num].write(command + self.end_of_line)
        time.sleep(10 * self.wait_time)
        response = ""
        response_len = self.tty[port_num].inWaiting()
        while response_len:
            response += self.tty[port_num].read(response_len)
            time.sleep(self.wait_time)
            response_len = self.tty[port_num].inWaiting()
        if len(response) > 0:
            return response

    def sendCommand(self, port_num, command):
        self.tty[port_num].flush()
        self.tty[port_num].write((command + self.end_of_line).encode())

    def shutDown(self):
        print("RS232 shutDown")
        del(self.tty)

    def getResponse(self, port_num):
        response = ""
        response_len = self.tty[port_num].inWaiting()
        while response_len:
            response += self.tty[port_num].read(response_len).decode()
            time.sleep(self.wait_time)
            response_len = self.tty[port_num].inWaiting()
        if len(response) > 0:
            return response

    def getStatus(self, port_num):
        return self.live[port_num]

    def waitResponse(self, port_num, end_of_response = 0, max_attempts = 200):
        if not end_of_response:
            end_of_response = str(self.end_of_line)
        attempts = 0
        response = ""
        index = -1
        while (index == -1) and (attempts < max_attempts):
            response_len = self.tty[port_num].inWaiting()
            if response_len > 0:
                response += self.tty[port_num].read(response_len).decode()
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

