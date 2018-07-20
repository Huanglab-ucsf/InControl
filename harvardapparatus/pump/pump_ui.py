#!/usr/bin/python

from PyQt5 import QtCore,QtWidgets
from functools import partial
import inLib
import sys
import numpy as np

from Utilities import QExtensions as qext


class UI(inLib.DeviceUI):
    
    def __init__(self, control):
        design_path = 'harvardapparatus.pump.pump_design'
        inLib.DeviceUI.__init__(self, control, design_path)
        self._ui.lineEdit_rate.setText('0')


        self._ui.pushButton_run.clicked.connect(self.start)
        self._ui.pushButton_stp.clicked.connect(self.stop)
        self._ui.comboBox_dia.currentIndexChanged.connect(self.set_diameter)
        self._ui.comboBox_drt.currentIndexChanged.connect(self.set_direction)
        # Initialize the UI
        ver = self._control.findPump()
        if (ver == ''):
            print("Cannnot find the pump.")
        self.set_diameter()

    # ================== Set the syringe pump parameters ====================

    def set_direction(self):
        self.direction = int(self._ui.comboBox_drt.currentIndex())


    def set_rate(self):
        rate = float(self._ui.lineEdit_rat.text())
        units = str(self._ui.comboBox_units.currentText())
        self._control.setRate(rate, units, self.direction)
    
    def set_diameter(self):
        dia_tx = str(self._ui.comboBox_units.currentTest())
        self._control.setDiameter(dia_tx)

    def set_volume(self):
        vol_tx = float(self._ui.lineEdit_vol.text())
        self._control.setVolume(vol_tx, self.direction)


    # ================== Operation functions ================================
    
    def start(self):
        self._control.run(self.direction)
                

    def stop(self):
        self.live=False
        self._control.stop(self._pumpNum)
           
    def clear_vol(self):
        '''
        clear the vol 
        '''
        pass


    def clear_rat(self):
        '''
        clear the rate
        '''
        pass
        
            
    def reset(self):
        pass




        

