#!/usr/bin/python

from PyQt5 import QtCore, QtGui, QAxContainer
import inLib
import time

'''
The list of buttons:
'''




class UI(inLib.DeviceUI):

    def __init__(self, control):
        design_path = 'thorlabs.thorlabsMotors.thorlabsMotors_design'
        print('Thorlabs stage: Initializing UI.')
        inLib.DeviceUI.__init__(self, control, design_path)

        #self.homeX, self.homeY, z = self._control.position()
        self.blrange = 0.01 # the backlash correction range
        self._ui.lineEdit_absolute.returnPressed.connect(self._move)
        self._ui.lineEdit_relative.returnPressed.connect(self._relative)
        self._ui.lineEdit_stepsize.returnPressed.connect(self._stepsize)
        # self._ui.pushButton connection
        self._ui.pushButton_absolute.clicked.connect(self._move)
        self._ui.pushButton_relative.clicked.connect(self._relative)
        self._ui.pushButton_stepsize.clicked.connect(self._stepsize)
        self._ui.pushButton_up.clicked.connect(self._stepUp)
        self._ui.pushButton_down.clicked.connect(self._stepDown)
        self._ui.pushButton_BL.clicked.connect(self._BLcorrect)
        self.dstep = 0.10


        self._control.initServo()



    def _move(self):
        pos = float(self._ui.lineEdit_absolute.text())
        self._control.setStage(pos)
#        self.aptUser.moveTo(pos)

    def _relative(self):
        '''
        relative movement
        '''
        pos = float(self._ui.lineEdit_relative.text())
        self._control.shiftStage(pos)
        # done with _relative

    def _stepsize(self):
        '''
        set the stepsize
        '''
        pos = float(self._ui.lineEdit_stepsize.text())
        self._control.setStep(pos)
        self.dstep = pos
        # done with _stepsize

    def _stepUp(self):
        #self.aptUser.jogUp()
        self._control.jogUp()

    def _stepDown(self):
        #self.aptUser.jogDown()
        self._control.jogDown()

    def _BLcorrect(self):
        '''
        backlash correction
        specify z_start
        '''
        z_start = float(self._ui.lineEdit_BL.text())
        dstep = self.dstep
        self._control.setStage(z_start+self.blrange)
        time.sleep(3)
        ndown = int(self.blrange/dstep)+1
        for ii in range(ndown):
            self._control.jogDown()
            time.sleep(0.25)
         # done with backlash correction

    def shutDown(self):
        self._control.shutDown()
        #self._positionUpdater.stop()





class APTUser1(QAxContainer.QAxWidget):
    def __init__(self, parent = None):
        QAxContainer.QAxWidget.__init__(self, parent)
        self.setControl("MGMOTOR.MGMotorCtrl.1")
        self.dynamicCall('SetHWSerialNum(int)', 83854883)
        self.dynamicCall('StartCtrl()')

        try:
            self.dynamicCall('LoadParamSet(char[])', "smallstep")
        except:
            print("loadparamset for APT User failed")

    def moveTo(self, pos):
        self.dynamicCall('MoveAbsoluteEx(int, double, double, bool)', 0, pos, 0.0, False)

    def jogUp(self):
        self.dynamicCall('MoveJog(int,int)', 0,1)

    def jogDown(self):
        self.dynamicCall('MoveJog(int,int)', 0,2)
