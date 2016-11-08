#!/usr/bin/python


from ctypes import *
import numpy as np


class API(object):
    '''
    A ctypes based Python wrapper for the SDK of PCIe based xySeries SLMs.
    The functions are a direct translation of the SDK DLL. Documentation is provided
    by Boulder Nonlinear.
    '''

    def __init__(self):
	# Load library:
	self.slm = cdll.LoadLibrary('C:\\PCIeLabVIEWSDK\\Interface.dll')

    def constructor(self,RAMWriteEnable,trueFrames,boardName):
        return self.slm.Constructor(RAMWriteEnable,trueFrames,boardName)

    def deconstructor(self):
        self.slm.Deconstructor()

    def slmPower(self,powerState):
        self.slm.SLMPower(powerState)

    def writeImage(self,board,image,imageSize):
        size = image.size
        image = image.astype(np.uint8).tostring()
        image = create_string_buffer(image,size)
        self.slm.WriteImage(board,image,imageSize)

    def loadLUTFile(self,board,LUTFile):
        self.slm.LoadLUTFile(board,LUTFile)
