"""
Created by Dan on 11/11/2016
psf_tools for processing, plotting and characterizing psfs.
"""

import numpy as np
from scipy.ndimage import interpolation
from scipy.ndimage import gaussian_filter as gf
from scipy import optimize

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
