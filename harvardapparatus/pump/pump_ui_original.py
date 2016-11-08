#!/usr/bin/python

from PyQt4 import QtCore,QtGui
from functools import partial
import inLib
import sys
import numpy as np

from Utilities import QExtensions as qext


class UI(inLib.DeviceUI):
    
    def __init__(self, control):
        design_path = 'harvardapparatus.pump.pump_design'
        inLib.DeviceUI.__init__(self, control, design_path)

        self._pumpNum = 0

        self._ui.comboBox_direction.addItem("Forward")
        self._ui.comboBox_direction.addItem("Reverse")

        self._ui.comboBox_units.addItem("uL/min")
        self._ui.comboBox_units.addItem("mL/min")
        self._ui.comboBox_units.addItem("uL/hr")

        self._ui.lineEdit_rate.setText('0')

        self._ui.pushButton_start.clicked.connect(self.start)

        self.live = False

        
    def start(self):
        self._pumpNum = int(self._ui.spinBox_pumpnum.value())
        if not self.live:
            direction = str(self._ui.comboBox_direction.currentText())
            rate = float(self._ui.lineEdit_rate.text())
            if self._ui.checkBox_maxrate.isChecked():
                if direction=="Forward":
                    self._control.setMaxForwardRate(self._pumpNum)
                elif direction=="Reverse":
                    self._control.setMaxReverseRate(self._pumpNum)
            else:
                units = int(self._ui.comboBox_units.currentIndex())
                if direction=="Forward":
                    self._control.setForwardRate(self._pumpNum, rate, units)
                elif direction=="Reverse":
                    self._control.setReverseRate(self._pumpNum, rate, units)
            if direction=="Forward":
                self._control.runForward(self._pumpNum)
            elif direction=="Reverse":
                self._control.runReverse(self._pumpNum)
            self.live=True
            self._ui.pushButton_start.setText('STOP')
            self._ui.pushButton_start.setStyleSheet("QPushButton { color: red }")
        else:
            self.live=False
            self._control.stop(self._pumpNum)
            self._ui.pushButton_start.setText('Start')
            self._ui.pushButton_start.setStyleSheet("QPushButton { color: black }")
            
            


        

