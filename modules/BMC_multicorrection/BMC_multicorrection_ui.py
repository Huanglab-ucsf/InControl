#!/usr/bin/python
# let me debug this through.

from PyQt4 import QtGui,QtCore
import inLib
import numpy as np
import copy
import time
import libtim.zern as lzern
import AO_algos.Image_metrics as ao_metric
from BMC_threadfuncs import BL_correction
from zern_funcs import zm_list
from functools import partial

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
        self.z_comps = zm_list(z_max = self.z_max, z_start = 4)
        self.radius = 128
        self.metrics = []
        self.z_correct = 0.01
        dz = 0.0003

        '''
        Below is the connection group
        '''
        self._ui.pushButton_apply2mirror.clicked.connect(self.apply2mirror)
        self._ui.pushButton_acquire.clicked.connect(self.acquireImage)
        self._ui.pushButton_snapshot.clicked.connect(self.acquireSnap)
        self._ui.pushButton_reset.clicked.connect(self.resetMirror)
        self._ui.pushButton_segments.clicked.connect(self.toDMSegs)
        self._ui.pushButton_clear.clicked.connect(self.clearPattern)
        self._ui.pushButton_flush.clicked.connect(self.flushZern)
        self._ui.pushButton_evolve.clicked.connect(self.evolve)
        self._ui.pushButton_metric.clicked.connect(self.single_Evaluate)
        self._ui.pushButton_BL.clicked.connect(self.BL_correct)
        self._ui.pushButton_stepZern.clicked.connect(partial(self.stepZern, None, True))
        self._ui.lineEdit_zernstep.returnPressed.connect(partial(self.setZern_step, None, None))
        self._ui.lineEdit_zernampli.returnPressed.connect(partial(self.updateZern, None, None))
        self._ui.lineEdit_gain.returnPressed.connect(self.setGain)
        self._ui.lineEdit_dz.returnPressed.connect(self.setScanstep)

        # done with initialization
        # a couple of initialization
        for iz in np.arange(self.z_max-3):
            zm = self.z_comps.grab_mode(iz+4)
            zm_check = zmode_status(zm.zmode, self) # zmode
            self._ui.verticalLayout_activeZ.insertWidget(iz, zm_check.checkbox)
            self.z_comps.switch(zm_check.index, True)

        self.setScanstep(dz)


    def apply2mirror(self):
        '''
        Apply the current pattern to mirror
        '''
        self._control.modulateDM('text.txt')

    def acquireImage(self):
        """
        acquire PSF or other images
        """
        self.nSlices = self._ui.spinbox_Nsteps.value()
        nFrames = 2
        range_ = (self.nSlices-1)*self.dz
        image_filename = str(self._ui.lineEdit_filename.text())
        image = self._control.acquirePSF(range_, self.nSlices, nFrames, center_xy=True, filename=image_filename, mask_size = 60, mask_center = (self.radius,self.radius)) # acquired image
        # done with

    def acquireSnap(self):
        '''
        acquire a snapshot
        '''
        snap = self._control.acquireSnap()
        return snap


    def calc_image_metric(self, image):
        '''
        calculate image metrics (second moment)
        '''
        if image.shape[0] >1:
            metric = ao_metric.secondMomentOnStack(image, pixelSize= 0.0965, diffLimit=800)
        else:
            metric = ao_metric.secondMoment(image, pixelSize=0.0965, diffLimit= 800)
        return metric

        # done with calc_image_metric

    def resetMirror(self):
        '''
        input an \n into the PIPE.
        '''
        self._control.advanceWithPipe()
        # done with reset Mirror

    def syncRawZern(self, usemask = False):
        '''
        create a raw_MOD.
        DM is not updated!!!
        '''
        z_coeff = self.z_comps.sync_coeffs()
        self.raw_MOD = lzern.calc_zernike(z_coeff, self.radius, mask = usemask, zern_data = {})


    def get_rawMOD(self):
        rm = np.copy(self.raw_MOD)
        return rm
        # done with get_rawMOD


    def toDMSegs(self):
        '''
        synthesize patterns.
        0. pass all the zernike coefficients to self.control.DM for zernike synthesis.
        1. create a pattern as self.control.raw_MOD
        2. display on the panel.
        '''
        self._control.pattern2Segs(self.raw_MOD)
        self.displaySegs()
        # done with toDMSegs

    def setGain(self):
        gain = float(self._ui.lineEdit_gain.text())
        self._control.setGain(gain)
        # done with setGain


    def setZern_step(self, zmode = None, stepsize = None):
        '''
        setZernike steps
        '''
        if(zmode is None and stepsize is None):
            zmode = int(self._ui.lineEdit_zmode.text())
            stepsize = float(self._ui.lineEdit_zernstep.text())
            print("Zernike mode:", zmode, "stepsize: ", stepsize)


        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("Form", str(stepsize), None, QtGui.QApplication.UnicodeUTF8))
        self._ui.table_Zcoeffs.setItem(zmode-4, 1, item)
        zm = self.z_comps.grab_mode(zmode)
        print(zm)
        zm.step = stepsize
        # done with setZern_step

    def stepZern(self, zmode = None, forward = True):
        '''
        step the zernike mode zmode by stepsize.
        '''
        if (zmode is None):
            zmode = int(self._ui.lineEdit_zmode.text())
            print("Step mode:", zmode)

        if forward:
            self.z_comps.grab_mode(zmode).stepup()
        else:
            self.z_comps.grab_mode(zmode).stepdown()

        ampli = self.z_comps.grab_mode(zmode).ampli
        self.updateTable_ampli(zmode)

        # this is really awkward.

    def updateZern(self, zmode = None, ampli = None):
        '''
        update the zernike coefficients, it may work for one or more zernike modes.
        The zmodes would include the first 4 orders. This is redundant but reduces potential pitfalls.
        '''
        if zmode is None:
            zmode = int(self._ui.lineEdit_zmode.text())
            if ampli is None:
                ampli = float(self._ui.lineEdit_zernampli.text())
                print("Zernike mode:", zmode, "Amplitude:", ampli)
            else:
                print(ampli)
                zmode = np.arange(1, len(ampli)+1)

        if np.isscalar(zmode):
            self.z_comps.grab_mode(zmode).ampli = ampli # set ampli
            self.updateTable_ampli(zmode) # update the table display
        else:
            '''
            set the amplitude one by one
            '''
            for nz, am in zip(zmode, ampli):
                self.z_comps.grab_mode(nz).ampli = am
                self.updateTable_ampli(nz)

        mask = self._ui.checkBox_mask.isChecked() # use mask or not?
        self.syncRawZern(mask)
        self.displayPhase()
        # done with updateZern

        # not done with stepZern

    def updateTable_ampli(self, z_mode):
        '''
        simply update the table display of the zernike modes.
        '''
        ampli = self.z_comps.grab_mode(z_mode).ampli
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("Form", str(ampli), None, QtGui.QApplication.UnicodeUTF8))
        self._ui.table_Zcoeffs.setItem(z_mode-4, 0, item)
        # done with updateDisplay


    def flushZern(self):
        '''
        flush all the zernike coefficients; set all the z_coeffs as zero.
        '''
        self.z_comps.flush_coeffs()
        self.flushTable()
        self._control.clearZern()
        self.clearPattern()
        # done with flushZern

    def flushTable(self):
        '''
        flush the table of Zernike coefficients and stepsizes.
        '''
        zm = self.z_max-4

        for zmode in np.arange(zm):
            item = QtGui.QTableWidgetItem()
            item.setText(QtGui.QApplication.translate("Form", str(0), None, QtGui.QApplication.UnicodeUTF8))
            self._ui.table_Zcoeffs.setItem(zmode-4, 0, item)
            item = QtGui.QTableWidgetItem()
            item.setText(QtGui.QApplication.translate("Form", str(0), None, QtGui.QApplication.UnicodeUTF8))
            self._ui.table_Zcoeffs.setItem(zmode-4, 1, item)
        # done with flushTable



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


    def single_Evaluate(self):
        '''
        Just apply the zernike coefficients, take the image and evaluate the sharpness
        z_coeffs: from 1 to z_max.
        '''
        z_coeff = self.z_comps.sync_coeffs()
        self.updateZern(ampli=z_coeff)# # this is amplitude only-mask = False, the raw_MOD is updated as well.
        self.displayPhase() # display on the figure
        self.toDMSegs() # this only modulates
        self.apply2mirror()
        snap = self.acquireSnap()
        self.resetMirror()
        mt = self.calc_image_metric(snap)
        self.metrics.append(mt)
        return mt
        '''
        OK, the mirror is reset and the metric is applied.
        what's next?
        '''

    def displayMetrics(self):
        '''
        display metrics
        '''
        self._ui.mpl_metrics.figure.axes[0].plot(np.array(self.metrics), cmap='RdBu')
        self._ui.mpl_metrics.draw()
        # done with displayMetrics

    def setScanstep(self, dz = None):
        '''
        setScanstep via thorlabs motor.
        '''
        if(dz is None):
            dz = float(self._ui.lineEdit_dz.text())
        self._control.setScanstep(dz)
        self.dz = dz # here we have a redundant dz

    def BL_correct(self):
        '''
        Backlash correction, threaded on 12/15.
        '''
        z_start  = float(self._ui.lineEdit_start.text())
        BL = BL_correction(self.z_correct, z_start)
        BL.finished.connect(self._position_ready)
        self._ui.pushButton_BL.setEnabled(False)
        BL.start()
        # done with threaded BL_correct

    def _switch_zern(self, zmode, status):
        '''
        switch on or off the zernike mode.
        '''
        self.z_comps.switch(zmode, status)



    def _position_ready(self):
        '''
        Set the position ready.
        '''
        self._ui.pushButton_BL.setEnabled(True)

    def evolve(self):
        '''
        To be filled up later. evolution of the zernikes.
        '''
        pass


class zmode_status:
    def __init__(self, index, ui):
        self.index = index
        print("mode:",self.index)
        self.checkbox = QtGui.QCheckBox(str(self.index))
        self.checkbox.stateChanged.connect(partial(ui._switch_zern, self.index, self.checkbox.isChecked()))
        self.checkbox.toggle()
