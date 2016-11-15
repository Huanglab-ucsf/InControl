"""
Created by Dan on 11/11/2016
psf_tools for processing, plotting and characterizing psfs.
"""

import numpy as np
from scipy.ndimage import interpolation
from scipy.ndimage import gaussian_filter as gf
from scipy import optimize

def psf_processing(raw_scan, r_mask = 40):
    """
    processing raw_scan
    """
    nz, ny, nx = raw_scan.shape
    PSF = np.zeros_like(raw_scan)

    cz, cy, cx = np.unravel_index(np.argmax(gf(raw_scan*mask,2)), raw_scan.shape)
    print "Center found at: ", (cz,cy,cx)
    self._center = [cz, cy, cx] # save this for one-run procedure
    # We laterally center the raw_scan at the brightest pixel
    shift_y = int(ny/2-cy)
    shift_x = int(nx/2-cx)
    PSF_raw = np.roll(raw_scan, shift_y, axis = 1)
    PSF_raw = np.roll(PSF_raw, shift_x, axis = 2)

    cut = raw_scan[:,cy-mask_size:cy+mask_size,cx-mask_size:cx+mask_size]
    PSF = np.zeros((nz,ny,nx))
    PSF[:,nx/2-mask_size:ny/2+mask_size,ny/2-mask_size:nx/2+mask_size] = cut
    # Background estimation
    self._background = np.mean(raw_scan[hcyl])
    print "Background guess: ", self._background
else:
    self._background = np.mean(raw_scan[hcyl])
    PSF[np.logical_not(new_cyl)] = self._background
