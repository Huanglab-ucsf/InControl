#!/usr/bin/python
#
# Active X based APTUser control.
#


from PyQt4 import QtCore, QtGui, QAxContainer

import sys
import time
import mgmotorAX

class API():
    def __init__(self):
        self.stage = mgmotorAX.APTUser1()
        #self.servo = mgmotorAX.APTUserTest
        #self.stage.show()
        self.servo = None

    def initServo(self):
        self.servo = mgmotorAX.APTUserTest()
        self.servo.show()

    def setStage(self, pos):
#        pass
        self.servo.moveTo(pos)
#        self.servo.show()

    def shiftStage(self, rpos):
        self.servo.moveBy(rpos)

    def jogUp(self):
        self.servo.jogUp()

    def jogDown(self):
        self.servo.jogDown()

    def setStepsize(self, dstep):
        self.servo.setStepsize(dstep)


    def shutDown(self):
        self.servo.stopControl()
        #self.stage.close()
