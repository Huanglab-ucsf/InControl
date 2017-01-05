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



    def update_coefficient(self, a_exp):
        '''
        Find the maximum and minimum of the simplex, and move the maximum node along the direction of the max-min axis
        a_ext: the relative length of the step (the fraction of max-min length)
        '''
        simplex = self.simplex
        z_min = np.argmin(simplex)
        z_max = np.argmax(simplex)
        '''
        Unfinished: need to update the stepsize along the direction of min-max
        '''


    def Evolve(self, zmodes, start_coeffs, use_simplex = True, Niter = 10):
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

        self.ui.updateZern(zmodes, start_coeffs)
        NZ = len(zmodes) # number of modes
        mt = self.single_Evaluate()
        sval = [mt]
        param = np.tile(start_coeffs, (NZ+1, 1)).astype('float64') # NZ+1 rows for simplex nodes
        step_size = self.ui.z_comps.get_parameters(zmodes)[1]
        param[1:] = param[1:] + np.diag(step_size) # set the 1 --- NZ rows of the param matrix
        print("Parameters:", param)

        for iz in np.arange(1, NZ+1):
            self.ui.updateZern(zmodes, param[iz])
            mt = self.single_Evaluate()
            sval.append(mt)
        print("simplex value:", sval)

        for ncycle in range(Niter):
            '''
            Update for the Niter iterations.
            '''
            new_param, ind_sup, ind_inf = simplex_assess(sval, param, gain = 0.8) # maximizing; gain = 1.0
            print("new parameter:", new_param)
            param[ind_inf] = new_param
            self.ui.updateZern(zmodes, new_param)
            mt = self.single_Evaluate()
            sval[ind_inf] = mt
            print("new simplex:", sval)

        return param # return the final parameter
