#!/usr/bin/python

from PyQt4 import QtCore
import inLib
from functools import partial
import time


class UI(inLib.DeviceUI):
    
    def __init__(self, control):
        design_path = 'asi.ms2000.ms2000_design'
        print 'ASI MS2000 xy-stage: Initializing UI.'
        inLib.DeviceUI.__init__(self, control, design_path)

        #self.homeX, self.homeY, z = self._control.position()

        self._ui.lineEdit_xpos.returnPressed.connect(self._moveX)
        self._ui.lineEdit_ypos.returnPressed.connect(self._moveY)
        self._ui.pushButton_up.clicked.connect(self._stepUp)
        self._ui.pushButton_down.clicked.connect(self._stepDown)
        self._ui.pushButton_left.clicked.connect(self._stepLeft)
        self._ui.pushButton_right.clicked.connect(self._stepRight)
        self._ui.pushButton_home.clicked.connect(self._moveHomeXY)
        self._ui.pushButton_halt.clicked.connect(self._halt)
        self._ui.pushButton_getSpeed.clicked.connect(self._getSpeed)
        self._ui.pushButton_setScan.clicked.connect(self._setScanParams)
        self._ui.pushButton_scan.clicked.connect(self._startScan)
        self._ui.lineEdit_xspeed.returnPressed.connect(self._setXSpeed)
        self._ui.lineEdit_yspeed.returnPressed.connect(self._setYSpeed)

        self._ui.updateInfo_checkBox.stateChanged.connect(self._updateInfo)

        self._ui.pushButton_test.clicked.connect(self._test)

        self._ui.waitTime_lineEdit.returnPressed.connect(self._setWaitTime)

        self._ui.startBackAndForth_pushButton.clicked.connect(self.startBackAndForth)
        self._ui.stopBackAndForth_pushButton.clicked.connect(self.stopBackAndForth)

        self._ui.storePos_pushButton.clicked.connect(self._storePos)
        self._ui.clearPos_pushButton.clicked.connect(self._clearPos)

        self.posRadioButtons = [self._ui.pos1_radioButton,
                                self._ui.pos2_radioButton,
                                self._ui.pos3_radioButton,
                                self._ui.pos4_radioButton]
        i=0
        for button in self.posRadioButtons:
            button.hide()
            button.clicked.connect(partial(self._goToStoredLoc, i))
            i=i+1

        self.waitTime = 30


        self._positionUpdater = QtCore.QTimer()
        self._positionUpdater.timeout.connect(self.updatePositionLabels)
        #self._positionUpdater.start(500) #only if updateInfo checkbox is true

        self._backAndForthTimer = QtCore.QTimer()
        self._backAndForthTimer.timeout.connect(self.backAndForth)
        self.current = False


    def _updateInfo(self):
        state = self._ui.updateInfo_checkBox.isChecked()
        if state:
            self._positionUpdater.start(500)
        else:
            if self._positionUpdater.isActive():
                self._positionUpdater.stop()

    def _storePos(self):
        locs = self._control.addLocation()
        for i in range(0,len(locs)):
            self.posRadioButtons[i].setText("Pos %i: %.2f,%.2f" % (i,locs[i][0]/10000.,locs[i][1]/10000.))
            self.posRadioButtons[i].setVisible(True)

    def _clearPos(self):
        self._control.clearLocations()
        for button in self.posRadioButtons:
            button.hide()
            button.setText("Pos: --,--")

    def _goToStoredLoc(self,num):
        self._control.goToLocations(num)

    def startBackAndForth(self):
        self._backAndForthTimer.start(self._control.waitTime*1000)

    def stopBackAndForth(self):
        self._backAndForthTimer.stop()

    def backAndForth(self):
        self._control.goToLocations(int(self.current))
        self.current = not self.current

    def _setWaitTime(self):
        #self.waitTime = float(self._ui.waitTime_lineEdit.text())
        wtime = float(self._ui.waitTime_lineEdit.text())
        self._control.setWaitTime(wtime)
                                            

    def _test(self):
        xpos,ypos = self._control.whereStage()
        self._ui.label_position.setText("%.2f, %.2f" % (xpos,ypos))
        print xpos,ypos

    def _setScanParams(self):
        rstart = float(self._ui.lineEdit_rstart.text())
        rstop = float(self._ui.lineEdit_rstop.text())
        vstart = float(self._ui.lineEdit_vstart.text())
        vstop = float(self._ui.lineEdit_vstop.text())
        vlines = int(self._ui.lineEdit_vlines.text())
        self._control.setRScan(rstart,rstop)
        self._control.setVScan(vstart,vstop,vlines)

    def _startScan(self):
        if self._ui.radioButton_xscan.isChecked():
            xscan = 1
            yscan = 0
            f = 0
        elif self._ui.radioButton_yscan.isChecked():
            xscan = 0
            yscan = 1
            f = 0
        elif self._ui.radioButton_xyraster.isChecked():
            xscan = 1
            yscan = 2
            f = 0
        elif self._ui.radioButton_xyserp.isChecked():
            xscan = 1
            yscan = 2
            f = 1
        else:
            return
        self._control.startScan(xscan,yscan,f)
        time.sleep(0.5)
        self._control.startScan(None,None,None)
            
        

    def _halt(self):
        self._control.halt()

    def _getSpeed(self):
        xspeed, yspeed = self._control.getSpeed()
        self._ui.label_speed.setText("%.2f mm/s, %.2f mm/s" % (xspeed, yspeed))

    def _setXSpeed(self):
        speed = float(self._ui.lineEdit_xspeed.text())
        self._control.setSpeed('x', speed)

    def _setYSpeed(self):
        speed = float(self._ui.lineEdit_yspeed.text())
        self._control.setSpeed('y', speed)

    def _moveX(self):
        xpos = float(self._ui.lineEdit_xpos.text())
        self._control.goAbsolute('x', xpos)

    def _moveY(self):
        ypos = float(self._ui.lineEdit_ypos.text())
        self._control.goAbsolute('y', ypos)

    def _stepUp(self):
        step = self._ui.doubleSpinBoxStep.value()
        self._control.goRelative('y',step)

    def _stepDown(self):
        step = self._ui.doubleSpinBoxStep.value()
        self._control.goRelative('y',-1*step)

    def _stepLeft(self):
        step = self._ui.doubleSpinBoxStep.value()
        self._control.goRelative('x',-1*step)

    def _stepRight(self):
        step = self._ui.doubleSpinBoxStep.value()
        self._control.goRelative('x',1*step)


    def _moveHomeXY(self):
        print "Moving home..."
        #self._control.goAbsolute(self.homeX,self.homeY)


    def updatePositionLabels(self):
        x,y,z = 0,0,0
        #x,y,z = self._control.position()
        #self._ui.labelX.setText('%.3f' % x)
        #self._ui.labelY.setText('%.3f' % y)


    def shutDown(self):
        self._positionUpdater.stop()



