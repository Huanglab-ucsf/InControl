'''
Evolution routines for aberration correction
Last update: 01/03/2017 by Dan.
'''

import numpy as np
import scipy as sp
import time
from AO_algos.simplex import simplex_assess



class Pattern_evolution(object):
    '''
    Pattern evolution, load the ui into the
    '''

    def __init__(self, ui_control):
        '''
        init function 0
        '''
        self.ui = ui_control
        self.simplex = None
        self.coeffs = None


    def single_Evaluate(self, n_mean=3):
        '''
        Just apply the zernike coefficients, take the image and evaluate the sharpness
        z_coeffs: from 1 to z_max.
        This can be reused.
        '''
        # amplitude only-mask = False, the raw_MOD is updated as well.
        self.ui.toDMSegs(display = False) # this only modulates
        self.ui.apply2mirror()
        time.sleep(0.05)
        mts = np.zeros(n_mean)
        snap = self.ui.acquireSnap(1)
        for ii in np.arange(n_mean):
            snap = self.ui.acquireSnap(1)
            mts[ii] = self.ui.calc_image_metric(snap, mode = 'sharp')
        # self.ui._control.laserSwitch(False)
        # self.ui.resetMirror() removed on 02/09/17.
        mt = np.mean(mts)
        msig = np.std(mts)
        return mt, msig,snap
        # done with single_Evaluate

    def singlemode_Nstep(self, zmode, start_coeff = 0.0, stepsize = 0.5, N=9):
        '''
        evaluate single mode
        '''
        HN = int(N/2)
        mt = np.zeros(N)
        msig = np.zeros(N)
        coef_array = (np.arange(N)-HN)*stepsize + start_coeff
        snap_stack = []
        for ii in np.arange(N):
            self.ui.updateZern(zmode, coef_array[ii])
            mt[ii], msig[ii], snap = self.single_Evaluate()
            snap_stack.append(snap)

        snap_stack = np.array(snap_stack)
        np.save('D:\Data\Dan\ZM_stack'+str(zmode), snap_stack)
        self.ui.displayMetrics(mt, msig)
        # np.save('D:\Data\Dan\Mt_'+ self.flabel + str(zmode), mt)
        max_ind = np.argmax(mt)
        if(max_ind == 0 or max_ind == N-1):
            new_coeff = coef_array[max_ind]
        else:
            p2 = np.polyfit(coef_array,mt, deg = 2)  # parabolic fit

            if p2[0]<0:
                new_coeff = -0.5*p2[1]/p2[0]
            else:
                new_coeff = coef_array[max_ind]
        return new_coeff, mt


    def dynamic_stepwise(self, zmode, step_0):
        '''
        update the z_mode coefficients dynamically
        '''

    def Evolve(self, zmodes, start_coeffs, Nmeasure, fpath):
        '''
        zmodes: the modes selected for optimization
        Start_coeffs: The starting coefficients of the evolution
        0. Update all the coefficients
        1. Evaluate sharpness
        2. Update the amplitude one by one, evaluate each sharpness value
        3. Construct a simplex
        4. Move along the minimization direction
        5. go to step 1.
        '''
        new_coeffs = np.copy(start_coeffs)
        metric_val = np.zeros([Nmeasure, len(zmodes)])
        self.ui.updateZern(zmodes, start_coeffs)
        NZ = len(zmodes) # number of modes
        for ii in np.arange(NZ):
            zm = zmodes[ii]
            coef0 = start_coeffs[ii]
            stepsize = self.ui.z_comps.grab_mode(zm).step
            new_para, mt = self.singlemode_Nstep(zm, coef0, stepsize, Nmeasure)
            new_coeffs[ii] = new_para
            self.ui.updateZern(zm, new_para)
            metric_val[:,ii] = mt


        np.save(fpath, metric_val)
        print("New coefficients:", new_coeffs)
