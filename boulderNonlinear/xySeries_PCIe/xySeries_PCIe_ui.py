#!/usr/bin/python

from PyQt4 import QtCore,QtGui
import inLib
import sys
from functools import partial

from Utilities import QExtensions as qext


class UI(inLib.DeviceUI):
    
    def __init__(self, control):
        design_path = 'boulderNonlinear.xySeries_PCIe.xySeries_PCIe_design'
        inLib.DeviceUI.__init__(self, control, design_path)

        p = self._control.getSLIParams()
        self._ui.doubleSpinBoxWavelength.setValue(p['l'])
        self._ui.doubleSpinBoxRefractiveIndex.setValue(p['n'])
        self._ui.doubleSpinBoxNA.setValue(p['NA'])
        self._ui.doubleSpinBoxFocalLength.setValue(p['f'])
        self._ui.doubleSpinBoxZ0.setValue(p['z0'])
        self._ui.doubleSpinBoxDMF.setValue(p['dmf'])

        self._ui.doubleSpinBoxCx.setValue(self._control._geometry.cx)
        self._ui.doubleSpinBoxCy.setValue(self._control._geometry.cy)
        self._ui.doubleSpinBoxDiameter.setValue(self._control._geometry.d)
        self._ui.doubleSpinBoxCx.editingFinished.connect(self._geometry_edited)
        self._ui.doubleSpinBoxCy.editingFinished.connect(self._geometry_edited)
        self._ui.doubleSpinBoxDiameter.editingFinished.connect(self._geometry_edited)

        self._ui.doubleSpinBoxCSTilt.editingFinished.connect(self._cs_tilt_edited)
        self._ui.doubleSpinBoxCSTiltDir.editingFinished.connect(self._cs_tilt_edited)

        self._ui.groupBoxFromFile.__class__.dragEnterEvent = self._drag_enter_event
        self._ui.groupBoxFromFile.__class__.dropEvent = self._drop_event

        self._ui.labelMirrorCorrection.dragEnterEvent = self._drag_enter_event
        self._ui.labelMirrorCorrection.dropEvent = self._drop_mirror_correction_event
        self._ui.checkBoxMirrorCorrection.toggled.connect(self._mirror_correction_toggled)

        self._ui.groupBoxFromFile.toggled.connect(self._from_file_toggled)
        self._ui.groupBoxZernike.toggled.connect(self._zernike_mods_toggled)
        self._ui.groupBoxSli4Pi.toggled.connect(self._sli_toggled)

        self._ui.checkBoxHTilt.stateChanged.connect(self._HTilt_toggled)
        self._ui.checkBoxVTilt.stateChanged.connect(self._VTilt_toggled)
        self._ui.checkBoxDefocus.stateChanged.connect(self._Defocus_toggled)
        self._ui.checkBox45Astigmatism.stateChanged.connect(self._45_Ast_toggled)
        self._ui.checkBox0Astigmatism.stateChanged.connect(self._0_Ast_toggled)
        self._ui.checkBoxVComa.stateChanged.connect(self._VComa_toggled)
        self._ui.checkBoxHComa.stateChanged.connect(self._HComa_toggled)
        self._ui.checkBox3rdSpherical.stateChanged.connect(self._3rd_toggled)
        self._ui.checkBoxTreX.stateChanged.connect(self._trefoil_1)
        self._ui.checkBoxTreY.stateChanged.connect(self._trefoil_2)
        self._ui.checkBoxTetX.stateChanged.connect(self._tetrafoil_1)
        self._ui.checkBoxTetY.stateChanged.connect(self._tetrafoil_2)
        self._ui.checkBox45Ast2.stateChanged.connect(self._ast45_2)
        self._ui.checkBox0Ast2.stateChanged.connect(self._ast0_2)
        
        self._ui.checkBoxMore.stateChanged.connect(self._More_toggled)

        self._ui.doubleSpinBoxHTilt.valueChanged.connect(self._HTilt_edited)
        self._ui.doubleSpinBoxVTilt.valueChanged.connect(self._VTilt_edited)
        self._ui.doubleSpinBoxDefocus.valueChanged.connect(self._Defocus_edited)
        self._ui.doubleSpinBox45Astigmatism.valueChanged.connect(self._45_Ast_edited)
        self._ui.doubleSpinBox0Astigmatism.valueChanged.connect(self._0_Ast_edited)
        self._ui.doubleSpinBoxVComa.valueChanged.connect(self._VComa_edited)
        self._ui.doubleSpinBoxHComa.valueChanged.connect(self._HComa_edited)
        self._ui.doubleSpinBox3rdSpherical.valueChanged.connect(self._3rd_edited)

        self._ui.doubleSpinBoxTreX.valueChanged.connect(self._trefoil_1_edited)
        self._ui.doubleSpinBoxTreY.valueChanged.connect(self._trefoil_2_edited)
        self._ui.doubleSpinBoxTetX.valueChanged.connect(self._tetrafoil_1_edited)
        self._ui.doubleSpinBoxTetY.valueChanged.connect(self._tetrafoil_2_edited)
        self._ui.doubleSpinBoxAst452.valueChanged.connect(self._ast45_2_edited)
        self._ui.doubleSpinBoxAst02.valueChanged.connect(self._ast0_2_edited)

        self._ui.lineEditMore.editingFinished.connect(self._More_edited)

        self._ui.doubleSpinBoxWavelength.valueChanged.connect(self._sli_edited)
        self._ui.doubleSpinBoxRefractiveIndex.valueChanged.connect(self._sli_edited)
        self._ui.doubleSpinBoxNA.valueChanged.connect(self._sli_edited)
        self._ui.doubleSpinBoxFocalLength.valueChanged.connect(self._sli_edited)
        self._ui.doubleSpinBoxZ0.valueChanged.connect(self._sli_edited)
        self._ui.doubleSpinBoxDMF.valueChanged.connect(self._sli_edited)
        self._ui.doubleSpinBoxMirrorHTilt.valueChanged.connect(self._sli_edited)
        self._ui.doubleSpinBoxMirrorVTilt.valueChanged.connect(self._sli_edited)

        self._ui.checkBoxModulate.stateChanged.connect(self._modulate_toggled)

        self._ui.pushButtonSave.clicked.connect(self.saveModulation)

        self._ui.checkBoxCalibration.stateChanged.connect(self.setReticleActive)

        self._mod_files = []

        self._ui.pushButton_invert.clicked.connect(self._invertHit)
        self._ui.pushButton_flipud.clicked.connect(self._flipudHit)
        self._ui.pushButton_fliplr.clicked.connect(self._fliplrHit)
        self._ui.pushButton_rot90.clicked.connect(self._rot90Hit)

        self._ui.pushButton_left.clicked.connect(partial(self._moveLeftRight,-1))
        self._ui.pushButton_right.clicked.connect(partial(self._moveLeftRight,1))
        self._ui.pushButton_up.clicked.connect(partial(self._moveUpDown,1))
        self._ui.pushButton_down.clicked.connect(partial(self._moveUpDown,-1))

        basic = [(1,-1),(1,1),(2,0),(2,-2),(2,2),(3,-1),(3,1),(4,0), (3,-3),
                 (3,3), (4,-4), (4,4), (4,-2), (4,2)]
        for mod in basic:
            self._control.setZernikeMode(mod, 0.0)
            self._control.setZernikeModeActive(mod, False)


    def _mirror_correction_toggled(self, state):
        self._control.setSLIMirrorCorrectionActive(state)

    def saveModulation(self):
        fname = QtGui.QFileDialog.getSaveFileName(None,'Save modulation',
                                                  '','*.npy')
        if fname:
                self._control.saveModulation(str(fname))


    def setReticleActive(self, state):

        self._control.setReticleActive(state)
        self.updateModulationDisplay()


    def addFile(self, path):
        if len(self._mod_files) == 0:
            self._ui.labelDropFile.hide()
        self._control.addFile(path)
        mod_file = ModulationFile(path,self)
        self._ui.verticalLayoutFromFile.addWidget(mod_file.checkbox)
        self._mod_files.append(mod_file)
        self.updateModulationDisplay()


    def _cs_tilt_edited(self):
        tilt = self._ui.doubleSpinBoxCSTilt.value()
        direction = self._ui.doubleSpinBoxCSTiltDir.value()
        self._control.setCoverslipTilt(tilt, direction)
        self.updateModulationDisplay()


    def _geometry_edited(self):
        cx = self._ui.doubleSpinBoxCx.value()
        cy = self._ui.doubleSpinBoxCy.value()
        d = self._ui.doubleSpinBoxDiameter.value()
        self._control.setGeometry(cx,cy,d)
        self.updateModulationDisplay()


    def _drag_enter_event(self,event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


    def _drop_event(self,event):
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
            self.addFile(path)

    def _drop_mirror_correction_event(self, event):
        for url in event.mimeData().urls():
            path = str(url.toLocalFile())
        self._ui.labelMirrorCorrection.setText(path)
        self._control.setSLIMirrorCorrectionFile(path)

    def _from_file_toggled(self, state):
        self._control.setFilesActive(state)
        self.updateModulationDisplay()


    def _zernike_mods_toggled(self,state):
        self._control.setZernikeActive(state)
        self.updateModulationDisplay()


    def _sli_toggled(self,state):
        self._control.setSLIActive(state)
        self.updateModulationDisplay()


    def _file_toggled(self,state):
        for f in self._mod_files:
            state = f.checkbox.isChecked()
            self._control.setFileActive(f.path, state)
        self.updateModulationDisplay()


    def _HTilt_edited(self):
        c = self._ui.doubleSpinBoxHTilt.value()
        self._control.setZernikeMode((1,1), c)
        self.updateModulationDisplay()


    def _VTilt_edited(self):
        c = self._ui.doubleSpinBoxVTilt.value()
        self._control.setZernikeMode((1,-1), c)
        self.updateModulationDisplay()


    def _Defocus_edited(self):
        c = self._ui.doubleSpinBoxDefocus.value()
        self._control.setZernikeMode((2,0), c)
        self.updateModulationDisplay()


    def _45_Ast_edited(self):
        c = self._ui.doubleSpinBox45Astigmatism.value()
        self._control.setZernikeMode((2,-2), c)
        self.updateModulationDisplay()


    def _0_Ast_edited(self):
        c = self._ui.doubleSpinBox0Astigmatism.value()
        self._control.setZernikeMode((2,2), c)
        self.updateModulationDisplay()


    def _VComa_edited(self):
        c = self._ui.doubleSpinBoxVComa.value()
        self._control.setZernikeMode((3,-1), c)
        self.updateModulationDisplay()


    def _HComa_edited(self):
        c = self._ui.doubleSpinBoxHComa.value()
        self._control.setZernikeMode((3,1), c)
        self.updateModulationDisplay()


    def _3rd_edited(self,state):
        c = self._ui.doubleSpinBox3rdSpherical.value()
        self._control.setZernikeMode((4,0), c)
        self.updateModulationDisplay()

    def _trefoil_1_edited(self,state):
        c = self._ui.doubleSpinBoxTreX.value()
        self._control.setZernikeMode((3,-3), c)
        self.updateModulationDisplay()

    def _trefoil_2_edited(self,state):
        c = self._ui.doubleSpinBoxTreY.value()
        self._control.setZernikeMode((3,3), c)
        self.updateModulationDisplay()

    def _tetrafoil_1_edited(self,state):
        c = self._ui.doubleSpinBoxTetX.value()
        self._control.setZernikeMode((4,-4), c)
        self.updateModulationDisplay()

    def _tetrafoil_2_edited(self,state):
        c = self._ui.doubleSpinBoxTetY.value()
        self._control.setZernikeMode((4,4), c)
        self.updateModulationDisplay()

    def _ast45_2_edited(self,state):
        c = self._ui.doubleSpinBoxAst452.value()
        self._control.setZernikeMode((4,-2), c)
        self.updateModulationDisplay()

    def _ast0_2_edited(self,state):
        c = self._ui.doubleSpinBoxAst02.value()
        self._control.setZernikeMode((4,2), c)
        self.updateModulationDisplay()

    def _HTilt_toggled(self,state):
        self._control.setZernikeModeActive((1,1), state)
        self.updateModulationDisplay()


    def _VTilt_toggled(self,state):
        self._control.setZernikeModeActive((1,-1), state)
        self.updateModulationDisplay()


    def _Defocus_toggled(self,state):
        self._control.setZernikeModeActive((2,0), state)
        self.updateModulationDisplay()


    def _45_Ast_toggled(self,state):
        self._control.setZernikeModeActive((2,-2), state)
        self.updateModulationDisplay()


    def _0_Ast_toggled(self,state):
        self._control.setZernikeModeActive((2,2), state)
        self.updateModulationDisplay()


    def _VComa_toggled(self,state):
        self._control.setZernikeModeActive((3,-1), state)
        self.updateModulationDisplay()


    def _HComa_toggled(self,state):
        self._control.setZernikeModeActive((3,1), state)
        self.updateModulationDisplay()


    def _3rd_toggled(self,state):
        self._control.setZernikeModeActive((4,0), state)
        self.updateModulationDisplay()

    def _trefoil_1(self,state):
        self._control.setZernikeModeActive((3,-3), state)
        self.updateModulationDisplay()

    def _trefoil_2(self,state):
        self._control.setZernikeModeActive((3,3), state)
        self.updateModulationDisplay()

    def _tetrafoil_1(self,state):
        self._control.setZernikeModeActive((4,-4), state)
        self.updateModulationDisplay()
        
    def _tetrafoil_2(self,state):
        self._control.setZernikeModeActive((4,4), state)
        self.updateModulationDisplay()

    def _ast45_2(self,state):
        self._control.setZernikeModeActive((4,-2), state)
        self.updateModulationDisplay()

    def _ast0_2(self,state):
        self._control.setZernikeModeActive((4,2), state)
        self.updateModulationDisplay()

    def _More_toggled(self,state):
        modstr = self._ui.lineEditMore.text()
        zernike = self._str2zernike(modstr)
        for mod in zernike:
            self._control.setZernikeModeActive(mod, state)
        self.updateModulationDisplay()


    def _str2zernike(self,modstr):
        zernike = {}
        try:
            if len(modstr)>0:
                mods = [_.split(':') for _ in modstr.split(';')]
                for mod in mods:
                    istr = mod[0].split(',')
                    n,m = int(istr[0]),int(istr[1])
                    coeff = int(mod[1])
                    zernike[(n,m)] = coeff
        except:
            print sys.exec_info()[0]
        return zernike


    def _More_edited(self):
        modstr = self._ui.lineEditMore.text()
        mods = self._str2zernike(modstr)
        for mod in mods:
            self._control.setZernikeMode(mod, mods[mod])
        self.updateModulationDisplay()   


    def _sli_edited(self):
        params = {}
        params['l'] = self._ui.doubleSpinBoxWavelength.value()
        params['n'] = self._ui.doubleSpinBoxRefractiveIndex.value()
        params['NA'] = self._ui.doubleSpinBoxNA.value()
        params['f'] = self._ui.doubleSpinBoxFocalLength.value()
        params['z0'] = self._ui.doubleSpinBoxZ0.value()
        params['dmf'] = self._ui.doubleSpinBoxDMF.value()
        params['tilt'] = (self._ui.doubleSpinBoxMirrorVTilt.value(),
                self._ui.doubleSpinBoxMirrorHTilt.value())
        self._control.setSLIParams(params)
        self.updateModulationDisplay()


    def _modulate_toggled(self,state):
        self._control.setActive(state)
        self.updateModulationDisplay()

    def _invertHit(self):
        self._control._invert()
        self.updateModulationDisplay()

    def _flipudHit(self):
        self._control._flipud()
        self.updateModulationDisplay()

    def _fliplrHit(self):
        self._control._fliplr()
        self.updateModulationDisplay()

    def _rot90Hit(self):
        self._control._rot90()
        self.updateModulationDisplay()


    def updateModulationDisplay(self):
        image = self._control.getModulation()
        qt_image = qext.numpy_to_qimage8(image,image.min(),image.max(),qext.QColortables8.RdBu)
        pixmap = QtGui.QPixmap.fromImage(qt_image)
        pixmap = pixmap.scaled(256,256,QtCore.Qt.KeepAspectRatio)
        self._ui.labelDisplay.setPixmap(pixmap)

    def _moveLeftRight(self, direction):
        self._control._shiftX(direction)
        self.updateModulationDisplay()

    def _moveUpDown(self, direction):
        self._control._shiftY(direction)
        self.updateModulationDisplay()

    
class ModulationFile:
    def __init__(self,path,ui):
        self.path = path
        self.name = path.split('/')[-1]
        self.checkbox = QtGui.QCheckBox(self.name)
        self.checkbox.toggle()
        self.checkbox.stateChanged.connect(ui._file_toggled)

