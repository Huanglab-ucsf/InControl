# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ti_design.ui'
#
# Created: Sat Jun 02 18:08:51 2012
#      by: PyQt4 UI code generator 4.8.5
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
        Form.resize(401, 182)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Scope", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBoxCali = QtGui.QGroupBox(Form)
        self.groupBoxCali.setTitle(QtGui.QApplication.translate("Form", "Focal plane position calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxCali.setObjectName(_fromUtf8("groupBoxCali"))
        self.verticalLayoutCali = QtGui.QVBoxLayout(self.groupBoxCali)
        self.verticalLayoutCali.setObjectName(_fromUtf8("verticalLayoutCali"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_6 = QtGui.QLabel(self.groupBoxCali)
        self.label_6.setText(QtGui.QApplication.translate("Form", "1) Max. depth [um]:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.doubleSpinBoxCaliMaxDepth = QtGui.QDoubleSpinBox(self.groupBoxCali)
        self.doubleSpinBoxCaliMaxDepth.setMaximum(99.0)
        self.doubleSpinBoxCaliMaxDepth.setSingleStep(0.1)
        self.doubleSpinBoxCaliMaxDepth.setProperty("value", 2.0)
        self.doubleSpinBoxCaliMaxDepth.setObjectName(_fromUtf8("doubleSpinBoxCaliMaxDepth"))
        self.gridLayout.addWidget(self.doubleSpinBoxCaliMaxDepth, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayoutCali.addLayout(self.gridLayout)
        self.label = QtGui.QLabel(self.groupBoxCali)
        self.label.setText(QtGui.QApplication.translate("Form", "2) Focus of coverslip.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayoutCali.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.groupBoxCali)
        self.label_2.setText(QtGui.QApplication.translate("Form", "3) ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.pushButtonCali = QtGui.QPushButton(self.groupBoxCali)
        self.pushButtonCali.setText(QtGui.QApplication.translate("Form", "Calibrate", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonCali.setObjectName(_fromUtf8("pushButtonCali"))
        self.horizontalLayout.addWidget(self.pushButtonCali)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayoutCali.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBoxCali)
        self.groupBoxInformation = QtGui.QGroupBox(Form)
        self.groupBoxInformation.setTitle(QtGui.QApplication.translate("Form", "Information", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxInformation.setObjectName(_fromUtf8("groupBoxInformation"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxInformation)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_3 = QtGui.QLabel(self.groupBoxInformation)
        self.label_3.setText(QtGui.QApplication.translate("Form", "Focal plane [um]:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.labelFocalPlane = QtGui.QLabel(self.groupBoxInformation)
        self.labelFocalPlane.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFocalPlane.setObjectName(_fromUtf8("labelFocalPlane"))
        self.gridLayout_2.addWidget(self.labelFocalPlane, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBoxInformation)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

