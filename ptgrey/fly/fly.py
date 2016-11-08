#!/usr/bin/python
#
# RJM 7/31/2012
#

import inLib
import time
import libs.imagewriters as writer
import numpy as np
import os

class Control(inLib.Device):
    def __init__(self, settings):

        inLib.Device.__init__(self, 'ptgrey.fly.cam_wrapper', settings)

        #Camera properties
        self._props = {}

        self.exposureTime = settings['exposure_time']*10e-3
        self.xdim = settings['dimensions'][0]
        self.ydim = settings['dimensions'][1]
        self.x0 = settings['roi'][0]
        self.y0 = settings['roi'][1]

        self.xdim_2 = 256
        self.ydim_2 = 256
        self.x0_2 = 0
        self.y0_2 = 0

        self.daxFile = 0
        self.recordedFrames = 0

    def newSettings(self, exposure=None, xdim=None, ydim=None,
                    x0=None, y0=None, xdim_2=None, ydim_2=None,
                    x0_2=None, y0_2=None):
        if exposure is not None:
            self.exposureTime = exposure
            self.setExposureTime(exposure)
            self._props['exposure_time'] = exposure
        if xdim is not None and ydim is not None:
            self.xdim = xdim
            self.ydim = ydim
            self._props['dimensions'] = xdim,ydim
        if x0 is not None:
            self.x0 = x0
            self._props['x_start'] = x0
        if y0 is not None:
            self.y0 = y0
            self._props['y_start'] = y0
        if xdim_2 is not None:
            self.xdim_2 = xdim_2
        if ydim_2 is not None:
            self.ydim_2 = ydim_2
        if x0_2 is not None:
            self.x0_2 = x0_2
        if y0_2 is not None:
            self.y0_2 = y0_2

    def setExposureTime(self,time):
        self.exposureTime = time
        self._api.setShutterTime(time)

    def getImage(self, secondary=False):
        im = self._api.getImage()
        return (im[self.x0:self.x0+self.xdim, self.y0:self.y0+self.ydim],0)

    def flatFieldCorrect(self):
        ims = self.getImage()[0]*1.0
        print ims
        for i in range(1,100):
            ims += self.getImage()[0]
        return ims/100.0
        
    def saveImage(self, filename):
        im = self.getImage()
        np.save(filename, im)

    def beginRecord(self, filename):
        self.recordedFrames = 0
        self.daxFile = writer.DaxFile(filename, self._props)

    def recordFrame(self):
        if self.daxFile!=0:
            im = self.getImage()
            temp = im.reshape(im.shape[0]*im.shape[1]).astype(np.dtype('>H'))
            self.daxFile.saveFrames(temp.tostring(), 1)
            self.recordedFrames += 1
            return self.recordedFrames

    def endRecording(self):
        self.daxFile.closeFile([0,0,0], 0)
        print "Closing DAX file " + str(self.daxFile.filename)
        self.daxFile = 0
        

    def shutDown(self):
        self._api.shutDown()

    
   
