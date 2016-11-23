import inLib
import numpy as np
import os
import time
import matplotlib.pyplot as plt
from DM_simulate import DM
from scipy.ndimage import interpolation
import psf_tools
import subprocess



class Control(inLib.Module):

    def __init__(self, control, settings):
        print 'Initializing BMC_multicorrection.'
        inLib.Module.__init__(self, control, settings) # inheriting
        dims = self._control.camera.getDimensions()
        self.dims = dims
        self.executable = settings['executable'] # specify the executable of the deformable mirror
        self._modulations = []
        self.n_mod = 0
        self._PSF = None
        self.DM = DM(nPixels = dims[0]) # Initialize a DM simulation
        self.proc = None # the procedure for running the deformable mirror
        self.gain = 1.0
        print('BMC_multicorrection initialized.')
    #------------------------- Private functions

    def _alignPupil(self,raw_MOD):
        '''
        Align the pupil pattern, which is vertical with the mirror pattern, which
        is horizontal.
        '''
        MOD = -1*raw_MOD
        MOD = np.flipud(MOD)
        MOD = np.rot90(MOD)
        MOD = np.rot90(-1.0*MOD)
        n_pattern = self.DM.nPixels
        zoom = n_pattern/MOD.shape[0]
        print(zoom)
        MOD = interpolation.zoom(MOD,zoom,order=0,mode='nearest')
        MOD_product = np.rot90(MOD-MOD.min())
        return MOD_product
        # done with _alignPupil

    def updateImSize(self):
        '''
        Gets the image size from the camera.
        _ui uses this for sharpness calculations...
        '''

        self.dims = self._control.camera.getDimensions()
        # endof updateImSize


    def acquirePSF(self, range_, nSlices, nFrames, center_xy=True, filename=None,
                   mask_size = 40, mask_center = (-1,-1)):

        '''
        Acquires a PSF stack. The PSF is returned but also stored internally.
        '''
        self.filename = filename

        # Some parameters
        start = range_/2.0
        end = -range_/2.0
        self._dz = abs(range_/(nSlices-1.0))

        # Scan the PSF:
        scan_psf = self._control.piezoscan.scan(start, end, nSlices, nFrames, filename)
        nz, ny, nx = scan_psf.shape
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


    def pattern2Segs(self, raw_MOD):
        new_MOD = self._alignPupil(raw_MOD)
        self.DM.setPattern(new_MOD)
        self.DM.findSeg()
        # end of pattern2Segs


    def modulateDM(self, fname):
        """
        Simply, modulate the created pattern.
        """
        # self.pattern2Segs()
        if self.proc is not None:
            print "Polling proc: ", self.proc.poll()
            if self.proc.poll() is None:
                self.proc.terminate()
                self.proc.communicate()
                self.proc = None

        self.DM.exportSegs(fname) # save the pattern as the output file

        args = [self.executable, fname, str(self.gain), "1", "-1"] # add only one  file
        self.proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        print("The pattern is added to the mirror.")



    def storeDM_seg(self):
        '''
        If this modulation is worth keeping
        '''
        seg_copy = self.getDM_segs()
        self._modulations.append[seg_copy]


        # get the handle of the DM

    def advanceWithPipe(self):
        '''
        Is it equivalent to typing a '\n' from the prompt?
        It seems yes!
        '''
        if self.proc is not None:
            self.proc.stdin.write("\n")
            output = self.proc.stdout.read()
            print("stdout:", output)
        # done with advanceWithPipe


    def getDM_segs(self):
        '''
        return the DM_segs
        '''
        seg_copy = np.copy(self.DM.getSegs())
        return seg_copy

        # done with clearMOD


    def clearZern(self):
        '''
        clear all the zernike mode coeeficients
        '''
        self.DM.clearPattern() # clear the deformable mirror pattern
        # done with clearZern

    def setGain(self, gain):
        self.gain = gain
