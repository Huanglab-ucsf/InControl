#!/usr/bin/python

import inLib
from PyQt4 import QtCore, QtGui, Qwt5
from Utilities import QExtensions as qext
from functools import partial
import time
import numpy as np
import os

def clickable(widget):
    class Filter(QtCore.QObject):
        clicked = QtCore.pyqtSignal(int,int)
        def eventFilter(self,obj,event):
            if obj == widget:
                if event.type() == QtCore.QEvent.MouseButtonRelease:
                    self.clicked.emit(event.x(),event.y())
                    return True
            return False
    filter=Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class UI(inLib.DeviceUI):

    def __init__(self, control):
        inLib.DeviceUI.__init__(self, control, 'imagingSource.ccd.ccd_design')

        self.filename = 'image0001'

        self._previewOn = False
        
        #Connecting signals
        self._ui.checkBox_autoscale.stateChanged.connect(self.setAutoscale)          #autoscale
        self._ui.pushButton_saveImage.clicked.connect(self._saveImageNumpy)            #set exposure/delay times
        self._ui.lineEdit_fileName.textChanged.connect(self._setFilename)
        self._ui.spinBox_fileNameIndex.valueChanged.connect(self._setFilename)
        self._ui.labelDisplay.paintEvent = self._labelDisplay_paintEvent
        self._ui.pushButton_setROI.clicked.connect(self._setROI)
        self._ui.exposuretime_lineEdit.returnPressed.connect(self._setTimings)
        self._ui.pushButton_preview.clicked.connect(self._imagePreviewer)
        clickable(self._ui.labelDisplay).connect(self._mousePressEvent)

        self._autoscale = True
        self._pixmap = None
        self._cmap = None
        self._vmin = 0.0
        self._vmax = 255.0 

        self.x=0
        self.y=0

        
        self._ui.labelDisplay.setGeometry(210,10,512,512)

        # A timer to update the image:
        self._updater = QtCore.QTimer()
        self._updater.timeout.connect(self._updateImage)

        self._ui.spinBox_fileNameIndex.setValue(1)
        self._ui.lineEdit_fileName.setText('image_')

        self._updateToDisk = QtCore.QTimer()
        self._updateToDisk.timeout.connect(self._fillDAX)
        self._toDiskUpdateTime = 200
        self._ui.lineEdit_toDiskTime.setText(str(self._toDiskUpdateTime))

        self._ui.pushButton_recordMovie.clicked.connect(self.beginRecord)
        self._ui.pushButton_stopRecord.clicked.connect(self.stopRecord)


    def _mousePressEvent(self,x,y):
        self.x = x
        self.y = y

    def _saveImageNumpy(self):
        self._control.saveImage(self.filename)
        self._ui.spinBox_fileNameIndex.setValue(self._ui.spinBox_fileNameIndex.value()+1)

    def _setTimings(self):
        exp_time = float(self._ui.exposuretime_lineEdit.text())
        self._control.setExposureTime(exp_time)


    def _setROI(self):
        x0 = int(self._ui.lineEdit_x0.text())
        y0 = int(self._ui.lineEdit_y0.text())
        self.xres = int(self._ui.lineEdit_xshape.text())
        self.yres = int(self._ui.lineEdit_yshape.text())
        if x0>=0 and x0<1024 and y0>=0 and y0<1024:
            self._control.newSettings(xdim=xres,ydim=yres,x0=x0,y0=y0)
            time.sleep(0.01)

    def _imagePreviewer(self):
        if not self._previewOn:
            self.xres = int(self._ui.lineEdit_xshape.text())
            self.yres = int(self._ui.lineEdit_yshape.text())
            x0 = int(self._ui.lineEdit_x0.text())
            y0 = int(self._ui.lineEdit_y0.text())
            exposure_time = float(self._ui.exposuretime_lineEdit.text())
            self._control.newSettings(exposure=exposure_time,
                                      xdim=self.xres, ydim=self.yres,
                                      x0=x0,y0=y0)
            self._control.readyCam()
            self._updater.start(100)
            self._previewOn = not self._previewOn
            self._ui.pushButton_preview.setText('Preview Stop')
        else:
            self._updater.stop()
            self._previewOn = not self._previewOn
            self._ui.pushButton_preview.setText('Preview')
        

    def _updateImage(self):
        np_image, np_image2 = self._control.getImage()
        if np_image is not None:
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
            self._ui.label_xy.setText("x,y: %i, %i" % (int(self.x*(self.xres/512.)), int(self.y*(self.xres/512.))))

    def _labelDisplay_paintEvent(self, event):
        qp = QtGui.QPainter(self._ui.labelDisplay)
        if self._pixmap != None:
            qp.drawPixmap(0,0,self._pixmap)
        qp.setPen(QtCore.Qt.red)
        if self._ui.checkBox_showTarget.isChecked():
            qp.drawLine(251,251,253,253)
            qp.drawLine(262,262,260,260)
            qp.drawLine(253,260,251,262)
            qp.drawLine(262,251,260,253)

    def _setFilename(self):
        filenum = "%.4i" % self._ui.spinBox_fileNameIndex.value()
        self.filename = self._ui.lineEdit_fileName.text() + filenum
        if os.path.exists(self.filename+".npy"):
            self._ui.label_fn.setStyleSheet("QLabel { color: red}")
            self._ui.spinBox_fileNameIndex.setStyleSheet("QLabel { color: red}")
            self._ui.spinBox_fileNameIndex.setStyleSheet("QLabel { border-color: red}")
        else:
            self._ui.label_fn.setStyleSheet("QLabel { color: black}")
            self._ui.spinBox_fileNameIndex.setStyleSheet("QLabel { color: black}")
            self._ui.spinBox_fileNameIndex.setStyleSheet("QLabel { border-color: black}")

    def beginRecord(self):
        self._setFilename()
        self._control.beginRecord(self.filename)
        self._toDiskUpdateTime = int(self._ui.lineEdit_toDiskTime.text())
        self._updateToDisk.start(self._toDiskUpdateTime)

    def stopRecord(self):
        self._updateToDisk.stop()
        self._control.endRecording()

    def _fillDAX(self):
        nImsRec = self._control.recordFrame()
        self._ui.label_nImsRec.setText(str(nImsRec))

    def setAutoscale(self, state):
        self._autoscale = state

    def shutDown(self):
        self._updater.stop()
