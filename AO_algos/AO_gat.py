"""
Created by Dan Xie on 11/07/2016
This is a guess-and-test strategy for AO-based aberration correction. The functions
should not talk directly to any hardware; instead, only patterns of modulations are
generated and returned.
Last update: 11/09/2016
"""

import inLib
from Utilities import zernike
import numpy as np
import scipy as sp
from libtim import zern
from scipy.ndimage import interpolation
from scipy.ndimage import gaussian_filter as gf
from scipy import optimize
import os
import time

from DM_simulate import Zernike_func

global nactuator = 140

class zmode_gat(object):
    """
    gat:guess and check
    key function:
    1. generate a zernike mode modulation with certain amplitude
    2. apply the modulation onto the Deformable mirror
    3. take one or more captures under the modulation
    4. Evaluate the image quality using Frequency-based metrics
    5. repeat the procedure by multiple times
    6. do the fitting.


    """
    def __init__(self, npixels):
        """
        initialize the AO correction
        """
        self.npixels = npixels
        self.nactuators = nactuators
        self.seg_pattern = np.zeros([12,12])
        self.seg_line = np.zeros(nactuator)
        self.Z_func = Zernike_func(radius = npixels/2)
        self.response = np.zeros(10)

    def single_zern_modulate(self, ampli):
        """
        Modulate single zernikes
        """

# --------------------------------------------------------------


class Control(inLib.Module):

    def __init__(self, control, settings):
        print 'Initializing Adaptive Optics.'
        inLib.Module.__init__(self, control, settings)
        dim = self._control.camera.getDimensions()
        # A list to store the indices of the 'Other' modulations, given by the SLM API:
        self._modulations = []
        print 'Adaptive Optics initialized.'


        self._PSF = None
        self._PF = None
        self._PFradius = None
        self._sharpness = None


        self.sharpnessList = []
        self.zernModesToFit = 22 #Number of zernike modes to fit unwrapped pupil functions



    def updateImSize(self):
        '''
        Gets the image size from the camera.
        _ui uses this for sharpness calculations...
        '''
        return self._control.camera.getDimensions()


    def _getGeo(self):
        '''
        Gets geometry from either SLM (if exist) or elsewhere
        '''
        geometry = self._control.mirror.getGeometry()
        return geometry


    def _addMOD(self, MOD):
        index = self._control.mirror.addOther(MOD)
        return index



    def _setZernModeFirstActive(self, coeff):
        if self.hasSLM:
            self._control.slm.setZernikeModeFirstActive(coeff)

    def _setOtherActive(self,other_index,state):
        if self.hasSLM:
            self._control.slm.setOtherActive(other_index, state)
        if self.hasMirror:
            self._control.mirror.setOtherActive(other_index, state)

    def acquireImagesVaryAO(self, nPatterns, nFrames,
                            filename=None):
        '''
        Acquires a stack of images while varying the mirror in some way...
        '''

        if self.hasMirror:
            ao = self._control.mirror
        elif self.hasSLM:
            ao = self._control.slm
        else:
            return None
        if not self.varyAOactive:
            return None

        dim = self._control.camera.getDimensions()
        data = np.zeros((nSteps,) + dim)
        slicesFrames = np.zeros((nFrames,)+dim)

        for i in xrange(nPatterns):
            ao.advancePatternWithPipe()
            for j in xrange(nFrames):
                im = self._control.camera.getMostRecentImageNumpy()
                if im is None:
                    time.sleep(frame_length)
                    im = self._control.camera.getMostRecentImageNumpy()
                slicesFrames[j] = im
                time.sleep(frame_length)
            data[i] = np.mean(slicesFrames, axis=0)
        if filename:
            print "ao: Saving vary ao to ", filename
            np.save(filename, data)
        return data



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

        # Some parameters
        start = range_/2.0
        end = -range_/2.0
        self._dz = abs(range_/(nSlices-1.0))

        # Scan the PSF:
        scan = self._control.piezoscan.scan(start, end, nSlices, nFrames, filename)

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
        if center_xy:
            # The coordinates of the brightest pixel
            cz, cx, cy = np.unravel_index(np.argmax(gf(scan*mask,2)), scan.shape)
            print "Center found at: ", (cz,cx,cy)
            # We laterally center the scan at the brightest pixel
            cut = scan[:,cx-mask_size:cx+mask_size,cy-mask_size:cy+mask_size]
            PSF = np.zeros((nz,nx,ny))
            PSF[:,nx/2-mask_size:nx/2+mask_size,ny/2-mask_size:ny/2+mask_size] = cut
            # Background estimation
            self._background = np.mean(scan[hcyl])
            print "Background guess: ", self._background
        else:
            self._background = np.mean(scan[hcyl])
        PSF[np.logical_not(new_cyl)] = self._background

        self._PSF = PSF
        if filename:
            np.save(filename, PSF)
        return PSF

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
        #------ done with sharpness calculation



    def fit(self):
        '''
        Fits the most recent pupil function to Zernike modes up to the fourth order.

        :Returns:
            *p*: numpy.array
                A 1-dimensional array of Zernike coefficients. Array indices correspond to
                the Noll coefficient *j* of Zernike modes.
            *PF*: numpy.array
                The phase pupil function as produced by the phase retrieval algorithm with Zernike
                coefficients.
        '''
        ''' Old fitting procedure
        p, success, error = zernike.fit_to_basic_set(self._PF.phase, np.zeros(15),
                self._pupil.r, self._pupil.theta)
        self._PF.zernike_coefficients = p
        '''
        nx,ny = self._PF.phase.shape
        self._PFradius = np.sum(self._pupil.r[nx/2,:]<1)/2
        print "Radius of fitted zernike: ", self._PFradius
        #fitResults = libtim.zern.fit_zernike(self._PF.phase, rad=radius, nmodes=15)
        unwrapped=self.unwrap()
        print "Unwrapped!"

        fitResults_wrong = libtim.zern.fit_zernike(self._PF.phase, rad=radius, nmodes=21)
        fitResults = libtim.zern.fit_zernike(unwrapped, rad=radius, nmodes=21)
        self._PF.zernike_coefficients = fitResults[0]
        #print("unwrapped:", fitResults[0])
        #print("original:", fitResults_wrong[0])

        return self._PF

    def unwrap(self):
        unwrapped = unwrap_phase(self._PF.phase)
        return unwrapped

    def setZernModesToFit(self, nmodes):
        self.zernModesToFit = nmodes

    def zernFitUnwrapped(self, skip4orders=False):
        unwrapped = self.unwrap()

        #geometry = self._control.slm.getGeometry()
        geometry = self._getGeo()

        nx,ny = unwrapped.shape
        rad = np.sum(self._pupil.r[nx/2,:]<1)/2

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
#             zernCalc = libtim.zern.calc_zernike(self._zernFitUnwrappedModes, r, mask=useMask)
            zernCalc = libtim.zern.calc_zernike(self._zernFitUnwrappedModes, r, mask = True)
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
                # tried on 07/21
