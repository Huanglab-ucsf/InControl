# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adaptiveOptics_design.ui'
#
# Created: Wed Jun 17 16:17:56 2015
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
        Form.resize(912, 508)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Adaptive Optics", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "PSF", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setText(QtGui.QApplication.translate("Form", "Range [um]:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.doubleSpinBoxRange = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxRange.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxRange.setSizePolicy(sizePolicy)
        self.doubleSpinBoxRange.setDecimals(1)
        self.doubleSpinBoxRange.setMinimum(-100.0)
        self.doubleSpinBoxRange.setSingleStep(0.1)
        self.doubleSpinBoxRange.setProperty("value", 4.0)
        self.doubleSpinBoxRange.setObjectName(_fromUtf8("doubleSpinBoxRange"))
        self.gridLayout_4.addWidget(self.doubleSpinBoxRange, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setText(QtGui.QApplication.translate("Form", "# Slices:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_4.addWidget(self.label_3, 2, 0, 1, 1)
        self.spinBoxSlices = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSlices.sizePolicy().hasHeightForWidth())
        self.spinBoxSlices.setSizePolicy(sizePolicy)
        self.spinBoxSlices.setReadOnly(False)
        self.spinBoxSlices.setMinimum(3)
        self.spinBoxSlices.setSingleStep(2)
        self.spinBoxSlices.setProperty("value", 21)
        self.spinBoxSlices.setObjectName(_fromUtf8("spinBoxSlices"))
        self.gridLayout_4.addWidget(self.spinBoxSlices, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setText(QtGui.QApplication.translate("Form", "# Frames/slice:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_4.addWidget(self.label_4, 3, 0, 1, 1)
        self.spinBoxFrames = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxFrames.sizePolicy().hasHeightForWidth())
        self.spinBoxFrames.setSizePolicy(sizePolicy)
        self.spinBoxFrames.setMinimum(1)
        self.spinBoxFrames.setProperty("value", 5)
        self.spinBoxFrames.setObjectName(_fromUtf8("spinBoxFrames"))
        self.gridLayout_4.addWidget(self.spinBoxFrames, 3, 2, 1, 1)
        self.pushButtonPSF = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonPSF.sizePolicy().hasHeightForWidth())
        self.pushButtonPSF.setSizePolicy(sizePolicy)
        self.pushButtonPSF.setText(QtGui.QApplication.translate("Form", "Acquire PSF", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonPSF.setObjectName(_fromUtf8("pushButtonPSF"))
        self.gridLayout_4.addWidget(self.pushButtonPSF, 10, 0, 1, 3)
        self.checkBoxSave = QtGui.QCheckBox(self.groupBox)
        self.checkBoxSave.setText(QtGui.QApplication.translate("Form", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxSave.setObjectName(_fromUtf8("checkBoxSave"))
        self.gridLayout_4.addWidget(self.checkBoxSave, 9, 0, 1, 1)
        self.lineEditFile = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFile.sizePolicy().hasHeightForWidth())
        self.lineEditFile.setSizePolicy(sizePolicy)
        self.lineEditFile.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEditFile.setObjectName(_fromUtf8("lineEditFile"))
        self.gridLayout_4.addWidget(self.lineEditFile, 9, 2, 1, 1)
        self.checkBoxCenterLateral = QtGui.QCheckBox(self.groupBox)
        self.checkBoxCenterLateral.setText(QtGui.QApplication.translate("Form", "Center PSF laterally", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxCenterLateral.setChecked(True)
        self.checkBoxCenterLateral.setObjectName(_fromUtf8("checkBoxCenterLateral"))
        self.gridLayout_4.addWidget(self.checkBoxCenterLateral, 7, 0, 1, 3)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setText(QtGui.QApplication.translate("Form", "Mask radius:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 4, 0, 1, 1)
        self.spinBox_maskRadius = QtGui.QSpinBox(self.groupBox)
        self.spinBox_maskRadius.setMinimum(16)
        self.spinBox_maskRadius.setMaximum(512)
        self.spinBox_maskRadius.setSingleStep(10)
        self.spinBox_maskRadius.setProperty("value", 40)
        self.spinBox_maskRadius.setObjectName(_fromUtf8("spinBox_maskRadius"))
        self.gridLayout_4.addWidget(self.spinBox_maskRadius, 4, 2, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox)
        self.label_11.setText(QtGui.QApplication.translate("Form", "Center X:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_4.addWidget(self.label_11, 5, 0, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox)
        self.label_12.setText(QtGui.QApplication.translate("Form", "Center Y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_4.addWidget(self.label_12, 6, 0, 1, 1)
        self.lineEdit_cX = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_cX.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_cX.setText(QtGui.QApplication.translate("Form", "128", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_cX.setObjectName(_fromUtf8("lineEdit_cX"))
        self.gridLayout_4.addWidget(self.lineEdit_cX, 5, 2, 1, 1)
        self.lineEdit_cY = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_cY.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_cY.setText(QtGui.QApplication.translate("Form", "128", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_cY.setObjectName(_fromUtf8("lineEdit_cY"))
        self.gridLayout_4.addWidget(self.lineEdit_cY, 6, 2, 1, 1)
        self.pushButton_runningSharpness = QtGui.QPushButton(self.groupBox)
        self.pushButton_runningSharpness.setText(QtGui.QApplication.translate("Form", "Continuous Sharpness", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_runningSharpness.setObjectName(_fromUtf8("pushButton_runningSharpness"))
        self.gridLayout_4.addWidget(self.pushButton_runningSharpness, 11, 0, 1, 3)
        self.pushButton_stopSharpness = QtGui.QPushButton(self.groupBox)
        self.pushButton_stopSharpness.setText(QtGui.QApplication.translate("Form", "Stop Sharpness", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_stopSharpness.setObjectName(_fromUtf8("pushButton_stopSharpness"))
        self.gridLayout_4.addWidget(self.pushButton_stopSharpness, 14, 0, 1, 3)
        self.pushButton_sharpnessVsZern = QtGui.QPushButton(self.groupBox)
        self.pushButton_sharpnessVsZern.setText(QtGui.QApplication.translate("Form", "Sharpness vs. Zernike", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_sharpnessVsZern.setObjectName(_fromUtf8("pushButton_sharpnessVsZern"))
        self.gridLayout_4.addWidget(self.pushButton_sharpnessVsZern, 12, 0, 1, 3)
        self.doubleSpinBox_zernAmpMin = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_zernAmpMin.setDecimals(3)
        self.doubleSpinBox_zernAmpMin.setMinimum(-10.0)
        self.doubleSpinBox_zernAmpMin.setMaximum(10.0)
        self.doubleSpinBox_zernAmpMin.setObjectName(_fromUtf8("doubleSpinBox_zernAmpMin"))
        self.gridLayout_4.addWidget(self.doubleSpinBox_zernAmpMin, 17, 2, 1, 1)

        """
        Below is a block of button setting for one-run

        """
        self.pushButton_oneRun = QtGui.QPushButton(self.groupBox)
        self.pushButton_oneRun.setText(QtGui.QApplication.translate("Form", "One Run!", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_oneRun.setObjectName(_fromUtf8("pushButton_oneRun"))
        self.gridLayout_4.addWidget(self.pushButton_oneRun, 22, 0, 1, 3)



        self.doubleSpinBox_zernAmpMax = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_zernAmpMax.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_zernAmpMax.setSizePolicy(sizePolicy)
        self.doubleSpinBox_zernAmpMax.setDecimals(3)
        self.doubleSpinBox_zernAmpMax.setMinimum(-10.0)
        self.doubleSpinBox_zernAmpMax.setMaximum(10.0)
        self.doubleSpinBox_zernAmpMax.setObjectName(_fromUtf8("doubleSpinBox_zernAmpMax"))
        self.gridLayout_4.addWidget(self.doubleSpinBox_zernAmpMax, 18, 2, 1, 1)
        self.label_mod_index = QtGui.QLabel(self.groupBox)
        self.label_mod_index.setText(QtGui.QApplication.translate("Form", "Index: --", None, QtGui.QApplication.UnicodeUTF8))
        self.label_mod_index.setObjectName(_fromUtf8("label_mod_index"))
        self.gridLayout_4.addWidget(self.label_mod_index, 17, 0, 1, 1)
        self.label_mod_value = QtGui.QLabel(self.groupBox)
        self.label_mod_value.setText(QtGui.QApplication.translate("Form", "Value: --", None, QtGui.QApplication.UnicodeUTF8))
        self.label_mod_value.setObjectName(_fromUtf8("label_mod_value"))
        self.gridLayout_4.addWidget(self.label_mod_value, 18, 0, 1, 1)
        self.label_15 = QtGui.QLabel(self.groupBox)
        self.label_15.setText(QtGui.QApplication.translate("Form", "Diffraction limit:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_4.addWidget(self.label_15, 19, 0, 1, 1)
        self.lineEdit_diffLimit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_diffLimit.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_diffLimit.setObjectName(_fromUtf8("lineEdit_diffLimit"))
        self.gridLayout_4.addWidget(self.lineEdit_diffLimit, 19, 2, 1, 1)
        self.label_sharpnessArgMax = QtGui.QLabel(self.groupBox)
        self.label_sharpnessArgMax.setText(QtGui.QApplication.translate("Form", "Arg. max: --", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sharpnessArgMax.setObjectName(_fromUtf8("label_sharpnessArgMax"))
        self.gridLayout_4.addWidget(self.label_sharpnessArgMax, 20, 0, 1, 3)
        self.label_sharpnessFitMax = QtGui.QLabel(self.groupBox)
        self.label_sharpnessFitMax.setText(QtGui.QApplication.translate("Form", "Fit max: --", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sharpnessFitMax.setObjectName(_fromUtf8("label_sharpnessFitMax"))
        self.gridLayout_4.addWidget(self.label_sharpnessFitMax, 21, 0, 1, 3)
        self.label_16 = QtGui.QLabel(self.groupBox)
        self.label_16.setText(QtGui.QApplication.translate("Form", "Wait time (s):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_4.addWidget(self.label_16, 13, 0, 1, 1)
        self.lineEdit_waitTime = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_waitTime.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_waitTime.setObjectName(_fromUtf8("lineEdit_waitTime"))
        self.gridLayout_4.addWidget(self.lineEdit_waitTime, 13, 2, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBoxPhase = QtGui.QGroupBox(Form)
        self.groupBoxPhase.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxPhase.sizePolicy().hasHeightForWidth())
        self.groupBoxPhase.setSizePolicy(sizePolicy)
        self.groupBoxPhase.setTitle(QtGui.QApplication.translate("Form", "Phase retrieval", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxPhase.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBoxPhase.setObjectName(_fromUtf8("groupBoxPhase"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBoxPhase)
        self.gridLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_5 = QtGui.QLabel(self.groupBoxPhase)
        self.label_5.setText(QtGui.QApplication.translate("Form", "Pixel size [um]:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 0, 0, 1, 1)
        self.doubleSpinBoxPixel = QtGui.QDoubleSpinBox(self.groupBoxPhase)
        self.doubleSpinBoxPixel.setDecimals(3)
        self.doubleSpinBoxPixel.setMaximum(9.0)
        self.doubleSpinBoxPixel.setSingleStep(0.01)
        self.doubleSpinBoxPixel.setProperty("value", 0.163)
        self.doubleSpinBoxPixel.setObjectName(_fromUtf8("doubleSpinBoxPixel"))
        self.gridLayout_3.addWidget(self.doubleSpinBoxPixel, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBoxPhase)
        self.label_6.setText(QtGui.QApplication.translate("Form", "Wavelength [um]:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)
        self.doubleSpinBoxWavelength = QtGui.QDoubleSpinBox(self.groupBoxPhase)
        self.doubleSpinBoxWavelength.setDecimals(3)
        self.doubleSpinBoxWavelength.setProperty("value", 0.525)
        self.doubleSpinBoxWavelength.setObjectName(_fromUtf8("doubleSpinBoxWavelength"))
        self.gridLayout_3.addWidget(self.doubleSpinBoxWavelength, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBoxPhase)
        self.label_7.setText(QtGui.QApplication.translate("Form", "Refractive index:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_3.addWidget(self.label_7, 2, 0, 1, 1)
        self.doubleSpinBoxIndex = QtGui.QDoubleSpinBox(self.groupBoxPhase)
        self.doubleSpinBoxIndex.setSingleStep(0.01)
        self.doubleSpinBoxIndex.setProperty("value", 1.33)
        self.doubleSpinBoxIndex.setObjectName(_fromUtf8("doubleSpinBoxIndex"))
        self.gridLayout_3.addWidget(self.doubleSpinBoxIndex, 2, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBoxPhase)
        self.label_8.setText(QtGui.QApplication.translate("Form", "NA:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_3.addWidget(self.label_8, 3, 0, 1, 1)
        self.doubleSpinBoxNA = QtGui.QDoubleSpinBox(self.groupBoxPhase)
        self.doubleSpinBoxNA.setSingleStep(0.01)
        self.doubleSpinBoxNA.setProperty("value", 0.8)
        self.doubleSpinBoxNA.setObjectName(_fromUtf8("doubleSpinBoxNA"))
        self.gridLayout_3.addWidget(self.doubleSpinBoxNA, 3, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBoxPhase)
        self.label_9.setText(QtGui.QApplication.translate("Form", "Focal length:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_3.addWidget(self.label_9, 4, 0, 1, 1)
        self.doubleSpinBoxFocal = QtGui.QDoubleSpinBox(self.groupBoxPhase)
        self.doubleSpinBoxFocal.setMaximum(9999.99)
        self.doubleSpinBoxFocal.setProperty("value", 5000.0)
        self.doubleSpinBoxFocal.setObjectName(_fromUtf8("doubleSpinBoxFocal"))
        self.gridLayout_3.addWidget(self.doubleSpinBoxFocal, 4, 1, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(self.groupBoxPhase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setTitle(QtGui.QApplication.translate("Form", "Initial guess", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.radioButtonPlane = QtGui.QRadioButton(self.groupBox_4)
        self.radioButtonPlane.setText(QtGui.QApplication.translate("Form", "Plane wave", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonPlane.setChecked(True)
        self.radioButtonPlane.setObjectName(_fromUtf8("radioButtonPlane"))
        self.gridLayout_2.addWidget(self.radioButtonPlane, 0, 0, 1, 1)
        self.radioButtonMirror = QtGui.QRadioButton(self.groupBox_4)
        self.radioButtonMirror.setText(QtGui.QApplication.translate("Form", "Mirror", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonMirror.setObjectName(_fromUtf8("radioButtonMirror"))
        self.gridLayout_2.addWidget(self.radioButtonMirror, 1, 0, 1, 1)
        self.doubleSpinBoxMirrorDistance = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBoxMirrorDistance.setSingleStep(0.01)
        self.doubleSpinBoxMirrorDistance.setProperty("value", 2.0)
        self.doubleSpinBoxMirrorDistance.setObjectName(_fromUtf8("doubleSpinBoxMirrorDistance"))
        self.gridLayout_2.addWidget(self.doubleSpinBoxMirrorDistance, 1, 1, 1, 1)
        self.radioButtonFromFile = QtGui.QRadioButton(self.groupBox_4)
        self.radioButtonFromFile.setText(QtGui.QApplication.translate("Form", "From file", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButtonFromFile.setObjectName(_fromUtf8("radioButtonFromFile"))
        self.gridLayout_2.addWidget(self.radioButtonFromFile, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_4, 7, 0, 1, 3)
        self.label_10 = QtGui.QLabel(self.groupBoxPhase)
        self.label_10.setText(QtGui.QApplication.translate("Form", "# Iterations:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 8, 0, 1, 1)
        self.spinBoxIterations = QtGui.QSpinBox(self.groupBoxPhase)
        self.spinBoxIterations.setMinimum(1)
        self.spinBoxIterations.setMaximum(999)
        self.spinBoxIterations.setProperty("value", 20)
        self.spinBoxIterations.setObjectName(_fromUtf8("spinBoxIterations"))
        self.gridLayout_3.addWidget(self.spinBoxIterations, 8, 1, 1, 1)
        self.pushButtonPhase = QtGui.QPushButton(self.groupBoxPhase)
        self.pushButtonPhase.setText(QtGui.QApplication.translate("Form", "Retrieve phase", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonPhase.setObjectName(_fromUtf8("pushButtonPhase"))
        self.gridLayout_3.addWidget(self.pushButtonPhase, 10, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 16, 0, 1, 1)
        self.checkBoxNeglectDefocus = QtGui.QCheckBox(self.groupBoxPhase)
        self.checkBoxNeglectDefocus.setText(QtGui.QApplication.translate("Form", "Neglect defocus", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxNeglectDefocus.setChecked(True)
        self.checkBoxNeglectDefocus.setObjectName(_fromUtf8("checkBoxNeglectDefocus"))
        self.gridLayout_3.addWidget(self.checkBoxNeglectDefocus, 6, 0, 1, 2)
        self.checkBox_invertPF = QtGui.QCheckBox(self.groupBoxPhase)
        self.checkBox_invertPF.setText(QtGui.QApplication.translate("Form", "Invert?", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_invertPF.setObjectName(_fromUtf8("checkBox_invertPF"))
        self.gridLayout_3.addWidget(self.checkBox_invertPF, 11, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBoxPhase)
        self.label_13.setText(QtGui.QApplication.translate("Form", "# Wavelengths:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_3.addWidget(self.label_13, 5, 0, 1, 1)
        self.spinBox_numWavelengths = QtGui.QSpinBox(self.groupBoxPhase)
        self.spinBox_numWavelengths.setMinimum(1)
        self.spinBox_numWavelengths.setProperty("value", 1)
        self.spinBox_numWavelengths.setObjectName(_fromUtf8("spinBox_numWavelengths"))
        self.gridLayout_3.addWidget(self.spinBox_numWavelengths, 5, 1, 1, 1)
        self.checkBox_resetAmp = QtGui.QCheckBox(self.groupBoxPhase)
        self.checkBox_resetAmp.setText(QtGui.QApplication.translate("Form", "Reset amplitude?", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_resetAmp.setObjectName(_fromUtf8("checkBox_resetAmp"))
        self.gridLayout_3.addWidget(self.checkBox_resetAmp, 12, 0, 1, 1)
        self.pushButton_unwrap = QtGui.QPushButton(self.groupBoxPhase)
        self.pushButton_unwrap.setText(QtGui.QApplication.translate("Form", "Unwrap", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_unwrap.setObjectName(_fromUtf8("pushButton_unwrap"))
        self.gridLayout_3.addWidget(self.pushButton_unwrap, 10, 1, 1, 1)
        self.pushButton_modUnwrapped = QtGui.QPushButton(self.groupBoxPhase)
        self.pushButton_modUnwrapped.setText(QtGui.QApplication.translate("Form", "Mod. Unwrpd", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_modUnwrapped.setObjectName(_fromUtf8("pushButton_modUnwrapped"))
        self.gridLayout_3.addWidget(self.pushButton_modUnwrapped, 11, 1, 1, 1)
        self.pushButton_zernFitUnwrapped = QtGui.QPushButton(self.groupBoxPhase)
        self.pushButton_zernFitUnwrapped.setText(QtGui.QApplication.translate("Form", "Fit Unwrpd", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_zernFitUnwrapped.setObjectName(_fromUtf8("pushButton_zernFitUnwrapped"))
        self.gridLayout_3.addWidget(self.pushButton_zernFitUnwrapped, 12, 1, 1, 1)
        self.checkBox_ignore4 = QtGui.QCheckBox(self.groupBoxPhase)
        self.checkBox_ignore4.setText(QtGui.QApplication.translate("Form", "Ignore 1st 4?", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_ignore4.setObjectName(_fromUtf8("checkBox_ignore4"))
        self.gridLayout_3.addWidget(self.checkBox_ignore4, 16, 1, 1, 1)
        self.spinBox_zernModesToFit = QtGui.QSpinBox(self.groupBoxPhase)
        self.spinBox_zernModesToFit.setObjectName(_fromUtf8("spinBox_zernModesToFit"))
        self.gridLayout_3.addWidget(self.spinBox_zernModesToFit, 13, 1, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBoxPhase)
        self.label_14.setText(QtGui.QApplication.translate("Form", "Num modes to fit to:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_3.addWidget(self.label_14, 13, 0, 1, 1)
        self.checkBox_symmeterize = QtGui.QCheckBox(self.groupBoxPhase)
        self.checkBox_symmeterize.setText(QtGui.QApplication.translate("Form", "Make symmetric?", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_symmeterize.setObjectName(_fromUtf8("checkBox_symmeterize"))
        self.gridLayout_3.addWidget(self.checkBox_symmeterize, 9, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBoxPhase)
        self.tabWidgetPF = QtGui.QTabWidget(Form)
        self.tabWidgetPF.setEnabled(False)
        self.tabWidgetPF.setIconSize(QtCore.QSize(15, 16))
        self.tabWidgetPF.setObjectName(_fromUtf8("tabWidgetPF"))
        self.tabWidgetPFPage1 = QtGui.QWidget()
        self.tabWidgetPFPage1.setObjectName(_fromUtf8("tabWidgetPFPage1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabWidgetPFPage1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.mplwidgetPhase = MatplotlibWidget(self.tabWidgetPFPage1)
        self.mplwidgetPhase.setObjectName(_fromUtf8("mplwidgetPhase"))
        self.verticalLayout.addWidget(self.mplwidgetPhase)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonSave = QtGui.QPushButton(self.tabWidgetPFPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSave.sizePolicy().hasHeightForWidth())
        self.pushButtonSave.setSizePolicy(sizePolicy)
        self.pushButtonSave.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButtonSave.setText(QtGui.QApplication.translate("Form", "Save to file", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonSave.setObjectName(_fromUtf8("pushButtonSave"))
        self.gridLayout.addWidget(self.pushButtonSave, 1, 1, 1, 1)
        self.pushButtonModulate = QtGui.QPushButton(self.tabWidgetPFPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonModulate.sizePolicy().hasHeightForWidth())

        # useful button: modulate
        self.pushButtonModulate.setSizePolicy(sizePolicy)
        self.pushButtonModulate.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButtonModulate.setText(QtGui.QApplication.translate("Form", "Modulate", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonModulate.setObjectName(_fromUtf8("pushButtonModulate"))
        self.gridLayout.addWidget(self.pushButtonModulate, 1, 3, 1, 1)
        self.pushButtonFit = QtGui.QPushButton(self.tabWidgetPFPage1)
        self.pushButtonFit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButtonFit.setText(QtGui.QApplication.translate("Form", "Fit to Zernike", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonFit.setObjectName(_fromUtf8("pushButtonFit"))
        self.gridLayout.addWidget(self.pushButtonFit, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tabWidgetPF.addTab(self.tabWidgetPFPage1, _fromUtf8(""))
        self.Sharpness = QtGui.QWidget()
        self.Sharpness.setObjectName(_fromUtf8("Sharpness"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.Sharpness)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.mplwidgetSharpness = MatplotlibWidget(self.Sharpness)
        self.mplwidgetSharpness.setObjectName(_fromUtf8("mplwidgetSharpness"))
        self.verticalLayout_3.addWidget(self.mplwidgetSharpness)
        self.tabWidgetPF.addTab(self.Sharpness, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.mplwidgetSharpness2 = MatplotlibWidget(self.tab)
        self.mplwidgetSharpness2.setObjectName(_fromUtf8("mplwidgetSharpness2"))
        self.verticalLayout_2.addWidget(self.mplwidgetSharpness2)
        self.tabWidgetPF.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.mplwidgetPhase_2 = MatplotlibWidget(self.tab_2)
        self.mplwidgetPhase_2.setGeometry(QtCore.QRect(10, 0, 380, 349))
        self.mplwidgetPhase_2.setObjectName(_fromUtf8("mplwidgetPhase_2"))
        self.pushButton_modulateZernike = QtGui.QPushButton(self.tab_2)
        self.pushButton_modulateZernike.setGeometry(QtCore.QRect(20, 360, 75, 23))
        self.pushButton_modulateZernike.setText(QtGui.QApplication.translate("Form", "Modulate", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_modulateZernike.setObjectName(_fromUtf8("pushButton_modulateZernike"))
        self.checkBox_useMask = QtGui.QCheckBox(self.tab_2)
        self.checkBox_useMask.setGeometry(QtCore.QRect(110, 360, 70, 17))
        self.checkBox_useMask.setText(QtGui.QApplication.translate("Form", "Use mask?", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_useMask.setObjectName(_fromUtf8("checkBox_useMask"))
        self.lineEdit_zernRadius = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_zernRadius.setGeometry(QtCore.QRect(20, 390, 113, 20))
        self.lineEdit_zernRadius.setText(QtGui.QApplication.translate("Form", "256", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_zernRadius.setObjectName(_fromUtf8("lineEdit_zernRadius"))
        self.pushButton_setZernRadius = QtGui.QPushButton(self.tab_2)
        self.pushButton_setZernRadius.setGeometry(QtCore.QRect(140, 390, 131, 23))
        self.pushButton_setZernRadius.setText(QtGui.QApplication.translate("Form", "Set Zernike Radius", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_setZernRadius.setObjectName(_fromUtf8("pushButton_setZernRadius"))
        self.tabWidgetPF.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tabWidgetPF.addTab(self.tab_3, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidgetPF)
        self.groupBoxModulations = QtGui.QGroupBox(Form)
        self.groupBoxModulations.setTitle(QtGui.QApplication.translate("Form", "Modulations", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxModulations.setCheckable(True)
        self.groupBoxModulations.setObjectName(_fromUtf8("groupBoxModulations"))
        self.verticalLayoutModulations = QtGui.QVBoxLayout(self.groupBoxModulations)
        self.verticalLayoutModulations.setObjectName(_fromUtf8("verticalLayoutModulations"))
        spacerItem1 = QtGui.QSpacerItem(20, 317, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayoutModulations.addItem(spacerItem1)
        self.pushButton_setMods = QtGui.QPushButton(self.groupBoxModulations)
        self.pushButton_setMods.setText(QtGui.QApplication.translate("Form", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_setMods.setObjectName(_fromUtf8("pushButton_setMods"))
        self.verticalLayoutModulations.addWidget(self.pushButton_setMods)
        self.horizontalLayout.addWidget(self.groupBoxModulations)

        self.retranslateUi(Form)
        self.tabWidgetPF.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        self.tabWidgetPF.setTabText(self.tabWidgetPF.indexOf(self.tabWidgetPFPage1), QtGui.QApplication.translate("Form", "Pupil Function", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidgetPF.setTabText(self.tabWidgetPF.indexOf(self.Sharpness), QtGui.QApplication.translate("Form", "Sharpness", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidgetPF.setTabText(self.tabWidgetPF.indexOf(self.tab), QtGui.QApplication.translate("Form", "Running Sharpness", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidgetPF.setTabText(self.tabWidgetPF.indexOf(self.tab_2), QtGui.QApplication.translate("Form", "Zernike Fit to Unwrapped", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidgetPF.setTabText(self.tabWidgetPF.indexOf(self.tab_3), QtGui.QApplication.translate("Form", "Gen Zernikes", None, QtGui.QApplication.UnicodeUTF8))

from matplotlibwidget import MatplotlibWidget
