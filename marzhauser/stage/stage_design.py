# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stage_design.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(415, 428)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.labelSetX = QtWidgets.QLabel(self.groupBox)
        self.labelSetX.setObjectName("labelSetX")
        self.gridLayout.addWidget(self.labelSetX, 0, 0, 1, 1)
        self.labelSetY = QtWidgets.QLabel(self.groupBox)
        self.labelSetY.setObjectName("labelSetY")
        self.gridLayout.addWidget(self.labelSetY, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 5, 1, 1)
        self.pushButtonUp = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonUp.setObjectName("pushButtonUp")
        self.gridLayout.addWidget(self.pushButtonUp, 1, 5, 1, 1)
        self.pushButtonHomeXY = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonHomeXY.setObjectName("pushButtonHomeXY")
        self.gridLayout.addWidget(self.pushButtonHomeXY, 2, 5, 1, 1)
        self.pushButtonDown = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonDown.setObjectName("pushButtonDown")
        self.gridLayout.addWidget(self.pushButtonDown, 3, 5, 1, 1)
        self.pushButtonLeft = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonLeft.setObjectName("pushButtonLeft")
        self.gridLayout.addWidget(self.pushButtonLeft, 2, 2, 1, 1)
        self.pushButtonRight = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonRight.setObjectName("pushButtonRight")
        self.gridLayout.addWidget(self.pushButtonRight, 2, 6, 1, 1)
        self.doubleSpinBoxStep = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxStep.setProperty("value", 1.0)
        self.doubleSpinBoxStep.setObjectName("doubleSpinBoxStep")
        self.gridLayout.addWidget(self.doubleSpinBoxStep, 3, 1, 1, 1)
        self.lineEdit_xpos = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_xpos.setObjectName("lineEdit_xpos")
        self.gridLayout.addWidget(self.lineEdit_xpos, 0, 1, 1, 1)
        self.lineEdit_ypos = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_ypos.setObjectName("lineEdit_ypos")
        self.gridLayout.addWidget(self.lineEdit_ypos, 1, 1, 1, 1)
        self.axisstatus_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.axisstatus_pushButton.setObjectName("axisstatus_pushButton")
        self.gridLayout.addWidget(self.axisstatus_pushButton, 0, 6, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_18 = QtWidgets.QLabel(self.groupBox_3)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 1, 1, 1, 1)
        self.labelGetX = QtWidgets.QLabel(self.groupBox_3)
        self.labelGetX.setObjectName("labelGetX")
        self.gridLayout_3.addWidget(self.labelGetX, 3, 0, 1, 1)
        self.labelGetY = QtWidgets.QLabel(self.groupBox_3)
        self.labelGetY.setObjectName("labelGetY")
        self.gridLayout_3.addWidget(self.labelGetY, 4, 0, 1, 1)
        self.labelX = QtWidgets.QLabel(self.groupBox_3)
        self.labelX.setObjectName("labelX")
        self.gridLayout_3.addWidget(self.labelX, 3, 1, 1, 1)
        self.labelY = QtWidgets.QLabel(self.groupBox_3)
        self.labelY.setObjectName("labelY")
        self.gridLayout_3.addWidget(self.labelY, 4, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.groupBox_3)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 1, 2, 1, 1)
        self.labelRangeX = QtWidgets.QLabel(self.groupBox_3)
        self.labelRangeX.setObjectName("labelRangeX")
        self.gridLayout_3.addWidget(self.labelRangeX, 3, 2, 1, 1)
        self.labelRangeY = QtWidgets.QLabel(self.groupBox_3)
        self.labelRangeY.setObjectName("labelRangeY")
        self.gridLayout_3.addWidget(self.labelRangeY, 4, 2, 1, 1)
        self.updateInfo_checkBox = QtWidgets.QCheckBox(self.groupBox_3)
        self.updateInfo_checkBox.setObjectName("updateInfo_checkBox")
        self.gridLayout_3.addWidget(self.updateInfo_checkBox, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.xsawtooth_radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.xsawtooth_radioButton.setObjectName("xsawtooth_radioButton")
        self.gridLayout_2.addWidget(self.xsawtooth_radioButton, 0, 1, 1, 1)
        self.ysawtooth_radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.ysawtooth_radioButton.setObjectName("ysawtooth_radioButton")
        self.gridLayout_2.addWidget(self.ysawtooth_radioButton, 0, 2, 1, 1)
        self.sawtoothMovement_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.sawtoothMovement_lineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.sawtoothMovement_lineEdit.setObjectName("sawtoothMovement_lineEdit")
        self.gridLayout_2.addWidget(self.sawtoothMovement_lineEdit, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 6, 1, 1)
        self.sawtoothRepeats_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.sawtoothRepeats_lineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.sawtoothRepeats_lineEdit.setObjectName("sawtoothRepeats_lineEdit")
        self.gridLayout_2.addWidget(self.sawtoothRepeats_lineEdit, 0, 5, 1, 1)
        self.sawtoothTimeDelay_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.sawtoothTimeDelay_lineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.sawtoothTimeDelay_lineEdit.setObjectName("sawtoothTimeDelay_lineEdit")
        self.gridLayout_2.addWidget(self.sawtoothTimeDelay_lineEdit, 0, 7, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 8, 1, 1)
        self.go_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.go_pushButton.setObjectName("go_pushButton")
        self.gridLayout_2.addWidget(self.go_pushButton, 1, 8, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setObjectName("groupBox_4")
        self.pushButton_getSpeed = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_getSpeed.setGeometry(QtCore.QRect(20, 20, 75, 23))
        self.pushButton_getSpeed.setObjectName("pushButton_getSpeed")
        self.label_vx = QtWidgets.QLabel(self.groupBox_4)
        self.label_vx.setGeometry(QtCore.QRect(110, 20, 81, 16))
        self.label_vx.setObjectName("label_vx")
        self.label_vy = QtWidgets.QLabel(self.groupBox_4)
        self.label_vy.setGeometry(QtCore.QRect(110, 40, 81, 16))
        self.label_vy.setObjectName("label_vy")
        self.lineEdit_vx = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_vx.setGeometry(QtCore.QRect(240, 20, 51, 20))
        self.lineEdit_vx.setObjectName("lineEdit_vx")
        self.lineEdit_vy = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_vy.setGeometry(QtCore.QRect(240, 50, 51, 20))
        self.lineEdit_vy.setObjectName("lineEdit_vy")
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(210, 20, 31, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(210, 50, 31, 16))
        self.label_7.setObjectName("label_7")
        self.pushButton_setVX = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_setVX.setGeometry(QtCore.QRect(300, 20, 51, 23))
        self.pushButton_setVX.setObjectName("pushButton_setVX")
        self.pushButton_setVY = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_setVY.setGeometry(QtCore.QRect(300, 50, 51, 23))
        self.pushButton_setVY.setObjectName("pushButton_setVY")
        self.verticalLayout.addWidget(self.groupBox_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Marzhauser stage"))
        self.groupBox.setTitle(_translate("Form", "Position Control"))
        self.labelSetX.setText(_translate("Form", "x"))
        self.labelSetY.setText(_translate("Form", "y"))
        self.label_4.setText(_translate("Form", "Step:"))
        self.label_5.setText(_translate("Form", "xy"))
        self.pushButtonUp.setText(_translate("Form", "^"))
        self.pushButtonHomeXY.setText(_translate("Form", "Home"))
        self.pushButtonDown.setText(_translate("Form", "v"))
        self.pushButtonLeft.setText(_translate("Form", "<"))
        self.pushButtonRight.setText(_translate("Form", ">"))
        self.axisstatus_pushButton.setText(_translate("Form", "STATUS"))
        self.groupBox_3.setTitle(_translate("Form", "Information"))
        self.label_18.setText(_translate("Form", "Position [um]"))
        self.labelGetX.setText(_translate("Form", "x"))
        self.labelGetY.setText(_translate("Form", "y"))
        self.labelX.setText(_translate("Form", "-"))
        self.labelY.setText(_translate("Form", "-"))
        self.label_21.setText(_translate("Form", "Range [um]"))
        self.labelRangeX.setText(_translate("Form", "-"))
        self.labelRangeY.setText(_translate("Form", "-"))
        self.updateInfo_checkBox.setText(_translate("Form", "update info?"))
        self.groupBox_2.setTitle(_translate("Form", "Saw-tooth movement"))
        self.xsawtooth_radioButton.setText(_translate("Form", "x"))
        self.ysawtooth_radioButton.setText(_translate("Form", "y"))
        self.label.setText(_translate("Form", "microns"))
        self.label_2.setText(_translate("Form", "repeats"))
        self.label_3.setText(_translate("Form", "ms time delay"))
        self.go_pushButton.setText(_translate("Form", "Go"))
        self.groupBox_4.setTitle(_translate("Form", "Velocity"))
        self.pushButton_getSpeed.setText(_translate("Form", "Get Speed"))
        self.label_vx.setText(_translate("Form", "vx: ----"))
        self.label_vy.setText(_translate("Form", "vy: ----"))
        self.label_6.setText(_translate("Form", "X Vel."))
        self.label_7.setText(_translate("Form", "Y Vel."))
        self.pushButton_setVX.setText(_translate("Form", "Set"))
        self.pushButton_setVY.setText(_translate("Form", "Set"))

