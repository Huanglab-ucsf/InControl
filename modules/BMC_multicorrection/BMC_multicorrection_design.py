# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BMC_multicorrection_design.ui'
#
# Created by: PyQt5 UI code generator 5.6
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
        Form.resize(920, 698)
        self.centralwidget = QtGui.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 470, 231, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Continuous_varying = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.Continuous_varying.setContentsMargins(1, 0, 1, 0)
        self.Continuous_varying.setObjectName("Continuous_varying")
        self.Zernike_slider = QtGui.QSlider(self.verticalLayoutWidget)
        self.Zernike_slider.setMinimum(-50)
        self.Zernike_slider.setMaximum(50)
        self.Zernike_slider.setSingleStep(1)
        self.Zernike_slider.setOrientation(QtCore.Qt.Horizontal)
        self.Zernike_slider.setObjectName("Zernike_slider")
        self.Continuous_varying.addWidget(self.Zernike_slider)
        self.Zernike_mode = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.Zernike_mode.setAutoFillBackground(False)
        self.Zernike_mode.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Zernike_mode.setObjectName("Zernike_mode")
        self.Continuous_varying.addWidget(self.Zernike_mode)
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(310, 70, 481, 481))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_clearpattern = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_clearpattern.setObjectName("pushButton_clearpattern")
        self.horizontalLayout.addWidget(self.pushButton_clearpattern)
        self.pushButton_Fit = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_Fit.setObjectName("pushButton_Fit")
        self.horizontalLayout.addWidget(self.pushButton_Fit)
        self.pushButton_modulate = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_modulate.setObjectName("pushButton_modulate")
        self.horizontalLayout.addWidget(self.pushButton_modulate)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 2, 1)
        self.Pupil_pattern = QtGui.QGraphicsView(self.gridLayoutWidget)
        self.Pupil_pattern.setObjectName("Pupil_pattern")
        self.gridLayout.addWidget(self.Pupil_pattern, 0, 0, 1, 1)
        self.Zernike_coefficients = QtGui.QTableWidget(self.centralwidget)
        self.Zernike_coefficients.setGeometry(QtCore.QRect(40, 70, 251, 391))
        self.Zernike_coefficients.setObjectName("Zernike_coefficients")
        self.Zernike_coefficients.setColumnCount(1)
        self.Zernike_coefficients.setRowCount(13)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.Zernike_coefficients.setHorizontalHeaderItem(0, item)
        self.pushButton_reset = QtGui.QPushButton(self.centralwidget)
        self.pushButton_reset.setGeometry(QtCore.QRect(40, 600, 151, 41))
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.pushButton_apply2mirror = QtGui.QPushButton(self.centralwidget)
        self.pushButton_apply2mirror.setGeometry(QtCore.QRect(200, 600, 141, 41))
        self.pushButton_apply2mirror.setObjectName("pushButton_apply2mirror")
        self.pushButton_acquire = QtGui.QPushButton(self.centralwidget)
        self.pushButton_acquire.setGeometry(QtCore.QRect(350, 600, 141, 41))
        self.pushButton_acquire.setObjectName("pushButton_acquire")
        Form.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Form)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 920, 25))
        self.menubar.setObjectName("menubar")
        Form.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Form)
        self.statusbar.setObjectName("statusbar")
        Form.setStatusBar(self.statusbar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "MainWindow"))
        self.pushButton_clearpattern.setText(_translate("Form", "Clear"))
        self.pushButton_Fit.setText(_translate("Form", "Fit"))
        self.pushButton_modulate.setText(_translate("Form", "Modulate"))
        item = self.Zernike_coefficients.verticalHeaderItem(0)
        item.setText(_translate("Form", "Z4 (defocus)"))
        item = self.Zernike_coefficients.verticalHeaderItem(1)
        item.setText(_translate("Form", "Z5 (astigm. )"))
        item = self.Zernike_coefficients.verticalHeaderItem(2)
        item.setText(_translate("Form", "Z6 (astigm. )"))
        item = self.Zernike_coefficients.verticalHeaderItem(3)
        item.setText(_translate("Form", "Z7 (coma)"))
        item = self.Zernike_coefficients.verticalHeaderItem(4)
        item.setText(_translate("Form", "Z8 (coma)"))
        item = self.Zernike_coefficients.verticalHeaderItem(5)
        item.setText(_translate("Form", "Z9"))
        item = self.Zernike_coefficients.verticalHeaderItem(6)
        item.setText(_translate("Form", "Z10"))
        item = self.Zernike_coefficients.verticalHeaderItem(7)
        item.setText(_translate("Form", "Z11 (pri. spherical)"))
        item = self.Zernike_coefficients.verticalHeaderItem(8)
        item.setText(_translate("Form", "Z12"))
        item = self.Zernike_coefficients.verticalHeaderItem(9)
        item.setText(_translate("Form", "Z13"))
        item = self.Zernike_coefficients.verticalHeaderItem(10)
        item.setText(_translate("Form", "Z14"))
        item = self.Zernike_coefficients.verticalHeaderItem(11)
        item.setText(_translate("Form", "Z15"))
        item = self.Zernike_coefficients.verticalHeaderItem(12)
        item.setText(_translate("Form", "Z16"))
        item = self.Zernike_coefficients.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Amplitude"))
        self.pushButton_reset.setText(_translate("Form", "Reset Mirror"))
        self.pushButton_apply2mirror.setText(_translate("Form", "Apply to mirror"))
        self.pushButton_acquire.setText(_translate("Form", "Acquire image"))