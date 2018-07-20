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

        #Pump 00 GUI
        self._pumpNum = 0  
        self._ui.comboBox_units.addItem("uL/hr")
        self._ui.comboBox_units.addItem("uL/min")
        self._ui.comboBox_units.addItem("mL/min")
        
        self._ui.comboBox_syringe.addItem("BD 1mL")
        self._ui.comboBox_syringe.addItem("BD 3mL")
        self._ui.comboBox_syringe.addItem("BD 5mL")
        self._ui.comboBox_syringe.addItem("BD 10mL")
        self._ui.comboBox_syringe.addItem("BD 20mL")
        self._ui.comboBox_syringe.addItem("BD 30mL")
        self._ui.comboBox_syringe.addItem("BD 50/60mL")
        self._ui.lineEdit_rate.setText('0')

        #Pump 01 GUI
        self._pumpNum1 = 1
        self._ui.comboBox_units1.addItem("uL/hr")
        self._ui.comboBox_units1.addItem("uL/min")
        self._ui.comboBox_units1.addItem("mL/min")
        
        self._ui.comboBox_syringe1.addItem("BD 1mL")
        self._ui.comboBox_syringe1.addItem("BD 3mL")
        self._ui.comboBox_syringe1.addItem("BD 5mL")
        self._ui.comboBox_syringe1.addItem("BD 10mL")
        self._ui.comboBox_syringe1.addItem("BD 20mL")
        self._ui.comboBox_syringe1.addItem("BD 30mL")
        self._ui.comboBox_syringe1.addItem("BD 50/60mL")
        self._ui.lineEdit_rate1.setText('0')

        #Call the start function when the start button is pressed
        self._ui.pushButton_start.clicked.connect(self.start)
        self.live = False

        #Call the stop function when the stop button is pressed
        self._ui.pushButton_stop.clicked.connect(self.stop)
        
        #Changes if a syringe is selected
        syrdiam = (self._ui.comboBox_syringe.currentIndex())
        syrdiam1 = (self._ui.comboBox_syringe1.currentIndex())
        self._control.setSyringeDiameter(self._pumpNum, syrdiam)
        self._control.setSyringeDiameter(self._pumpNum1, syrdiam1)

        self._ui.comboBox_syringe.currentIndexChanged.connect(self.changeSyringe)
        self._ui.comboBox_syringe1.currentIndexChanged.connect(self.changeSyringe1)

    def changeSyringe(self,index):
        syrdiam = index
        self._control.setSyringeDiameter(self._pumpNum, syrdiam)

    def changeSyringe1(self,index):
        syrdiam1 = index
        self._control.setSyringeDiameter(self._pumpNum1, syrdiam1)

    #Start Function - Update pump parameters and start the pump
    def start(self):
        if not self.live:
            
            #Syringe Pump 00 Setup
            rate = float(self._ui.lineEdit_rate.text())
            units = int(self._ui.comboBox_units.currentIndex())
            
            print('PUMP 00 COMMANDS')
            self._control.setAndRun(self._pumpNum, rate, units)

            #Syringe Pump 01 Setup
            rate1 = float(self._ui.lineEdit_rate1.text())
            units1 = int(self._ui.comboBox_units1.currentIndex())

            print('PUMP 01 COMMANDS')
            if rate1 >= 0:
                self._control.setForwardRate(self._pumpNum1, rate1, units1)
                self._control.runForward(self._pumpNum1)
            else:
                self._control.setReverseRate(self._pumpNum1, -rate1, units1)
                self._control.runReverse(self._pumpNum1)
                
            self.live=True
            oldrate = [rate, rate1]
            return oldrate

        #IF ALREADY RUNNING PRESSING BUTTON AGAIN WILL UPDATE FLOW RATES
        else:
            rate = float(self._ui.lineEdit_rate.text())
            units = int(self._ui.comboBox_units.currentIndex())
            
            print('PUMP 00 COMMANDS')
            self._control.setAndRun(self._pumpNum, rate, units)

            #Syringe Pump 01 Setup
            rate1 = float(self._ui.lineEdit_rate1.text())
            units1 = int(self._ui.comboBox_units1.currentIndex())

            print('PUMP 01 COMMANDS')
            if rate1 == 0:
                self._control.stop(self._pumpNum1)
##            elif rate1 == oldrate1:
##                quit
            elif rate1 > 0:
                self._control.setForwardRate(self._pumpNum1, rate1, units1)
                self._control.runForward(self._pumpNum1)
            else:
                self._control.setReverseRate(self._pumpNum1, -rate1, units1)
                self._control.runReverse(self._pumpNum1)
                
            self.live=True
            oldrate = rate
            oldrate1 = rate1

    def stop(self):
        self.live=False
        self._control.stop(self._pumpNum)
        self._control.stop(self._pumpNum1)
           
            
            


        

