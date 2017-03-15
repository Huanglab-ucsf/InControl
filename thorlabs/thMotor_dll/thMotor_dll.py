#!/usr/bin/python
#
import inLib
import sys
import time
import ctypes
import numpy as np

class Control(inLib.Device):
    def __init__(self,settings):
        inLib.Device.__init__(self, 'thorlabs.thMotor_dll.thMotor_dll_api',settings)
        self.position = 0.
