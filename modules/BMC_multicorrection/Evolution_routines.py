'''
Evolution routines for aberration correction
Last update: 01/03/2017 by Dan.
'''

import numpy as np
import scipy as sp
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


    def single_Evaluate(self, n_mean = 1):
        '''
        Just apply the zernike coefficients, take the image and evaluate the sharpness
        z_coeffs: from 1 to z_max.
        '''
        self.ui.syncRawZern()
        # amplitude only-mask = False, the raw_MOD is updated as well.
        self.ui.toDMSegs() # this only modulates
        self.ui.apply2mirror()
        if n_mean >1:
            snap = []
            for nm in range(n_mean):
                snap.append(self.ui.acquireSnap()) #single_Evaluate
            snap = np.array(snap).mean(axis = 0)
        else:
            snap = self.ui.acquireSnap()

        self.ui.resetMirror() # great, reset mirror is already included.
        mt = self.ui.calc_image_metric(snap)
        self.ui.metrics.append(mt)
        return mt
        # done with single_Evaluate

    def singlemode_Nstep(self, zmode, start_coeff = 0.0, stepsize = 0.5, N=5):
        '''
        evaluate single mode
        '''
        HN = int(N/2)
        metric = np.zeros(N)
        coef_array = (np.arange(N)-HN)*stepsize + start_coeff
        for ii in np.arange(N):
            self.ui.updateZern(zmode, coef_array[ii])
            mt[ii] = self.single_Evaluate()

        max_ind = np.argmax(mt)
        if(max_ind == 0 or max_ind == N-1):
            new_coeff = coef_array[max_ind]
        else:
            p2 = np.polyfit(coef_array,mt, deg = 2)  # parabolic fit
            if p2[0]<0:
                new_coeff = -0.5*p2[1]/p2[0]
            else:
                new_coeff = coef_array[max_ind]
        return new_coeff

    def Evolve(self, zmodes, start_coeffs, use_simplex = True, Nmeasure = 5):
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
        self.ui.updateZern(zmodes, start_coeffs)
        NZ = len(zmodes) # number of modes
        for ii in np.arange(NZ):
            zm = zmodes[ii]
            coef0 = start_coeffs[ii]
            new_para = self.singlemode_Nstep(zm, coef0, stepsize = 0.5, Nmeasure)
            new_coeffs[ii] = new_para
            self.ui.updateZern(zm, new_para)

        return new_coeffs # return the final parameter
