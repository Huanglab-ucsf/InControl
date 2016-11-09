# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nanodrive_design.ui'
#
# Created: Wed Jan 30 16:15:38 2013
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
        Form.resize(449, 280)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Piezo stage", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Position Control", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelSetX = QtGui.QLabel(self.groupBox)
        self.labelSetX.setText(QtGui.QApplication.translate("Form", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSetX.setObjectName(_fromUtf8("labelSetX"))
        self.gridLayout.addWidget(self.labelSetX, 0, 0, 1, 1)
        self.labelSetY = QtGui.QLabel(self.groupBox)
        self.labelSetY.setText(QtGui.QApplication.translate("Form", "y", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSetY.setObjectName(_fromUtf8("labelSetY"))
        self.gridLayout.addWidget(self.labelSetY, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setText(QtGui.QApplication.translate("Form", "z", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setText(QtGui.QApplication.translate("Form", "Step:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setText(QtGui.QApplication.translate("Form", "xy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 5, 1, 1)
        self.pushButtonUp = QtGui.QPushButton(self.groupBox)
        self.pushButtonUp.setText(QtGui.QApplication.translate("Form", "^", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonUp.setObjectName(_fromUtf8("pushButtonUp"))
        self.gridLayout.addWidget(self.pushButtonUp, 1, 5, 1, 1)
        self.pushButtonHomeXY = QtGui.QPushButton(self.groupBox)
        self.pushButtonHomeXY.setText(QtGui.QApplication.translate("Form", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonHomeXY.setObjectName(_fromUtf8("pushButtonHomeXY"))
        self.gridLayout.addWidget(self.pushButtonHomeXY, 2, 5, 1, 1)
        self.pushButtonDown = QtGui.QPushButton(self.groupBox)
        self.pushButtonDown.setText(QtGui.QApplication.translate("Form", "v", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDown.setObjectName(_fromUtf8("pushButtonDown"))
        self.gridLayout.addWidget(self.pushButtonDown, 3, 5, 1, 1)
        self.pushButtonLeft = QtGui.QPushButton(self.groupBox)
        self.pushButtonLeft.setText(QtGui.QApplication.translate("Form", "<", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLeft.setObjectName(_fromUtf8("pushButtonLeft"))
        self.gridLayout.addWidget(self.pushButtonLeft, 2, 2, 1, 1)
        self.pushButtonRight = QtGui.QPushButton(self.groupBox)
        self.pushButtonRight.setText(QtGui.QApplication.translate("Form", ">", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonRight.setObjectName(_fromUtf8("pushButtonRight"))
        self.gridLayout.addWidget(self.pushButtonRight, 2, 6, 1, 1)
        self.pushButtonUpZ = QtGui.QPushButton(self.groupBox)
        self.pushButtonUpZ.setText(QtGui.QApplication.translate("Form", "^", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonUpZ.setObjectName(_fromUtf8("pushButtonUpZ"))
        self.gridLayout.addWidget(self.pushButtonUpZ, 1, 7, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setText(QtGui.QApplication.translate("Form", "z", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 7, 1, 1)
        self.pushButtonHomeZ = QtGui.QPushButton(self.groupBox)
        self.pushButtonHomeZ.setText(QtGui.QApplication.translate("Form", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonHomeZ.setObjectName(_fromUtf8("pushButtonHomeZ"))
        self.gridLayout.addWidget(self.pushButtonHomeZ, 2, 7, 1, 1)
        self.pushButtonDownZ = QtGui.QPushButton(self.groupBox)
        self.pushButtonDownZ.setText(QtGui.QApplication.translate("Form", "v", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonDownZ.setObjectName(_fromUtf8("pushButtonDownZ"))
        self.gridLayout.addWidget(self.pushButtonDownZ, 3, 7, 1, 1)
        self.doubleSpinBoxX = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxX.setObjectName(_fromUtf8("doubleSpinBoxX"))
        self.gridLayout.addWidget(self.doubleSpinBoxX, 0, 1, 1, 1)
        self.doubleSpinBoxY = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxY.setObjectName(_fromUtf8("doubleSpinBoxY"))
        self.gridLayout.addWidget(self.doubleSpinBoxY, 1, 1, 1, 1)
        self.doubleSpinBoxZ = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxZ.setObjectName(_fromUtf8("doubleSpinBoxZ"))
        self.gridLayout.addWidget(self.doubleSpinBoxZ, 2, 1, 1, 1)
        self.doubleSpinBoxStep = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxStep.setProperty("value", 1.0)
        self.doubleSpinBoxStep.setObjectName(_fromUtf8("doubleSpinBoxStep"))
        self.gridLayout.addWidget(self.doubleSpinBoxStep, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtGui.QGroupBox(Form)
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Form", "Information", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_18 = QtGui.QLabel(self.groupBox_3)
        self.label_18.setText(QtGui.QApplication.translate("Form", "Position [um]", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_3.addWidget(self.label_18, 1, 1, 1, 1)
        self.labelGetX = QtGui.QLabel(self.groupBox_3)
        self.labelGetX.setText(QtGui.QApplication.translate("Form", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGetX.setObjectName(_fromUtf8("labelGetX"))
        self.gridLayout_3.addWidget(self.labelGetX, 3, 0, 1, 1)
        self.labelGetY = QtGui.QLabel(self.groupBox_3)
        self.labelGetY.setText(QtGui.QApplication.translate("Form", "y", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGetY.setObjectName(_fromUtf8("labelGetY"))
        self.gridLayout_3.addWidget(self.labelGetY, 4, 0, 1, 1)
        self.label_16 = QtGui.QLabel(self.groupBox_3)
        self.label_16.setText(QtGui.QApplication.translate("Form", "z", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_3.addWidget(self.label_16, 5, 0, 1, 1)
        self.labelX = QtGui.QLabel(self.groupBox_3)
        self.labelX.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelX.setObjectName(_fromUtf8("labelX"))
        self.gridLayout_3.addWidget(self.labelX, 3, 1, 1, 1)
        self.labelY = QtGui.QLabel(self.groupBox_3)
        self.labelY.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelY.setObjectName(_fromUtf8("labelY"))
        self.gridLayout_3.addWidget(self.labelY, 4, 1, 1, 1)
        self.labelZ = QtGui.QLabel(self.groupBox_3)
        self.labelZ.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelZ.setObjectName(_fromUtf8("labelZ"))
        self.gridLayout_3.addWidget(self.labelZ, 5, 1, 1, 1)
        self.label_21 = QtGui.QLabel(self.groupBox_3)
        self.label_21.setText(QtGui.QApplication.translate("Form", "Range [um]", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout_3.addWidget(self.label_21, 1, 2, 1, 1)
        self.labelRangeX = QtGui.QLabel(self.groupBox_3)
        self.labelRangeX.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRangeX.setObjectName(_fromUtf8("labelRangeX"))
        self.gridLayout_3.addWidget(self.labelRangeX, 3, 2, 1, 1)
        self.labelRangeY = QtGui.QLabel(self.groupBox_3)
        self.labelRangeY.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRangeY.setObjectName(_fromUtf8("labelRangeY"))
        self.gridLayout_3.addWidget(self.labelRangeY, 4, 2, 1, 1)
        self.labelRangeZ = QtGui.QLabel(self.groupBox_3)
        self.labelRangeZ.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRangeZ.setObjectName(_fromUtf8("labelRangeZ"))
        self.gridLayout_3.addWidget(self.labelRangeZ, 5, 2, 1, 1)
        self.updateInfo_checkBox = QtGui.QCheckBox(self.groupBox_3)
        self.updateInfo_checkBox.setText(QtGui.QApplication.translate("Form", "Update info?", None, QtGui.QApplication.UnicodeUTF8))
        self.updateInfo_checkBox.setObjectName(_fromUtf8("updateInfo_checkBox"))
        self.gridLayout_3.addWidget(self.updateInfo_checkBox, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass
