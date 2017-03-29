#!/usr/bin/python
#
import inLib
import sys
import time
import numpy as np

class Control(inLib.Device):
    def __init__(self,settings):
        inLib.Device.__init__(self, 'thorlabs.thMotor_dll.thMotor_dll_api',settings)
        self.position = 0.

    def initServo(self):
        self._api.init_hardware()

    def goHome(self):
        self._api.go_home()

    def moveAbsolute(self, abs_pos):
        self._api.move_to(abs_pos)

    def moveRelative(self, rel_pos):
        self._api.move_by(rel_pos)

    def stepUp(self):
        self._api.jog_up()

    def stepDown(self):
        self._api.jog_down()

    def stepSize(self, stepsize):
        self._api.set_stepsize(stepsize)

    def currentPos(self):
        cpos = self._api.get_pos()
        return cpos

    def bl_correction(self,dest_position):
        self._api.bl_correction(dest_position)

    def shutDown(self):
        self._api.clean_up()

