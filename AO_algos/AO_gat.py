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

        self.dims = None
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

        self.dims =  self._control.camera.getDimensions()
        return self.dims
        

    def _getGeo(self):
        '''
        Gets geometry from either SLM (if exist) or elsewhere
        '''
        geometry = self._control.mirror.getGeometry()
        return geometry


    def _addMOD(self, MOD):
        index = self._control.mirror.addOther(MOD)
        return index



    def acquireImage(self, nsteps = 1):
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

        dim = self._control.camera.getDimensions()
        if(nsteps ==1):
            Ims = self._control.camera.getMostRecentImageNumpy()

        else:
            Ims = np.zeros([nsteps, dim])
            for nn in xrange(nsteps):



        return Ims



        # Some parameters
