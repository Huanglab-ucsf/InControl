"""
Created by Dan on 11/09. Zernike function.
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import seaborn


class Zernike_func(object):
    def __init__(self,radius, mask=True):
        self.radius = radius
        self.useMask = mask
        self.pattern = []


    def single_zern(self, mode, amp):
        modes = np.zeros((mode))
        modes[mode-1] = amp
        self.pattern= libtim.zern.calc_zernike(modes, self.radius, mask = self.useMask, zern_data= {})

        return self.pattern


    def multi_zern(self, amps):
        self.pattern = libtim.zern.calc_zernike(amps, self.radius, mask = self.useMask, zern_data = {})
        return self.pattern
#         RMSE[ii] = np.sqrt(np.var(PF_core))
#         ii +=1

    def plot_zern(self):
        plt.imshow(self.pattern, interpolation='none')
        plt.show()