#                 index = self._control.mirror.addOther(newMOD)
                index = self._control.mirror.addOther(newMOD)
            self._modulations.append(index)
            return index


    def removePTTD(self):
        # remove the first four Zernike modes
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
                zernCalc = libtim.zern.calc_zernike(self._zernFitUnwrappedModes,geometry.d/2.0, mask = True,
                                               zern_data ={})
                MOD0=-1*zernCalc

            else:
                print "not pre-fitted!"
                MOD0 = -1*libtim.zern.calc_zernike(self._PF.zernike_coefficients, geometry.d/2.0, mask= False,
                                               zern_data ={})
            print "Using zernike to modulate. Radius of calculated mod: ", (geometry.d/2.0)
            np.save("testing_mod0.npy", MOD0)
            MOD0 = np.flipud(MOD0)
            MOD0 = np.rot90(MOD0)
            MOD0 = np.rot90(-1.0*MOD0)
            MODx,MODy = MOD0.shape
            newMOD = np.zeros((geometry.nx,geometry.ny))
            newMOD[geometry.cx-np.floor(MODx/2.):geometry.cx+np.ceil(MODx/2.),geometry.cy-np.floor(MODy/2.0):geometry.cy+np.ceil(MODy/2.)] = MOD0.copy()
            MOD = newMOD


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


    def getNumberOfZernToVary(self):
        if self.hasMirror:
            num = self._control.mirror.getNumberOfZernToVary()
        elif self.hasSLM:
            num = 100
        else:
            num = 0
        return num


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
