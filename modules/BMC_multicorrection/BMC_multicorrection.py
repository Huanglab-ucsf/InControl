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
from AO_algos.DM_simulate import DM
import psf_tools


class Control(inLib.Module):

    def __init__(self, control, settings):
        print 'Initializing BMC_multicorrection.'
        inLib.Module.__init__(self, control, settings) # inheriting
        dims = self._control.camera.getDimensions()
        # A list to store the indices of the 'Other' modulations, given by the SLM API:
        self._modulations = []
        print('BMC_multicorrection initialized.')

        self._PSF = None
        self.DM = DM(nPixels = dims.min()) # where to store the patterns



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
        nz, ny, nx = scan.shape
        # An empty PSF
        PSF, background = psf_tools.psf_processing(scan_psf, raw_center=mask_center, r_mask = mask_size)

        # Hollow cylinder
        self._PSF = PSF
        self._background = background
        if filename:
            np.save(filename+"_raw", scan_psf)
            np.save(filename, PSF)
        return PSF
        # end of acquiring PSF


    def modulateDM(self):
        """
        Simply, modulate the created pattern.
        """
        self.control.
