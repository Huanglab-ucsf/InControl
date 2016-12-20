'''
Simplex method
'''
import numpy as np


class simplex(object):
    def __init__(self, simp_0, paras):
        '''
        Initialize the simplex value and step size
        Inside the simplex, every node should be equivalent.
        '''
        self.paras = paras # stepsize is one -element less than the val.
        self.val = simp_0

    def evaluate(self, maximizing = True):
        '''
        update the simplex and return a direction
        If maximizing is True, update in the direction of maximizing the simplex, otherwize Minimize the simplex.
        '''
        ind_max, ind_min = (np.argmax(self.val), np.argmin(self.val))

        if(maximizing):
            ind_good = ind_max
            ind_bad = ind_min
        else:
            ind_good = ind_min
            ind_bad = ind_max

        if(ind_sup >0): # if not the node self
            self.stepsize[ind_sup-1] *=2 # go further
        if(ind_inf >0): # if not the node self
            self.stepsize[ind_inf-1] *=-1 # flip
        return ind_max, ind_min # superior, inferior

    def get_steps(self):
        return self.stepsize
