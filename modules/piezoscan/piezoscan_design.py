# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'piezoscan_design.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(311, 119)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 5, 0, 1, 1)
        self.doubleSpinBoxStart = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBoxStart.setMinimum(-99.99)
        self.doubleSpinBoxStart.setProperty("value", -2.0)
        self.doubleSpinBoxStart.setObjectName("doubleSpinBoxStart")
        self.gridLayout.addWidget(self.doubleSpinBoxStart, 3, 1, 1, 1)
        self.doubleSpinBoxEnd = QtWidgets.QDoubleSpinBox(Form)
        self.doubleSpinBoxEnd.setMinimum(-99.0)
        self.doubleSpinBoxEnd.setProperty("value", 2.0)
        self.doubleSpinBoxEnd.setObjectName("doubleSpinBoxEnd")
        self.gridLayout.addWidget(self.doubleSpinBoxEnd, 4, 1, 1, 1)
        self.spinBoxNSteps = QtWidgets.QSpinBox(Form)
        self.spinBoxNSteps.setMinimum(2)
        self.spinBoxNSteps.setMaximum(9999)
        self.spinBoxNSteps.setProperty("value", 5)
        self.spinBoxNSteps.setObjectName("spinBoxNSteps")
        self.gridLayout.addWidget(self.spinBoxNSteps, 5, 1, 1, 1)
        self.pushButtonScan = QtWidgets.QPushButton(Form)
        self.pushButtonScan.setEnabled(True)
        self.pushButtonScan.setObjectName("pushButtonScan")
        self.gridLayout.addWidget(self.pushButtonScan, 6, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.spinBoxNFrames = QtWidgets.QSpinBox(Form)
        self.spinBoxNFrames.setMinimum(1)
        self.spinBoxNFrames.setMaximum(100)
        self.spinBoxNFrames.setProperty("value", 1)
        self.spinBoxNFrames.setObjectName("spinBoxNFrames")
        self.gridLayout.addWidget(self.spinBoxNFrames, 6, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 2, 1, 1)
        self.labelStepSize = QtWidgets.QLabel(Form)
        self.labelStepSize.setObjectName("labelStepSize")
        self.gridLayout.addWidget(self.labelStepSize, 3, 3, 1, 1)
        self.checkBoxSave = QtWidgets.QCheckBox(Form)
        self.checkBoxSave.setChecked(True)
        self.checkBoxSave.setObjectName("checkBoxSave")
        self.gridLayout.addWidget(self.checkBoxSave, 4, 2, 1, 1)
        self.lineEditFile = QtWidgets.QLineEdit(Form)
        self.lineEditFile.setObjectName("lineEditFile")
        self.gridLayout.addWidget(self.lineEditFile, 4, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Piezoscan"))
        self.label_7.setText(_translate("Form", "Start [um]:"))
        self.label_8.setText(_translate("Form", "End [um]:"))
        self.label_9.setText(_translate("Form", "# Steps:"))
        self.pushButtonScan.setText(_translate("Form", "Start"))
        self.label_2.setText(_translate("Form", "# Frames/step:"))
        self.label_11.setText(_translate("Form", "Step size [nm]:"))
        self.labelStepSize.setText(_translate("Form", "-"))
        self.checkBoxSave.setText(_translate("Form", "Save"))

