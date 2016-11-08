#!/usr/bin/python
#
# Active X based APTUser control.
#
# Hazen 8/09
#

from PyQt4 import QtCore, QtGui, QAxContainer

import sys
import time


#class Cube405(QAxContainer.QAxObject):
#    def __init__(self, parent = None):
#        QAxContainer.QAxObject.__init__(self, parent)


class APTUser1(QAxContainer.QAxWidget):
    def __init__(self, parent = None):
        QAxContainer.QAxWidget.__init__(self, parent)
        self.setControl("MGMOTOR.MGMotorCtrl.1")
        self.dynamicCall('SetHWSerialNum(int)', 83854883)
        self.dynamicCall('StartCtrl()')

    def moveTo(self, pos):
        self.dynamicCall('MoveAbsoluteEx(int, double, double, bool)', 0, pos, 0.0, False)

class APTUser2(QAxContainer.QAxWidget):
    def __init__(self, parent = None):
        QAxContainer.QAxWidget.__init__(self, parent)
        self.setControl("MGMOTOR.MGMotorCtrl.1")
        self.dynamicCall('SetHWSerialNum(int)', 80834516)
        self.dynamicCall('StartCtrl()')

    def moveTo(self, pos):
        self.dynamicCall('SetAbsMovePos(int, int)', 0, pos)
        self.dynamicCall('MoveAbsolute(int, bool)', 0, True)

#
# Testing
#

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    aptUser = APTUser1()
    #aptUser.show()
    aptUser2 = APTUser2()
    #aptUser2.show()

    time.sleep(5)

    aptUser2.moveTo(60)
    time.sleep(4)
    aptUser2.moveTo(120)
    time.sleep(4)
    
    sys.exit(app.exec_())


#        params = QtCoreQVariant([
#        print self.dynamicCall('GetPosition_Position(int)', 0).toString()
#        self.dynamicCall('MoveAbsoluteEx(int, double, double, bool)', 0, 13.0, 0.0, False)
#        time.sleep(2)
#        self.dynamicCall('MoveAbsoluteEx(int, double, double, bool)', 0, 14.0, 0.0, False)
#        time.sleep(2)


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

