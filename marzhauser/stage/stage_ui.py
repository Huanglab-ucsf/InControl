#!/usr/bin/python

from PyQt4 import QtCore
import inLib
import time


class UI(inLib.DeviceUI):
    
    def __init__(self, control):
        design_path = 'marzhauser.stage.stage_design'
        print 'Marzhauser xy-stage: Initializing UI.'
        inLib.DeviceUI.__init__(self, control, design_path)

        self.homeX, self.homeY, z = self._control.position()

        self._ui.lineEdit_xpos.returnPressed.connect(self._moveX)
        self._ui.lineEdit_ypos.returnPressed.connect(self._moveY)
        self._ui.pushButtonUp.clicked.connect(self._stepUp)
        self._ui.pushButtonDown.clicked.connect(self._stepDown)
        self._ui.pushButtonLeft.clicked.connect(self._stepLeft)
        self._ui.pushButtonRight.clicked.connect(self._stepRight)
        self._ui.pushButtonHomeXY.clicked.connect(self._moveHomeXY)

        self._ui.pushButton_getSpeed.clicked.connect(self.getSpeed)
        self._ui.pushButton_setVX.clicked.connect(self.setVX)
        self._ui.pushButton_setVY.clicked.connect(self.setVY)

        self._ui.axisstatus_pushButton.clicked.connect(self.axisStatus)

        self._ui.updateInfo_checkBox.stateChanged.connect(self._updateInfo)


        self._positionUpdater = QtCore.QTimer()
        self._positionUpdater.timeout.connect(self.updatePositionLabels)
        #self._positionUpdater.start(500) #only if updateInfo checkbox is true

        self._ui.go_pushButton.clicked.connect(self._sawtooth)
        self._sawtoothThread = None

        self._moveThread = None

    def _updateInfo(self):
        state = self._ui.updateInfo_checkBox.isChecked()
        if state:
            self._positionUpdater.start(500)
        else:
            if self._positionUpdater.isActive():
                self._positionUpdater.stop()

    def axisStatus(self):
        status = self._control.getStatusAxis()
        print "Marz axis status: ", status
        if status[0]=='M' or status[1]=='M':
            print "Marz axis status: Moving"

    def _sawtooth(self):
        if self._ui.go_pushButton.text() == 'Go':
            movement = float(self._ui.sawtoothMovement_lineEdit.text())
            repeats = int(self._ui.sawtoothRepeats_lineEdit.text())
            timedelay = int(self._ui.sawtoothTimeDelay_lineEdit.text())
            if self._ui.xsawtooth_radioButton.isChecked():
                xy = 'x'
            else:
                xy = 'y'
            self._sawtoothThread = Sawtooth(self._control, xy,
                                            movement, repeats, timedelay)
            self._window.connect(self._sawtoothThread,
                                 QtCore.SIGNAL('sawtoothDone'),
                                 self._on_sawtoothDone)
            self._ui.go_pushButton.setText('Wait...')
            self._sawtoothThread.start()
    
        
    def _on_sawtoothDone(self):
        self._ui.go_pushButton.setText('Go')
        self._sawtoothThread = None

    def _moveX(self):
        xpos = float(self._ui.lineEdit_xpos.text())
        ypos = self._control.position()[1]
        self._moveThread = Move(self._control, xpos, ypos)
        self._moveThread.start()
        '''
        xpos = float(self._ui.lineEdit_xpos.text())
        ypos = self._control.position[1]
        self._control.goAbsolute(xpos, ypos)
        '''

    def _moveY(self):
        ypos = float(self._ui.lineEdit_ypos.text())
        xpos = self._control.position()[0]
        self._moveThread = Move(self._control, xpos, ypos)
        self._moveThread.start()
        #self._control.goAbsolute(xpos, ypos)

    def _stepUp(self):
        step = self._ui.doubleSpinBoxStep.value()
        self._control.goRelative(0,step)

    def _stepDown(self):
        step = self._ui.doubleSpinBoxStep.value()
        self._control.goRelative(0,-1*step)

    def _stepLeft(self):
        step = self._ui.doubleSpinBoxStep.value()
        self._control.goRelative(-1*step,0)

    def _stepRight(self):
        step = self._ui.doubleSpinBoxStep.value()
        self._control.goRelative(1*step,0)


    def _moveHomeXY(self):
        self._control.goAbsolute(self.homeX,self.homeY)

    def getSpeed(self):
        vx,vy = self._control.getSpeed()
        self._ui.label_vx.setText("%.2f" % vx)
        self._ui.label_vy.setText("%.2f" % vy)

    def setVX(self):
        vx = float(self._ui.lineEdit_vx.text())
        self._control.setSpeed('x', vx)

    def setVY(self):
        vy = float(self._ui.lineEdit_vy.text())
        self._control.setSpeed('y', vy)

    def updatePositionLabels(self):
        x,y,z = self._control.position()
        self._ui.labelX.setText('%.3f' % x)
        self._ui.labelY.setText('%.3f' % y)


    def shutDown(self):
        self._positionUpdater.stop()

class Sawtooth(QtCore.QThread):
    def __init__(self, control, xy, movement, repeats, timedelay):
        QtCore.QThread.__init__(self)

        self.control = control
        self.movement = movement
        self.repeats = repeats
        self.timedelay = timedelay
        self.xy = xy

    def run(self):
        self.control.sawtooth(self.xy,self.movement,self.repeats,self.timedelay)
        self.emit(QtCore.SIGNAL('sawtoothDone'))

class Move(QtCore.QThread):
    def __init__(self, control, xpos, ypos):
        QtCore.QThread.__init__(self)

        self.control = control
        self.xpos = xpos
        self.ypos = ypos

    def run(self):
        self.control.goAbsolute(self.xpos, self.ypos)

