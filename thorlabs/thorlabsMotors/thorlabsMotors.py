#!/usr/bin/python
#
import inLib
import sys
import time

class Control(inLib.Device):
    def __init__(self, settings):
        inLib.Device.__init__(self, 'thorlabs.thorlabsMotors.thorlabsMotors_api', settings)
        self.position = 0.

    def initServo(self):
        self._api.initServo()

    def jogUp(self):
        self._api.jogUp()

    def jogDown(self):
        self._api.jogDown()

    def shiftStage(self, rpos):
        self._api.shiftStage(rpos)

    def setStage(self, pos):
        self._api.setStage(pos)

    def setStep(self, pos):
        '''
        This should be tested for the real step size
        '''
        dpos = int(pos*10)
        print(dpos)
        self._api.setStepsize(dpos)

    def shutDown(self):
        self._api.shutDown()
