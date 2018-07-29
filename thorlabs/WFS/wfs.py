import inLib
import numpy as np
import os 
import matplotlib.pyplot as plt

class Control(inLib.Device):
    '''
    the core control program for wave front sensor. 
    '''
    def __init__(self,settings):
        inLib.Device.__init__(self, 'thorlabs.WFS.WFS_api', settings)
        self.wavefront = None


    def acquire_WF(self):
        '''
        acquire wavefront and perform fitting.
        '''

    def zern_fit(self):
        '''
        fit the current wavefront to zernike.
        '''
