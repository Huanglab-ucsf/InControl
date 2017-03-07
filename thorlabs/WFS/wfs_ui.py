from PyQt4 import QtCore,QtGui
import inLib
import numpy as np
import libtim.zern as lzern

class UI(inLib.ModuleUI):

    def __init__(self,control,ui_control):
        '''
        This is the initialization part of the UI.
        '''
        design_path = 'thorlabs.WFS.wfs_design'
        inLib.ModuleUI.__init__(self,control,ui_control,design_path)

        # pushbutton and input lines assignment

