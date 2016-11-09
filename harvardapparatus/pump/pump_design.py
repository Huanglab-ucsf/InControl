# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pump_design_edited.ui'
#
# Created: Thu Aug 02 13:40:49 2012
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
        Form.resize(363, 233)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Syringe Pump", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setText(QtGui.QApplication.translate("Form", "Rate (F5):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 10, 0, 1, 1)
        self.lineEdit_rate1 = QtGui.QLineEdit(Form)
        self.lineEdit_rate1.setObjectName(_fromUtf8("lineEdit_rate1"))
        self.gridLayout.addWidget(self.lineEdit_rate1, 10, 1, 1, 1)
        self.comboBox_units1 = QtGui.QComboBox(Form)
        self.comboBox_units1.setObjectName(_fromUtf8("comboBox_units1"))
        self.gridLayout.addWidget(self.comboBox_units1, 10, 2, 1, 1)
        self.checkBox_withdraw1 = QtGui.QCheckBox(Form)
        self.checkBox_withdraw1.setText(QtGui.QApplication.translate("Form", "Withdraw (F4)", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_withdraw1.setObjectName(_fromUtf8("checkBox_withdraw1"))
        self.gridLayout.addWidget(self.checkBox_withdraw1, 10, 3, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setText(QtGui.QApplication.translate("Form", "Pump 01", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 4)
        self.label_7 = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setText(QtGui.QApplication.translate("Form", "Pump 00", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 4)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setText(QtGui.QApplication.translate("Form", "Syringe Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)
        self.comboBox_syringe1 = QtGui.QComboBox(Form)
        self.comboBox_syringe1.setObjectName(_fromUtf8("comboBox_syringe1"))
        self.gridLayout.addWidget(self.comboBox_syringe1, 8, 1, 1, 1)
        self.comboBox_units = QtGui.QComboBox(Form)
        self.comboBox_units.setObjectName(_fromUtf8("comboBox_units"))
        self.gridLayout.addWidget(self.comboBox_units, 5, 2, 1, 1)
        self.lineEdit_rate = QtGui.QLineEdit(Form)
        self.lineEdit_rate.setObjectName(_fromUtf8("lineEdit_rate"))
        self.gridLayout.addWidget(self.lineEdit_rate, 5, 1, 1, 1)
        self.comboBox_syringe = QtGui.QComboBox(Form)
        self.comboBox_syringe.setObjectName(_fromUtf8("comboBox_syringe"))
        self.gridLayout.addWidget(self.comboBox_syringe, 4, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setText(QtGui.QApplication.translate("Form", "Syringe Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setText(QtGui.QApplication.translate("Form", "Rate (F4):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)
        self.checkBox_withdraw = QtGui.QCheckBox(Form)
        self.checkBox_withdraw.setText(QtGui.QApplication.translate("Form", "Withdraw (F3)", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_withdraw.setChecked(False)
        self.checkBox_withdraw.setObjectName(_fromUtf8("checkBox_withdraw"))
        self.gridLayout.addWidget(self.checkBox_withdraw, 5, 3, 1, 1)
        self.pushButton_start = QtGui.QPushButton(Form)
        self.pushButton_start.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setText(QtGui.QApplication.translate("Form", "Start/Stop (F1)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_start.setObjectName(_fromUtf8("pushButton_start"))
        self.gridLayout.addWidget(self.pushButton_start, 13, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 1, 0, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 11, 0, 1, 4)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 0, 1, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

