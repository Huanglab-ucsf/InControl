# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mirror_design.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
sys.path.append('D:\\Dan\\Programs\\InControl\\myWidget\\')
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(781, 617)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 50))
        self.groupBox_2.setMaximumSize(QtCore.QSize(300, 100))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_segment = QtWidgets.QLabel(self.groupBox_2)
        self.label_segment.setObjectName("label_segment")
        self.gridLayout_2.addWidget(self.label_segment, 1, 0, 1, 1)
        self.label_addition = QtWidgets.QLabel(self.groupBox_2)
        self.label_addition.setObjectName("label_addition")
        self.gridLayout_2.addWidget(self.label_addition, 1, 1, 1, 1)
        self.spinBox_segment = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_segment.setMinimum(1)
        self.spinBox_segment.setMaximum(144)
        self.spinBox_segment.setObjectName("spinBox_segment")
        self.gridLayout_2.addWidget(self.spinBox_segment, 2, 0, 1, 1)
        self.lineEdit_pokeval = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_pokeval.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_pokeval.setObjectName("lineEdit_pokeval")
        self.gridLayout_2.addWidget(self.lineEdit_pokeval, 2, 1, 1, 1)
        self.pushButton_poke = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_poke.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_poke.setObjectName("pushButton_poke")
        self.gridLayout_2.addWidget(self.pushButton_poke, 2, 2, 1, 1)
        self.checkBox_pokeAll = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_pokeAll.setObjectName("checkBox_pokeAll")
        self.gridLayout_2.addWidget(self.checkBox_pokeAll, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 14, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 4, 0, 1, 1)
        self.lineEdit_cx = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cx.setObjectName("lineEdit_cx")
        self.gridLayout_3.addWidget(self.lineEdit_cx, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 3, 0, 1, 1)
        self.lineEdit_loadMult = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_loadMult.setObjectName("lineEdit_loadMult")
        self.gridLayout_3.addWidget(self.lineEdit_loadMult, 2, 1, 1, 1)
        self.pushButton_load = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_load.setObjectName("pushButton_load")
        self.gridLayout_3.addWidget(self.pushButton_load, 2, 0, 1, 1)
        self.pushButton_loadSegs = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_loadSegs.setObjectName("pushButton_loadSegs")
        self.gridLayout_3.addWidget(self.pushButton_loadSegs, 1, 0, 1, 1)
        self.pushButton_refresh = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.gridLayout_3.addWidget(self.pushButton_refresh, 0, 1, 1, 1)
        self.pushButton_clear = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.gridLayout_3.addWidget(self.pushButton_clear, 0, 0, 1, 1)
        self.lineEdit_cy = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cy.setObjectName("lineEdit_cy")
        self.gridLayout_3.addWidget(self.lineEdit_cy, 4, 1, 1, 1)
        self.pushButton_reset = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_reset.sizePolicy().hasHeightForWidth())
        self.pushButton_reset.setSizePolicy(sizePolicy)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.gridLayout_3.addWidget(self.pushButton_reset, 15, 1, 1, 1)
        self.pushButton_toMirror = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.pushButton_toMirror.sizePolicy().hasHeightForWidth())
        self.pushButton_toMirror.setSizePolicy(sizePolicy)
        self.pushButton_toMirror.setMaximumSize(QtCore.QSize(16777215, 200))
        self.pushButton_toMirror.setObjectName("pushButton_toMirror")
        self.gridLayout_3.addWidget(self.pushButton_toMirror, 15, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 5, 0, 1, 1)
        self.lineEdit_npixels = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_npixels.setObjectName("lineEdit_npixels")
        self.gridLayout_3.addWidget(self.lineEdit_npixels, 5, 1, 1, 1)
        self.pushButton_reconfig = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_reconfig.setObjectName("pushButton_reconfig")
        self.gridLayout_3.addWidget(self.pushButton_reconfig, 6, 0, 1, 2)
        self.lineEdit_mult = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_mult.setObjectName("lineEdit_mult")
        self.gridLayout_3.addWidget(self.lineEdit_mult, 13, 1, 1, 1)
        self.pushButton_rot90 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_rot90.setObjectName("pushButton_rot90")
        self.gridLayout_3.addWidget(self.pushButton_rot90, 7, 0, 1, 1)
        self.pushButton_mult = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_mult.setObjectName("pushButton_mult")
        self.gridLayout_3.addWidget(self.pushButton_mult, 13, 0, 1, 1)
        self.lineEdit_premult = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_premult.setObjectName("lineEdit_premult")
        self.gridLayout_3.addWidget(self.lineEdit_premult, 12, 1, 1, 1)
        self.pushButton_pad = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_pad.setObjectName("pushButton_pad")
        self.gridLayout_3.addWidget(self.pushButton_pad, 10, 0, 1, 1)
        self.lineEdit_rotate = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_rotate.setObjectName("lineEdit_rotate")
        self.gridLayout_3.addWidget(self.lineEdit_rotate, 9, 1, 1, 1)
        self.pushButton_rotate = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_rotate.setObjectName("pushButton_rotate")
        self.gridLayout_3.addWidget(self.pushButton_rotate, 9, 0, 1, 1)
        self.pushButton_flipud = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_flipud.setObjectName("pushButton_flipud")
        self.gridLayout_3.addWidget(self.pushButton_flipud, 8, 1, 1, 1)
        self.pushButton_fliplr = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_fliplr.setObjectName("pushButton_fliplr")
        self.gridLayout_3.addWidget(self.pushButton_fliplr, 8, 0, 1, 1)
        self.pushButton_premult = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_premult.setObjectName("pushButton_premult")
        self.gridLayout_3.addWidget(self.pushButton_premult, 12, 0, 1, 1)
        self.lineEdit_pad = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_pad.setObjectName("lineEdit_pad")
        self.gridLayout_3.addWidget(self.lineEdit_pad, 10, 1, 1, 1)
        self.pushButton_getSegs = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_getSegs.setObjectName("pushButton_getSegs")
        self.gridLayout_3.addWidget(self.pushButton_getSegs, 11, 0, 1, 2)
        self.horizontalLayout.addWidget(self.groupBox)
        self.tabWidgetPF = QtWidgets.QTabWidget(Form)
        self.tabWidgetPF.setEnabled(True)
        self.tabWidgetPF.setIconSize(QtCore.QSize(15, 16))
        self.tabWidgetPF.setObjectName("tabWidgetPF")
        self.tabWidgetPFPage1 = QtWidgets.QWidget()
        self.tabWidgetPFPage1.setObjectName("tabWidgetPFPage1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tabWidgetPFPage1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mplwidgetPhase = MatplotlibWidget(self.tabWidgetPFPage1)
        self.mplwidgetPhase.setObjectName("mplwidgetPhase")
        self.verticalLayout.addWidget(self.mplwidgetPhase)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_Save = QtWidgets.QPushButton(self.tabWidgetPFPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Save.sizePolicy().hasHeightForWidth())
        self.pushButton_Save.setSizePolicy(sizePolicy)
        self.pushButton_Save.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_Save.setObjectName("pushButton_Save")
        self.gridLayout.addWidget(self.pushButton_Save, 1, 1, 1, 1)
        self.pushButton_Modulate = QtWidgets.QPushButton(self.tabWidgetPFPage1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Modulate.sizePolicy().hasHeightForWidth())
        self.pushButton_Modulate.setSizePolicy(sizePolicy)
        self.pushButton_Modulate.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_Modulate.setObjectName("pushButton_Modulate")
        self.gridLayout.addWidget(self.pushButton_Modulate, 1, 3, 1, 1)
        self.pushButton_Load = QtWidgets.QPushButton(self.tabWidgetPFPage1)
        self.pushButton_Load.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_Load.setObjectName("pushButton_Load")
        self.gridLayout.addWidget(self.pushButton_Load, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tabWidgetPF.addTab(self.tabWidgetPFPage1, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.mplwidgetSegs = MatplotlibWidget(self.tab_4)
        self.mplwidgetSegs.setGeometry(QtCore.QRect(0, 0, 371, 371))
        self.mplwidgetSegs.setObjectName("mplwidgetSegs")
        self.label_meanSeg = QtWidgets.QLabel(self.tab_4)
        self.label_meanSeg.setGeometry(QtCore.QRect(30, 410, 121, 16))
        self.label_meanSeg.setObjectName("label_meanSeg")
        self.label_maxSeg = QtWidgets.QLabel(self.tab_4)
        self.label_maxSeg.setGeometry(QtCore.QRect(30, 440, 121, 16))
        self.label_maxSeg.setObjectName("label_maxSeg")
        self.label_minSeg = QtWidgets.QLabel(self.tab_4)
        self.label_minSeg.setGeometry(QtCore.QRect(30, 470, 141, 16))
        self.label_minSeg.setObjectName("label_minSeg")
        self.tabWidgetPF.addTab(self.tab_4, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.mplwidgetZern = MatplotlibWidget(self.tab_2)
        self.mplwidgetZern.setGeometry(QtCore.QRect(10, 0, 380, 349))
        self.mplwidgetZern.setObjectName("mplwidgetZern")
        self.pushButton_modulateZernike = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_modulateZernike.setGeometry(QtCore.QRect(20, 350, 75, 23))
        self.pushButton_modulateZernike.setObjectName("pushButton_modulateZernike")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 390, 391, 151))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(10, 48, 30, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(121, 48, 51, 16))
        self.label_7.setObjectName("label_7")
        self.spinBox_zernMode = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBox_zernMode.setGeometry(QtCore.QRect(52, 48, 63, 19))
        self.spinBox_zernMode.setMinimum(1)
        self.spinBox_zernMode.setObjectName("spinBox_zernMode")
        self.lineEdit_zernAmp = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_zernAmp.setGeometry(QtCore.QRect(178, 48, 50, 19))
        self.lineEdit_zernAmp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_zernAmp.setObjectName("lineEdit_zernAmp")
        self.checkBox_zernMask = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_zernMask.setGeometry(QtCore.QRect(234, 49, 47, 17))
        self.checkBox_zernMask.setObjectName("checkBox_zernMask")
        self.pushButton_applyZern = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_applyZern.setGeometry(QtCore.QRect(289, 48, 86, 19))
        self.pushButton_applyZern.setObjectName("pushButton_applyZern")
        self.spinBox_numZerns = QtWidgets.QSpinBox(self.groupBox_3)
        self.spinBox_numZerns.setGeometry(QtCore.QRect(52, 73, 63, 19))
        self.spinBox_numZerns.setMinimum(1)
        self.spinBox_numZerns.setMaximum(999)
        self.spinBox_numZerns.setObjectName("spinBox_numZerns")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setGeometry(QtCore.QRect(10, 73, 25, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(121, 73, 44, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(121, 98, 48, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_minZAmp = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_minZAmp.setGeometry(QtCore.QRect(178, 73, 50, 19))
        self.lineEdit_minZAmp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_minZAmp.setObjectName("lineEdit_minZAmp")
        self.lineEdit_maxZAmp = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_maxZAmp.setGeometry(QtCore.QRect(178, 98, 50, 19))
        self.lineEdit_maxZAmp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_maxZAmp.setObjectName("lineEdit_maxZAmp")
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(10, 98, 26, 16))
        self.label_11.setObjectName("label_11")
        self.lineEdit_wTime = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_wTime.setGeometry(QtCore.QRect(52, 98, 63, 19))
        self.lineEdit_wTime.setObjectName("lineEdit_wTime")
        self.checkBox_zernWithSharpness = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_zernWithSharpness.setGeometry(QtCore.QRect(234, 74, 141, 17))
        self.checkBox_zernWithSharpness.setObjectName("checkBox_zernWithSharpness")
        self.label_14 = QtWidgets.QLabel(self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(10, 23, 36, 16))
        self.label_14.setObjectName("label_14")
        self.lineEdit_zernRad = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_zernRad.setGeometry(QtCore.QRect(52, 23, 63, 19))
        self.lineEdit_zernRad.setObjectName("lineEdit_zernRad")
        self.checkBox_clearFirst = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_clearFirst.setGeometry(QtCore.QRect(234, 99, 75, 17))
        self.checkBox_clearFirst.setChecked(True)
        self.checkBox_clearFirst.setObjectName("checkBox_clearFirst")
        self.tabWidgetPF.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.mplwidgetGrouped = MatplotlibWidget(self.tab_3)
        self.mplwidgetGrouped.setGeometry(QtCore.QRect(19, 10, 401, 401))
        self.mplwidgetGrouped.setObjectName("mplwidgetGrouped")
        self.label_12 = QtWidgets.QLabel(self.tab_3)
        self.label_12.setGeometry(QtCore.QRect(10, 440, 291, 16))
        self.label_12.setObjectName("label_12")
        self.lineEdit_group = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_group.setGeometry(QtCore.QRect(10, 460, 300, 20))
        self.lineEdit_group.setObjectName("lineEdit_group")
        self.pushButton_createGroup = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_createGroup.setGeometry(QtCore.QRect(320, 460, 121, 23))
        self.pushButton_createGroup.setObjectName("pushButton_createGroup")
        self.lineEdit_groupVal = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_groupVal.setGeometry(QtCore.QRect(20, 490, 81, 20))
        self.lineEdit_groupVal.setObjectName("lineEdit_groupVal")
        self.pushButton_setToGroup = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_setToGroup.setGeometry(QtCore.QRect(110, 490, 121, 23))
        self.pushButton_setToGroup.setObjectName("pushButton_setToGroup")
        self.tabWidgetPF.addTab(self.tab_3, "")
        self.horizontalLayout.addWidget(self.tabWidgetPF)

        self.retranslateUi(Form)
        self.tabWidgetPF.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Deformable Mirror"))
        self.groupBox.setTitle(_translate("Form", "Pattern"))
        self.groupBox_2.setTitle(_translate("Form", "Poke One Segment"))
        self.label_segment.setText(_translate("Form", "Segment"))
        self.label_addition.setText(_translate("Form", "Addition"))
        self.pushButton_poke.setText(_translate("Form", "Set"))
        self.checkBox_pokeAll.setText(_translate("Form", "All "))
        self.label_2.setText(_translate("Form", "Center y:"))
        self.label.setText(_translate("Form", "Center x:"))
        self.pushButton_load.setText(_translate("Form", "Load"))
        self.pushButton_loadSegs.setText(_translate("Form", "Load Segs"))
        self.pushButton_refresh.setText(_translate("Form", "Refresh"))
        self.pushButton_clear.setText(_translate("Form", "Clear"))
        self.pushButton_reset.setText(_translate("Form", "Reset the mirror"))
        self.pushButton_toMirror.setText(_translate("Form", "Apply to Mirror"))
        self.label_3.setText(_translate("Form", "Number of pxls:"))
        self.pushButton_reconfig.setText(_translate("Form", "Reconfig Geometry"))
        self.pushButton_rot90.setText(_translate("Form", "Rotate 90"))
        self.pushButton_mult.setText(_translate("Form", "Multiplier"))
        self.pushButton_pad.setText(_translate("Form", "Pad Zeros"))
        self.pushButton_rotate.setText(_translate("Form", "Rotate"))
        self.pushButton_flipud.setText(_translate("Form", "Flip U-D"))
        self.pushButton_fliplr.setText(_translate("Form", "Flip L-R"))
        self.pushButton_premult.setText(_translate("Form", "Pre Multiplier"))
        self.pushButton_getSegs.setText(_translate("Form", "Calculate Segments"))
        self.pushButton_Save.setText(_translate("Form", "Save to file"))
        self.pushButton_Modulate.setText(_translate("Form", "Modulate"))
        self.pushButton_Load.setText(_translate("Form", "Fit to Zernike"))
        self.tabWidgetPF.setTabText(self.tabWidgetPF.indexOf(self.tabWidgetPFPage1), _translate("Form", "Pattern"))
        self.label_meanSeg.setText(_translate("Form", "Mean: --"))
        self.label_maxSeg.setText(_translate("Form", "Maximum: --"))
        self.label_minSeg.setText(_translate("Form", "Minimum: --"))
        self.tabWidgetPF.setTabText(self.tabWidgetPF.indexOf(self.tab_4), _translate("Form", "Segment"))
        self.pushButton_modulateZernike.setText(_translate("Form", "Modulate"))
        self.groupBox_3.setTitle(_translate("Form", "Add Zernike"))
        self.label_6.setText(_translate("Form", "Mode:"))
        self.label_7.setText(_translate("Form", "Amplitude:"))
        self.checkBox_zernMask.setText(_translate("Form", "Mask"))
        self.pushButton_applyZern.setText(_translate("Form", "Apply"))
        self.label_8.setText(_translate("Form", "Num:"))
        self.label_9.setText(_translate("Form", "Min Amp:"))
        self.label_10.setText(_translate("Form", "Max Amp:"))
        self.lineEdit_minZAmp.setText(_translate("Form", "-1"))
        self.lineEdit_maxZAmp.setText(_translate("Form", "1"))
        self.label_11.setText(_translate("Form", "Wait:"))
        self.lineEdit_wTime.setText(_translate("Form", "-1"))
        self.checkBox_zernWithSharpness.setText(_translate("Form", "With running sharpness?"))
        self.label_14.setText(_translate("Form", "Radius:"))
        self.lineEdit_zernRad.setText(_translate("Form", "256"))
        self.checkBox_clearFirst.setText(_translate("Form", "Clear first?"))
        self.tabWidgetPF.setTabText(self.tabWidgetPF.indexOf(self.tab_2), _translate("Form", "Zernikes"))
        self.label_12.setText(_translate("Form", "Enter segments to group together (comma separated):"))
        self.pushButton_createGroup.setText(_translate("Form", "Create Group"))
        self.pushButton_setToGroup.setText(_translate("Form", "Add value to group"))
        self.tabWidgetPF.setTabText(self.tabWidgetPF.indexOf(self.tab_3), _translate("Form", "GroupSegs"))

from matplotlibwidget import MatplotlibWidget
