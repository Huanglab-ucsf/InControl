import inLib
import numpy as np
import os 
import matplotlib.pyplot as plt

class Control(inLib.Module):
    '''
    the core control program for wave front sensor. 
    '''
    def __init__(self,control,settings):
        self.executable = settings['executable']
        self.wavefront = None


    def acquire_WF(self):
        '''
        acquire wavefront and perform fitting.
        '''

    def zern_fit(self):
        '''
        fit the current wavefront to zernike.
        '''
