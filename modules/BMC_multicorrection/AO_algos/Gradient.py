'''
Created by Dan on 01/03/2017, the gradient method.
'''

import numpy as np
import scipy as sp


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


def conjugate_gradient(hess, grad, u0):
    '''
    conjugate gradient method, from numerical recipies.
    '''
