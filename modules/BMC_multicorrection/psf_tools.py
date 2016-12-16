"""
Created by Dan on 11/11/2016
psf_tools for processing, plotting and characterizing psfs.
"""

import numpy as np
from scipy.ndimage import interpolation
from scipy.ndimage import gaussian_filter as gf
from scipy import optimize


class pupil_geometry:

    '''
    A base class which provides basic
    geometrical data of a microscope experiment.

    Parameters
    ----------
    size: tuple
        The pixel size of a device in the pupil plane of the
        microscope.
    cx: float
        The x coordinate of the pupil function center on the
        pupil plane device in pixels.
    cy: float
        The y coordinate (see cx).
    '''

    def __init__(self, size, cy, cx, r_mask = None):

        self.cy = float(cy)
        self.cx = float(cx)
        self.size = size
        self.ny, self.nx = size
        self.x_pxl, self.y_pxl = np.meshgrid(np.arange(self.nx),np.arange(self.ny))
        self.x_pxl -= cx
        self.y_pxl -= cy
        self.r_pxl = np.sqrt(self.y_pxl**2+self.x_pxl**2)
        self.theta = np.arctan2(self.y_pxl, self.x_pxl)
        if r_mask is not None:
            self.mask = self.r_pxl < r_mask
        # done initialization

def psf_processing(raw_scan, raw_center, r_mask = 40):
    """
    processing raw_scan: find the center, trim background
    """
    nz, ny, nx = raw_scan.shape
    cy, cx = raw_center
    PSF = np.zeros_like(raw_scan)

    pupil_g = pupil_geometry((ny,nx), cy, cx, r_mask)
    center = np.unravel_index(np.argmax(gf(raw_scan*pupil_g.mask,2)), raw_scan.shape)
    print "Center found at: ", center
    pz, py, px = center
    pupil_g = pupil_geometry((ny,nx), py, px, r_mask) # new geometry
    hcyl = np.array(nz*[np.logical_and(pupil_g.r_pxl>=r_mask*1.30, pupil_g.r_pxl<1.50)])
    background = np.mean(raw_scan[hcyl]) # average in the hollow cylinder is taken as the background
    new_cyl = np.array(nz*[pupil_g.mask])
    PSF[new_cyl] = raw_scan[new_cyl]
    PSF[np.logical_not(new_cyl)] = background
    return PSF, background
#-------------------------- a small class of geometry
