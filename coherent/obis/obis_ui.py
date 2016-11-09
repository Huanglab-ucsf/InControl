#!/usr/bin/python

from PyQt4 import QtCore,QtGui
from functools import partial
import inLib
import sys
import numpy as np

from Utilities import QExtensions as qext


class UI(inLib.DeviceUI):
    
    def __init__(self, control):
        design_path = 'coherent.obis.obis_design'
        inLib.DeviceUI.__init__(self, control, design_path)

        laser_lines = np.array(self._control.laser_lines)

        w401 = np.where(abs(laser_lines - 401) < 10)
        w488 = np.where(abs(laser_lines - 488) < 10)
        w642 = np.where(abs(laser_lines - 642) < 10)

        laser_ports = [w401[0], w488[0], w642[0]]
        print laser_ports

        self.sliders = [self._ui.Slider401, self._ui.Slider488, self._ui.Slider642]
        self.onoff = [self._ui.On401, self._ui.On488, self._ui.On642]
        self.groupBoxes = [self._ui.OBIS401, self._ui.OBIS488, self._ui.OBIS642]
        color = ["(135,0,205,80)", "(0,240,255,80)", "(255,10,0,80)"]
        self.digMod = [self._ui.checkBox_digMod401, self._ui.checkBox_digMod488, self._ui.checkBox_digMod642]

        for i in range(0,len(laser_ports)):
            if len(laser_ports[i])==1:
                print (i, laser_ports[i][0])
                self.sliders[i].valueChanged.connect(partial(self._updatePower, i, laser_ports[i][0]))
                self.onoff[i].stateChanged.connect(partial(self._turnOnOff, i, laser_ports[i][0]))
                self.digMod[i].stateChanged.connect(partial(self._setDigitalMod, i, laser_ports[i][0]))
                self.groupBoxes[i].setStyleSheet("QGroupBox {background-color: rgba"+color[i]+"}")
            else:
                self.sliders[i].setDisabled(True)
                self.onoff[i].setDisabled(True)
                self.groupBoxes[i].hide()
    

    def _updatePower(self, index, port):
        sliderValue = self.sliders[index].value()
        power_in_mw = self._control._powerInMW(port, sliderValue/100.)
        self._control.setPower(port, power_in_mw)

    def _setDigitalMod(self, index, port):
        state = self.digMod[index].isChecked()
        if state:
            self._control.setExtControl(port, "DIG")
        else:
            self._control.setInternalCW(port)

    def _turnOnOff(self, index, port):
        state = self.onoff[index].isChecked()
        print port, state
        print (self.onoff[0].isChecked(), self.onoff[1].isChecked(), self.onoff[2].isChecked())
        self._control.setLaserOnOff(port, state)
        

