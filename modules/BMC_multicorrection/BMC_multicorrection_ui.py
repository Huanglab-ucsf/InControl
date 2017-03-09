#!/usr/bin/python
# let me debug this through.

from PyQt4 import QtGui,QtCore
import inLib
import numpy as np
import copy
import time
import libtim.zern as lzern
import AO_algos.Image_metrics as ao_metric
from BMC_threadfuncs import BL_correction, Optimize_pupil
from zern_funcs import zm_list
from functools import partial
from Evolution_routines import Pattern_evolution
from itertools import product


class UI(inLib.ModuleUI):
    '''
    From now on, all the functions will be ordered alphabetically.
    '''

    def __init__(self, control, ui_control):
        '''
        This is the initialization part of the UI.
        '''
        design_path = 'modules.BMC_multicorrection.BMC_multicorrection_design'
        inLib.ModuleUI.__init__(self, control, ui_control, design_path)
        self.raw_MOD = np.zeros(self._control.dims)
        self.z_max = self._control._settings['zmax']
        self.z_comps = zm_list(z_max = self.z_max, z_start = 4)
        self.radius = 128
        self.metrics = []
        self.z_correct = 0.01
        self.zm_status = []
        self.BL_thread = None
        self.EV_thread = None
        self.Evolution = Pattern_evolution(self)
        dz = 0.0003

#     Below is the connection group
        self._ui.pushButton_apply2mirror.clicked.connect(self.apply2mirror)
        self._ui.pushButton_acquire.clicked.connect(self.acquireImage)
        self._ui.pushButton_snapshot.clicked.connect(self.acquireSnap)
        self._ui.pushButton_reset.clicked.connect(self.resetMirror)
        self._ui.pushButton_segments.clicked.connect(partial(self.toDMSegs, True))
        self._ui.pushButton_clear.clicked.connect(self.clearPattern)
        self._ui.pushButton_flush.clicked.connect(self.flushZern)
        self._ui.pushButton_evolve.clicked.connect(self.evolve)
        self._ui.pushButton_BL.clicked.connect(self.BL_correct)
        self._ui.pushButton_singleEval.clicked.connect(partial(self.single_Evaluate, 10))
        self._ui.pushButton_stepZern.clicked.connect(partial(self.stepZern, None, True))
        self._ui.pushButton_synthesize.clicked.connect(self.syncRawZern)
        self._ui.pushButton_checkall.clicked.connect(partial(self.switch_all, True ))
        self._ui.pushButton_uncheckall.clicked.connect(partial(self.switch_all, False))
        self._ui.pushButton_ampall.clicked.connect(partial(self.updateZern, -1, None))
        self._ui.pushButton_stpall.clicked.connect(partial(self.setZern_step, -1, None))
        self._ui.pushButton_fcscan.clicked.connect(self.scan_focus)
        self._ui.radioButton_laser.toggled.connect(self.laserSwitch)
        self._ui.lineEdit_zernstep.returnPressed.connect(partial(self.setZern_step, None, None))
        self._ui.lineEdit_zernampli.returnPressed.connect(partial(self.updateZern, None, None))
        self._ui.lineEdit_gain.returnPressed.connect(self.setGain)
        self._ui.lineEdit_dz.returnPressed.connect(partial(self.setScanstep, None))
        self._ui.table_Zcoeffs.itemClicked.connect(self.testTable)

        # done with initialization
        # a couple of initialization
        for iz in np.arange(self.z_max-3):
            zm = self.z_comps.grab_mode(iz+4)
            zm_check = zmode_status(zm.zmode, self) # zmode
            self._ui.verticalLayout_activeZ.insertWidget(iz, zm_check.checkbox)
            self.zm_status.append(zm_check)
            self.z_comps.switch(zm_check.index, False)

        self.setScanstep(dz)
        # done with initialization
# -----------------------------Below are some test functions (unfinished)
    def testTable(self):
        crow = self._ui.table_Zcoeffs.currentRow()
        citem = self._ui.table_Zcoeffs.currentItem()
        print("Current row:", crow)
        print("Current item", citem)
