# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'focusLock_design.ui'
#
# Created: Fri Dec 14 16:28:14 2012
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
        Form.resize(688, 427)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 171, 161))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Sampling Rate", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setText(QtGui.QApplication.translate("Form", "Samples: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.samples_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.samples_lineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.samples_lineEdit.setObjectName(_fromUtf8("samples_lineEdit"))
        self.gridLayout.addWidget(self.samples_lineEdit, 0, 1, 1, 1)
        self.sampleRate_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.sampleRate_lineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.sampleRate_lineEdit.setObjectName(_fromUtf8("sampleRate_lineEdit"))
        self.gridLayout.addWidget(self.sampleRate_lineEdit, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setText(QtGui.QApplication.translate("Form", "Sample Rate:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setText(QtGui.QApplication.translate("Form", "Update Time (ms):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.updaterTime_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.updaterTime_lineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.updaterTime_lineEdit.setObjectName(_fromUtf8("updaterTime_lineEdit"))
        self.gridLayout.addWidget(self.updaterTime_lineEdit, 2, 1, 1, 1)
        self.twochannels_checkBox = QtGui.QCheckBox(self.groupBox)
        self.twochannels_checkBox.setText(QtGui.QApplication.translate("Form", "Use two channels?", None, QtGui.QApplication.UnicodeUTF8))
        self.twochannels_checkBox.setObjectName(_fromUtf8("twochannels_checkBox"))
        self.gridLayout.addWidget(self.twochannels_checkBox, 4, 0, 1, 2)
        self.plotOnlyPos_checkBox = QtGui.QCheckBox(self.groupBox)
        self.plotOnlyPos_checkBox.setText(QtGui.QApplication.translate("Form", "Plot only position?", None, QtGui.QApplication.UnicodeUTF8))
        self.plotOnlyPos_checkBox.setObjectName(_fromUtf8("plotOnlyPos_checkBox"))
        self.gridLayout.addWidget(self.plotOnlyPos_checkBox, 5, 0, 1, 2)
        self.qwtPlot = Qwt5.QwtPlot(Form)
        self.qwtPlot.setGeometry(QtCore.QRect(20, 210, 591, 200))
        self.qwtPlot.setObjectName(_fromUtf8("qwtPlot"))
        self.start_pushButton = QtGui.QPushButton(Form)
        self.start_pushButton.setGeometry(QtCore.QRect(190, 0, 91, 23))
        self.start_pushButton.setText(QtGui.QApplication.translate("Form", "START", None, QtGui.QApplication.UnicodeUTF8))
        self.start_pushButton.setObjectName(_fromUtf8("start_pushButton"))
        self.saveData_pushButton = QtGui.QPushButton(Form)
        self.saveData_pushButton.setGeometry(QtCore.QRect(190, 30, 61, 23))
        self.saveData_pushButton.setText(QtGui.QApplication.translate("Form", "Save Data", None, QtGui.QApplication.UnicodeUTF8))
        self.saveData_pushButton.setObjectName(_fromUtf8("saveData_pushButton"))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(340, 10, 281, 191))
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabWidgetPage1 = QtGui.QWidget()
        self.tabWidgetPage1.setObjectName(_fromUtf8("tabWidgetPage1"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabWidgetPage1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.prop_lineEdit = QtGui.QLineEdit(self.tabWidgetPage1)
        self.prop_lineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.prop_lineEdit.setObjectName(_fromUtf8("prop_lineEdit"))
        self.gridLayout_2.addWidget(self.prop_lineEdit, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.tabWidgetPage1)
        self.label_4.setText(QtGui.QApplication.translate("Form", "Proportional:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.isOnFeedback_checkBox = QtGui.QCheckBox(self.tabWidgetPage1)
        self.isOnFeedback_checkBox.setText(QtGui.QApplication.translate("Form", "Turn on?", None, QtGui.QApplication.UnicodeUTF8))
        self.isOnFeedback_checkBox.setObjectName(_fromUtf8("isOnFeedback_checkBox"))
        self.gridLayout_2.addWidget(self.isOnFeedback_checkBox, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.tabWidgetPage1)
        self.label_5.setText(QtGui.QApplication.translate("Form", "Lock Value:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.lock_lineEdit = QtGui.QLineEdit(self.tabWidgetPage1)
        self.lock_lineEdit.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lock_lineEdit.setObjectName(_fromUtf8("lock_lineEdit"))
        self.gridLayout_2.addWidget(self.lock_lineEdit, 2, 1, 1, 1)
        self.current_pushButton = QtGui.QPushButton(self.tabWidgetPage1)
        self.current_pushButton.setText(QtGui.QApplication.translate("Form", "Current Position", None, QtGui.QApplication.UnicodeUTF8))
        self.current_pushButton.setObjectName(_fromUtf8("current_pushButton"))
        self.gridLayout_2.addWidget(self.current_pushButton, 2, 2, 1, 1)
        self.label_6 = QtGui.QLabel(self.tabWidgetPage1)
        self.label_6.setText(QtGui.QApplication.translate("Form", "Piezo Offset: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 3, 0, 1, 1)
        self.piezoOffset_lineEdit = QtGui.QLineEdit(self.tabWidgetPage1)
        self.piezoOffset_lineEdit.setObjectName(_fromUtf8("piezoOffset_lineEdit"))
        self.gridLayout_2.addWidget(self.piezoOffset_lineEdit, 3, 1, 1, 1)
        self.findPiezoOffset_pushButton = QtGui.QPushButton(self.tabWidgetPage1)
        self.findPiezoOffset_pushButton.setText(QtGui.QApplication.translate("Form", "Find Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.findPiezoOffset_pushButton.setObjectName(_fromUtf8("findPiezoOffset_pushButton"))
        self.gridLayout_2.addWidget(self.findPiezoOffset_pushButton, 3, 2, 1, 1)
        self.calibrate_pushButton = QtGui.QPushButton(self.tabWidgetPage1)
        self.calibrate_pushButton.setText(QtGui.QApplication.translate("Form", "Calibrate", None, QtGui.QApplication.UnicodeUTF8))
        self.calibrate_pushButton.setObjectName(_fromUtf8("calibrate_pushButton"))
        self.gridLayout_2.addWidget(self.calibrate_pushButton, 1, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.tabWidgetPage1)
        self.label_7.setText(QtGui.QApplication.translate("Form", "Intensity Thrshld:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 4, 0, 1, 1)
        self.intThreshold_lineEdit = QtGui.QLineEdit(self.tabWidgetPage1)
        self.intThreshold_lineEdit.setObjectName(_fromUtf8("intThreshold_lineEdit"))
        self.gridLayout_2.addWidget(self.intThreshold_lineEdit, 4, 1, 1, 1)
        self.setThreshold_pushButton = QtGui.QPushButton(self.tabWidgetPage1)
        self.setThreshold_pushButton.setText(QtGui.QApplication.translate("Form", "Set Threshold", None, QtGui.QApplication.UnicodeUTF8))
        self.setThreshold_pushButton.setObjectName(_fromUtf8("setThreshold_pushButton"))
        self.gridLayout_2.addWidget(self.setThreshold_pushButton, 4, 2, 1, 1)
        self.tabWidget.addTab(self.tabWidgetPage1, _fromUtf8(""))
        self.Calibration = QtGui.QWidget()
        self.Calibration.setAutoFillBackground(False)
        self.Calibration.setObjectName(_fromUtf8("Calibration"))
        self.gridLayout_3 = QtGui.QGridLayout(self.Calibration)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.dist1_label = QtGui.QLabel(self.Calibration)
        self.dist1_label.setText(QtGui.QApplication.translate("Form", "Distance:", None, QtGui.QApplication.UnicodeUTF8))
        self.dist1_label.setObjectName(_fromUtf8("dist1_label"))
        self.gridLayout_3.addWidget(self.dist1_label, 0, 0, 1, 1)
        self.slope1_label = QtGui.QLabel(self.Calibration)
        self.slope1_label.setText(QtGui.QApplication.translate("Form", "Slope: ", None, QtGui.QApplication.UnicodeUTF8))
        self.slope1_label.setObjectName(_fromUtf8("slope1_label"))
        self.gridLayout_3.addWidget(self.slope1_label, 0, 1, 1, 1)
        self.dist2_label = QtGui.QLabel(self.Calibration)
        self.dist2_label.setText(QtGui.QApplication.translate("Form", "Distance: ", None, QtGui.QApplication.UnicodeUTF8))
        self.dist2_label.setObjectName(_fromUtf8("dist2_label"))
        self.gridLayout_3.addWidget(self.dist2_label, 1, 0, 1, 1)
        self.slope2_label = QtGui.QLabel(self.Calibration)
        self.slope2_label.setText(QtGui.QApplication.translate("Form", "Slope: ", None, QtGui.QApplication.UnicodeUTF8))
        self.slope2_label.setObjectName(_fromUtf8("slope2_label"))
        self.gridLayout_3.addWidget(self.slope2_label, 1, 1, 1, 1)
        self.dist3_label = QtGui.QLabel(self.Calibration)
        self.dist3_label.setText(QtGui.QApplication.translate("Form", "Distance: ", None, QtGui.QApplication.UnicodeUTF8))
        self.dist3_label.setObjectName(_fromUtf8("dist3_label"))
        self.gridLayout_3.addWidget(self.dist3_label, 2, 0, 1, 1)
        self.slope3_label = QtGui.QLabel(self.Calibration)
        self.slope3_label.setText(QtGui.QApplication.translate("Form", "Slope:", None, QtGui.QApplication.UnicodeUTF8))
        self.slope3_label.setObjectName(_fromUtf8("slope3_label"))
        self.gridLayout_3.addWidget(self.slope3_label, 2, 1, 1, 1)
        self.tabWidget.addTab(self.Calibration, _fromUtf8(""))
        self.frame = QtGui.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(200, 60, 105, 71))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.radioButton_plotRealtime = QtGui.QRadioButton(self.frame)
        font = QtGui.QFont()
        font.setKerning(True)
        self.radioButton_plotRealtime.setFont(font)
        self.radioButton_plotRealtime.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.radioButton_plotRealtime.setAutoFillBackground(False)
        self.radioButton_plotRealtime.setText(QtGui.QApplication.translate("Form", "Plot Realtime", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_plotRealtime.setObjectName(_fromUtf8("radioButton_plotRealtime"))
        self.verticalLayout.addWidget(self.radioButton_plotRealtime)
        self.radioButton_plotMeans = QtGui.QRadioButton(self.frame)
        self.radioButton_plotMeans.setText(QtGui.QApplication.translate("Form", "Plot Means", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_plotMeans.setObjectName(_fromUtf8("radioButton_plotMeans"))
        self.verticalLayout.addWidget(self.radioButton_plotMeans)
        self.radioButton_noPlot = QtGui.QRadioButton(self.frame)
        self.radioButton_noPlot.setText(QtGui.QApplication.translate("Form", "Do not plot", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_noPlot.setObjectName(_fromUtf8("radioButton_noPlot"))
        self.verticalLayout.addWidget(self.radioButton_noPlot)
        self.clearData_pushButton = QtGui.QPushButton(Form)
        self.clearData_pushButton.setGeometry(QtCore.QRect(260, 30, 75, 23))
        self.clearData_pushButton.setText(QtGui.QApplication.translate("Form", "Clear Data", None, QtGui.QApplication.UnicodeUTF8))
        self.clearData_pushButton.setObjectName(_fromUtf8("clearData_pushButton"))
        self.label_mean = QtGui.QLabel(Form)
        self.label_mean.setGeometry(QtCore.QRect(20, 180, 151, 16))
        self.label_mean.setText(QtGui.QApplication.translate("Form", "Mean: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_mean.setObjectName(_fromUtf8("label_mean"))
        self.verticalSlider = QtGui.QSlider(Form)
        self.verticalSlider.setGeometry(QtCore.QRect(640, 90, 20, 221))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName(_fromUtf8("verticalSlider"))
        self.upperLim_lineEdit = QtGui.QLineEdit(Form)
        self.upperLim_lineEdit.setGeometry(QtCore.QRect(630, 60, 40, 20))
        self.upperLim_lineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.upperLim_lineEdit.setObjectName(_fromUtf8("upperLim_lineEdit"))
        self.lowerLim_lineEdit = QtGui.QLineEdit(Form)
        self.lowerLim_lineEdit.setGeometry(QtCore.QRect(630, 330, 40, 20))
        self.lowerLim_lineEdit.setMaximumSize(QtCore.QSize(40, 16777215))
        self.lowerLim_lineEdit.setObjectName(_fromUtf8("lowerLim_lineEdit"))

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), QtGui.QApplication.translate("Form", "Focus Position", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Calibration), QtGui.QApplication.translate("Form", "Calibration", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import Qwt5
