#!/usr/bin/python


from PyQt4 import QtGui,QtCore
import inLib
import numpy as np
from numpy.lib.scimath import sqrt as _msqrt
import copy
import time
import libtim.zern as lzern

class UI(inLib.ModuleUI):

    def __init__(self, control, ui_control):
        '''
        This is the initialization part of the UI.
        '''
        design_path = 'modules.BMC_multicorrection.BMC_multicorrection_design'
        print('design_path is:', design_path)
        inLib.ModuleUI.__init__(self, control, ui_control,  'modules.BMC_multicorrection.BMC_multicorrection_design')
        self.raw_MOD = np.zeros(self._control.dims)
        self.z_max = self._control._settings['zmax']
        self.z_coeff = np.zeros(self.z_max)
        self.z_step = np.zeros(self.z_max)
        '''
        Below is the pushButton links group
        '''
        self._ui.pushButton_apply2mirror.clicked.connect(self.apply2mirror)
        self._ui.pushButton_acquire.clicked.connect(self.acquireImage)
        self._ui.pushButton_reset.clicked.connect(self.resetMirror)
        self._ui.pushButton_synthesize.clicked.connect(self.pattern2Segs)
        self._ui.pushButton_clear.clicked.connect(self.clearPattern)
        self._ui.pushButton_flush.clicked.connect(self.flushZern)
        self._ui.pushButton_setsingleZern.clicked.connect(self.setZern_ampli)
        self._ui.lineEdit_zernstep.returnPressed.connect(self.setZern_step)
        self._ui.lineEdit_zernampli.returnPressed.connect(self.setZern_ampli)
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

    def syncRawZern(self, mask = False):
        '''
        create a raw_MOD.
        DM is not updated!!!
        '''
        self.raw_MOD = lzern.calc_zernike(self.z_coeff, self.radius, mask, zern_data = {})


    def get_rawMOD(self):
        rm = np.copy(self.raw_MOD)
        return rm


    def toDMSegs(self):
        '''
        synthesize patterns.
        0. pass all the zernike coefficients to self.control.DM for zernike synthesis.
        1. create a pattern as self.control.raw_MOD
        2. display on the panel.
        '''
        self._control.pattern2Segs(self.raw_MOD)


    def setZern_ampli(self, zmode, ampli):
        '''
        set single zernike
        since the zmode starts from defocusing (4th), the row number should subtract 4.
        display ampli.
        '''
        item = self._ui.table_Zcoeffs.item(zmode-4, 0) # find the correct item
        item.setText(_translate("Form", str(ampli)))
        mask = self._ui.checkBox_mask.isChecked() # use mask or not?
        self.updateZern(zmode, ampli, mask)
        # done with setZern

    def setZern_step(self, zmode, stepsize):
        '''
        setZernike steps 
        '''


    def updateZern(self, zmode, ampli, mask = False):
        '''
        update the zernike coefficients
        '''
        self.z_coeff[zmode-1] = ampli
        self.syncRawZern(mask)


    def flushZern(self):
        '''
        flush all the zernike coefficients.
        '''
        self.z_coeff[:] = 0
        self._control.clearZern()
        # done with flushZern

    def clearPattern(self):
        '''
        Clear current raw pattern.
        '''
        self.raw_MOD[:] = 0.0
        self.displayPhase()

        # done with clearPattern

    def displayPhase(self):
        '''
        display phase (undiscretized, unrotated) on canvas mpl_phase
        '''
        phase = self.raw_MOD # this is the raw phase
        self._ui.mpl_phase.figure.axes[0].matshow(phase, cmap='RdBu')
        self._ui.mpl_phase.draw()
        # done with displayPhase

    def displaySegs(self):
        '''
        display segments (discretized) on canvas mpl_phase
        '''
        segs = self._control.getDM_segs()
        self._ui.mpl_phase.figure.axes[0].matshow(segs, cmap ='RdBu')
        self._ui.mpl_phase.draw()


    def single_runGradZern(self, n_modes):
        '''
        run gradient algorithm over the selected modes. Use sharpness as a metric.
        0. set a starting point. if None, use the current zernike settings.
        1. nModes: a list of zernike modes (4 --- 25)
        '''
        z_coeff = self.z_coeff
        for zn in n_modes:
            ampli = z_coeff[zn-1] +
            rm = self.get_rawMOD()
            self.toDMSegs(rm)






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
