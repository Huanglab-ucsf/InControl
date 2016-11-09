#!/usr/bin/python


from ctypes import *


class API:
    
    def __init__(self):
	# Load library:
	self.mcl = cdll.LoadLibrary("C:\\Program Files\\Mad City Labs\\NanoDrive\\Madlib")
	# Define the return types of some the functions
	self.mcl.MCL_GetCalibration.restype = c_double
	self.mcl.MCL_SingleReadN.restype = c_double
	# Get stage handle:
	self.handle = self.mcl.MCL_InitHandle()

    def getCalibration(self,axis):
        return self.mcl.MCL_GetCalibration(c_ulong(axis),self.handle)

    def singleReadN(self,axis):
        return self.mcl.MCL_SingleReadN(c_ulong(axis), self.handle)

    def singleWriteN(self,position,axis):
        self.mcl.MCL_SingleWriteN(c_double(position),c_ulong(axis),self.handle)

    def releaseHandle(self):
        self.mcl.MCL_ReleaseHandle(self.handle)
