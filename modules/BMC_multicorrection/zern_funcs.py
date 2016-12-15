"""
Created by Dan on 11/09. Zernike function.
This is my first attempt to use python properties. To be more Pythonic!
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt


class zern_mode(object):
    '''
    This is a small class of Zernike modes.
    '''
    def __init__(self, z_mode, ampli, step = 0.10):
        self._zmode = z_mode
        self._ampli = ampli
        self._step = step

    @property
    def zmode(self):
        return self._zmode
    #this property does not have a setter. Is that OK?

    @property
    def ampli(self):
        return self._ampli

    @ampli.setter
    def ampli(self, value):
        self._ampli = value


    @property
    def step(self):
        return(self._step)

    @step.setter
    def step(self, value):
        self._step = value

    def stepup(self):
        self._ampli+=self._step

    def stepdown(self):
        self._ampli-=self.step

    # -------------------------------Done with zern_mode -------------------


class zm_list(object):
    '''
    A bigger class, a list of zern_mode.
    '''
    def __init__(self, z_max = 25, z_start = 4):
        self.zlist = []
        self.start_mode = z_start
        self.max_mode = z_max
        self.NL = z_max-n_start+1
        self.active = np.zeros(self.NL).astype('bool') # by default: all zero , the indices should-1

        for iz in np.arange(self.NL):
            new_mode = zern_mode(z_mode=iz, ampli = 0)
            self.zlist.append(new_mode)
        # done initialization

    def switch(self, z_mode, status = True):
        '''
        Turn the mode on or off
        '''
        if z_mode > self.max_mode or z_mode < self.start_mode:
            raise ValueError("Oops! The mode is out of range.")
        self.zlist[z_mode-self.start] = status
        # done with the switch

    def grab_mode(self, z_mode):
        '''
        grab the z_mode node in the list
        '''
        if z_mode > self.max_mode or z_mode < self.start_mode:
            raise ValueError("Oops! The mode is out of range.")
        return self.zlist[z_mode - self.start_mode] # return a node.

    def sync_coeffs(self):
        z_coeffs = np.zeros(self.max_mode) # a complete coefficient list
        activated = np.where(self.active == True)

        while nac in activated:
            val = self.zlist[nac].ampli()
            zm = self.zlist[nac].zmode()
            z_coeffs[zm-1] = val

        return sync_coeffs # this is a coefficient list that can be used for other zernikes. 
