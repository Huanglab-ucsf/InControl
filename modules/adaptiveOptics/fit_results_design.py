# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fit_results_design.ui'
#
# Created: Mon Mar 25 18:33:19 2013
#      by: PyQt5 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(733, 385)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mplwidget = MatplotlibWidget(Dialog)
        self.mplwidget.setObjectName(_fromUtf8("mplwidget"))
        self.horizontalLayout.addWidget(self.mplwidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBoxRemovePTTD = QtWidgets.QCheckBox(Dialog)
        self.checkBoxRemovePTTD.setChecked(True)
        self.checkBoxRemovePTTD.setObjectName(_fromUtf8("checkBoxRemovePTTD"))
        self.gridLayout.addWidget(self.checkBoxRemovePTTD, 0, 1, 1, 1)
        self.lineEditCoefficients = QtWidgets.QLineEdit(Dialog)
        self.lineEditCoefficients.setReadOnly(True)
        self.lineEditCoefficients.setObjectName(_fromUtf8("lineEditCoefficients"))
        self.gridLayout.addWidget(self.lineEditCoefficients, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Zernike fit results", None, QtWidgets.QApplication.UnicodeUTF8))
        self.checkBoxRemovePTTD.setText(QtWidgets.QApplication.translate("Dialog", "Remove Piston, Tip, Tilt, Defocus", None, QtWidgets.QApplication.UnicodeUTF8))

#from matplotlibwidget import MatplotlibWidget
