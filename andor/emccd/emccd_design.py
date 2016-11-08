# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\emccd_design.ui'
#
# Created: Fri Apr 13 13:29:25 2012
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
        Form.resize(622, 530)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Camera", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pushButtonShutter = QtGui.QPushButton(Form)
        self.pushButtonShutter.setText(QtGui.QApplication.translate("Form", "Open shutter", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonShutter.setObjectName(_fromUtf8("pushButtonShutter"))
        self.verticalLayout_2.addWidget(self.pushButtonShutter)
        self.pushButtonSnapshot = QtGui.QPushButton(Form)
        self.pushButtonSnapshot.setText(QtGui.QApplication.translate("Form", "Snapshot", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSnapshot.setObjectName(_fromUtf8("pushButtonSnapshot"))
        self.verticalLayout_2.addWidget(self.pushButtonSnapshot)
        self.labelGain = QtGui.QLabel(Form)
        self.labelGain.setText(QtGui.QApplication.translate("Form", "EM Gain:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGain.setObjectName(_fromUtf8("labelGain"))
        self.verticalLayout_2.addWidget(self.labelGain)
        self.horizontalSliderGain = QtGui.QSlider(Form)
        self.horizontalSliderGain.setMaximum(300)
        self.horizontalSliderGain.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderGain.setTickPosition(QtGui.QSlider.NoTicks)
        self.horizontalSliderGain.setTickInterval(10)
        self.horizontalSliderGain.setObjectName(_fromUtf8("horizontalSliderGain"))
        self.verticalLayout_2.addWidget(self.horizontalSliderGain)
        self.checkBoxAutoscale = QtGui.QCheckBox(Form)
        self.checkBoxAutoscale.setText(QtGui.QApplication.translate("Form", "Autoscale", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxAutoscale.setChecked(True)
        self.checkBoxAutoscale.setTristate(False)
        self.checkBoxAutoscale.setObjectName(_fromUtf8("checkBoxAutoscale"))
        self.verticalLayout_2.addWidget(self.checkBoxAutoscale)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setText(QtGui.QApplication.translate("Form", "Min:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.labelMin = QtGui.QLabel(Form)
        self.labelMin.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMin.setObjectName(_fromUtf8("labelMin"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.labelMin)
        self.label = QtGui.QLabel(Form)
        self.label.setText(QtGui.QApplication.translate("Form", "Max:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.labelMax = QtGui.QLabel(Form)
        self.labelMax.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMax.setObjectName(_fromUtf8("labelMax"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.labelMax)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setText(QtGui.QApplication.translate("Form", "Mean:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.labelMean = QtGui.QLabel(Form)
        self.labelMean.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMean.setObjectName(_fromUtf8("labelMean"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.labelMean)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setText(QtGui.QApplication.translate("Form", "Median:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_3)
        self.labelMedian = QtGui.QLabel(Form)
        self.labelMedian.setText(QtGui.QApplication.translate("Form", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.labelMedian.setObjectName(_fromUtf8("labelMedian"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.labelMedian)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.qwtPlotHistogram = Qwt5.QwtPlot(Form)
        self.qwtPlotHistogram.setMaximumSize(QtCore.QSize(100, 16777215))
        self.qwtPlotHistogram.setFrameShadow(QtGui.QFrame.Plain)
        self.qwtPlotHistogram.setLineWidth(1)
        self.qwtPlotHistogram.setObjectName(_fromUtf8("qwtPlotHistogram"))
        self.verticalLayout_2.addWidget(self.qwtPlotHistogram)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.labelDisplay = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDisplay.sizePolicy().hasHeightForWidth())
        self.labelDisplay.setSizePolicy(sizePolicy)
        self.labelDisplay.setMinimumSize(QtCore.QSize(512, 512))
        self.labelDisplay.setMaximumSize(QtCore.QSize(512, 512))
        self.labelDisplay.setFrameShape(QtGui.QFrame.Box)
        self.labelDisplay.setFrameShadow(QtGui.QFrame.Sunken)
        self.labelDisplay.setText(_fromUtf8(""))
        self.labelDisplay.setObjectName(_fromUtf8("labelDisplay"))
        self.horizontalLayout.addWidget(self.labelDisplay)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

from PyQt4 import Qwt5
