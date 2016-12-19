'''
Evolution routines for aberration correction
'''

import numpy as np
import scipy as sp
from AO_algos import simplex

class Pattern_evolution(object):
    '''
    Pattern evolution, load the ui into the
    '''

    def __init__(self, ui_control):
        '''
        init function 0
        '''
        self.ui = ui_control
        self.simplex = []
        self.coeffs = None


    def single_Evaluate(self, n_mean = 1):
        '''
        Just apply the zernike coefficients, take the image and evaluate the sharpness
        z_coeffs: from 1 to z_max.
        '''
        self.ui.syncRawZern()
        # amplitude only-mask = False, the raw_MOD is updated as well.
        self.ui.displayPhase() # display on the figure
        self.ui.toDMSegs() # this only modulates
        self.ui.apply2mirror()
        if n_mean >1:
            snap = []
            for nm in range(n_mean):
                snap.append(self.ui.acquireSnap()) #single_Evaluate
            snap = np.array(snap).mean(axis = 0)
        else:
            snap = self.ui.acquireSnap()

        self.ui.resetMirror()
        mt = self.ui.calc_image_metric(snap)
        self.ui.metrics.append(mt)
        return mt
        # done with single_Evaluate


    def calc_simplex(self, z_directions, coeff_0, stepsize):
        '''
        Evaluate the simplex
        '''
        simplex = []
        z_coeffs = coeffs_0
        simplex.append(self.single_Evaluate())
        self.edges = np.zeros()
        for zi in z_directions:
            '''
            This should be refined: How to select the effective modes?
            '''
            z_coeffs[zi] += stepsize[zi]
            simplex.append(self.single_Evaluate(z_coeffs)) # increase the simplex
            z_coeffs[zi] -= stepsize[zi]


        z_max = np.argmax(simplex) # find the maximum corner of the simplex
        z_coeffs[zi] -= stepsize[zi] # update the simplex by flipping

        self.coeffs = z_coeffs
        self.z_max = z_max
        self.simplex = simplex
        return z_max, simplex

        # done with calc_simplex


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


    def Evolve(self, zmodes, start_coeffs):
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
        mt = self.single_Evaluate()
        print("The metric is:", mt)
