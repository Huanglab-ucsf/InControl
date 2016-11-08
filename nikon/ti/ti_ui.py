#!/usr/bin/python


from PyQt4 import QtCore
import inLib
import numpy as np


class UI(inLib.DeviceUI):
    
    def __init__(self, control):
        design_path = 'nikon.ti.ti_design'
        inLib.DeviceUI.__init__(self, control, design_path)

        self._window.resize(450, 500)

        self._ui.pushButtonCali.clicked.connect(self.calibrateFocalPlanePosition)
       
        self._ui.mplCanvasCali = inLib.MplCanvasAxes()
        self._ui.mplCanvasCali.axes.set_xlabel('PFS offset [counts]')
        self._ui.mplCanvasCali.axes.set_ylabel('Focal plane position [um]')
        self._ui.mplCanvasCali.update()
        self._ui.verticalLayoutCali.addWidget(self._ui.mplCanvasCali)
        self._ui.mplCanvasCali.draw()

        self._calibrator = None

        self.FocalPlaneUpdater = QtCore.QTimer()
        self.FocalPlaneUpdater.timeout.connect(self.updateFocalPlane)
        self.FocalPlaneUpdater.start(1000)


    def calibrateFocalPlanePosition(self):
        self._ui.pushButtonCali.setEnabled(False)
        max_depth = self._ui.doubleSpinBoxCaliMaxDepth.value()
        self._calibrator = _Calibrator(self._control, max_depth)
        self._window.connect(self._calibrator, QtCore.SIGNAL('calibrationDone'),
                self._on_calibration_done)
        self._calibrator.start()

    def _on_calibration_done(self, calibration):
        PFS, z, z_pol = calibration
        self._ui.mplCanvasCali.axes.clear()
        self._ui.mplCanvasCali.axes.set_xlabel('PFS offset [counts]')
        self._ui.mplCanvasCali.axes.set_ylabel('Focal plane position [um]')
        self._ui.mplCanvasCali.axes.plot(PFS, z, '.')
        PFS_fit = np.linspace(min(PFS), max(PFS), 100)
        z_fit = z_pol(PFS_fit)
        self._ui.mplCanvasCali.axes.plot(PFS_fit, z_fit)
        self._ui.mplCanvasCali.draw()
        self._ui.pushButtonCali.setEnabled(True)

    def shutDown(self):
        if self._calibrator:
            print 'scope: Waiting for calibration to finish.'
            self._calibrator.wait()

    def updateFocalPlane(self):
        position = self._control.getFocalPlanePosition()
        if position:
            self._ui.labelFocalPlane.setText('%.3f' % position)
            PFS = self._control.PFS.getPosition()
            if len(self._ui.mplCanvasCali.axes.lines) == 4:
                del self._ui.mplCanvasCali.axes.lines[-2:]
            self._ui.mplCanvasCali.axes.axhline(y=position)
            self._ui.mplCanvasCali.axes.axvline(x=PFS)
            self._ui.mplCanvasCali.draw()


class _Calibrator(QtCore.QThread):
    def __init__(self, control, max_depth):
        QtCore.QThread.__init__(self)
        self.control = control
        self.max_depth = max_depth

    def run(self):
        calibration = self.control.calibrateFocalPlanePosition(self.max_depth, simulation=False)
        self.emit(QtCore.SIGNAL('calibrationDone'), calibration)
