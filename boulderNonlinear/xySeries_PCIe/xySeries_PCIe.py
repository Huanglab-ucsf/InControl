#!/usr/bin/python

import inLib
import numpy as np
from Utilities import zernike
from modules.adaptiveOptics import pupil_forInControl as pupil
import time
import ctypes


class Control(inLib.Device):

    '''
    The control class of an xySeries PCIe SLM by Boulder Nonlinear Systems.
    Each time the modulation on the SLM is updated. The program waits until the liquid
    crystal responded.
    '''    

    def __init__(self, settings):
        api_path = 'boulderNonlinear.xySeries_PCIe.xySeries_PCIe_api'
        inLib.Device.__init__(self, api_path, settings)

        n_SLMs = self._api.constructor(False,6,'PCIe'+str(self._settings['n_pixels']))
        if n_SLMs == 1:
            self.loadLUTFile(self._settings['lut_file'])
            blank = ctypes.create_string_buffer(512*512)
            self._api.slm.WriteImage(1,blank.raw,512)
            self._api.slmPower(True)

        else:
            try:
                self._api.deconstructor()
            except:
                pass

        self._active = True
        self._geometry = pupil.Geometry((self._settings['n_pixels'],
                                               self._settings['n_pixels']),
                                              settings['cx'],
                                              settings['cy'],
                                              settings['d'])
        
        self._settings['wait_time'] = 2*self._settings['response_time']

        self._files = _FileModulations()
        self._zernikes = _ZernikeModulations()
        self._sli = _SLIModulation(settings['sli_settings'], self._geometry)
        self._other = _OtherModulations()

        self._reticle = _ReticleModulation(self._geometry)

        #
        # This is a quick and dirty hack, because CoverslipTiltModulation depends on the sli experiment instance.
        # Consequently, all cs_tilt recalculations have to be done AFTER SLIModulation recalculations.
        # I should eventually make this foolproof by moving some SLI parameters to a more general parameter list.
        #
        self._cs_tilt = _CoverslipTiltModulation(self, 0, 0)

        self._mod = np.zeros((self._settings['n_pixels'],self._settings['n_pixels']))
        


    def addFile(self, path):
        '''
        Adds a modulation from file. The file should be in .npy format and contain the phase
        modulation in radians.

        :Parameters:
        *path*: str
            The path to the file.
        '''
        self._files.files[path] = _FileModulation(path)
        if self._active and self._files.active:
            self._sum_send()
        

    def addOther(self, data, on_geometry_changed=None, args=()):
        '''
        Adds an 'Other' modulation.

        :Parameters:
            *data*: numpy.array
                The modulation data to be loaded. 
                The dimensions have to match the SLM pixel size. Phase data is in radians.
        
        :Returns:
            *index*: int
                Each 'Other' modulation has an individual index, so I can be accessed later.

        '''
        index = self._other.counter
        self._other.others[index] = _OtherModulation(data, on_geometry_changed, args)
        self._other.counter += 1
        if self._active and self._other.active:
            self._sum_send()
        return index



    def deleteOther(self, index):
        '''
        Deletes a previously created 'Other' modulation.

        :Parameters:
            *index*: int
                The index of the to be deleted 'Other' modulation as given by :func:`addOther`.
        '''
        self._other.others.pop(index)
        if self._active and self._other.active:
            self._sum_send()


    def getModulation(self):
        '''
        Returns the current modulation.

        :Returns:
            *modulation*: numpy.array
        '''
        return self._mod


    def getResponseTime(self):
        '''
        
        :Returns:
            *response_time*: float
                The response time of the liquid crystal, as measured by Boulder, in seconds.
        '''
        return self._settings['response_time']


    def getSLIExperiment(self):
        '''

        :Returns:
            *experiment*: Utilities.pupil.Experiment
                An instance of pupil's Experiment class which is used to calculate
                single lens interference patterns.

        ''' 
        return self._sli.exp


    def getSLIMirrorCorrection(self):
        return self._sli.getSLIMirrorCorrection()


    def saveModulation(self, filename):
        '''
        Saves the current modulation in the .npy format.

        :Parameters:
            *filename*: str
        '''
        np.save(filename, self._mod)


    def setFileActive(self, path, state):
        '''
        Enables or disables the modulation from a file.

        :Parameters:
            *path*: str
                The path to the file.
            *state*: bool
                If *True*, the modulation of this file is enabled.
        '''
        self._files.files[path].active = state
        if self._active and self._files.active:
            self._sum_send()


    def setFilesActive(self, state):
        '''
        Enables or disables the modulation of all files.

        :Parameters:
            *state*: bool
                If *True*, the modulation will be enabled.
        '''
        self._files.active = state
        if self._active:
            self._sum_send()


    def setSLIMirrorCorrectionFile(self, path):
        correction = np.load(path)
        self._sli.setSLIMirrorCorrection(correction)


    def setSLIMirrorCorrectionActive(self, state):
        self._sli.setSLIMirrorCorrectionActive(state)


    def setOtherActive(self, index, state):
        '''
        Enables or disables an 'Other' modulation.

        :Parameters:
            *index*: int
                The index of the to be deleted 'Other' modulation as given by :func:`addOther`.
            *state*: bool
                If *True*, the modulation will be enabled.
        '''
        self._other.others[index].active = state
        if self._active and self._other.active:
            self._sum_send()


    def setOthersActive(self, state):
        '''
        Toggles all 'Other' modulations on or off.

        :Parameters:
            *state*: bool
        '''
        self._other.active = state
        if self._active:
            self._sum_send()


    def setOtherData(self, index, data):
        '''
        Sets the modulation data of an existing 'Other' modulation.

        :Parameters:
            *index*: int
                The index of the to be deleted 'Other' modulation as given by :func:`addOther`.
            *data*: numpy.array
                The modulation data in radians. The dimensions have to match the SLM pixels.
        '''
        if not np.array_equal(self._other.others[index].data, data):
            self._other.others[index].data = data
            if self._active and self._other.active and self._other.others[index].active:
                self._sum_send()


    def loadLUTFile(self, LUTFile):
        ''' Loads a look-up table file which provides the SLM calibration. '''
        self._settings['lut_file'] = LUTFile
        self._api.loadLUTFile(1, LUTFile)


    def setReticleActive(self, state):
        self._reticle.active = state
        self._sum_send()


    def shutDown(self):
        ''' Shuts down the SLM. '''
	self._api.slmPower(False)
        self._api.deconstructor()


    def setActive(self, state):
        '''
        Enables or disables SLM modulation.

        :Parameters:
            *state*: bool
                If True, SLM modulation is enabled.
        '''
        self._active = state
        self._sum_send()


    def setCoverslipTilt(self, tilt, direction):

        self._cs_tilt.setTilt(tilt, direction)
        if self._active:
            self._sum_send()


    def setGeometry(self, cx, cy, d):
        '''
        Sets the geometry of modulations on the SLM pixel grid. All inputs are in pixels.

        :Parameters:
            *cx*: float
                Lateral center coordinate
            *cy*: float
                Horizontal center coordinate
            *d*: float
                Pupil diameter
        '''
	
	self._settings['cx'] = cx
	self._settings['cy'] = cy
	self._settings['d'] = d

        self._geometry = pupil.Geometry((self._settings['n_pixels'],
                                               self._settings['n_pixels']),
                                              cx,cy,d)

        for mod in self._zernikes.zernikes.values():
            mod.geometry = self._geometry
            mod.calculate()

        for mod in self._other.others.values():
            if mod.on_geometry_changed:
                mod.data = mod.on_geometry_changed(*mod.args)

        self._sli.geometry = self._geometry

        self._reticle.setGeometry(self._geometry)

        self._cs_tilt.calculate()

        if self._active:
            self._sum_send()


    def setSLIActive(self, state):
        '''
        Enables or disables the single lens interference modulation.

        :Parameters:
            *state*: bool
                If True, single lens interference modulation is enabled.
        '''
        self._sli.active = state
        if self._active:
            self._sum_send()


    def setSLIParams(self, params):
        '''
        Sets the parameters for single lens interference modulation.

        :Parameters:
            *params*: dict
                A dictionary containing all necessary parameters for single lens interference
                calculations.

                Keys:

                * 'l': Wavelength in um
                * 'n': Refractive index
                * 'NA': Numerical aperture
                * 'f': Objective lens focal length
                * 'z0': Distance of emitter to mirror
                * 'dmf': Distance of objective focus to mirror
                * 'tilt': Coefficients of Zernike modes (1,-1) and (1,1) to be added to the
                          pupil function of the mirror image.
        '''
        # Good would be a check if new params are different than old ones.
        self._sli.params = params
        if self._active and self._sli.active:
            self._sum_send()
        self._settings['sli_settings'] = params


    def setZernikeActive(self, state):
        '''
        Enables or disables the modulation of all Zernike modes.

        :Parameters:
            *state*: bool
                If True, Zernike modulation is enabled.
        '''
        self._zernikes.active = state
        if self._active:
            self._sum_send()


    def setZernikeMode(self, indices, coefficient):
        '''
        Sets the coefficient of a Zernike mode.

        :Parameters:
            *indices*: tuple
                The indices (n,m) of the Zernike mode. m can be negative to access the odd
                polynomials.
            *coefficient*: float
                The coefficient of the Zernike mode.
        '''
        if indices in self._zernikes.zernikes.keys():
            state = self._zernikes.zernikes[indices].active
        else:
            state = True
        self._zernikes.zernikes[indices] = _ZernikeModulation(indices, coefficient,
                                                              self._geometry, state)
        if self._active and self._zernikes.active and self._zernikes.zernikes[indices].active:
            self._sum_send()

    def setZernikeModeFirstActive(self, coefficient):
        '''
        Sets the coefficient of the first active (checked in the UI) mode
        '''
        keys_indices = []
        current_coeff = []
        for z in self._zernikes.zernikes.values():
            if z.active:
                keys_indices.append(z.indices)
                current_coeff.append(z.coefficient)
        if len(keys_indices)>0:
            self.setZernikeMode(keys_indices[0], coefficient)
        else:
            print "Found no active Zernike..."



    def setZernikeModeActive(self, indices, state):
        '''
        Enables or disables the modulation of a specific Zernike mode.

        :Parameters:
            *indices*: tuple
                The indices (n,m) of the Zernike mode. m can be negative to access the odd
                polynomials.
            *state*: bool
                If true, the modulation with this Zernike mode is enabled.
        '''
        self._zernikes.zernikes[indices].active = state
        if self._active and self._zernikes.active:
            self._sum_send()


    def getGeometry(self):
        '''

        :Returns:
            *geometry*: Utilities.pupil.Geometry
                An instance of pupil's Geometry class which stores geometry information
                of a pupil plane.
        '''
        return self._geometry


    def getNPixels(self):
        '''

        :Returns:
            *n_pixels*: int
                The side length of the SLM in pixels.
        '''
        return self._settings['n_pixels']


    def getSLIParams(self):
        '''

        :Returns:
            *params*: dict
                A dictionary containing all the parameters used for Single Lens Interference
                calculations.

                Keys:

                * 'l': Wavelength in um
                * 'n': Refractive index
                * 'NA': Numerical aperture
                * 'f': Objective lens focal length
                * 'z0': Distance of emitter to mirror
                * 'dmf': Distance of objective focus to mirror
        '''
        return self._sli.params


    def _sum_send(self):
        
        self._mod = np.zeros((self._settings['n_pixels'],self._settings['n_pixels']))
        if self._active:
            if self._files.active:
                for f in self._files.files.values():
                    if f.active:
                        self._mod += f.data
            if self._zernikes.active:
                for z in self._zernikes.zernikes.values():
                    if z.active:
                        self._mod += z.data
            if self._sli.active:
                self._mod += self._sli.data
            if self._other.active:
                for o in self._other.others.values():
                    if o.active:
                        self._mod += o.data
            if self._reticle.active:
                self._mod += self._reticle.data
            self._mod += self._cs_tilt.data

        self._writeToSLM()

    def _getMODSegment(self):
        d = self._geometry.d
        cx = self._geometry.cx
        cy = self._geometry.cy
        x1 = cy-np.floor(d/2.)
        x2 = cy+np.ceil(d/2.)
        y1 = cx-np.floor(d/2.)
        y2 = cx+np.ceil(d/2.)
        segment = self._mod[x1:x2,y1:y2].copy()
        return segment,x1,x2,y1,y2

    def _invert(self):
        seg,x1,x2,y1,y2 = self._getMODSegment()
        self._mod[x1:x2,y1:y2] = -1*seg
        self._writeToSLM()

    def _flipud(self):
        seg,x1,x2,y1,y2 = self._getMODSegment()
        self._mod[x1:x2,y1:y2] = np.flipud(seg)
        self._writeToSLM()

    def _fliplr(self):
        seg,x1,x2,y1,y2 = self._getMODSegment()
        self._mod[x1:x2,y1:y2] = np.fliplr(seg)
        self._writeToSLM()

    def _rot90(self):
        seg,x1,x2,y1,y2 = self._getMODSegment()
        self._mod[x1:x2,y1:y2] = np.rot90(seg)
        self._writeToSLM()

    def _shiftX(self,direction):
        seg,x1,x2,y1,y2 = self._getMODSegment()
        #print "SHIFT_X> segment size: ", seg.shape
        if direction>0:
            self._mod *= 0.0
            #print "SHIFT_X +> mod shape: ", self._mod[x1+1:x2+1,y1:y2].shape
            self._mod[x1+1:x2+1,y1:y2] = seg
        elif direction<0:
            self._mod *= 0.0
            #print "SHIFT_X -> mod shape: ", self._mod[x1-1:x2-1,y1:y2].shape
            self._mod[x1-1:x2-1,y1:y2] = seg
        self._writeToSLM()

    def _shiftY(self,direction):
        seg,x1,x2,y1,y2 = self._getMODSegment()
        if direction>0:
            self._mod *= 0.0
            self._mod[x1:x2,y1+1:y2+1] = seg
        elif direction<0:
            self._mod *= 0.0
            self._mod[x1:x2,y1-1:y2-1] = seg
        self._writeToSLM()    

    def _writeToSLM(self):
        self._mod -= self._mod.min()
        temp = np.mod(self._mod, 2.0*np.pi)
        image = temp*255/(2*np.pi)
        w = image.shape[0]
        self._api.writeImage(1, image, w)
        time.sleep(self._settings['wait_time'])



