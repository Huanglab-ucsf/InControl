import inLib
import numpy as np
from Utilities import zernike
from scipy.ndimage import interpolation
from scipy.ndimage import gaussian_filter as gf
from scipy import optimize
import os
import time
import matplotlib.pyplot as plt
import libtim
import libtim.zern
import skimage
from skimage.restoration import unwrap_phase


class Control(inLib.Module):

    def __init__(self, control, settings):
        print 'Initializing BMC_multicorrection.'
        inLib.Module.__init__(self, control, settings) # inheriting
        dim = self._control.camera.getDimensions()
        # A list to store the indices of the 'Other' modulations, given by the SLM API:
        self._modulations = []
        print 'BMC_multicorrection initialized.'

        self._PSF = None

    #------------------------- Private functions
    def _getGeo(self):
        '''
        Gets geometry from either SLM (if exist) or elsewhere
        '''
        geometry = self._control.mirror.getGeometry()
        return geometry
        # endof _getGeo




    def updateImSize(self):
        '''
        Gets the image size from the camera.
        _ui uses this for sharpness calculations...
        '''
        return self._control.camera.getDimensions()
        # endof updateImSize


    def acquirePSF(self, range_, nSlices, nFrames, center_xy=True, filename=None,
                   mask_size = 40, mask_center = (-1,-1)):
        '''
        Acquires a PSF stack. The PSF is returned but also stored internally.

        :Parameters:
            *range_*: float
                The range of the scan around the current axial position in micrometers.
            *nSlices*: int
                The number of PSF slices to acquire.
            *nFrames*: int
                The number of frames to be averaged for each PSF slice.
            *filename*: str
                The file name into which the PSF will be saved.

        :Returns:
            *PSF*: numpy.array
                An array of shape (k,l,m), where k are the number of PSF slices and
                (l,m) the lateral slice dimensions.
        '''

        # Logging
        self._settings['range'] = range_
        self._settings['nSlices'] = nSlices
        self._settings['nFrames'] = nFrames
        self._settings['filename'] = filename

        self.filename = filename

        # Some parameters
        start = range_/2.0
        end = -range_/2.0
        self._dz = abs(range_/(nSlices-1.0))

        # Scan the PSF:
        scan_psf = self._control.piezoscan.scan(start, end, nSlices, nFrames, filename)
        self._PSF = psf_processing(scan_psf)

        nz, nx, ny = scan.shape
        # An empty PSF
        PSF = np.zeros_like(scan)
        # Geometry info
        g = pupil.Geometry((nx,ny), nx/2.-0.5, ny/2.-0.5, 16)
        # Filled cylinder:
        cyl = np.array(nz*[g.r_pxl<16])
        new_cyl = np.array(nz*[g.r_pxl<mask_size])
        # Fill the empty PSF with every voxel in scan where cyl=True
        if not center_xy:
            PSF[cyl] = scan[cyl]
        # Hollow cylinder
        hcyl = np.array(nz*[np.logical_and(g.r_pxl>=50, g.r_pxl<61)])
        if mask_center[0] > -1:
            g2 = pupil.Geometry((nx,ny), mask_center[0], mask_center[1], 16)
            mask = g2.r_pxl<mask_size
        else:
            mask = g.r_pxl<mask_size
        if filename:
            np.save(filename+"pre-cut", scan)

            print "Background guess: ", self._background
        else:
            self._background = np.mean(scan[hcyl])
        PSF[np.logical_not(new_cyl)] = self._background

        self._PSF = PSF
        if filename:
            np.save(filename, PSF)
        return PSF
        # end of acquiring PSF

    def getSharpness(self, pixelSize=163, diffLimit=800):
        '''
        Finds the sharpnes of self._PSF
        '''
        if self._PSF is None:
            time.sleep(2)
        sharpness = signalForAO.secondMomentOnStack(self._PSF,pixelSize,diffLimit)
        self._sharpness = sharpness
        print "Maximum sharpness = ", sharpness.max()
        return sharpness




    def unwrap(self):
        unwrapped = unwrap_phase(self._PF.phase)
        print "The unwrapped phase has a size of :"
        print unwrapped.shape

        return unwrapped

    def setZernModesToFit(self, nmodes):
        self.zernModesToFit = nmodes

    def zernFitUnwrapped(self, skip4orders=False):
        unwrapped = self.unwrap()

        #geometry = self._control.slm.getGeometry()
        geometry = self._getGeo()

        nx,ny = unwrapped.shape
        rad = np.sum(self._pupil.r[nx/2,:]<1)/2
        print "radius:", rad


        if skip4orders:
            zernModes, resultFit, errFit = libtim.zern.fit_zernike(unwrapped, nmodes=self.zernModesToFit, rad=rad,
                                                                   startmode=5)
        else:
            zernModes, resultFit, errFit = libtim.zern.fit_zernike(unwrapped, nmodes=self.zernModesToFit, rad=rad)

        MOD0 = resultFit
        newMOD = np.zeros((geometry.nx,geometry.ny))
        nx,ny = MOD0.shape
        newMOD[geometry.cx-np.floor(nx/2.):geometry.cx+np.ceil(nx/2.),geometry.cy-np.floor(ny/2.0):geometry.cy+np.ceil(ny/2.)] = MOD0.copy()
        self._zernFitUnwrapped = newMOD
        self._zernFitUnwrappedModes = zernModes

        return resultFit

    def modZernFitUnwrapped(self, useMask=False, radius=0):
        #geometry = self._control.slm.getGeometry()
        geometry = self._getGeo()
        d = geometry.d
        if radius==0:
            r = d/2
        else:
            r = radius
        cx = geometry.cx
        cy = geometry.cy
        if self._zernFitUnwrappedModes is not None:
            print "ZernFitUnwrapped Modes: ", self._zernFitUnwrappedModes
            print "Radius for zernCalc: ", r
            zernCalc = libtim.zern.calc_zernike(self._zernFitUnwrappedModes, r, mask=useMask)

            MOD = -1*zernCalc
            MOD = np.flipud(MOD)
            MOD = np.rot90(MOD)
            MOD = np.rot90(-1.0*MOD)
            #MOD = interpolation.shift(MOD,(cy-255.5,cx-255.5),order=0,
            #                                       mode='nearest')
            newMOD = np.zeros((geometry.nx,geometry.ny))
            nx,ny = MOD.shape
            newMOD[cy-np.floor(nx/2.):cy+np.ceil(nx/2.),cx-np.floor(ny/2.):cx+np.ceil(ny/2.)] = MOD.copy()
            if self.hasSLM:
                index = self._control.slm.addOther(newMOD)
            else:
                index = self._control.mirror.addOther(newMOD)
            self._modulations.append(index)
            return index


    def removePTTD(self):
        p = self._PF.zernike_coefficients
        p[0:4] = 0
        self._PF.zernike_coefficients = p
        #self._PF.zernike_coefficients[0:4] = 0
        return self._PF


    def modulatePF(self, use_zernike=True):
        '''
        Sends phase of the current internally stored pupil function to the SLM.

        :Returns:
            *index*: int
                Each modulation that is sent to the SLM by the AdaptiveOptics module has an
                individual index, which can be used later to access this modulation.
        '''
        print 'Modulating pupil function.'

        #geometry = self._control.slm.getGeometry()
        geometry = self._getGeo()

        if use_zernike:
            # The SLM vs camera image is flipped upside down. That's why we define a
            # flipped theta:
            #x_pxl = -geometry.x_pxl
            #theta = np.arctan2(geometry.y_pxl, x_pxl)
            #MOD = -zernike.basic_set(self._PF.zernike_coefficients, geometry.r, theta)
            if self._zernFitUnwrappedModes is not None:
                print "ZernFitUnwrapped Modes: ", self._zernFitUnwrappedModes
                    #print "Radius for zernCalc: ", r
                zernCalc = libtim.zern.calc_zernike(self._zernFitUnwrappedModes,geometry.d/2.0,
                                               zern_data ={}, mask = False)
                MOD0=-1*zernCalc

            else:
                print "not pre-fitted!"
                MOD0 = -1*libtim.zern.calc_zernike(self._PF.zernike_coefficients, geometry.d/2.0,
                                               zern_data ={}, mask = False)
            print "Using zernike to modulate. Radius of calculated mod: ", (geometry.d/2.0)
            MOD0 = np.flipud(MOD0)
            MOD0 = np.rot90(MOD0)
            MOD0 = np.rot90(-1.0*MOD0)
            MODx,MODy = MOD0.shape
            newMOD = np.zeros((geometry.nx,geometry.ny))
            newMOD[geometry.cx-np.floor(MODx/2.):geometry.cx+np.ceil(MODx/2.),geometry.cy-np.floor(MODy/2.0):geometry.cy+np.ceil(MODy/2.)] = MOD0.copy()
            MOD = newMOD
            # Added by Dan on 08/26, save automatically the zernike-fitted pupil. re
            # Added by Dan on 09/02, save the zernike-fitted pupil without mask, but when apply,
            # apply the masked one so that the patterns can be visualized clearer.
            Rmod = geometry.d/2.0


            np.save(self.filename+'_zfit', MOD)


        else:
            MOD = -1*self._PF.phase
            MOD = np.flipud(MOD)
            MOD = np.rot90(MOD)
            cx,cy,d = geometry.cx, geometry.cy, geometry.d
            # Diameter of phase retrieval output [pxl]:
            dPhRt = (self._pupil.k_max/self._pupil.kx.max())*self._pupil.nx
            # Zoom needed to fit onto SLM map:
            zoom = d/dPhRt
            MOD = interpolation.zoom(MOD,zoom,order=0,mode='nearest')
            # Flip up down:
            #MOD = np.flipud(MOD)
            # Flip left right:
            #MOD = np.fliplr(MOD)
            #MOD = np.rot90(MOD)
            MOD = np.rot90(-1.0*MOD) #Invert and rot90
            # Shift center:
            MOD = interpolation.shift(MOD,(cy-255.5,cx-255.5),order=0,
                                                   mode='nearest')
            # Cut out center 512x512:
            c = MOD.shape[0]/2
            MOD = MOD[c-256:c+256,c-256:c+256]


        # Add an 'Other' modulation using the SLM API. Store the index in _modulations:
        #index = self._control.slm.addOther(MOD)
        index = self._addMOD(MOD)
        self._modulations.append(index)
        return index

    def modulatePF_unwrapped(self):
        #geometry = self._control.slm.getGeometry()
        geometry = self._getGeo()
        MOD = -1*self.unwrap()
        MOD = np.flipud(MOD)
        MOD = np.rot90(MOD)
        cx,cy,d = geometry.cx, geometry.cy, geometry.d
        # Diameter of phase retrieval output [pxl]:
        dPhRt = (self._pupil.k_max/self._pupil.kx.max())*self._pupil.nx
        # Zoom needed to fit onto SLM map:
        zoom = d/dPhRt
        MOD = interpolation.zoom(MOD,zoom,order=0,mode='nearest')
        # Flip up down:
        #MOD = np.flipud(MOD)
        # Flip left right:
        #MOD = np.fliplr(MOD)
        #MOD = np.rot90(MOD)
        MOD = np.rot90(-1.0*MOD) #Invert and rot90
        # Shift center:
        MOD = interpolation.shift(MOD,(cy-255.5,cx-255.5),order=0,
                                                       mode='nearest')
        # Cut out center 512x512:
        c = MOD.shape[0]/2
        MOD = MOD[c-256:c+256,c-256:c+256]


        # Add an 'Other' modulation using the SLM API. Store the index in _modulations:
        #index = self._control.slm.addOther(MOD)
        index = self._addMOD(MOD)
        self._modulations.append(index)
        return index


    def savePF(self, filename):
        '''
        Saves the most recent pupil function in InControl's working directory.

        :Parameters:
            *filename*: str
        '''
        working_dir = self._control.getWorkingDir()
        np.save(os.path.join(working_dir, filename + '_complex.npy'), self._PF.complex)
        np.save(os.path.join(working_dir, filename + '_amplitude.npy'), self._PF.amplitude)
        np.save(os.path.join(working_dir, filename + '_phase.npy'), self._PF.phase)


    def setModulationActive(self, index, state):
        '''
        Enables or disables a modulation.

        :Parameters:
            *index*: int
                The modulation index given by :func:`modulatePF`.
            *state*: bool
                If True, the modulation at *index* is enabled.
        '''
        # Retrieve the index of the respective 'Other' Modulation, generated previously by the
        # SLM API:
        other_index = self._modulations[index]
        #self._control.slm.setOtherActive(other_index, state)
        self._setOtherActive(other_index,state)

    def resetZernAmpIndex(self):
        self.currentZernAmpIndex = 0

    def setZernAmps(self, zmin, zmax, num=100):
        '''
        Creats 1D array of Zernike amplitudes to apply.
        RunningSharpness thread will advance through these
        '''
        self.zernAmps = np.linspace(zmax,zmin,num)

    def getZernMinMax(self):
        return self.zernAmpMin, self.zernAmpMax

    def getNumberOfZernToVary(self):
        if self.hasMirror:
            num = self._control.mirror.getNumberOfZernToVary()
        elif self.hasSLM:
            num = 100
        else:
            num = 0
        return num

    def advanceModulation(self):
        '''
        In RunningSharpness thread this advances the next pattern
        to be dispalyed on adaptive optics device
        '''
        if self.currentZernAmpIndex >= len(self.zernAmps):
            self.currentZernAmpIndex = 0
        coeff = self.zernAmps[self.currentZernAmpIndex]
        if self.hasSLM:
            self._control.slm.setZernikeModeFirstActive(coeff)
            self._setZernModeFirstActive(coeff)
        elif self.hasMirror:
            self._control.mirror.advancePatternWithPipe()
        self.currentZernAmpIndex += 1
        return coeff

    def findSharpnessEachFrame(self, pixelSize, diffLimit, mask=None):
        frame_length = 1.0/self._control.camera.getFrameRate()
        #np_image = self._control._control.camera.getImageForPreview()
        im = self._control.camera.getMostRecentImageNumpy()
        if mask is not None:
            background_est = np.median(im * np.logical_not(mask))
            im = (im * mask) + (background_est * np.logical_not(mask))
        if im is not None:
            sharpness = signalForAO.secondMoment(im,pixelSize,diffLimit)
            if len(self.sharpnessList)<200:
                self.sharpnessList.append(sharpness)
            else:
                self.sharpnessList = self.sharpnessList[1:] + [sharpness]
        else:
            sharpness = None
        time.sleep(frame_length)
        return sharpness, self.sharpnessList


    """
    Below are functions defined by dan.
    """
    def Strehl_ratio(self):
        # this is very raw. Should save the indices for pixels inside the pupil.
        in_pupil = self._pupil.k < self._pupil.k_max
        NK = in_pupil.sum()
        c_up = np.abs(self.pf_complex.sum())**2
        c_down = (self.pf_ampli**2).sum()*NK

        strehl = c_up/c_down
        return strehl
