#!/usr/bin/python

# API for thorlabs wave front sensor.


import sys
import time
import ctypes as ct
wfs = 0

def loadWFSDLL():
    global wfs
    if (wfs ==0):
        wfs = ct.windll.LoadLibrary("D:\Dan/Programs/InControl/thorlabs/WFS/WFS_64.dll")
        
instantiated = 0

class API():
    def __init__(self):
        count = ct.c_int32()
        list_index = ct.c_int32()

        instr_name = ct.create_string_buffer(b"",20)
        instr_serial = ct.create_string_buffer(b"",20)




        self.device_ID = ct.c_int32()
        self.in_use = ct.c_int32()
        self.instr_handle = ct.c_ulong()
        self.ID_query = ct.c_bool()
        self.reset_device = ct.c_bool()
        self.resource_name = ct.create_string_buffer(b"", 30)

        loadWFSDLL()
        global instantiated
        assert instantiated == 0, "Initialization."
        instantiated = 1
        wfs.WFS_GetInstrumentListLen(None, ct.byref(count))
        print("Wavefront Sensor connected:", str(count.value))
        wfs.WFS_GetInstrumentListInfo(None, list_index,ct.byref(self.device_ID), ct.byref(self.in_use), instr_name,instr_serial, self.resource_name)
        print(self.resource_name.value)
        wfs.WFS_init(self.resource_name,self.ID_query,self.reset_device,ct.byref(self.instr_handle))
        print(self.instr_handle.value) 

    def device_config(self):
        self.MX, self.MY = 768, 768 
        self.pupil_diam = 4.5
        self.error_message = ct.create_string_buffer(b"", 512)
        self.error_code = ct.c_int32()
        pix_format = ct.c_int32()
        pix_format.value = 0

        dev_status = wfs.WFS_ConfigureCam(self.instr_handle)
        pass


    def wavefront_measure(self,n_measure =1):
        pass


    def shutDown(self):
        wfs.WFS_close(self.instr_handle)


def main():
    wfs_API = API()
    wfs_API.shutDown()


if __name__ == "__main__":
    main()
