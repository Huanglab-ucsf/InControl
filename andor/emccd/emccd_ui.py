#!/usr/bin/python


import inLib
from PyQt4 import QtCore, QtGui, Qwt5
from Utilities import QExtensions as qext
import time
import numpy as np


class UI(inLib.DeviceUI):

    def __init__(self, control):
        inLib.DeviceUI.__init__(self, control, 'andor.emccd.emccd_design')

        self._ui.pushButtonShutter.clicked.connect(self.toggleShutter)
        self._ui.pushButtonSnapshot.clicked.connect(self.saveSnapshot)
        self._ui.labelDisplay.paintEvent = self._labelDisplay_paintEvent
        self._ui.checkBoxAutoscale.stateChanged.connect(self.setAutoscale)

        # A histogram of the current frame:
        self._ui.qwtPlotHistogram.enableAxis(0, False)
        self._ui.qwtPlotHistogram.enableAxis(2, False)
        canvas = self._ui.qwtPlotHistogram.canvas().setLineWidth(0)
        #canvas.setLineWidth(10)
        self._histogram = Qwt5.QwtPlotCurve('')
        self._histogram.setStyle(Qwt5.QwtPlotCurve.Sticks)
        self._histogram.attach(self._ui.qwtPlotHistogram)

        em_min, em_max = self._control.getEMGainRange()
        self._ui.horizontalSliderGain.setRange(em_min, em_max)
        em_gain = self._control.getEMCCDGain()
        self._ui.labelGain.setText('EM Gain: ' + str(em_gain))
        self._ui.horizontalSliderGain.setValue(em_gain)
        self._ui.horizontalSliderGain.valueChanged.connect(self.setEMCCDGain)

        self._autoscale = True
        self._pixmap = None
        self._cmap = None
        #self._cmap = qext.QColortables8.spectral
        self._vmin = 0.0
        self._vmax = 65535.0

        # A timer to update the image:
        self._updater = QtCore.QTimer()
        self._updater.timeout.connect(self._update)
        self._updater.start(100)


    def setEMCCDGain(self, em_gain):
        self._ui.labelGain.setText('EM Gain: ' + str(em_gain))
        self._control.setEMCCDGain(em_gain)


    def toggleShutter(self):
        text = self._ui.pushButtonShutter.text()
        if text == 'Open shutter':
            self._ui.pushButtonShutter.setText('Close shutter')
            self._control.openShutter()
        else:
            self._ui.pushButtonShutter.setText('Open shutter')
            self._control.closeShutter()


    def saveSnapshot(self):
        fname = QtGui.QFileDialog.getSaveFileName(None,'Save snapshot',
                                                  '',
                                                  '*.npy')
        if fname:
                self._control.saveSnapshot(str(fname))


    def _update(self):
        np_image = self._control.getMostRecentImageNumpy()
        np_min = np_image.min()
        np_max = np_image.max()
        if self._autoscale:
            self.vmin = np_min
            self.vmax = np_max
        qt_image = qext.numpy_to_qimage8(np_image, self.vmin, self.vmax, self._cmap)
        self._pixmap = QtGui.QPixmap.fromImage(qt_image)
        self._pixmap = self._pixmap.scaled(512, 512, QtCore.Qt.KeepAspectRatio)
        self._ui.labelDisplay.update()
        self._ui.labelMin.setText(str(np_min))
        self._ui.labelMax.setText(str(np_max))
        self._ui.labelMean.setText(str(int(np_image.mean())))
        self._ui.labelMedian.setText(str(int(np.median(np_image))))
        self._ui.qwtPlotHistogram.setAxisScale(2, np_min, np_max, 0)
        hist, bin_edges = np.histogram(np_image, 100)
        self._histogram.setData(bin_edges, hist)
        self._ui.qwtPlotHistogram.replot()


    def _labelDisplay_paintEvent(self, event):
        qp = QtGui.QPainter(self._ui.labelDisplay)
        if self._pixmap != None:
            qp.drawPixmap(0, 0, self._pixmap)
        qp.setPen(QtCore.Qt.red)
        qp.drawLine(251, 251, 253, 253)
        qp.drawLine(262, 262, 260, 260)
        qp.drawLine(253, 260, 251, 262)
        qp.drawLine(262, 251, 260, 253)


    def setAutoscale(self, state):
        self._autoscale = state


    def shutDown(self):
        self._updater.stop()
