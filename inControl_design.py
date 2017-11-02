# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inControl_design.ui'
#
# Created: Wed Aug 01 11:30:34 2012
#      by: PyQt5 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(197, 355)
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtWidgets.QLabel(Form)
        self.label.setText(QtWidgets.QApplication.translate("Form", "Devices:", None))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.listWidgetDevices = QtWidgets.QListWidget(Form)
        self.listWidgetDevices.setObjectName(_fromUtf8("listWidgetDevices"))
        self.verticalLayout.addWidget(self.listWidgetDevices)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Modules:", None))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.listWidgetModules = QtWidgets.QListWidget(Form)
        self.listWidgetModules.setObjectName(_fromUtf8("listWidgetModules"))
        self.verticalLayout.addWidget(self.listWidgetModules)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "Working Directory:", None))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelDir = QtWidgets.QLabel(Form)
        self.labelDir.setText(QtWidgets.QApplication.translate("Form", "-", None))
        self.labelDir.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelDir.setObjectName(_fromUtf8("labelDir"))
        self.horizontalLayout.addWidget(self.labelDir)
        self.pushButtonDir = QtWidgets.QPushButton(Form)
        self.pushButtonDir.setMaximumSize(QtCore.QSize(25, 16777215))
        self.pushButtonDir.setText(QtWidgets.QApplication.translate("Form", "...", None))
        self.pushButtonDir.setObjectName(_fromUtf8("pushButtonDir"))
        self.horizontalLayout.addWidget(self.pushButtonDir)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit_workingDir = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_workingDir.setObjectName(_fromUtf8("lineEdit_workingDir"))
        self.horizontalLayout_2.addWidget(self.lineEdit_workingDir)
        self.pushButton_setDir = QtWidgets.QPushButton(self.widget)
        self.pushButton_setDir.setMaximumSize(QtCore.QSize(30, 50))
        self.pushButton_setDir.setText(QtWidgets.QApplication.translate("Form", "Set", None))
        self.pushButton_setDir.setObjectName(_fromUtf8("pushButton_setDir"))
        self.horizontalLayout_2.addWidget(self.pushButton_setDir)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

