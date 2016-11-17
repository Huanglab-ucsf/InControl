import inLib
import numpy as np
import os
import time
import matplotlib.pyplot as plt
from DM_simulate import DM, pupil_geometry
import psf_tools



class Control(inLib.Module):

    def __init__(self, control, settings):
        print 'Initializing BMC_multicorrection.'
        inLib.Module.__init__(self, control, settings) # inheriting
        dims = self._control.camera.getDimensions()
        self.executable = settings['executable'] # specify the executable of the deformable mirror
        self._modulations = []
        self.n_mod = 0
        self._PSF = None
        self.DM = DM(nPixels = dims.min()) # Initialize a DM simulation
        self.proc = None # the procedure for running the deformable mirror
        self.gain = 1.0
        self.raw_MOD = np.zeros(dims)
        print('BMC_multicorrection initialized.')
    #------------------------- Private functions

    def _alignPupil(self):
        '''
        Align the pupil pattern, which is vertical with the mirror pattern, which
        is horizontal.
        '''
        MOD = -1*self.raw_MOD
        MOD = np.flipud(MOD)
        MOD = np.rot90(MOD)
        MOD = np.rot90(-1.0*MOD)
        n_pattern = self.DM.nPixels
        zoom = n_pattern/MOD.shape[0]
        MOD = interpolation.zoom(MOD,zoom,order=0,mode='nearest')

        return MOD
        # done with _alignPupil

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



    def modulateDM(self, fname):
        """
        Simply, modulate the created pattern.
        """
        new_MOD = self._alignPupil()

        if self.proc is not None:
            print "Polling proc: ", self.proc.poll()
            if self.proc.poll() is None:
                self.proc.terminate()
                self.proc.communicate()
                self.proc = None

        self.DM.exportSegs(fname) # save the pattern as the output file

        args = [self.executable, fname, str(self.gain), "1", "-1"] # add only one  file
        self.proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


        self.new_MOD = new_MOD


    def storeMOD(self):
        '''
        If this modulation is worth keeping
        '''
        if(self.new_MOD is not None):
            self._modulations.append(new_MOD)
            self.n_mod+=1
            self.new_MOD = None
        else:
            print("no new modulation to save.")
        # get the handle of the DM

    def advanceWithPipe(self):
        '''
        Is it equivalent to typing a '\n' from the prompt?
        It seems yes!
        '''
        if self.proc is not None:
            self.proc.stdin.write("\n")
