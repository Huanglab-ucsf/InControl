# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BMC_multicorrection_design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from matplotlibwidget import MatplotlibWidget


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(968, 698)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(Form)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(230, 430, 357, 131))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.grid_mainbuttons = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.grid_mainbuttons.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.grid_mainbuttons.setHorizontalSpacing(6)
        self.grid_mainbuttons.setObjectName(_fromUtf8("grid_mainbuttons"))
        self.pushButton_segments = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_segments.sizePolicy().hasHeightForWidth())
        self.pushButton_segments.setSizePolicy(sizePolicy)
        self.pushButton_segments.setObjectName(_fromUtf8("pushButton_segments"))
        self.grid_mainbuttons.addWidget(self.pushButton_segments, 0, 1, 1, 1)
        self.pushButton_clear = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_clear.sizePolicy().hasHeightForWidth())
        self.pushButton_clear.setSizePolicy(sizePolicy)
        self.pushButton_clear.setObjectName(_fromUtf8("pushButton_clear"))
        self.grid_mainbuttons.addWidget(self.pushButton_clear, 0, 4, 1, 1)
        self.pushButton_apply2mirror = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_apply2mirror.sizePolicy().hasHeightForWidth())
        self.pushButton_apply2mirror.setSizePolicy(sizePolicy)
        self.pushButton_apply2mirror.setObjectName(_fromUtf8("pushButton_apply2mirror"))
        self.grid_mainbuttons.addWidget(self.pushButton_apply2mirror, 1, 1, 1, 1)
        self.pushButton_reset = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_reset.sizePolicy().hasHeightForWidth())
        self.pushButton_reset.setSizePolicy(sizePolicy)
        self.pushButton_reset.setObjectName(_fromUtf8("pushButton_reset"))
        self.grid_mainbuttons.addWidget(self.pushButton_reset, 1, 4, 1, 1)
        self.pushButton_acquire = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_acquire.sizePolicy().hasHeightForWidth())
        self.pushButton_acquire.setSizePolicy(sizePolicy)
        self.pushButton_acquire.setObjectName(_fromUtf8("pushButton_acquire"))
        self.grid_mainbuttons.addWidget(self.pushButton_acquire, 0, 0, 1, 1)
        self.pushButton_snapshot = QtGui.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_snapshot.sizePolicy().hasHeightForWidth())
        self.pushButton_snapshot.setSizePolicy(sizePolicy)
        self.pushButton_snapshot.setObjectName(_fromUtf8("pushButton_snapshot"))
        self.grid_mainbuttons.addWidget(self.pushButton_snapshot, 1, 0, 1, 1)
        self.tab_display = QtGui.QTabWidget(self.centralwidget)
        self.tab_display.setGeometry(QtCore.QRect(10, 40, 581, 361))
        self.tab_display.setObjectName(_fromUtf8("tab_display"))
        self.tab_image_phase = QtGui.QWidget()
        self.tab_image_phase.setObjectName(_fromUtf8("tab_image_phase"))
        self.mpl_image = MatplotlibWidget(self.tab_image_phase)
        self.mpl_image.setGeometry(QtCore.QRect(10, 30, 271, 271))
        self.mpl_image.setObjectName(_fromUtf8("mpl_image"))
        self.mpl_phase =MatplotlibWidget(self.tab_image_phase)
        self.mpl_phase.setGeometry(QtCore.QRect(280, 30, 281, 271))
        self.mpl_phase.setObjectName(_fromUtf8("mpl_phase"))
        self.tab_display.addTab(self.tab_image_phase, _fromUtf8(""))
        self.tab_metric = QtGui.QWidget()
        self.tab_metric.setObjectName(_fromUtf8("tab_metric"))
        self.mpl_metrics = MatplotlibWidget(self.tab_metric)
        self.mpl_metrics.setGeometry(QtCore.QRect(10, 60, 551, 251))
        self.mpl_metrics.setObjectName(_fromUtf8("mpl_metrics"))
        self.pushButton_metric = QtGui.QPushButton(self.tab_metric)
        self.pushButton_metric.setGeometry(QtCore.QRect(10, 10, 131, 41))
        self.pushButton_metric.setObjectName(_fromUtf8("pushButton_metric"))
        self.tab_display.addTab(self.tab_metric, _fromUtf8(""))
        self.tab_Optimize = QtGui.QWidget()
        self.tab_Optimize.setObjectName(_fromUtf8("tab_Optimize"))
        self.tab_display.addTab(self.tab_Optimize, _fromUtf8(""))
        self.table_Zcoeffs = QtGui.QTableWidget(self.centralwidget)
        self.table_Zcoeffs.setGeometry(QtCore.QRect(610, 40, 341, 331))
        self.table_Zcoeffs.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table_Zcoeffs.setObjectName(_fromUtf8("table_Zcoeffs"))
        self.table_Zcoeffs.setColumnCount(2)
        self.table_Zcoeffs.setRowCount(22)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(19, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(20, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setVerticalHeaderItem(21, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.table_Zcoeffs.setItem(5, 0, item)
        self.gridLayoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(610, 390, 341, 171))
        self.gridLayoutWidget_3.setObjectName(_fromUtf8("gridLayoutWidget_3"))
        self.grid_zernset = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.grid_zernset.setObjectName(_fromUtf8("grid_zernset"))
        self.pushButton_evolve = QtGui.QPushButton(self.gridLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_evolve.sizePolicy().hasHeightForWidth())
        self.pushButton_evolve.setSizePolicy(sizePolicy)
        self.pushButton_evolve.setObjectName(_fromUtf8("pushButton_evolve"))
        self.grid_zernset.addWidget(self.pushButton_evolve, 4, 2, 1, 1)
        self.pushButton_flush = QtGui.QPushButton(self.gridLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_flush.sizePolicy().hasHeightForWidth())
        self.pushButton_flush.setSizePolicy(sizePolicy)
        self.pushButton_flush.setObjectName(_fromUtf8("pushButton_flush"))
        self.grid_zernset.addWidget(self.pushButton_flush, 4, 1, 1, 1)
        self.pushButton_setsingleZern = QtGui.QPushButton(self.gridLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_setsingleZern.sizePolicy().hasHeightForWidth())
        self.pushButton_setsingleZern.setSizePolicy(sizePolicy)
        self.pushButton_setsingleZern.setObjectName(_fromUtf8("pushButton_setsingleZern"))
        self.grid_zernset.addWidget(self.pushButton_setsingleZern, 4, 0, 1, 1)
        self.lineEdit_gain = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_gain.setObjectName(_fromUtf8("lineEdit_gain"))
        self.grid_zernset.addWidget(self.lineEdit_gain, 1, 1, 1, 1)
        self.label_gain = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_gain.setObjectName(_fromUtf8("label_gain"))
        self.grid_zernset.addWidget(self.label_gain, 0, 1, 1, 1)
        self.label_zmode = QtGui.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_zmode.sizePolicy().hasHeightForWidth())
        self.label_zmode.setSizePolicy(sizePolicy)
        self.label_zmode.setObjectName(_fromUtf8("label_zmode"))
        self.grid_zernset.addWidget(self.label_zmode, 0, 0, 1, 1)
        self.lineEdit_zmode = QtGui.QLineEdit(self.gridLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_zmode.sizePolicy().hasHeightForWidth())
        self.lineEdit_zmode.setSizePolicy(sizePolicy)
        self.lineEdit_zmode.setObjectName(_fromUtf8("lineEdit_zmode"))
        self.grid_zernset.addWidget(self.lineEdit_zmode, 1, 0, 1, 1)
        self.label_zampli = QtGui.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_zampli.sizePolicy().hasHeightForWidth())
        self.label_zampli.setSizePolicy(sizePolicy)
        self.label_zampli.setObjectName(_fromUtf8("label_zampli"))
        self.grid_zernset.addWidget(self.label_zampli, 2, 0, 1, 1)
        self.lineEdit_zernampli = QtGui.QLineEdit(self.gridLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_zernampli.sizePolicy().hasHeightForWidth())
        self.lineEdit_zernampli.setSizePolicy(sizePolicy)
        self.lineEdit_zernampli.setObjectName(_fromUtf8("lineEdit_zernampli"))
        self.grid_zernset.addWidget(self.lineEdit_zernampli, 3, 0, 1, 1)
        self.label_zernstep = QtGui.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_zernstep.sizePolicy().hasHeightForWidth())
        self.label_zernstep.setSizePolicy(sizePolicy)
        self.label_zernstep.setObjectName(_fromUtf8("label_zernstep"))
        self.grid_zernset.addWidget(self.label_zernstep, 2, 1, 1, 1)
        self.lineEdit_zernstep = QtGui.QLineEdit(self.gridLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_zernstep.sizePolicy().hasHeightForWidth())
        self.lineEdit_zernstep.setSizePolicy(sizePolicy)
        self.lineEdit_zernstep.setObjectName(_fromUtf8("lineEdit_zernstep"))
        self.grid_zernset.addWidget(self.lineEdit_zernstep, 3, 1, 1, 1)
        self.checkBox_mask = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.checkBox_mask.setObjectName(_fromUtf8("checkBox_mask"))
        self.grid_zernset.addWidget(self.checkBox_mask, 1, 2, 1, 1)
        self.label_segfile = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_segfile.setObjectName(_fromUtf8("label_segfile"))
        self.grid_zernset.addWidget(self.label_segfile, 2, 2, 1, 1)
        self.lineEdit_segfile = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_segfile.setObjectName(_fromUtf8("lineEdit_segfile"))
        self.grid_zernset.addWidget(self.lineEdit_segfile, 3, 2, 1, 1)
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 430, 211, 131))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.grid_acquisition = QtGui.QGridLayout(self.gridLayoutWidget)
        self.grid_acquisition.setObjectName(_fromUtf8("grid_acquisition"))
        self.label_masksize = QtGui.QLabel(self.gridLayoutWidget)
        self.label_masksize.setObjectName(_fromUtf8("label_masksize"))
        self.grid_acquisition.addWidget(self.label_masksize, 2, 1, 1, 1)
        self.label_nsteps = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_nsteps.sizePolicy().hasHeightForWidth())
        self.label_nsteps.setSizePolicy(sizePolicy)
        self.label_nsteps.setObjectName(_fromUtf8("label_nsteps"))
        self.grid_acquisition.addWidget(self.label_nsteps, 2, 0, 1, 1)
        self.lineEdit_mask = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_mask.setObjectName(_fromUtf8("lineEdit_mask"))
        self.grid_acquisition.addWidget(self.lineEdit_mask, 3, 1, 1, 1)
        self.lineEdit_dz = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_dz.setObjectName(_fromUtf8("lineEdit_dz"))
        self.grid_acquisition.addWidget(self.lineEdit_dz, 1, 1, 1, 1)
        self.spinbox_Nsteps = QtGui.QSpinBox(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinbox_Nsteps.sizePolicy().hasHeightForWidth())
        self.spinbox_Nsteps.setSizePolicy(sizePolicy)
        self.spinbox_Nsteps.setMinimum(3)
        self.spinbox_Nsteps.setMaximum(50)
        self.spinbox_Nsteps.setObjectName(_fromUtf8("spinbox_Nsteps"))
        self.grid_acquisition.addWidget(self.spinbox_Nsteps, 3, 0, 1, 1)
        self.label_fname = QtGui.QLabel(self.gridLayoutWidget)
        self.label_fname.setObjectName(_fromUtf8("label_fname"))
        self.grid_acquisition.addWidget(self.label_fname, 0, 0, 1, 1)
        self.lineEdit_filename = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_filename.setObjectName(_fromUtf8("lineEdit_filename"))
        self.grid_acquisition.addWidget(self.lineEdit_filename, 1, 0, 1, 1)
        self.label_stepsize = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_stepsize.sizePolicy().hasHeightForWidth())
        self.label_stepsize.setSizePolicy(sizePolicy)
        self.label_stepsize.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_stepsize.setObjectName(_fromUtf8("label_stepsize"))
        self.grid_acquisition.addWidget(self.label_stepsize, 0, 1, 1, 1)
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 580, 411, 54))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioButton_laser = QtGui.QRadioButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.radioButton_laser.setFont(font)
        self.radioButton_laser.setObjectName(_fromUtf8("radioButton_laser"))
        self.horizontalLayout.addWidget(self.radioButton_laser)
        self.pushButton_BL = QtGui.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_BL.sizePolicy().hasHeightForWidth())
        self.pushButton_BL.setSizePolicy(sizePolicy)
        self.pushButton_BL.setObjectName(_fromUtf8("pushButton_BL"))
        self.horizontalLayout.addWidget(self.pushButton_BL)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_start = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_start.setObjectName(_fromUtf8("label_start"))
        self.verticalLayout.addWidget(self.label_start)
        self.lineEdit_starting = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit_starting.setObjectName(_fromUtf8("lineEdit_starting"))
        self.verticalLayout.addWidget(self.lineEdit_starting)
        self.horizontalLayout.addLayout(self.verticalLayout)
        Form.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Form)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 968, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Form.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Form)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Form.setStatusBar(self.statusbar)

        self.retranslateUi(Form)
        self.tab_display.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "MainWindow", None))
        self.pushButton_segments.setText(_translate("Form", "Segments", None))
        self.pushButton_clear.setText(_translate("Form", "Clear Pattern", None))
        self.pushButton_apply2mirror.setText(_translate("Form", "Apply to DM", None))
        self.pushButton_reset.setText(_translate("Form", "Reset Mirror", None))
        self.pushButton_acquire.setText(_translate("Form", "Acquire stack", None))
        self.pushButton_snapshot.setText(_translate("Form", "Snapshot", None))
        self.tab_display.setTabText(self.tab_display.indexOf(self.tab_image_phase), _translate("Form", "Image and phase", None))
        self.pushButton_metric.setText(_translate("Form", "Get_Metric", None))
        self.tab_display.setTabText(self.tab_display.indexOf(self.tab_metric), _translate("Form", "Metric", None))
        self.tab_display.setTabText(self.tab_display.indexOf(self.tab_Optimize), _translate("Form", "Optimization", None))
        item = self.table_Zcoeffs.verticalHeaderItem(0)
        item.setText(_translate("Form", "Z4 (defocus)", None))
        item = self.table_Zcoeffs.verticalHeaderItem(1)
        item.setText(_translate("Form", "Z5 (astigm. )", None))
        item = self.table_Zcoeffs.verticalHeaderItem(2)
        item.setText(_translate("Form", "Z6 (astigm. )", None))
        item = self.table_Zcoeffs.verticalHeaderItem(3)
        item.setText(_translate("Form", "Z7 (coma)", None))
        item = self.table_Zcoeffs.verticalHeaderItem(4)
        item.setText(_translate("Form", "Z8 (coma)", None))
        item = self.table_Zcoeffs.verticalHeaderItem(5)
        item.setText(_translate("Form", "Z9", None))
        item = self.table_Zcoeffs.verticalHeaderItem(6)
        item.setText(_translate("Form", "Z10", None))
        item = self.table_Zcoeffs.verticalHeaderItem(7)
        item.setText(_translate("Form", "Z11 (pri.spher.)", None))
        item = self.table_Zcoeffs.verticalHeaderItem(8)
        item.setText(_translate("Form", "Z12", None))
        item = self.table_Zcoeffs.verticalHeaderItem(9)
        item.setText(_translate("Form", "Z13", None))
        item = self.table_Zcoeffs.verticalHeaderItem(10)
        item.setText(_translate("Form", "Z14", None))
        item = self.table_Zcoeffs.verticalHeaderItem(11)
        item.setText(_translate("Form", "Z15", None))
        item = self.table_Zcoeffs.verticalHeaderItem(12)
        item.setText(_translate("Form", "Z16", None))
        item = self.table_Zcoeffs.verticalHeaderItem(13)
        item.setText(_translate("Form", "Z17", None))
        item = self.table_Zcoeffs.verticalHeaderItem(14)
        item.setText(_translate("Form", "Z18", None))
        item = self.table_Zcoeffs.verticalHeaderItem(15)
        item.setText(_translate("Form", "Z19", None))
        item = self.table_Zcoeffs.verticalHeaderItem(16)
        item.setText(_translate("Form", "Z20", None))
        item = self.table_Zcoeffs.verticalHeaderItem(17)
        item.setText(_translate("Form", "Z21", None))
        item = self.table_Zcoeffs.verticalHeaderItem(18)
        item.setText(_translate("Form", "Z22", None))
        item = self.table_Zcoeffs.verticalHeaderItem(19)
        item.setText(_translate("Form", "Z23", None))
        item = self.table_Zcoeffs.verticalHeaderItem(20)
        item.setText(_translate("Form", "Z24", None))
        item = self.table_Zcoeffs.verticalHeaderItem(21)
        item.setText(_translate("Form", "Z25", None))
        item = self.table_Zcoeffs.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Amplitude", None))
        item = self.table_Zcoeffs.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Stepsize", None))
        __sortingEnabled = self.table_Zcoeffs.isSortingEnabled()
        self.table_Zcoeffs.setSortingEnabled(False)
        item = self.table_Zcoeffs.item(5, 0)
        item.setText(_translate("Form", "15", None))
        self.table_Zcoeffs.setSortingEnabled(__sortingEnabled)
        self.pushButton_evolve.setText(_translate("Form", "Evolve", None))
        self.pushButton_flush.setText(_translate("Form", "Flush", None))
        self.pushButton_setsingleZern.setText(_translate("Form", "Set", None))
        self.lineEdit_gain.setText(_translate("Form", "-5", None))
        self.label_gain.setText(_translate("Form", "Gain", None))
        self.label_zmode.setText(_translate("Form", "Z_modes", None))
        self.label_zampli.setText(_translate("Form", "Amplitude", None))
        self.label_zernstep.setText(_translate("Form", "stepsize", None))
        self.checkBox_mask.setText(_translate("Form", "Mask", None))
        self.label_segfile.setText(_translate("Form", "seg_file", None))
        self.lineEdit_segfile.setText(_translate("Form", "dummy.txt", None))
        self.label_masksize.setText(_translate("Form", "r_mask", None))
        self.label_nsteps.setText(_translate("Form", "# of steps", None))
        self.lineEdit_mask.setText(_translate("Form", "50", None))
        self.lineEdit_dz.setText(_translate("Form", "0.0003", None))
        self.label_fname.setText(_translate("Form", "Filename", None))
        self.lineEdit_filename.setText(_translate("Form", "test.npy", None))
        self.label_stepsize.setText(_translate("Form", "dz", None))
        self.radioButton_laser.setText(_translate("Form", "Laser", None))
        self.pushButton_BL.setText(_translate("Form", "Backlash correct", None))
        self.label_start.setText(_translate("Form", "Starting position (micron)", None))
        self.lineEdit_starting.setText(_translate("Form", "0.1500", None))
