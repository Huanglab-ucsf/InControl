#!/usr/bin/python

from PyQt5 import QtWidgets,QtCore
import inLib
from functools import partial
from Utilities import QExtensions as qext

class UI(inLib.DeviceUI):
    def __init__(self, control):
        design_path = 'arduino.parallax.parallax_design'
        inLib.DeviceUI.__init__(self, control, design_path)
        self._ui.radioButton_488OD0.toggled.connect(partial(self.set_488, 0))
        self._ui.radioButton_488OD1.toggled.connect(partial(self.set_488, 1))
        self._ui.radioButton_488OD2.toggled.connect(partial(self.set_488, 2))
        self._ui.radioButton_488OD3.toggled.connect(partial(self.set_488, 3))

    def set_488(self, n_OD):
        print("Optical density:", 0)
        if n_OD ==0:
            pass