#--------------------------------End of test functions


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

    def acquireSnap(self, n_mean):
        '''
        acquire a snapshot, ragardless of whether a pattern is applied or not
        '''
        snap = self._control.acquireSnap(n_mean)
        self.displayImage(snap)
        return snap

    def BL_correct(self):
        '''
        Backlash correction, threaded on 12/15.
        '''
        z_start  = float(self._ui.lineEdit_start.text())
        self.BL_thread = BL_correction(self._control, self.z_correct, z_start)
        self.BL_thread.finished.connect(self._position_ready)
        self._ui.pushButton_BL.setEnabled(False)
        self.BL_thread.start()

    def calc_image_metric(self, image, diffLimit=520, mode = 'sharp'):
        '''
        calculate image metrics (second moment)
        '''
        if len(image.shape) == 3:
            metric = ao_metric.secondMomentOnStack(image, 96.5, diffLimit)
        else:
            metric = ao_metric.secondMoment(image, 96.5, diffLimit)
        if mode == 'max':
            metric = np.max(image)
            print("max_pixel", metric)
        return metric


    def clearPattern(self):
        '''
        Clear current raw pattern.
        '''
        self.raw_MOD[:] = 0.0
        self.displayPhase()

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

    def displayMetrics(self, metrics):
        '''
        display metrics
        '''
        self._ui.mpl_metrics.figure.axes[0].plot(metrics, '-gx', linewidth = 2)
        self._ui.mpl_metrics.draw()
            # done with displayMetrics

    def displayImage(self, snapIm):
        '''
        display the last image
        '''
        self._ui.mpl_image.figure.axes[0].imshow(snapIm, cmap = 'Greys_r')
        self._ui.mpl_image.draw()
        # done with displayImage

    def evolve(self):
        '''
        To be filled up later. evolution of the zernikes.
        0. Select the active modes and their coefficients
        '''
        act_ind = self._switch_zern()
        start_coeffs = self.z_comps.get_parameters(act_ind)[0] # only get those
        flabel = self._ui.lineEdit_evname.text() #
        Nmeasure = self.spinbox_evsteps.value()
        self.EV_thread = Optimize_pupil(self.Evolution, act_ind, start_coeffs, Nmeasure, flabel)
        self.EV_thread.finished.connect(self._evolution_ready)
        self._ui.pushButton_evolve.setEnabled(False)
        self.EV_thread.start()


    def flushZern(self):
        '''
        flush all the zernike coefficients; set all the z_coeffs as zero.
        '''
        self.z_comps.flush_coeffs()
        self.flushTable()
        self._control.clearZern()
        self.clearPattern()
        self.switch_all(False)
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

    def laserSwitch(self):
        '''
        laser switch
        '''
        status = self._ui.radioButton_laser.isChecked()
        self._control.laserSwitch(status)
        # end laser switch

    def resetMirror(self):
        '''
        input an \n into the PIPE.
        '''
        self._control.advanceWithPipe()
        # done with reset Mirror

    def syncRawZern(self):
        '''
        create a raw_MOD.
        DM is not updated!!!
        '''
        # self._switch_zern()
        usemask = self._ui.checkBox_mask.isChecked() # use mask or not?
        z_coeff = self.z_comps.sync_coeffs() # OK this is to be used only once. Otherwise too inconvenient.
        print("zernike coefficients:", z_coeff)
        self.raw_MOD = lzern.calc_zernike(z_coeff, self.radius, mask = usemask, zern_data = {})
        self.displayPhase()
        # done with syncRawZern

    def get_rawMOD(self):
        rm = np.copy(self.raw_MOD)
        return rm
        # done with get_rawMOD


    def toDMSegs(self, display = True):
        '''
        synthesize patterns to 12 * 12 segments
        '''
        self._control.pattern2Segs(self.raw_MOD)
        if display:
            self.displaySegs()
        # done with toDMSegs
    def scan_focus(self):
        '''
        scan_focus, measure the position with maximum sharpness and/or signal value.
        '''
        print("This function is not completed yet.")


    def setGain(self):
        gain = float(self._ui.lineEdit_gain.text())
        self._control.setGain(gain)
        # done with setGain


    def setZern_step(self, zmode = None, stepsize = None):
        '''
        setZernike steps
        '''
        if(stepsize is None):
            stepsize = float(self._ui.lineEdit_zernstep.text())

        if(zmode is None):
            zmode = self._ui.spinBox_Zmode.value()
        elif(zmode == -1):

            for iz in np.arange(4,self.z_max):
                item = QtGui.QTableWidgetItem()
                item.setText(QtGui.QApplication.translate("Form", str(stepsize), None, QtGui.QApplication.UnicodeUTF8))
                self._ui.table_Zcoeffs.setItem(iz-4, 1, item)
                self.z_comps.grab_mode(iz).step = stepsize
        else: #zmode is not -1. set single z_steps
            if(np.isscalar(zmode)):
                item = QtGui.QTableWidgetItem()
                item.setText(QtGui.QApplication.translate("Form", str(stepsize), None, QtGui.QApplication.UnicodeUTF8))
                self._ui.table_Zcoeffs.setItem(zmode-4, 1, item)
                self.z_comps.grab_mode(zmode).step = stepsize
            else:
                for iz, zs in zip(zmode,stepsize):
                    item = QtGui.QTableWidgetItem()
                    item.setText(QtGui.QApplication.translate("Form", str(stepsize), None, QtGui.QApplication.UnicodeUTF8))
                    self._ui.table_Zcoeffs.setItem(iz-4, 1, item)
                    self.z_comps.grab_mode(iz).step = zs
        # done with setZern_step

    def stepZern(self, zmode = None, forward = True):
        '''
        step the zernike mode zmode by stepsize.
        '''
        if (zmode is None):
            zmode = self._ui.spinBox_Zmode.value()
            print("Step mode:", zmode)

        if forward:
            self.z_comps.grab_mode(zmode).stepup()
        else:
            self.z_comps.grab_mode(zmode).stepdown()
        self.updateTable_ampli(zmode)

        self._switch_zern()
        self.syncRawZern()

        # this is really awkward.

    def updateZern(self, zmode = None, ampli = None):
        '''
        update the zernike coefficients, it may work for one or more zernike modes.
        The zmodes would include the first 4 orders. This is redundant but reduces potential pitfalls.
        '''
        # if the zmode is empty, then read zmode from the spinBox.
        if ampli is None:
            ampli = float(self._ui.lineEdit_zernampli.text())


        if zmode is None:
            zmode = self._ui.spinBox_Zmode.value()
        elif zmode == -1:
            zmode = np.arange(4, self.z_max)
            ampli = np.ones_like(zmode)*ampli

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

        self._switch_zern()
        self.syncRawZern()
        # done with updateZern


    def updateTable_ampli(self, z_mode):
        '''
        simply update the table display of the zernike modes.
        '''
        ampli = self.z_comps.grab_mode(z_mode).ampli
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("Form", str(ampli), None, QtGui.QApplication.UnicodeUTF8))
        self._ui.table_Zcoeffs.setItem(z_mode-4, 0, item)
        # done with updateDisplay



    def setScanstep(self, dz = None):
        '''
        setScanstep via thorlabs motor.
        '''
        if(dz is None):
            dz = float(self._ui.lineEdit_dz.text())
        self._control.setScanstep(dz)
        self.dz = dz # here we have a redundant dz


        # done with threaded BL_correct

    def switch_all(self, status = False):
        '''
        uncheck all the Zernike modes.
        '''
        for zms in self.zm_status:
            zms.checkbox.setChecked(status)
            zmode = zms.index
            self.z_comps.switch(zmode, status)
        # done with switch all

    # private functions, not directly called from the UI
    def _switch_zern(self):
        '''
        switch on or off the zernike mode.
        '''
        for zms in self.zm_status:
            status = zms.checkbox.isChecked()
            zmode = zms.index
            self.z_comps.switch(zmode, status)

        act_ind = self.z_comps.get_active()
        return act_ind
        # done with _switch_zern

    def _position_ready(self):
        '''
        Set the position ready.
        '''
        self._ui.pushButton_BL.setEnabled(True)

    def _evolution_ready(self):
        '''
        Set the evolution ready.
        '''
        self._ui.pushButton_evolve.setEnabled(True)
        # report postion is ready.

    def single_Evaluate(self, rep = 3):
        '''
        Evaluate single coefficients, do nothing to the pattern, just take the snapshot and evaluate.
        "Metrics" button.
        '''
        mts = np.zeros(rep)
        for ii in np.arange(rep):
            snap = self.acquireSnap(1)
            mts[ii] = self.calc_image_metric(snap)
        mt = np.mean(mts)
        sd = np.std(mts)
        print(mts)
        print("Metric:", mt, 'SD:', sd)
        # done with single_Evaluate


    def shutDown(self):
        if self.BL_thread:
            self.BL_thread.wait()
        if self.EV_thread:
            self.EV_thread.wait()
        # shutdown


class zmode_status:
    def __init__(self, index, ui):
        self.index = index
        print("mode:",self.index)
        self.checkbox = QtGui.QCheckBox(str(self.index))
        # self.checkbox.toggle()
