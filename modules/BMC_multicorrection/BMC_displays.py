'''
This is a module for displaying
'''
import numpy as np
import matplotlib.pyplot as plt

class displays(UI_control):
    def __init__(self, UI_control):
        self.ui_control = UI_control


    def displayPhase(self):
        '''
        display phase (undiscretized, unrotated) on canvas mpl_phase
        '''
        phase = self.raw_MOD # this is the raw phase
        self._ui.mpl_phase.figure.axes[0].matshow(phase, cmap='RdBu')
        self._ui.mpl_phase.draw()
