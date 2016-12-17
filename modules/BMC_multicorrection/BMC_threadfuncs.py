'''
Created by Dan on 12/15/2016.

'''

from PyQt4 import QtGui,QtCore
import numpy as np


class Scanner(QtCore.QThread):

    def __init__(self, control, range_, nSlices, nFrames, center_xy, fname, maskRadius, maskCenter):
        QtCore.QThread.__init__(self)

        self.control = control
        self.range_ = range_
        self.nSlices = nSlices
        self.nFrames = nFrames
        self.center_xy = center_xy
        self.fname = fname
        self.maskRadius = maskRadius
        self.maskCenter = maskCenter

    def run(self):
        self.control.acquirePSF(self.range_, self.nSlices, self.nFrames,
                                self.center_xy, self.fname,
                                self.maskRadius, self.maskCenter)
    # done with Scanner


class BL_correction(QtCore.QThread):
    '''
    Backlash correction
    '''
    def __init__(self, control, z_correct, z_start):
        QtCore.QThread.__init__(self)
        self.control = control
        self.z_correct = z_correct
        self.z_start = z_start
        print("Initialized!", self.z_correct, self.z_start)


    def run(self):
        self.control.positionReset(self.z_correct, self.z_start)
