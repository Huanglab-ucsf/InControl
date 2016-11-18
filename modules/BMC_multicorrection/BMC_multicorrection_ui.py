#!/usr/bin/python


from PyQt4 import QtGui,QtCore
import inLib
import numpy as np
from numpy.lib.scimath import sqrt as _msqrt
import copy
import time


class UI(inLib.ModuleUI):

    def __init__(self, control, ui_control):
        '''
        This is the initialization part of the UI.
        '''
        design_path = 'modules.BMC_multicorrection.BMC_multicorrection_design'
        print('design_path is:', design_path)
        inLib.ModuleUI.__init__(self, control, ui_control,  'modules.BMC_multicorrection.BMC_multicorrection_design')
        self._ui.pushButton_apply2mirror.clicked.connect(self.apply2mirror)
        self._ui.pushButton_acquire.clicked.connect(self.acquireImage)
        self._ui.pushButton_reset.clicked.connect(self.resetMirror)
        self._ui.pushButton_synthesize.clicked.connect(self.syncPattern)
        # done with initialization

    def apply2mirror(self):
        '''
        Apply the current pattern to mirror
        '''
        self._control.modulateDM('text.txt')

    def acquireImage(self):
        """
        acquire PSF or other images
        """
        dz = float(self._ui.lineEdit_dz.text()) # set the steps
        nSlices = self._ui.spinbox_Nsteps.value()
        center_xy = self._ui.checkBoxCenterLateral.isChecked()
        maskRadius = int(self._ui.lineEdit_mask.text())
        self._control.acquirePSF(range_, nSlices, nFrames, center_xy=True, filename=None,
                       mask_size = 40, mask_center = (-1,-1))
        pass # to be filled later


    def resetMirror(self):
        '''
        input an \n into the PIPE.
        '''
        self._control.advanceWithPipe()
        # done with reset Mirror


    def syncPattern(self):
        '''
        synthesize patterns.
        0. pass all the zernike coefficients to self.control.DM for zernike synthesis.
        1. create a pattern as self.control.raw_MOD
        2. display on the panel.
        '''
        pass


    def setZern(self):
        '''
        set single zernike
        '''
        item = self.table_Zcoeffs.item(0, 0)
        item.setText(_translate("Form", "3.3"))



    def clearPattern(self):
        '''
        Clear current pattern.
        '''




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
