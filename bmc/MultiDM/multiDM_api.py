'''
Multi-DM api written by Dan. Last update : 11/13/2017
'''
from ctypes import *
import time
multi_dm = 0

bmc_dllpath = 'C:\Program Files\Boston Micromachines\Usb\CIUsbLib'
def loadMultiDM_DLL():
    global multi_dm
    if(multi_dm==0):
        multi_dm = windll.LoadLibrary(bmc_dllpath)


class API():
    def __init__(self):
        self.wait = 0
        loadMultiDM_DLL()

        self.good = -1 # current status
        multi_dm.CIUsb_GetAvailableDevices()
