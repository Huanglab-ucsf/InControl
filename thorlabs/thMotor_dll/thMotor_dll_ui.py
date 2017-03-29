import numpy as np

from PyQt4 import import QtCore, QtGui
import sys
import time
from functools import partial
'''
This is the UI calling the thMotor_dll.py.
'''

class UI(inLib.DeviceUI):
    def __init__(self, control):
        design_path = 'thorlabs.thMotor_dll.thMotor_dll_design'
        print('Thorlabs stage: Initializing UI.')
        inLib.DeviceUI.__init__(self, control, design_path)
        # Below is a list of assignment to buttons and lineEdits
        self._ui.lineEdit_absolute.returnPressed.connect(partial(self.move_to,None))
        self._ui.lineEdit_relative.returnPressed.connect(partial(self.move_by,None))
        self._ui.lineEdit_stepsize.returnPressed.connect(partial(self.stepsize,None))
        self._ui.pushButton_absolute.clicked.connect(partial(self.move_to,None))
        self._ui.pushButton_relative.clicked.connect(partial(self.move_by,None))
        self._ui.pushButton_stepsize.clicked.connect(partial(self.stepsize,None))
        self._ui.pushButton_up.clicked.connect(self.step_up)
        self._ui.pushButton_down.clicked.connect(self.step_down)
        self._ui.pushButton_home.clicked.connect(self.go_home)
        self._control.initServo()
        self.pos_update()

    def pos_update(self):
        self.c_pos = self._control.currentPos()
        self._ui.lcd_current.display(self.c_pos)

    def go_home(self):
        self._control.goHome()
        self.pos_update()

    def move_to(self, pos = None):
        if pos is None:
            pos = float(self._ui.lineEdit_absolute.text())
        self._control.moveAbsolute(pos)
        self.pos_update()

    def move_by(self, rpos = None):
        if rpos is None:
            rpos = float(self._ui.lineEdit_relative.text())
        self._control.move_relative(rpos)
        self.pos_update()


    def stepsize(self, stp = None):
        if stp = None:
            stp = float(self._ui.lineEdit_stepsize.text())
        self._control.stepSize(stp)
        self.lcd_stepsize.display(stp)

    def step_up(self):
        self._control.stepUp()
        self.pos_update()

    def step_down(self):
        self._control.stepDown()
        self.pos_update()


    def bl_correction(self, dest = None):
        if dest is None:
            dest = float(self._ui.lineEdit_dest.text())
        self._control.bl_correction(dest)
        self.pos_update()


    def shutdown(self):
        self._control.shutDown()