class _FileModulations:   
    def __init__(self):
        self.active = True
        self.files = {}
        

class _FileModulation:   
    def __init__(self, path):
        self.active = True
        self.path = path
        self.data = np.load(path)


class _ZernikeModulations:
    def __init__(self):
        self.active = True
        self.zernikes = {}
            
    

class _ZernikeModulation: 
    def __init__(self, indices, coefficient, geometry, active=True):
        self.active = active
        self.indices = indices
        self.geometry = geometry
        self.coefficient = coefficient
        self.calculate()

    def calculate(self):
        r = self.geometry.r
        theta = self.geometry.theta
        self.data = self.coefficient * zernike.zernike(self.indices, r, theta)

        
class _CoverslipTiltModulation(object):

    def __init__(self, control, tilt, direction):
        
        self._control = control
        self._tilt = tilt
        self._direction = direction
        self.calculate()

    def calculate(self):
        exp = self._control.getSLIExperiment()
        self.data = -np.angle(exp.get_pupil_function(0, coverslip_tilt=self._tilt, coverslip_tilt_direction=self._direction))

    def setTilt(self, tilt, direction):
        self._tilt = tilt
        self._direction = direction
        self.calculate()



class _SLIModulation(object):

    def __init__(self, params, geometry):

        self.active = False
        self._params = params
        self._geometry = geometry
        self._mirror_correction = None
        self._mirror_correction_active = False
        self._calculate()

    def _calculate(self):
        l = self._params['l']
        n = self._params['n']
        NA = self._params['NA']
        f = self._params['f']
        z0 = self._params['z0']
        dmf = self._params['dmf']
        tilt = self._params['tilt']
        if self._mirror_correction_active:
            correction = self._mirror_correction
        else:
            correction = None
        self._exp = pupil.Experiment(self._geometry, l, n, NA, f)
        self._data = self._exp.get_sli_virtual_focalplane_modulation(z0, dmf, tilt, correction)

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, new_params):
        self._params = new_params
        self._calculate()

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, new_geometry):
        self._geometry = new_geometry
        self._calculate()

    @property
    def exp(self):
        return self._exp

    @property
    def data(self):
        return self._data

    def getSLIMirrorCorrection(self):
        return self._mirror_correction

    def setSLIMirrorCorrection(self, correction):
        self._mirror_correction = correction

    def setSLIMirrorCorrectionActive(self, state):
        self._mirror_correction_active = state


class _OtherModulations:
    def __init__(self):
        self.active = True
        self.others = {}
        self.counter = 0



class _OtherModulation:

    def __init__(self, data, on_geometry_changed, args):

        self.active = True
        self.data = data
        self.on_geometry_changed = on_geometry_changed
        self.args = args


class _ReticleModulation:
    
    def __init__(self, geometry):

        self.active = False
        self.setGeometry(geometry)
        
    def setGeometry(self, geometry):
        
        ring = np.logical_and(geometry.r<=1.0, geometry.r>=0.9)
        hbar = np.logical_and(geometry.x<=0.05, geometry.x>=-0.05)
        vbar = np.logical_and(geometry.y<=0.05, geometry.y>=-0.05)
        self.data = np.pi*np.logical_or(np.logical_or(hbar, vbar), ring)

        
