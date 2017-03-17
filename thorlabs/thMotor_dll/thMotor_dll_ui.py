import numpy as np

from PyQt4 import import QtCore, QtGui
import sys
import time

'''
This is the UI calling the thMotor_dll.py.
'''

class UI(inLib.DeviceUI):
    def __init__(self, control):
        design_path = 'thorlabs.thMotor_dll.thMotor_dll.design'
        inLib.DeviceUI.__init__(self, control, design_path)
        '''
        Here I should fill up a couple of definitations for buttons, lineEdits and other Qt gadgets. 
        '''

        def _move_to(self, pos = None):
            '''
            move the stage to a certain position, if pos = None, read from the line Edit.
            '''

        def _move_by(self, rpos = None):
            '''
            move the stage by rpos from current position. If rpos = None, read from the line Edit.
            '''

        def _stepsize(self, stp = None):
            '''
            reset the stepsize
            '''

        def bl_correction(self, dest, bl_range = 0.030):
            '''
            backlash correction
            '''

