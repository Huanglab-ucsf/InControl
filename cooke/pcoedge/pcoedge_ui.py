#!/usr/bin/python

import inLib
from PyQt4 import QtCore, QtGui, Qwt5
from Utilities import QExtensions as qext
from functools import partial
import time, os
import numpy as np
import multiprocessing
from multiprocessing import Process, Pipe, Queue, Array, Manager
import pyqtgraph as pg
from pyqtgraph import opengl

RECORD_DAX = 1
RECORD_MEMORY = 0

def clickable(widget):
    class Filter(QtCore.QObject):
        clicked = QtCore.pyqtSignal(int,int,bool,bool)
        def eventFilter(self,obj,event):
            if obj == widget:
                if event.type() == QtCore.QEvent.MouseButtonRelease:
                    left = (event.button() == QtCore.Qt.LeftButton)
                    right = (event.button() == QtCore.Qt.RightButton)
                    self.clicked.emit(event.x(),event.y(), left, right)
                    return True
            return False
    filter=Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

def testProc(e):
    e.wait()
    print "EVENT FIRED..."

def unwrap_self(arg, **kwarg):
    return UI.testProc(arg, **kwarg)

class UI(inLib.DeviceUI):

    def __init__(self, control):
        inLib.DeviceUI.__init__(self, control, 'cooke.pcoedge.pcoedge_design')

        self._control.beginPreview()

        self._previewMode = True

        self._ui.checkBoxAutoscale.stateChanged.connect(self.setAutoscale)
        self._ui.pushButton_SaveImages.clicked.connect(self._saveImages)
        self._ui.setROI_pushButton.clicked.connect(self._setROI)
        self._ui.resetPreview_pushButton.clicked.connect(self._resetPreview)

        self._ui.lineEdit_fileName.setText("movie")
        self._ui.lineEdit_fileName.textChanged.connect(self._setFilename)
        self._ui.spinBox_fileNameIndex.valueChanged.connect(self._setFilename)
        self._ui.comboBox_filename.currentIndexChanged.connect(self._setFilename)

        self._ui.comboBox_expunits.addItem("ns")
        self._ui.comboBox_expunits.addItem("us")
        self._ui.comboBox_expunits.addItem("ms")

        self._ui.comboBox_delayunits.addItem("ns")
        self._ui.comboBox_delayunits.addItem("us")
        self._ui.comboBox_delayunits.addItem("ms")

        #Combobox for filename suffix
        self._ui.comboBox_filename.addItem("")
        self._ui.comboBox_filename.addItem("_647")
        self._ui.comboBox_filename.addItem("_561")
        self._ui.comboBox_filename.addItem("_532")
        self._ui.comboBox_filename.addItem("_488")
        self._ui.comboBox_filename.addItem("_conv")
        self._ui.comboBox_filename.addItem("_LED")
        self._ui.comboBox_filename.setCurrentIndex(0)

        self._ui.pushButton_SetTimings.clicked.connect(self._setTimings)

        xdim,ydim = self._control._getResolution()
        self._ui.labelResolution.setText("%i, %i" % (xdim,ydim))
        self._control._props['dimensions'] = xdim,ydim
        self._xres, self._yres = xdim,ydim

        self._getDisplayTimings()

        self._autoscale = True
        self._pixmap = None
        self._cmap = None
        self._vmin = 0.0
        self._vmax = 16384.0

        ##Settings
        self._ui.settings2_radioButton.hide()
        self._ui.settings3_radioButton.hide()
        self._ui.settings4_radioButton.hide()
        self._ui.settings5_radioButton.hide()
        self._ui.settings6_radioButton.hide()

        settings_name = self._control.loadedSettings['settings_filename']
        self._ui.settings1_radioButton.setText(settings_name)
        self._ui.settings1_radioButton.setChecked(True)

        self._max_saved = 6

        ##Handling file drops
        #self._ui.mainwidget.__class__.dragEnterEvent = self._dragEnterEvent
        #self._ui.mainwidget.__class__.dropEvent = self._dropEvent

        # A timer to update the image:
        self._updater = QtCore.QTimer()
        self._updater.timeout.connect(self._update)
        self.updateDisplayTime = 100
        self._updater.start(self.updateDisplayTime)

        self._updateBuffsPending = QtCore.QTimer()
        self._updateBuffsPending.timeout.connect(self._fillBuffers)
        self._buffUpdateTime = 1
        self.DAX_or_Memory = RECORD_DAX

        self._bufferFilling = False
        self._ui.pushButton_RecordDAX.clicked.connect(self._recordToDAX)
        self._ui.pushButton_RecordMemory.clicked.connect(self._recordToMemory)
        self._ui.memToDAX_pushButton.clicked.connect(self._memToDAX)

        self._ui.updateTime_lineEdit.returnPressed.connect(self.newUpdateTime)

        self._ui.updateDisplayTime_lineEdit.returnPressed.connect(self.newDisplayUpdateTime)

        #Scaling of displayed image
        self._ui.horizontalSlider_min.setRange(0,16384)
        self._ui.horizontalSlider_max.setRange(0,16384)
        self._ui.horizontalSlider_min.valueChanged.connect(self._setDispMin)
        self._ui.horizontalSlider_max.valueChanged.connect(self._setDispMax)

        ##Printing camera info
        self._ui.printRecStruct_pushButton.clicked.connect(self.printInfo)

        self._ui.bufsToQueue_lineEdit.returnPressed.connect(self.bufsToQueue)

        self._ui.acquireFastImages_pushButton.clicked.connect(self.getFastImages)
        self._ui.displayFastImage_lineEdit.returnPressed.connect(self.displayFastImage)

        self._ui.initFramesMP_lineEdit.returnPressed.connect(self.setInitFramesMP)
        self._ui.endMP_pushButton.clicked.connect(self._endMP)
        self._ui.stateOfMP_pushButton.clicked.connect(self._printMPState)

        self._displayTxtInfo = True
        self._ui.displayTxtInfo_checkBox.stateChanged.connect(self._changeDisplayTxtInfo)

        #self.testp = Process(target=unwrap_self, args=(self,self._control.resultsEvent,))
        #self.testp.start()
        self._lookForMPEventsQTimer = QtCore.QTimer()
        self._lookForMPEventsQTimer.timeout.connect(self._lookForMPEvents)
        self._lookForMPEventsQTimer.start(300)

        self._updateQueueQTimer = QtCore.QTimer()
        self._updateQueueQTimer.timeout.connect(self._imShift)
        

        #Multiprocessing / Queue Testing
        signalFrame, captureFrame = self._control.whenToEmitAndCapture()
        self._ui.emitSigFrame_lineEdit.setText("%i" % signalFrame)
        self._ui.captureFrame_lineEdit.setText("%i" % captureFrame)
        self._ui.setMPTesting_pushButton.clicked.connect(self._changeMPTesting)

        #Subimage (again, for testing multiprocessing / queue / communication with camera module
        self.subimCols = 3
        self.subimRows = 8
        self.subimX = 8
        self.subimY = 64
        
        self._ui.subimRows_lineEdit.setText("%i" % self.subimRows)
        self._ui.subimCols_lineEdit.setText("%i" % self.subimCols)
        self._ui.subimX_lineEdit.setText("%i" % self.subimX)
        self._ui.subimY_lineEdit.setText("%i" % self.subimY)

        self._ui.subimSet_pushButton.clicked.connect(self._changeSubIm)

        self._ui.flushImQ_pushButton.clicked.connect(self._flushImQ)

    def _changeSubIm(self):
        self.subimCols = int(self._ui.subimCols_lineEdit.text())
        self.subimRows = int(self._ui.subimRows_lineEdit.text())
        self.subimY = int(self._ui.subimX_lineEdit.text())
        self.subimX = int(self._ui.subimY_lineEdit.text())

    def _changeMPTesting(self):
        emit = int(self._ui.emitSigFrame_lineEdit.text())
        capt = int(self._ui.captureFrame_lineEdit.text())
        self._control.changeWhenToEmitAndCapture(emit,capt)

    def _lookForMPEvents(self):
        x0,x1,y0,y1 = self._control._getROI()
        xdim,ydim = x1-x0+1,y1-y0+1
        new_xdim = self.subimX
        new_ydim = self.subimY
        rows = self.subimRows
        cols = self.subimCols
        largeIm = np.zeros((rows*new_xdim, cols*new_ydim))
        if self._control.resultsEvent.is_set():
            print "MP EVENT SET (FROM QTIMER)"
            #while not self._control.qIms.empty():
            for i in range(0,rows):
                for j in range(0,cols):
                    if not self._control.qIms.empty():
                        ims = self._control.qIms.get()
                        numIms = len(ims)/(xdim*ydim)
                        imFromQueue = np.array(ims[0:xdim*ydim].reshape(ydim,xdim))[0:new_xdim,21:21+new_ydim]
                        largeIm[new_xdim*i:new_xdim*(i+1), new_ydim*j:new_ydim*(j+1)] = imFromQueue
            self._ui.graphicsView.setImage(np.flipud(np.rot90(largeIm)))
            self._ui.graphicsView.show()
            self.largeIm = largeIm
            self._updateQueueQTimer.start(10)
            self._control.unSetEvent()
        
        #self._control.resultsEvent.clear()

    def _imShift(self):
        x0,x1,y0,y1 = self._control._getROI()
        xdim,ydim = x1-x0+1,y1-y0+1
        new_xdim = self.subimX
        new_ydim = self.subimY
        rows = self.subimRows
        cols = self.subimCols
        im = self.largeIm
        if not self._control.qIms.empty():
            for i in range(0,rows):
                for j in range(0,cols):
                    if j<(cols-1):
                        oneAhead = im[new_xdim*i:new_xdim*(i+1), new_ydim*(j+1):new_ydim*(j+2)]
                        im[new_xdim*i:new_xdim*(i+1), new_ydim*j:new_ydim*(j+1)] = oneAhead
                    else:
                        if i<(rows-1):
                            oneAhead = im[new_xdim*(i+1):new_xdim*(i+2), new_ydim*0:new_ydim*(0+1)]
                            im[new_xdim*i:new_xdim*(i+1), new_ydim*j:new_ydim*(j+1)] = oneAhead
            imQ = self._control.qIms.get()
            i = rows-1
            j = cols-1
            im[new_xdim*i:new_xdim*(i+1), new_ydim*j:new_ydim*(j+1)] = np.array(imQ[0:xdim*ydim].reshape(ydim,xdim))[0:new_xdim,21:21+new_ydim]
            self.largeIm = im
            self._ui.graphicsView.setImage(np.flipud(np.rot90(im)))
            self._ui.graphicsView.show()
            

    def _flushImQ(self):
        self._control.flushImQ()

    def _dragEnterEvent(self,event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def _dropEvent(self, event):
        for url in event.mimeData().urls():
            filename = str(url.encodedPath())[1:]
            try:
                self._newSettings(filename)
            except:
                print "Unable to load settings file ", filename

    def printInfo(self):
        prec = self._control.getRecordingStruct()
        print "RecSubMode: ", prec.wRecSubmode
        print "RecState: ", prec.wRecState
        print "StorageMode: ", prec.wStorageMode

    def _newSettings(self, filename):
        self._saved_settings = [filename] + self._saved_settings
        self._control.newSettings(filename)
        if len(self._control.saved_settings) > self._max_saved:
            self._control.saved_settings.pop()
        for i,p in enumerate(self._control.saved_settings):
            filename = p['settings_filename']
            radioButton = getattr(self._ui, "settings"+str(i+1)+"_radioButton")
            radiobutton.setText(filename)
            radiobutton.show()

        self._ui.settings1_radioButton.click()

    def toggleSettings(self):
        for i,p in enumerate(self._control.saved_settings):
            radioButton = getattr(self._ui, "settings"+str(i+1)+"_radioButton")
            if radioButton.isChecked():
                #Probably should stop and restart camera here
                self._control.updateSettings('no_file', settings_dict=p)

    def _changeDisplayTxtInfo(self):
        self._displayTxtInfo = self._ui.displayTxtInfo_checkBox.isChecked()

    def _setFilename(self):
        filenum = "%.4i" % self._ui.spinBox_fileNameIndex.value()
        suffix = self._ui.comboBox_filename.currentText()
        self.filename = self._ui.lineEdit_fileName.text() + '_' + filenum + suffix
        if os.path.exists(self.filename+".dax"):
            self._ui.label_fn.setStyleSheet("QLabel { color: red}")
            self._ui.spinBox_fileNameIndex.setStyleSheet("QLabel { color: red}")
            self._ui.spinBox_fileNameIndex.setStyleSheet("QLabel { border-color: red}")
        else:
            self._ui.label_fn.setStyleSheet("QLabel { color: black}")
            self._ui.spinBox_fileNameIndex.setStyleSheet("QLabel { color: black}")
            self._ui.spinBox_fileNameIndex.setStyleSheet("QLabel { border-color: black}")

    def _setDispMin(self):
        self._vmin = self._ui.horizontalSlider_min.value()
        self._ui.label_minSlider.setText("Min: %.1f" % self._vmin)

    def _setDispMax(self):
        self._vmax = self._ui.horizontalSlider_max.value()
        self._ui.label_maxSlider.setText("Max: %.1f" % self._vmax)        
        
    def _getDisplayTimings(self):
        self._delay, self._exp = self._control._getDelayExposureTime()
        self._ui.labelDelay.setText("Actual: %f ms" % (self._delay*1000))
        self._ui.labelExposure.setText("Actual: %f ms" % (self._exp*1000))

    def _setTimings(self):
        exp_time = int(self._ui.lineEdit_ExposureTime.text())
        delay_time = int(self._ui.lineEdit_DelayTime.text())
        exp_units = str(self._ui.comboBox_expunits.currentText())
        delay_units = str(self._ui.comboBox_delayunits.currentText())

        if exp_units not in ['ms','us','ns']:
            exp_units = 'ms'
        if delay_units not in ['ms','us','ns']:
            delay_units = 'ms'

        self._control._setDelayExposureTime(delay_time, exp_time,
                                            delay_units, exp_units)

        self._getDisplayTimings()

    def _resetPreview(self):
        self._previewMode = False
        self._control.stopPreview()
        self._control.beginPreview()
        self._previewMode = True

    def _setROI(self):
        self._control.stopPreview()
        x0 = int(self._ui.x0_lineEdit.text())
        x1 = int(self._ui.x1_lineEdit.text())
        y0 = int(self._ui.y0_lineEdit.text())
        y1 = int(self._ui.y1_lineEdit.text())
        if y1>y0 and x1>x0 and x0>=0 and y0>=0:
            self._control._setROI([x0,x1,y0,y1])
            self._resetPreview()
        x0,x1,y0,y1 = self._control._getROI()
        self._ui.x0_label.setText("%i" % x0)
        self._ui.x1_label.setText("%i" % x1)
        self._ui.y0_label.setText("%i" % y0)
        self._ui.y1_label.setText("%i" % y1)
        xdim,ydim = x1-x0+1,y1-y0+1
        self._ui.labelResolution.setText("%i, %i" % (xdim,ydim))
        self._control._props['dimensions'] = xdim,ydim
        self._ROIDisplayHelper(x0,x1,y0,y1)

    def _ROIDisplayHelper(self, x0,x1,y0,y1):
        roi_display = np.zeros((320,320),dtype=np.uint8)
        x0_scaled = x0/8
        x1_scaled = x1/8
        y0_scaled = y0/8
        y1_scaled = y1/8
        print x0_scaled, x1_scaled
        print y0_scaled, y1_scaled
        roi_display[y0_scaled:y1_scaled+1, x0_scaled:x1_scaled+1] = 255/2
        roi_display[270:,:] = 255
        qt_roiimage = qext.numpy_to_qimage8(roi_display, 0,255,self._cmap)
        roi_pixmap = QtGui.QPixmap.fromImage(qt_roiimage)
        roi_pixmap = roi_pixmap.scaled(320/3, 320/3, QtCore.Qt.KeepAspectRatio)
        self._ui.labelROIDisplay.setPixmap(roi_pixmap)

    def setInitFramesMP(self):
        frames = int(self._ui.initFramesMP_lineEdit.text())
        self._control.setInitFramesMP(frames)

    def _update(self, frame=None):
        if frame is None:
            if self._previewMode:
                np_image = self._control.getImageForPreview()
            else:
                ims = self._control.getImageBuffer()
                if len(ims) > 0:
                    np_image = ims[-1].reshape(self._xres, self._yres)
                else:
                    np_image = None
        else:
            np_image = frame
        if np_image is not None:
            np_min = np_image.min()
            np_max = np_image.max()
            if self._autoscale:
                self._vmin = np_min
                self._vmax = np_max
                self._ui.horizontalSlider_min.setValue(int(np_min))
                self._ui.horizontalSlider_max.setValue(int(np_max))
            qt_image = qext.numpy_to_qimage8(np_image, self._vmin, self._vmax, self._cmap)
            self._pixmap = QtGui.QPixmap.fromImage(qt_image)
            self._pixmap = self._pixmap.scaled(self._xres, self._yres, QtCore.Qt.KeepAspectRatio)
            if self._displayTxtInfo:
                self._ui.labelMin.setText(str(np_min))
                self._ui.labelMax.setText(str(np_max))
                self._ui.labelMean.setText(str(int(np_image.mean())))
                self._ui.labelMedian.setText(str(int(np.median(np_image))))
            self._ui.labelDisplay.setPixmap(self._pixmap)

    def newUpdateTime(self):
        updateTime = float(self._ui.updateTime_lineEdit.text())
        self._buffUpdateTime = updateTime
        print "New buffer update time of: ", self._buffUpdateTime

    def newDisplayUpdateTime(self):
        displayUpdate = float(self._ui.updateDisplayTime_lineEdit.text())
        self.updateDisplayTime = displayUpdate
        self._updater.stop()
        self._updater.start(self.updateDisplayTime)
        print "New display update time of: ", self.updateDisplayTime

    def _startFillBuffers(self):
        self._previewMode = False
        self._control.beginBufferFill()
        self._updateBuffsPending.start(self._buffUpdateTime)

    def _stopFillBuffers(self):
        self._updateBuffsPending.stop()
        self._control.beginPreview()
        self._previewMode = True

    def getFastImages(self):
        numImages = int(self._ui.fastImagesToGet_lineEdit.text())
        self._control.captureFast(numImages)

    def displayFastImage(self):
        frameNumber = int(self._ui.displayFastImage_lineEdit.text())
        image = self._control.getFastImageFrame(frameNumber)
        self._update(frame=image)
        np.save("imageTest.npy", image)
        

    def bufsToQueue(self):
        nBufs = int(self._ui.bufsToQueue_lineEdit.text())
        self._control.addManyBuffers(nBufs)

    def _memToDAX(self):
        self._control.writeMemoryToDAX(self.filename)

    def _recordToDAX(self):
        palette = QtGui.QPalette()
        brush_black = QtGui.QBrush(QtGui.QColor(0,0,0))
        brush_black.setStyle(QtCore.Qt.SolidPattern)
        brush_red = QtGui.QBrush(QtGui.QColor(170,0,0))
        brush_red.setStyle(QtCore.Qt.SolidPattern)
        if not self._bufferFilling:
            self.DAX_or_Memory = RECORD_DAX
            self._control.beginDAXRecording(self.filename)
            self._ui.pushButton_RecordDAX.setText('STOP')
            palette.setBrush(QtGui.QPalette.Active,
                             QtGui.QPalette.Text, brush_red)
            palette.setBrush(QtGui.QPalette.Inactive,
                             QtGui.QPalette.Text, brush_red)
            self._ui.pushButton_RecordDAX.setPalette(palette)
            self._previewMode = False
            self._control.beginBufferFill() #Sets camera to recording state
            self._updateBuffsPending.start(self._buffUpdateTime)
            self._bufferFilling=True
        else:
            self._ui.pushButton_RecordDAX.setText('Record DAX')
            palette.setBrush(QtGui.QPalette.Active,
                             QtGui.QPalette.Text, brush_black)
            palette.setBrush(QtGui.QPalette.Inactive,
                             QtGui.QPalette.Text, brush_black)
            self._updateBuffsPending.stop()
            self._control.beginPreview()
            self._previewMode = True
            self._bufferFilling=False
            self._control.endDAX()
            
    def _recordToMemory(self):
        palette = QtGui.QPalette()
        brush_black = QtGui.QBrush(QtGui.QColor(0,0,0))
        brush_black.setStyle(QtCore.Qt.SolidPattern)
        brush_red = QtGui.QBrush(QtGui.QColor(170,0,0))
        brush_red.setStyle(QtCore.Qt.SolidPattern)
        if not self._bufferFilling:
            self.DAX_or_Memory = RECORD_MEMORY
            self._control._initImages()
            self._ui.pushButton_RecordMemory.setText('STOP')
            palette.setBrush(QtGui.QPalette.Active,
                             QtGui.QPalette.Text, brush_red)
            palette.setBrush(QtGui.QPalette.Inactive,
                             QtGui.QPalette.Text, brush_red)
            self._ui.pushButton_RecordMemory.setPalette(palette)
            self._previewMode = False
            self._control.beginBufferFill() #Sets camera to recording state
            self._updateBuffsPending.start(self._buffUpdateTime)
            self._bufferFilling=True
        else:
            self._ui.pushButton_RecordMemory.setText('Record Memory')
            palette.setBrush(QtGui.QPalette.Active,
                             QtGui.QPalette.Text, brush_black)
            palette.setBrush(QtGui.QPalette.Inactive,
                             QtGui.QPalette.Text, brush_black)
            self._updateBuffsPending.stop()
            self._control.endMP()
            self._control.beginPreview()
            self._previewMode = True
            self._bufferFilling=False
   
    #Connected to QTimer _updateBuffsPending
    def _fillBuffers(self):
        nIms, pending = self._control._fillImages(toDAX=self.DAX_or_Memory)
        if self._displayTxtInfo:
            if nIms>-1:
                self._ui.labelImagesInRAM.setText(str(nIms))
            self._ui.labelImagesPending.setText(str(pending))

    def _saveImages(self):
        self._control._saveImages()

    def _endMP(self): #This should happen when stop recording, but just in case...
        self._control.endMP()

    def _printMPState(self):
        self._control.stateOfProcesses()


    def setAutoscale(self, state):
        self._autoscale = state


    def shutDown(self):
        self._updater.stop()
        self._updateBuffsPending.stop()
