# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 11:41:43 2019

@author: Huanglab
"""
import numpy as np
import matplotlib.pyplot as plt
import glob


sq2 = np.sqrt(0.5)
transform_mat = np.array([
    [0., -1, 0.],
    [sq2, 0., sq2],
    [-sq2, 0., sq2]
    ]) # the transform matrix between the lab frame and the image frame

def _phase_construct_(NK, x0):
    hk = int(NK//2)
    kk = np.arange(NK) - hk # the zero-frequency is in the middle

    phi = 2.0*np.pi*kk*x0/NK
    phase = np.cos(phi) - np.sin(phi)*1j
    return phase

def shift_fourier(img, dy, dx = 0.):
    '''
    shift the image in Fourier space
    '''
    NY, NX = img.shape
    yp = _phase_construct_(NY, dy)
    xp = _phase_construct_(NX, dx)
    phase_img = np.outer(yp,xp)
    fimg = np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(img)) * phase_img)
    img_shifted = np.fft.ifft2(fimg)

    return np.abs(img_shifted)

def deskew_stack(stack, scan_range = 6.0, pxl = 0.103, method = 'fourier'):
    '''
    img: the raw image acquired
    scan_range: the range of Z-scanning, unit micron.
    pxl: pixel size, unit micron.
    have a zero-padded stack.
    method: 'direct' or 'fourier'
    '''
    NZ, NY, NX = stack.shape
    n_pad = int(np.ceil(scan_range/(2*np.sqrt(2.)*pxl)))# half number of padded points
    padded_stack = np.zeros((NZ, NY + 2*n_pad, NX))
    DXB = np.linspace(0., scan_range, NZ) # The scan range
    z_range = DXB/np.sqrt(2.)
    #y_range = -z_range

    if method == 'direct':
        for nn in range(NZ):
            y_shift = int(z_range[NZ-nn-1]/pxl)
            print('y_shift:', y_shift)
            padded_stack[nn, y_shift:(y_shift + NY), :] = stack[nn]
    elif method == 'fourier':
        for nn in range(NZ):
            y_shift = int(z_range[NZ-nn-1]/pxl)
            padded_slice = np.pad(stack[nn], ((n_pad, n_pad),(0,0)), 'constant')
            padded_stack[nn] = shift_fourier(padded_slice, y_shift)
    # next, shift the y back
    return padded_stack


# -------------------------------------A small test for deskew --------------------
def main():
    '''
    load and test the data
    '''
    SC_list = glob.glob(global_datapath + '*SC*.npy')
    SC_psf = np.load(SC_list[0])
    padded_stack = transform(SC_psf, method = 'fourier').astype('uint16')

    tf.imsave('padded_ft.tif', padded_stack)
    tf.imsave('original.tif', SC_psf.astype('uint16'))

if __name__ == '__main__':
    main()

