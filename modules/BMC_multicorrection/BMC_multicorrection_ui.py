#!/usr/bin/python


from PyQt4 import QtGui,QtCore
import inLib
import numpy as np
import copy
import time
import libtim.zern as lzern
import AO_algos.Image_metrics as ao_metric



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
        self.image = None
        self.radius = 128
        '''
        Below is the initial value group
        '''
        self._ui.lineEdit_filename.setText('test.npy')
        self._ui.lineEdit_dz.setText(str("0.30"))
        '''
        Below is the pushButton and lineEdits links group
        '''
        self._ui.pushButton_apply2mirror.clicked.connect(self.apply2mirror)
        self._ui.pushButton_acquire.clicked.connect(self.acquireImage)
        self._ui.pushButton_reset.clicked.connect(self.resetMirror)
        self._ui.pushButton_segments.clicked.connect(self.toDMSegs)
        self._ui.pushButton_clear.clicked.connect(self.clearPattern)
        self._ui.pushButton_flush.clicked.connect(self.flushZern)
        self._ui.pushButton_evolve.clicked.connect(self.runGradZern)
        self._ui.lineEdit_zernstep.returnPressed.connect(self.setZern_step)
        self._ui.lineEdit_zernampli.returnPressed.connect(self.setZern_ampli)
        self._ui.lineEdit_gain.returnPressed.connect(self.setGain)
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
        nFrames = 2
        range_ = (nSlices-1)*dz
        image_filename = str(self._ui.lineEdit_filename.text())
        self.image = self._control.acquirePSF(range_, nSlices, nFrames, center_xy=True, filename=image_filename,
                       mask_size = 40, mask_center = (-1,-1)) # acquired image
        # done with acquireImage


    def calc_image_metric(self):
        '''
        calculate image metrics (second moment)
        '''
        if self.image is not None:
            image = self.image
            if image.shape[0] >1:
                metric = ao_metric.secondMomentOnStack(image, pixelSize= 0.0965, diffLimit=800)
            else:
                metric = ao_metric.secondMoment(image, pixelSize=0.0965, diffLimit= 800)


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
        self.raw_MOD = lzern.calc_zernike(self.z_coeff, self.radius, mask = usemask, zern_data = {})


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


    def setZern_ampli(self, zmode = None, ampli = None):
        '''
        set single zernike
        since the zmode starts from defocusing (4th), the row number should subtract 4.
        display ampli.
        '''
        if(zmode is None and ampli is None):
            zmode = int(self._ui.lineEdit_zmode.text())
            ampli = float(self._ui.lineEdit_zernampli.text())
            print("Zernike mode:", zmode, "Amplitude:", ampli)

        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("Form", str(ampli), None, QtGui.QApplication.UnicodeUTF8))
        self._ui.table_Zcoeffs.setItem(zmode-4, 0, item)

        mask = self._ui.checkBox_mask.isChecked() # use mask or not?
        self.updateZern(ampli, zmode, mask)
        # done with setZern

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
        # done with setZern_step


    def updateZern(self, ampli, zmode = None, mask = False):
        '''
        update the zernike coefficients, it may work for one or more zernike modes.
        '''
        if zmode is None:
            zmode = np.arange(1, len(ampli)+1)
        self.z_coeff[zmode-1] = ampli
        self.syncRawZern(mask)
        self.displayPhase()
        # done with updateZern


    def flushZern(self):
        '''
        flush all the zernike coefficients; set all the z_coeffs as zero.
        '''
        self.z_coeff[:] = 0
        self.flushTable()
        self._control.clearZern()
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


    def single_Evaluate(self, z_coeffs):
        '''
        Just apply the zernike coefficients, take the image and evaluate the sharpness
        z_coeffs: from 1 to z_max.
        '''
        self.updateZern(z_coeffs) # mask = False, the raw_MOD is updated as well.
        self.displayPhase() # display on the figure
        self.toDMSegs() # this only modulates
        self.apply2mirror()
        self.acquireImage()
        self.resetMirror()
        mt = self.calc_image_metric()
        return mt
        '''
        OK, the mirror is reset and the metric is applied.
        what's next?
        '''

    def step_Hessian(self, z_modes, z_coeffs, z_steps):
        '''
        z_modes: selected modes for optimization. 4 --- zmax
        z_coeffs: the coefficients of the zernike modes
        z_steps: the designed steps in each mode. If it is 0 or ignored, then the mode is dropped.
        '''
        N_search = len(z_modes) # the dimension of the search space
        zc_input = np.zeros(self.z_max)
        st_input = np.zeros(self.z_max)
        try:
            zc_input[z_modes-4] = z_coeffs
        except ValueError:
            print('dimension mismatch for amplitudes.')
            return -1

        # assign the steps
        try:
            zc_input[z_modes-4] = z_steps
        except ValueError:
            print('dimension mismatch for stepsize.')
            return -2

        S_mat= np.zeros([N_search+1, N_search]) # the first row saves the first derivative, the rest N_search rows save the second.
        hess = np.zeros([N_search, N_search])

        S0 = self.single_Evaluate(zc_input)
        for iz in z_modes:
            '''
            iterate through z_modes
            '''



        # done with single_runGradZern

    def runGradZern(self, nmodes, nsteps):
        '''
        run GradZernike for multiple steps.
        This function utilizes the conjugate gradient method
        (CGM, see numerical recipies).
        '''
        metrics = []
        for xn in np.arange(nsteps):
            mt = self.single_GradZern(nmodes)
            metrics.append(mt)

        return(metrics)






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
