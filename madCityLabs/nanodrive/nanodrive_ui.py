#!/usr/bin/python

from PyQt5 import QtCore
import inLib
import time


class UI(inLib.DeviceUI):
    
    def __init__(self, control):
        design_path = 'madCityLabs.nanodrive.nanodrive_design'
        print('piezo: Initializing UI.')
        inLib.DeviceUI.__init__(self, control, design_path)

        self._nAxis = self._control.getNAxis()

        if self._nAxis == 1:
            self._ui.doubleSpinBoxY.setEnabled(False)
            self._ui.pushButtonUp.setEnabled(False)
            self._ui.pushButtonDown.setEnabled(False)
            self._ui.doubleSpinBoxY.setEnabled(False)
            self._ui.labelSetY.setEnabled(False)
            self._ui.labelGetY.setEnabled(False)
            self._ui.labelY.setEnabled(False)
            self._ui.labelRangeY.setEnabled(False)
            self._ui.doubleSpinBoxX.setEnabled(False)
            self._ui.pushButtonRight.setEnabled(False)
            self._ui.pushButtonLeft.setEnabled(False)
            self._ui.doubleSpinBoxX.setEnabled(False)
            self._ui.labelSetX.setEnabled(False)
            self._ui.labelGetX.setEnabled(False)
            self._ui.labelX.setEnabled(False)
            self._ui.labelRangeX.setEnabled(False)
            self._ui.pushButtonHomeXY.setEnabled(False)

        elif self._nAxis == 2:
            self._ui.doubleSpinBoxZ.setEnabled(False)
            self._ui.pushButtonUpZ.setEnabled(False)
            self._ui.pushButtonDownZ.setEnabled(False)
            self._ui.doubleSpinBoxZ.setEnabled(False)
            self._ui.labelSetZ.setEnabled(False)
            self._ui.labelGetZ.setEnabled(False)
            self._ui.labelZ.setEnabled(False)
            self._ui.labelRangeZ.setEnabled(False)

        axis_range = self._control.getAxisRange()

        if self._nAxis in (1,3):
            self._ui.labelRangeZ.setText('%.3f' % axis_range[3])
        if self._nAxis in (2,3):
            self._ui.labelRangeX.setText('%.3f' % axis_range[1])
            self._ui.labelRangeY.setText('%.3f' % axis_range[2])

        self._ui.doubleSpinBoxX.editingFinished.connect(self._moveToX)
        self._ui.doubleSpinBoxY.editingFinished.connect(self._moveToY)
        self._ui.doubleSpinBoxZ.editingFinished.connect(self._moveToZ)
        self._ui.pushButtonUp.clicked.connect(self._stepUp)
        self._ui.pushButtonUpZ.clicked.connect(self._stepUpZ)
        self._ui.pushButtonDownZ.clicked.connect(self._stepDownZ)
        #self._window.connect(self._ui.pushButtonUp,QtCore.SIGNAL('clicked()'),self._stepUp)
        #self._window.connect(self._ui.pushButtonDown,QtCore.SIGNAL('clicked()'),self._stepDown)
        #self._window.connect(self._ui.pushButtonLeft,QtCore.SIGNAL('clicked()'),self._stepLeft)
        #self._window.connect(self._ui.pushButtonRight,QtCore.SIGNAL('clicked()'),self._stepRight)
        #self._window.connect(self._ui.pushButtonHomeXY,QtCore.SIGNAL('clicked()'),self.moveHomeXY)
        #self._window.connect(self._ui.pushButtonUpZ,QtCore.SIGNAL('clicked()'),self._stepUpZ)
        #self._window.connect(self._ui.pushButtonDownZ,QtCore.SIGNAL('clicked()'),self._stepDownZ)
        #self._window.connect(self._ui.pushButtonHomeZ,QtCore.SIGNAL('clicked()'),self.moveHomeZ)

        self._ui.updateInfo_checkBox.stateChanged.connect(self._updateInfo)
        self._positionUpdater = QtCore.QTimer()
        self._positionUpdater.timeout.connect(self.updatePositionLabels)
        #self._positionUpdater.start(500)

    def _updateInfo(self):
        state = self._ui.updateInfo_checkBox.isChecked()
        if state:
            self._positionUpdater.start(500)
        else:
            if self._positionUpdater.isActive():
                self._positionUpdater.stop()

    def moveTo(self, axis, position):
        self._control.moveTo(axis, position)


    def _moveToX(self):
        position = self._ui.doubleSpinBoxX.value()
        self.moveTo(1, position)


    def _moveToY(self):
        position = self._ui.doubleSpinBoxY.value()
        self._control.moveTo(2, position)


    def _moveToZ(self):
        position = self._ui.doubleSpinBoxZ.value()
        self.moveTo(3, position)


    def step(self, axis, step):
        self._control.step(axis, step)


    def _stepUp(self):
        step = self._ui.doubleSpinBoxStep.value()
        self.step(2, step)


    def _stepDown(self):
        step = self._ui.doubleSpinBoxStep.value()
        self.step(2, -step)


    def _stepLeft(self):
        step = self._ui.doubleSpinBoxStep.value()
        self.step(1, -step)


    def _stepRight(self):
        step = self._ui.doubleSpinBoxStep.value()
        self.step(1, step)


    def moveHomeXY(self):
        self._control.moveHomeXY()


    def _stepUpZ(self):
        step = self._ui.doubleSpinBoxStep.value()
        self.step(3, step)


    def _stepDownZ(self):
        step = self._ui.doubleSpinBoxStep.value()
        self.step(3, -step)


    def moveHomeZ(self):
        self._control.moveHomeZ()


    def updatePositionLabels(self):
        if self._nAxis in (1,3):
            position = self._control.getPosition(3)
            self._ui.labelZ.setText('%.3f' % position)
        if self._nAxis in (2,3):
            position = self._control.getPosition(1)
            self._ui.labelX.setText('%.3f' % position)
            position = self._control.getPosition(2)
            self._ui.labelY.setText('%.3f' % position)


    def shutDown(self):
        self._positionUpdater.stop()
