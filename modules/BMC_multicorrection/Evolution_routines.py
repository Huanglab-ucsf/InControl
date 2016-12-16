'''
Evolution routines for aberration correction
'''

import numpy as np
import scipy as sp


class Simplex():
    '''
    Simplex method
    '''
    def __init__(self, ui_control):
        '''
        init function 0
        '''
        self.ui = ui_control
        self.simplex = []
        self.coeffs = None


    def calc_simplex(self, z_directions, coeff_0, stepsize):
        '''
        Evaluate the simplex
        '''
        simplex = []
        z_coeffs = coeffs_0
        simplex.append(self.ui.single_Evaluate(coeffs_0))
        self.edges = np.zeros()
        for zi in z_directions:
            '''
            This should be refined: How to select the effective modes?
            '''
            z_coeffs[zi] += stepsize[zi]
            simplex.append(self.ui.single_Evaluate(z_coeffs)) # increase the simplex
            z_coeffs[zi] -= stepsize[zi]


        z_max = np.argmax(simplex) # find the maximum corner of the simplex
        z_coeffs[zi] -= stepsize[zi] # update the simplex by flipping

        self.coeffs = z_coeffs
        self.z_max = z_max
        self.simplex = simplex
        self.edges =
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




class conjugate_gradient():
    def __init__(self, control):
        '''
        '''
        self._control = control



    def step_Hessian(self, z_modes, z_coeffs, z_steps):
        '''
        z_modes: selected modes for optimization. 4 --- zmax
        z_coeffs: the coefficients of the zernike modes
        z_steps: the designed steps in each mode. If it is 0 or ignored, then the mode is dropped.
        '''
        N_search = len(z_modes) # the dimension of the search space
        zc_input = np.zeros(self.z_max)
        st_input = np.zeros(self.z_max)
        try:
            zc_input[z_modes-1] = z_coeffs
        except ValueError:
            print('dimension mismatch for amplitudes.')
            return -1

        # assign the steps
        try:
            st_input[z_modes-1] = z_steps
        except ValueError:
            print('dimension mismatch for stepsize.')
            return -2

        S_vec = np.zeros(N_search)
        deriv = np.zeros(N_search)
        S_mat= np.zeros([N_search, N_search]) # the first row saves the first derivative, the rest N_search rows save the second.
        hess = np.zeros([N_search, N_search])

        S0 = self.single_Evaluate(zc_input)

        for iz in np.arange(N_search):
            '''
            iterate through z_modes: outer cycle
            '''
            step_i = st_input[iz]
            nz = z_modes[iz] # select the modes out
            zc_input[nz-1] +=step_i
            S_vec[iz] = self.single_Evaluate(zc_input)
            # zc_input[nz-1] -=step_i

            for jz in np.arange(iz, N_search): # this gives the upper right triangle values
                '''
                iterate through z_modes: inner cycle
                '''
                step_j = st_input[jz]
                mz = z_modes[jz]
                zc_input[mz-1] +=step_j
                S_mat[iz, jz] = self.single_Evaluate(zc_input)
                S_mat[jz, iz] = S_mat[iz, jz] # symmetrize
                zc_input[mz-1] -=step_j
            # return the zc_input to its original form
            zc_input[nz-1] -=step_i
        # OK, now the whole S_vec and S_mat is computed.

        [DS, DK] = np.meshgrid(S_vec, S_vec) # meshgrid
        [sts, stk] = np.meshgrid(st_input, st_input)
        hess = S_mat-(DS+DK) + S0/(sts*stk)

        return hess # bingo!!! But actually, this is not a very complete set.
        # done with single_runGradZern
