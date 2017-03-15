'''
Created by Dan on 12/15/2016.

'''

from PyQt4 import QtGui,QtCore
import numpy as np


class Scanner(QtCore.QThread):

    def __init__(self, control, range_, nSlices, nFrames, center_xy, fname, maskRadius, maskCenter):
        QtCore.QThread.__init__(self)

        self.control = control
        self.range_ = range_
        self.nSlices = nSlices
        self.nFrames = nFrames
        self.center_xy = center_xy
        self.fname = fname
        self.maskRadius = maskRadius
        self.maskCenter = maskCenter

    def run(self):
        self.control.acquirePSF(self.range_, self.nSlices, self.nFrames,
                                self.center_xy, self.fname,
                                self.maskRadius, self.maskCenter)
    # done with Scanner


class BL_correction(QtCore.QThread):
    '''
    Backlash correction
    '''
    def __init__(self, control, z_correct, z_start):
        QtCore.QThread.__init__(self)
        self.control = control
        self.z_correct = z_correct
        self.z_start = z_start


    def run(self):
        self.control.positionReset(self.z_correct, self.z_start)
    # done with BL_correction


class Optimize_pupil(QtCore.QThread):
    '''
    Optimize the pupil
    This one should be adaptable to the single-mode optimization!
    '''
    def __init__(self, ev_control, zmodes, start_coeffs, Nmeasure, flabel):
        QtCore.QThread.__init__(self)
        self.ev_control = ev_control
        self.zmodes = zmodes
        self.start_coeffs  = start_coeffs
        self.Nmeasure = Nmeasure
        self.data_path = 'D://Data//Dan//zmet_'+ flabel


    def run(self):
        '''
        run the pupil optimization (this is solely Zernike based)
        '''
        self.ev_control.Evolve(self.zmodes,self.start_coeffs, Nmeasure = self.Nmeasure, fpath = self.data_path)
    # done with Optimize_pupil



class Single_modulation(QtCore.QThread):
    '''
    modulate the deformable mirror with the single mode
    variables: 140
    '''

    def __init__(self,mod_control,segments,ampli,flabel):
        QtCore.QThread.__init__(self)
        self.mod_control = mod_control
        self.segments = segments
        self.amplitude = ampli
        self.data_path = 'D://Data//Dan//segmod_'+ flabel
        self._log_modulation_()

    def _log_modulation_(self):
        '''
        export the modulation as log
        '''
        output = np.array([self.segments, self.amplitude])
        np.save(self.data_path+'_mod_' + int(self.Niter), output)
        self.Niter +=1


    def run(self):
        '''
        run the single segments modulation
        unfinished 
        '''
        pass 
