__all__ = [ ]

import os
import platform
import sys
import textwrap
import numpy as np
from numpy import ctypeslib
import ctypes
import ctypes.util
import ctypes.wintypes
import warnings

from ctypes.wintypes import BYTE
from ctypes.wintypes import WORD
from ctypes.wintypes import DWORD
from ctypes.wintypes import BOOL
HCAM = ctypes.wintypes.HANDLE
from ctypes.wintypes import HDC
from ctypes.wintypes import HWND
from ctypes.wintypes import INT
c_char = ctypes.c_byte
c_char_p = ctypes.POINTER(ctypes.c_byte)
c_int_p = ctypes.POINTER(ctypes.c_int)
c_double_p = ctypes.POINTER(ctypes.c_double)
from ctypes import c_int, c_uint, c_double, c_bool, c_long, c_ulong, c_float
from ctypes import byref
IS_CHAR = ctypes.c_byte 

dll_name = 'tisgrabber.dll'
cam = ctypes.windll.LoadLibrary(dll_name)

serialNum = ctypes.create_string_buffer(20)
serialNum = "ISB3200016679"

filenm = ctypes.create_string_buffer("test.bmp")

initLib = cam.__getattr__('IC_InitLibrary')
closeLib = cam.__getattr__('IC_CloseLibrary')
createGrabber = cam.__getattr__('IC_CreateGrabber')
releaseGrabber = cam.__getattr__('IC_ReleaseGrabber')
getDeviceName = cam.__getattr__('IC_GetDeviceName')
getDevice = cam.__getattr__('IC_GetDevice')
getDeviceCount = cam.__getattr__('IC_GetDeviceCount')
openDevice = cam.__getattr__('IC_OpenVideoCaptureDevice')
getSerialNumber = cam.__getattr__('IC_GetSerialNumber')
getUniqueNameFromList = cam.__getattr__('IC_GetUniqueNamefromList')
getFrameRate = cam.__getattr__('IC_GetFrameRate')
startLive = cam.__getattr__('IC_StartLive')
prepareLive = cam.__getattr__('IC_PrepareLive')
suspendLive = cam.__getattr__('IC_SuspendLive')
stopLive = cam.__getattr__('IC_StopLive')
snapImage = cam.__getattr__('IC_SnapImage')
saveImage = cam.__getattr__('IC_SaveImage') #0 = jpeg; 1 = bitmap
getImagePtr = cam.__getattr__('IC_GetImagePtr')
getExpRegVal = cam.__getattr__('IC_GetExpRegVal')
getExpRegValRange = cam.__getattr__('IC_GetExpRegValRange')
getExpAbsValRange = cam.__getattr__('IC_GetExpAbsValRange')
getExpAbsVal = cam.__getattr__('IC_GetExpAbsVal')
setExpAbsVal = cam.__getattr__('IC_SetExpAbsVal')
getVideoProperty = cam.__getattr__('IC_GetVideoProperty')
getAutoVideoProperty = cam.__getattr__('IC_GetAutoVideoProperty')
getImageDescription = cam.__getattr__('IC_GetImageDescription')
enableAutoVideoProperty = cam.__getattr__('IC_EnableAutoVideoProperty')
#continuousMode not available in live mode
setContinuousMode = cam.__getattr__('IC_SetContinuousMode') #params: hGrabber (handle), cont (0=continuous snap, 1=not)
setFrameReadyCallback = cam.__getattr__('IC_SetFrameReadyCallback')


