#!/usr/bin/python

from PyQt5 import QtWidgets,QtCore
import inLib
from Utilities import QExtensions as qext
import numpy as np
from numpy.lib.scimath import sqrt as _msqrt
import copy
import time
import skimage
import threading

class UI(inLib.DeviceUI):
    
    def __init__(self, control):

        #path to design_path
        design_path = 'bmc.MultiDM.mirror_design'
        inLib.DeviceUI.__init__(self, control, design_path)

        self._applyToMirrorThread = ApplyToMirror(self._control)
        self._ui.pushButton_load.clicked.connect(self.loadPattern)
        self._ui.pushButton_rot90.clicked.connect(self.patternRot90)
        self._ui.pushButton_fliplr.clicked.connect(self.patternFlipLR)
        self._ui.pushButton_flipud.clicked.connect(self.patternFlipUD)
        self._ui.pushButton_rotate.clicked.connect(self.patternRotate)
        self._ui.pushButton_getSegs.clicked.connect(self.getSegments)
        self._ui.pushButton_toMirror.clicked.connect(self.toMirror)
        self._ui.pushButton_reset.clicked.connect(self.resetMirror)
        self._ui.pushButton_reconfig.clicked.connect(self.reconfig)
        self._ui.pushButton_mult.clicked.connect(self.setMultiplier)
        self._ui.pushButton_premult.clicked.connect(self.setPreMultiplier)
        self._ui.pushButton_poke.clicked.connect(self.pokeSegment)
        self._ui.pushButton_clear.clicked.connect(self.clearPattern)
        self._ui.pushButton_refresh.clicked.connect(self.refreshPattern)
        self._ui.pushButton_pad.clicked.connect(self.padZeros)
        self._ui.pushButton_applyZern.clicked.connect(self.calcZernike)
        self._ui.pushButton_modulateZernike.clicked.connect(self.modZernike)
        self._ui.pushButton_createGroup.clicked.connect(self.createGroup)
        self._ui.pushButton_setToGroup.clicked.connect(self.setGroupVal)

        self._ui.pushButton_loadSegs.clicked.connect(self.loadSegs)

        self.varyfilename = None

        self._ui.lineEdit_loadMult.setText("10")
        self._ui.lineEdit_npixels.setText(str(self._control.pixels))
        self._ui.lineEdit_zernAmp.setText("0")
        self._ui.lineEdit_premult.setText(str(self._control.preMultiplier))

        self.pattern=None


    def loadPattern(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(None,'Open pattern','','*.npy')
        m = float(self._ui.lineEdit_loadMult.text())
        pattern = self._control.loadPattern(filename, m)
        self._displayPhase(pattern)

    def loadVaryFile(self):
        self.varyfilename = QtWidgets.QFileDialog.getOpenFileName(None,'Open list of files file','','*.*')
        self._ui.label_filenameloaded.setText(self.varyfilename)

    def loadSegs(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None,'Open segments','','*.*')
        print(filename)
        self._control.loadSegments(str(filename))
        segments = self._control.getSegments()
        self._displaySegments(segments)

    def clearPattern(self):
        self._control.clear()
        self._displayPhase(self._control.returnPattern())
        self.reportGeo()

    def refreshPattern(self):
        self._displayPhase(self._control.returnPattern())

    def patternRot90(self):
        pattern = self._control.patternRot90()
        self._displayPhase(pattern)

    def patternFlipLR(self):
        pattern = self._control.patternFlipLR()
        self._displayPhase(pattern)

    def patternFlipUD(self):
        pattern = self._control.patternFlipUD()
        self._displayPhase(pattern)

    def patternRotate(self):
        rot = float(self._ui.lineEdit_rotate.text())
        pattern = self._control.patternRotate(rot)
        self._displayPhase(pattern)

    def getSegments(self):
        self._control.findSegments()
        segments = self._control.getSegments()
        self._displaySegments(segments)

    def reconfig(self):
        cx = int(self._ui.lineEdit_cx.text())
        cy = int(self._ui.lineEdit_cy.text())
        npixels = int(self._ui.lineEdit_npixels.text())
        pattern = self._control.reconfigGeo(cx,cy,npixels)
        self._displayPhase(pattern)
        self.reportGeo()

    def setMultiplier(self):
        mult = float(self._ui.lineEdit_mult.text())
        self._control.setMultiplier(mult)

    def setPreMultiplier(self):
        mult = float(self._ui.lineEdit_premult.text())
        self._control.setPreMultiplier(mult)

    def toMirror(self):
        #self._applyToMirrorThread = ApplyToMirror(self._control)
        self._applyToMirrorThread.start()

    def resetMirror(self):
        print("reset the mirror!")
        self._applyToMirrorThread.stop()

    def pokeSegment(self):
        segment = self._ui.spinBox_segment.value()
        toAdd = int(self._ui.lineEdit_pokeval.text())
        pokeAll = self._ui.checkBox_pokeAll.isChecked()
        self._control.pokeSegment(segment-1,toAdd,pokeAll=pokeAll)
        self._displayPhase(self._control.returnPattern())
        self._displaySegments(self._control.returnSegments())

    def padZeros(self):
        toPad = int(self._ui.lineEdit_pad.text())
        pattern = self._control.padZeros(toPad)
        self._displayPhase(pattern)
        self.reportGeo()

    def reportGeo(self):
        npixels, cx, cy = self._control.getGeoParams()
        self._ui.lineEdit_npixels.setText(str(npixels))
        self._ui.lineEdit_cx.setText(str(int(cx)))
        self._ui.lineEdit_cy.setText(str(int(cy)))

    def calcZernike(self):
        mode = self._ui.spinBox_zernMode.value()
        amplitude = float(self._ui.lineEdit_zernAmp.text())
        mask = self._ui.checkBox_zernMask.isChecked()
        radius = int(self._ui.lineEdit_zernRad.text())
        zern = self._control.calcZernike(mode, amplitude, radius=radius, useMask=mask)
        self._displayZern(zern)

    def modZernike(self):
        pattern = self._control.addZernike()
        self._displayPhase(pattern)

    def createGroup(self):
        groupStr = self._ui.lineEdit_group.text()
        group = np.array([int(s) for s in groupStr.split(',')]) - 1
        p = self._control.highlight_dummy_mirror_segs(group)
        self._displayDummyPattern(p)
        return group

    def setGroupVal(self):
        group = self.createGroup()
        toAdd = int(self._ui.lineEdit_groupVal.text())
        self._control.pokeGroup(group, toAdd)
        #for g in group:
        #    self._control.pokeSegment(g,toAdd,pokeAll=False)
        self._displayPhase(self._control.returnPattern())
        self._displaySegments(self._control.returnSegments())

    
    def _displayDummyPattern(self, pattern):
        if pattern is not None:
            self._ui.mplwidgetGrouped.figure.axes[0].matshow(pattern, cmap='RdBu')
            self._ui.mplwidgetGrouped.draw()

    def _displayZern(self, zernike):
        if zernike is not None:
            self._ui.mplwidgetZern.figure.axes[0].matshow(zernike, cmap='RdBu')
            self._ui.mplwidgetZern.draw()
        
    def _displayPhase(self, phase):
        if phase is not None:
            self._ui.mplwidgetPhase.figure.axes[0].matshow(phase, cmap='RdBu')
            self._ui.mplwidgetPhase.draw()

    def _displaySegments(self, segs):
        if segs is not None:
            self._ui.mplwidgetSegs.figure.axes[0].matshow(segs, cmap='RdBu')
            self._ui.mplwidgetSegs.draw()
        flatsegs = segs.flatten()
        trueSegs = np.zeros((140))
        trueSegs[0:10] = flatsegs[1:11]
        trueSegs[10:130] = flatsegs[12:132]
        trueSegs[130:140] = flatsegs[133:143]
        self._ui.label_meanSeg.setText("Mean: %.2f" % trueSegs.mean())
        self._ui.label_maxSeg.setText("Maximum: %.2f" % trueSegs.max())
        self._ui.label_minSeg.setText("Minimum: %.2f" % trueSegs.min())


    def shutDown(self):
        pass
        #
        #if self._scanner:
        #    self._scanner.wait()


class ApplyToMirror(QtCore.QThread):
    def __init__(self, control):
        QtCore.QThread.__init__(self)
        self._control = control
        self._lock = threading.Lock()

    def stop(self):
        with self._lock:
            self._control.advancePipe()

    def run(self):
        print("Let's apply a pattern to the mirror!")
        self._control.applyToMirror()

