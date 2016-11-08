# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ms2000_design.ui'
#
# Created: Thu May 29 19:15:18 2014
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(608, 591)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "ASI Stage Control", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Position Control", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 91, 16))
        self.label.setText(QtGui.QApplication.translate("Form", "X Position:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 81, 16))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Y Position: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_xpos = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_xpos.setGeometry(QtCore.QRect(90, 30, 113, 20))
        self.lineEdit_xpos.setObjectName(_fromUtf8("lineEdit_xpos"))
        self.lineEdit_ypos = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_ypos.setGeometry(QtCore.QRect(90, 60, 113, 20))
        self.lineEdit_ypos.setObjectName(_fromUtf8("lineEdit_ypos"))
        self.pushButton_up = QtGui.QPushButton(self.groupBox)
        self.pushButton_up.setGeometry(QtCore.QRect(380, 20, 75, 23))
        self.pushButton_up.setText(QtGui.QApplication.translate("Form", "/\\", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_up.setObjectName(_fromUtf8("pushButton_up"))
        self.pushButton_down = QtGui.QPushButton(self.groupBox)
        self.pushButton_down.setGeometry(QtCore.QRect(380, 80, 75, 23))
        self.pushButton_down.setText(QtGui.QApplication.translate("Form", "\\/", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_down.setObjectName(_fromUtf8("pushButton_down"))
        self.pushButton_left = QtGui.QPushButton(self.groupBox)
        self.pushButton_left.setGeometry(QtCore.QRect(300, 50, 75, 23))
        self.pushButton_left.setText(QtGui.QApplication.translate("Form", "<", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_left.setObjectName(_fromUtf8("pushButton_left"))
        self.pushButton_right = QtGui.QPushButton(self.groupBox)
        self.pushButton_right.setGeometry(QtCore.QRect(460, 50, 75, 23))
        self.pushButton_right.setText(QtGui.QApplication.translate("Form", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_right.setObjectName(_fromUtf8("pushButton_right"))
        self.pushButton_home = QtGui.QPushButton(self.groupBox)
        self.pushButton_home.setGeometry(QtCore.QRect(380, 50, 75, 23))
        self.pushButton_home.setText(QtGui.QApplication.translate("Form", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_home.setObjectName(_fromUtf8("pushButton_home"))
        self.updateInfo_checkBox = QtGui.QCheckBox(self.groupBox)
        self.updateInfo_checkBox.setGeometry(QtCore.QRect(30, 250, 70, 17))
        self.updateInfo_checkBox.setText(QtGui.QApplication.translate("Form", "Update?", None, QtGui.QApplication.UnicodeUTF8))
        self.updateInfo_checkBox.setObjectName(_fromUtf8("updateInfo_checkBox"))
        self.doubleSpinBoxStep = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxStep.setGeometry(QtCore.QRect(90, 100, 62, 22))
        self.doubleSpinBoxStep.setObjectName(_fromUtf8("doubleSpinBoxStep"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 61, 16))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Step size:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(110, 250, 46, 13))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Position:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_position = QtGui.QLabel(self.groupBox)
        self.label_position.setGeometry(QtCore.QRect(160, 250, 161, 16))
        self.label_position.setText(QtGui.QApplication.translate("Form", "--, --", None, QtGui.QApplication.UnicodeUTF8))
        self.label_position.setObjectName(_fromUtf8("label_position"))
        self.pushButton_test = QtGui.QPushButton(self.groupBox)
        self.pushButton_test.setGeometry(QtCore.QRect(330, 240, 231, 23))
        self.pushButton_test.setText(QtGui.QApplication.translate("Form", "Test -- get positions", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_test.setObjectName(_fromUtf8("pushButton_test"))
        self.pushButton_halt = QtGui.QPushButton(self.groupBox)
        self.pushButton_halt.setGeometry(QtCore.QRect(20, 210, 75, 23))
        self.pushButton_halt.setText(QtGui.QApplication.translate("Form", "HALT!", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_halt.setObjectName(_fromUtf8("pushButton_halt"))
        self.pushButton_getSpeed = QtGui.QPushButton(self.groupBox)
        self.pushButton_getSpeed.setGeometry(QtCore.QRect(300, 130, 75, 23))
        self.pushButton_getSpeed.setText(QtGui.QApplication.translate("Form", "Get Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_getSpeed.setObjectName(_fromUtf8("pushButton_getSpeed"))
        self.label_speed = QtGui.QLabel(self.groupBox)
        self.label_speed.setGeometry(QtCore.QRect(395, 130, 131, 20))
        self.label_speed.setText(QtGui.QApplication.translate("Form", "-- mm/s, -- mm/s", None, QtGui.QApplication.UnicodeUTF8))
        self.label_speed.setObjectName(_fromUtf8("label_speed"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 430, 481, 131))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Form", "SCAN", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 40, 101, 16))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Raster scan:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(110, 20, 46, 13))
        self.label_6.setText(QtGui.QApplication.translate("Form", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(190, 20, 46, 13))
        self.label_7.setText(QtGui.QApplication.translate("Form", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(20, 70, 91, 16))
        self.label_8.setText(QtGui.QApplication.translate("Form", "Vertical scan:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.lineEdit_rstart = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_rstart.setGeometry(QtCore.QRect(90, 40, 81, 20))
        self.lineEdit_rstart.setObjectName(_fromUtf8("lineEdit_rstart"))
        self.lineEdit_vstart = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_vstart.setGeometry(QtCore.QRect(90, 70, 81, 20))
        self.lineEdit_vstart.setObjectName(_fromUtf8("lineEdit_vstart"))
        self.lineEdit_rstop = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_rstop.setGeometry(QtCore.QRect(180, 40, 81, 20))
        self.lineEdit_rstop.setObjectName(_fromUtf8("lineEdit_rstop"))
        self.lineEdit_vstop = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_vstop.setGeometry(QtCore.QRect(180, 70, 81, 20))
        self.lineEdit_vstop.setObjectName(_fromUtf8("lineEdit_vstop"))
        self.lineEdit_vlines = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_vlines.setGeometry(QtCore.QRect(270, 70, 81, 20))
        self.lineEdit_vlines.setObjectName(_fromUtf8("lineEdit_vlines"))
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(280, 20, 81, 16))
        self.label_9.setText(QtGui.QApplication.translate("Form", "Number of lines", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.pushButton_setScan = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_setScan.setGeometry(QtCore.QRect(30, 100, 75, 23))
        self.pushButton_setScan.setText(QtGui.QApplication.translate("Form", "Set Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_setScan.setObjectName(_fromUtf8("pushButton_setScan"))
        self.radioButton_xscan = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_xscan.setGeometry(QtCore.QRect(380, 20, 82, 17))
        self.radioButton_xscan.setText(QtGui.QApplication.translate("Form", "X Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_xscan.setObjectName(_fromUtf8("radioButton_xscan"))
        self.radioButton_yscan = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_yscan.setGeometry(QtCore.QRect(380, 40, 82, 17))
        self.radioButton_yscan.setText(QtGui.QApplication.translate("Form", "Y Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_yscan.setObjectName(_fromUtf8("radioButton_yscan"))
        self.radioButton_xyraster = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_xyraster.setGeometry(QtCore.QRect(380, 60, 82, 17))
        self.radioButton_xyraster.setText(QtGui.QApplication.translate("Form", "XY Raster", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_xyraster.setObjectName(_fromUtf8("radioButton_xyraster"))
        self.radioButton_xyserp = QtGui.QRadioButton(self.groupBox_2)
        self.radioButton_xyserp.setGeometry(QtCore.QRect(380, 80, 91, 17))
        self.radioButton_xyserp.setText(QtGui.QApplication.translate("Form", "XY Serpentine", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_xyserp.setObjectName(_fromUtf8("radioButton_xyserp"))
        self.pushButton_scan = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_scan.setGeometry(QtCore.QRect(380, 100, 75, 23))
        self.pushButton_scan.setText(QtGui.QApplication.translate("Form", "SCAN", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_scan.setObjectName(_fromUtf8("pushButton_scan"))
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(310, 170, 46, 13))
        self.label_10.setText(QtGui.QApplication.translate("Form", "X-Speed:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(310, 200, 46, 13))
        self.label_11.setText(QtGui.QApplication.translate("Form", "Y-Speed:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.lineEdit_xspeed = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_xspeed.setGeometry(QtCore.QRect(360, 170, 113, 20))
        self.lineEdit_xspeed.setObjectName(_fromUtf8("lineEdit_xspeed"))
        self.lineEdit_yspeed = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_yspeed.setGeometry(QtCore.QRect(360, 200, 113, 20))
        self.lineEdit_yspeed.setObjectName(_fromUtf8("lineEdit_yspeed"))
        self.label_12 = QtGui.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(20, 140, 46, 13))
        self.label_12.setText(QtGui.QApplication.translate("Form", "x1:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.lineEdit_x1 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_x1.setGeometry(QtCore.QRect(60, 140, 61, 20))
        self.lineEdit_x1.setObjectName(_fromUtf8("lineEdit_x1"))
        self.label_13 = QtGui.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(20, 170, 46, 13))
        self.label_13.setText(QtGui.QApplication.translate("Form", "x2:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.lineEdit_x2 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_x2.setGeometry(QtCore.QRect(60, 170, 61, 20))
        self.lineEdit_x2.setObjectName(_fromUtf8("lineEdit_x2"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 280, 571, 151))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Form", "Stored Locations", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.storePos_pushButton = QtGui.QPushButton(self.groupBox_3)
        self.storePos_pushButton.setGeometry(QtCore.QRect(20, 20, 121, 23))
        self.storePos_pushButton.setText(QtGui.QApplication.translate("Form", "Store Current Position", None, QtGui.QApplication.UnicodeUTF8))
        self.storePos_pushButton.setObjectName(_fromUtf8("storePos_pushButton"))
        self.pos1_radioButton = QtGui.QRadioButton(self.groupBox_3)
        self.pos1_radioButton.setGeometry(QtCore.QRect(20, 60, 83, 17))
        self.pos1_radioButton.setText(QtGui.QApplication.translate("Form", "Pos 1: -,-", None, QtGui.QApplication.UnicodeUTF8))
        self.pos1_radioButton.setObjectName(_fromUtf8("pos1_radioButton"))
        self.pos2_radioButton = QtGui.QRadioButton(self.groupBox_3)
        self.pos2_radioButton.setGeometry(QtCore.QRect(20, 80, 82, 17))
        self.pos2_radioButton.setText(QtGui.QApplication.translate("Form", "Pos 2: -,-", None, QtGui.QApplication.UnicodeUTF8))
        self.pos2_radioButton.setObjectName(_fromUtf8("pos2_radioButton"))
        self.pos3_radioButton = QtGui.QRadioButton(self.groupBox_3)
        self.pos3_radioButton.setGeometry(QtCore.QRect(20, 100, 82, 17))
        self.pos3_radioButton.setText(QtGui.QApplication.translate("Form", "Pos 3: -,-", None, QtGui.QApplication.UnicodeUTF8))
        self.pos3_radioButton.setObjectName(_fromUtf8("pos3_radioButton"))
        self.pos4_radioButton = QtGui.QRadioButton(self.groupBox_3)
        self.pos4_radioButton.setGeometry(QtCore.QRect(20, 120, 82, 17))
        self.pos4_radioButton.setText(QtGui.QApplication.translate("Form", "Pos 4: -,-", None, QtGui.QApplication.UnicodeUTF8))
        self.pos4_radioButton.setObjectName(_fromUtf8("pos4_radioButton"))
        self.clearPos_pushButton = QtGui.QPushButton(self.groupBox_3)
        self.clearPos_pushButton.setGeometry(QtCore.QRect(140, 20, 91, 23))
        self.clearPos_pushButton.setText(QtGui.QApplication.translate("Form", "Clear Positions", None, QtGui.QApplication.UnicodeUTF8))
        self.clearPos_pushButton.setObjectName(_fromUtf8("clearPos_pushButton"))
        self.startBackAndForth_pushButton = QtGui.QPushButton(self.groupBox_3)
        self.startBackAndForth_pushButton.setGeometry(QtCore.QRect(160, 60, 161, 23))
        self.startBackAndForth_pushButton.setText(QtGui.QApplication.translate("Form", "Go From 1 -> 2 -> 1 ...", None, QtGui.QApplication.UnicodeUTF8))
        self.startBackAndForth_pushButton.setObjectName(_fromUtf8("startBackAndForth_pushButton"))
        self.label_14 = QtGui.QLabel(self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(340, 60, 81, 16))
        self.label_14.setText(QtGui.QApplication.translate("Form", "Wait time (sec):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.waitTime_lineEdit = QtGui.QLineEdit(self.groupBox_3)
        self.waitTime_lineEdit.setGeometry(QtCore.QRect(440, 60, 113, 20))
        self.waitTime_lineEdit.setObjectName(_fromUtf8("waitTime_lineEdit"))
        self.stopBackAndForth_pushButton = QtGui.QPushButton(self.groupBox_3)
        self.stopBackAndForth_pushButton.setGeometry(QtCore.QRect(160, 90, 161, 23))
        self.stopBackAndForth_pushButton.setText(QtGui.QApplication.translate("Form", "Stop back and forth", None, QtGui.QApplication.UnicodeUTF8))
        self.stopBackAndForth_pushButton.setObjectName(_fromUtf8("stopBackAndForth_pushButton"))
        self.horizontalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