class API(HCAM):
    def __init__(self):
        HCAM.__init__(self)
        err = initLib(serialNum)
        self.cam = createGrabber()
        self.count = getDeviceCount()
        self.device = getDevice(INT(0))
        self.name = getUniqueNameFromList(INT(0))
        self.width = 0
        self.height = 0
        self.bpp = 0
        self.buffer = []
        openDevice(self.cam, self.device)
        startLive(self.cam, INT(0)) #{param: 1: show video, 0: do not show} [prepareLive has same param]

    def initBuffer(self):
        self.width, self.height, self.bpp = self.getImageDesc()
        self.buffer_temp = np.zeros((self.width*self.height*3),dtype=np.uint8)
        self.image = np.zeros((self.width,self.height),dtype=np.uint8)

    def setContinuousMode(self):
        return setContinuousMode(self.cam, INT(0))

    def getExposureTime(self):
        fexp = c_float()
        getExpAbsVal(self.cam, byref(fexp))
        return fexp.value

    def setExposureTime(self, exptime):
        setExpAbsVal(self.cam, c_float(exptime))
        
    def getImageDesc(self):
        lwidth = c_long()
        lheight = c_long()
        ibpp = c_int()
        iformat = c_int()
        err = getImageDescription(self.cam, byref(lwidth), byref(lheight), byref(ibpp), byref(iformat))
        if err!=1:
            print "Error getting Image description."
            return 0,0,0
        else:
            return lwidth.value, lheight.value, ibpp.value

    def getImage(self, delay):
        '''
        delay: timeout in ms; no timeout if delay = -1
        '''
        err = snapImage(self.cam, INT(delay))
        xdim,ydim = self.width,self.height
        if err!=1:
            print "Error in snapImage."
            return 0
        d = getImagePtr(self.cam)
        dp = ctypes.cast(d,ctypes.c_void_p)
        ctypes.memmove(self.buffer_temp.ctypes.data,dp,xdim*ydim*ctypes.sizeof(ctypes.c_ubyte)*3)
        self.image = np.frombuffer(self.buffer_temp, dtype=np.uint8).reshape(ydim,xdim,3).sum(axis=-1)

    def returnImage(self):
        return self.image

    def getVideoProps(self):
        vidprop = c_long()
        for i in range(0,10):
            getVideoProperty(self.cam, INT(i), byref(vidprop))
            print vidprop.value

    def disableAuto(self):
        for i in range(0,10):
            enableAutoVideoProperty(self.cam, INT(i), INT(0))

    def shutDown(self):
        stopLive(self.cam)
        releaseGrabber(ctypes.byref(INT(self.cam)))
        

'''
hGrab = createGrabber()
openDevice(hGrab,getDeviceName(c_int(hGrab)))
getSerialNumber(hGrab, serialNum2)

class data(ctypes.Structure):
    _field_ = [("image", ctypes.c_ubyte*1024*768)]

iccam = camera()
xdim = 1024
ydim = 768
buf = np.zeros((xdim*ydim),dtype=np.uint8)
buf2 = ctypes.create_string_buffer(xdim*ydim)
buf3 = (ctypes.c_ubyte*xdim*ydim)()
 
a = openDevice(iccam.cam, iccam.device)
b = startLive(iccam.cam, INT(0))
c = snapImage(iccam.cam, INT(1000))

vidprop = c_long()
for i in range(0,10):
    getVideoProperty(iccam.cam, INT(i), byref(vidprop))
    print vidprop.value

lmin = c_long()
lmax = c_long()
getExpRegValRange(iccam.cam, byref(lmin), byref(lmax))
fmin = c_float()
fmax = c_float()
getExpAbsValRange(iccam.cam, byref(fmin), byref(fmax))
fexp = c_float()
getExpAbsVal(iccam.cam, byref(fexp))

lWidth = c_long()
lHeight = c_long()
iBPP = c_int()
iFormat = c_int()
getImageDescription(iccam.cam, byref(lWidth), byref(lHeight), byref(iBPP), byref(iFormat))

#s = saveImage(iccam.cam, filenm, INT(1), INT(90))
#ctypes.memset(d(),0,xdim*ydim)
#c = snapImage(iccam.cam, INT(10000))
d = getImagePtr(iccam.cam)
#print buf.ctypes.data
ctypes.memset(buf.ctypes.data,0,xdim*ydim)
dp = ctypes.cast(d,ctypes.c_void_p)
#ctypes.memmove(ctypes.cast(d,ctypes.c_void_p),buf.ctypes.data,xdim*ydim*ctypes.sizeof(ctypes.c_ubyte))
ctypes.memmove(buf.ctypes.data,dp,xdim*ydim*ctypes.sizeof(ctypes.c_ubyte))
npbuf = np.frombuffer(buf, dtype=np.uint8)
e = stopLive(iccam.cam)
f = releaseGrabber(ctypes.byref(INT(iccam.cam)))


'''


