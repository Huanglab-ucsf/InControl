# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filter_wheels.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.groupBox_488 = QtWidgets.QGroupBox(Form)
        self.groupBox_488.setGeometry(QtCore.QRect(0, 100, 391, 51))
        self.groupBox_488.setObjectName("groupBox_488")
        self.radioButton_488OD0 = QtWidgets.QRadioButton(self.groupBox_488)
        self.radioButton_488OD0.setGeometry(QtCore.QRect(30, 20, 95, 17))
        self.radioButton_488OD0.setObjectName("radioButton_488OD0")
        self.radioButton_488OD1 = QtWidgets.QRadioButton(self.groupBox_488)
        self.radioButton_488OD1.setGeometry(QtCore.QRect(80, 20, 129, 17))
        self.radioButton_488OD1.setObjectName("radioButton_488OD1")
        self.radioButton_488OD2 = QtWidgets.QRadioButton(self.groupBox_488)
        self.radioButton_488OD2.setGeometry(QtCore.QRect(130, 20, 197, 17))
        self.radioButton_488OD2.setObjectName("radioButton_488OD2")
        self.radioButton_488OD3 = QtWidgets.QRadioButton(self.groupBox_488)
        self.radioButton_488OD3.setGeometry(QtCore.QRect(180, 20, 399, 17))
        self.radioButton_488OD3.setObjectName("radioButton_488OD3")
        self.groupBox_561 = QtWidgets.QGroupBox(Form)
        self.groupBox_561.setGeometry(QtCore.QRect(0, 190, 391, 51))
        self.groupBox_561.setObjectName("groupBox_561")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_561)
        self.radioButton.setGeometry(QtCore.QRect(30, 20, 82, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_561)
        self.radioButton_2.setGeometry(QtCore.QRect(80, 20, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_488.setTitle(_translate("Form", "488 nm"))
        self.radioButton_488OD0.setText(_translate("Form", "OD0"))
        self.radioButton_488OD1.setText(_translate("Form", "OD1"))
        self.radioButton_488OD2.setText(_translate("Form", "OD2"))
        self.radioButton_488OD3.setText(_translate("Form", "OD3"))
        self.groupBox_561.setTitle(_translate("Form", "561 nm"))
        self.radioButton.setText(_translate("Form", "OD0"))
        self.radioButton_2.setText(_translate("Form", "OD1"))

