#!/usr/bin/python


from ctypes import *
from ctypes import wintypes
from ctypes.wintypes import WORD, DWORD, BYTE, LONG, SHORT
import numpy as np
import sys
import Queue
import threading, multiprocessing
import time
import pywintypes, win32event

PCO_STRUCTREV = 102
PCO_BUFCNT = 16
PCO_MAXDELEXPTABLE = 16
PCO_RAMSEGCNT  = 4
PCO_MAXVERSIONHW = 10
PCO_MAXVERSIONFW = 10
NUM_MAX_SIGNALS = 20
PCO_SENSORDUMMY = 7
PCO_TIMINGDUMMY = 24
PCO_STORAGEDUMMY = 39
PCO_RECORDINGDUMMY = 33
PCO_CL_DEFAULT_BAUDRATE = 9600
PCO_CL_PIXELCLOCK_40MHZ = 40000000
PCO_CL_PIXELCLOCK_66MHZ = 66000000
PCO_CL_PIXELCLOCK_80MHZ = 80000000
PCO_CL_PIXELCLOCK_32MHZ = 32000000
PCO_CL_PIXELCLOCK_64MHZ = 64000000
PCO_CL_CCLINE_LINE1_TRIGGER          = 0x01
PCO_CL_CCLINE_LINE2_ACQUIRE          = 0x02
PCO_CL_CCLINE_LINE3_HANDSHAKE        = 0x04
PCO_CL_CCLINE_LINE4_TRANSMIT_ENABLE  = 0x08

class PCO_SC2_Hardware_DESC(Structure):
    _field_ = [("szName[16]", c_char*16),
               ("wBatchNo",     WORD),
               ("wRevision",    WORD),
               ("wVariant", WORD),
               ("ZZwDummy[20]", WORD)]
               
class PCO_SC2_Firmware_DESC(Structure):
    _field_ = [("szName[16]", c_char*16),
               ("bMinorRev",     BYTE),
               ("bMajorRev",    BYTE),
               ("wVariant", WORD),
               ("ZZwDummy[20]", WORD)]

class PCO_HW_Vers(Structure):
    _fields_ = [("BoardNum", WORD),
                ("Board[PCO_MAXVERSIONHW]", PCO_SC2_Hardware_DESC)]

class PCO_FW_Vers(Structure):
    _fields_ = [("DeviceNum", WORD),
                ("Device[PCO_MAXVERSIONFW]", PCO_SC2_Firmware_DESC)]
    

class PCO_CameraType(Structure):
    _fields_ = [("wSize",WORD),  #size of this structure 
                ("wCamType",WORD),  #  	
                ("wCamSubType",WORD),  #  
                ("ZZwAlignDummy1",WORD),  #  
                ("dwSerialNumber",DWORD),  #  
                ("dwHWVersion",DWORD),  #  
                ("dwFWVersion",DWORD),  # 
                ("wInterfaceType",WORD),  # 
                ("strHardwareVersion", PCO_HW_Vers),  #  
                ("strFirmwareVersion", PCO_FW_Vers),
                ("ZZwDummy[39]",        WORD)]  # 	

class PCO_General(Structure):
    _fields_ = [("wSize",                   WORD),  #size of this structure 
                ("ZZwAlignDummy1",          WORD),  #  	
                ("strCamType",              PCO_CameraType),  #  
                ("dwCamHealthWarnings",     DWORD),  #  
                ("dwCamHealthErrors",       DWORD),  #  
                ("dwCamHealthStatus",       DWORD),  #  
                ("sCCDTemperature",         SHORT),  # 
                ("sCamTemperature",         SHORT),  # 
                ("sPowerSupplyTemperature", SHORT),  #  
                ("ZZwDummy[37]",            WORD)]  #

class PCO_Description(Structure):
    _fields_ = [("wSize",   WORD),
                ("wSensorTypeDESC", WORD),
                ("wSensorSubTypeDESC", WORD),
                ("wMaxHorzResStdDESC", WORD),
                ("wMaxVertResStdDESC", WORD),
                ("wMaxHorzResExtDESC", WORD),
                ("wMaxVertResExtDESC", WORD),
                ("wDynResDESC", WORD),
                ("wMaxBinHorzDESC", WORD),
                ("wBinHorzSteppingDESC", WORD),
                ("wMaxBinVertDESC", WORD),
                ("wBinVertSteppingDESC", WORD),
                ("wRoiHorStepsDESC", WORD),
                ("wRoiVertStepsDESC", WORD),
                ("wNumADCsDESC", WORD),
                ("ZZwAlignDummy1", WORD),
                ("dwPixelRateDESC[4]", DWORD*4),
                ("ZZdwDummypr[20]", DWORD*20),
                ("wConvFactDESC[4]", WORD*4),
                ("ZZdwDummycv[20]", WORD*20),
                ("wIRDESC", WORD),
                ("ZZwAlignDummy2", WORD),
                ("dwMinDelayDESC", DWORD),
                ("dwMaxDelayDESC", DWORD),
                ("dwMinDelayStepDESC", DWORD),
                ("dwMinExposureDESC", DWORD),
                ("dwMaxExposureDESC", DWORD),
                ("dwMinExposureStepDESC", DWORD),
                ("dwMinDelayIRDESC", DWORD),
                ("dwMaxDelayIRDESC", DWORD),
                ("dwMinExposureIRDESC", DWORD),
                ("dwMaxExposureIRDESC", DWORD),
                ("wTimeTableDESC", WORD),
                ("wDoubleImageDESC", WORD),
                ("sMinCoolSetDESC", SHORT),
                ("sMaxCoolSetDESC", SHORT),
                ("sDefaultCoolSetDESC", SHORT),
                ("wPowerDownModeDESC", WORD),
                ("wOffsetRegulationDESC", WORD),
                ("wColorPatternDESC", WORD),
                ("wPatternTypeDESC", WORD),
                ("wDummy1", WORD),
                ("wDummy2", WORD),
                ("ZZwAlignDummy3", WORD),
                ("dwGeneralCapsDESC1", DWORD),
                ("dwGeneralCapsDESC2", DWORD),
                ("dwExtSyncFrequency[2]", DWORD*2),
                ("dwReservedDESC[4]", DWORD*4),
                ("ZZdwDummy[40]", DWORD*40)]

class PCO_Description2(Structure):
    _fields_ = [("wSize", WORD),
                ("ZZwAlignDummy1", WORD),
                ("dwMinPeriodicalTimeDESC2", DWORD),
                ("dwMaxPeriodicalTimeDESC2", DWORD),
                ("dwMinPeriodicalConditionDESC2", DWORD),
                ("dwMaxNumberOfExposuresDESC2", DWORD),
                ("lMinMonitorSignalOffsetDESC2", LONG),
                ("dwMaxMonitorSignalOffsetDESC2", DWORD),
                ("dwMinPeriodicalStepDESC2", DWORD),
                ("dwStartTimeDelayDESC2", DWORD),
                ("dwMinMonitorStepDESC2", DWORD),
                ("dwMinDelayModDESC2", DWORD),
                ("dwMaxDelayModDESC2", DWORD),
                ("dwMinDelayStepModDESC2", DWORD),
                ("dwMinExposureModDESC2", DWORD),
                ("dwMaxExposureModDESC2", DWORD),
                ("dwMinExposureStepModDESC2", DWORD),
                ("dwModulateCapsDESC2", DWORD),
                ("dwReserved[16]", DWORD*16),
                ("ZZdwDummy[41]", DWORD*41)]
                                

class PCO_Single_Signal_Desc(Structure):
    _fields_ = [("wSize", WORD),
                ("ZZwAlignDummy1", WORD),
                ("strSignalName[4][25]", c_char*4*25),
                ("wSignalDefinitions", WORD),
                ("wSignalTypes", WORD),
                ("wSignalPolarity", WORD),
                ("wSignalFilter", WORD),
                ("dwDummy[22]", DWORD*22)]

class PCO_Signal_Description(Structure):
    _fields_ = [("wSize", WORD),
                ("wNumOfSignals", WORD),
                ("strSingeSignalDesc[NUM_MAX_SIGNALS]", PCO_Single_Signal_Desc*NUM_MAX_SIGNALS),
                ("dwDummy[524]", DWORD)]


class PCO_Sensor(Structure):
    _fields_ = [("wSize", WORD),
                ("ZZwAlignDummy1", WORD),
                ("strDescription", PCO_Description),
                ("strDescription2", PCO_Description2),
                ("ZZdwDummy2[256]", DWORD*256),
                ("wSensorformat", WORD),
                ("wRoiX0", WORD),
                ("wRoiY0", WORD),
                ("wRoiX1", WORD),
                ("wRoiY1", WORD),
                ("wBinHorz", WORD),
                ("wBinVert", WORD),
                ("ZZwAlignDummy2", WORD),
                ("dwPixelRate", DWORD),
                ("wConvFact", WORD),
                ("wDoubleImage", WORD),
                ("wADCOperation", WORD),
                ("wIR", WORD),
                ("sCoolSet", SHORT),
                ("wOffsetRegulation", WORD),
                ("wNoiseFilterMode", WORD),
                ("wFastReadoutMode", WORD),
                ("wDSNUAdjustMode", WORD),
                ("wCDIMode", WORD),
                ("ZZwDummy[36]", WORD*36),
                ("strSignalDesc", PCO_Signal_Description),
                ("ZZdwDummy[PCO_SENSORDUMMY]", DWORD*PCO_SENSORDUMMY)]
                
                
class PCO_Signal(Structure):
    _fields_ = [("wSize", WORD),
                ("wSignalNum", WORD),
                ("wEnabled", WORD),
                ("wType", WORD),
                ("wPolarity", WORD),
                ("wFilterSetting", WORD),
                ("wSelected", WORD),
                ("ZZwReserved", WORD),
                ("ZZdwReserved[11]", DWORD*11)]


class PCO_ImageTiming(Structure):
    _fields_= [("wSize", WORD),
               ("wDummy", WORD),
               ("FrameTime_ns", DWORD),
               ("FrameTime_s", DWORD),
               ("ExposureTime_ns", DWORD),
               ("ExposureTime_s", DWORD),
               ("TriggerSystemDelay_ns", DWORD),
               ("TriggerSystemJitter_ns", DWORD),
               ("TriggerDelay_ns", DWORD),
               ("TriggerDelay_s", DWORD),
               ("ZZdwDummy[11]", DWORD*11)]

class PCO_Timing(Structure):
    _fields_= [("wSize", WORD),
               ("wTimeBaseDelay", WORD),
               ("wTimeBaseExposure", WORD),
               ("ZZwAlignDummy1", WORD),
               ("ZZdwDummy0[2]", DWORD*2),
               ("dwDelayTable[PCO_MAXDELEXPTABLE]", DWORD*PCO_MAXDELEXPTABLE),
               ("ZZdwDummy1[114]", DWORD*114),
               ("dwExposureTable[PCO_MAXDELEXPTABLE]", DWORD*PCO_MAXDELEXPTABLE),
               ("ZZdwDummy2[112]", DWORD*112),
               ("wTriggerMode", WORD),
               ("wForceTrigger", WORD),
               ("wCameraBusyStatus", WORD),
               ("wPowerDownMode", WORD),
               ("dwPowerDownTime", DWORD),
               ("wExpTrgSignal", WORD),
               ("wFPSExposureMode", WORD),
               ("dwFPSExposureTime", DWORD),
               ("wModulationMode", WORD),
               ("wCameraSynchMode", WORD),
               ("dwPeriodicalTime", DWORD),
               ("wTimeBasePeriodical", WORD),
               ("ZZwAlignDummy3", WORD),
               ("dwNumberOfExposures", DWORD),
               ("lMonitorOffset", LONG),
               ("strSignal[NUM_MAX_SIGNALS]", PCO_Signal*NUM_MAX_SIGNALS),
               ("wStatusFrameRate", WORD),
               ("wFrameRateMode", WORD),
               ("dwFrameRate", DWORD),
               ("dwFrameRateExposure", DWORD),
               ("wTimingControlMode", WORD),
               ("wFastTimingMode", WORD),
               ("ZZwDummy[PCO_TIMINGDUMMY]", WORD*PCO_TIMINGDUMMY)]

class PCO_Storage(Structure):
    _fields_ = [("wSize", WORD),
                ("ZZwAlignDummy1", WORD),
                ("dwRamSize", DWORD),
                ("wPageSize", WORD),
                ("ZZwAlignDummy4", WORD),
                ("dwRamSegSize[PCO_RAMSEGCNT]", DWORD*PCO_RAMSEGCNT),
                ("ZZdwDummyrs[20]", DWORD*20),
                ("wActSeg", WORD),
                ("ZZwDummy[PCO_STORAGEDUMMY]", WORD*PCO_STORAGEDUMMY)]

class PCO_Recording(Structure):
    _fields_ = [("wSize", WORD),
                ("wStorageMode", WORD), #0=recorder; 1=fifo
                ("wRecSubmode", WORD), #0=sequence; 1=ringbuffer
                ("wRecState", WORD), #0=off; 1=on
                ("wAcquMode", WORD), #0=internal auto; 1=external
                ("wAcquEnableStatus", WORD),
                ("ucDay", BYTE),
                ("ucMonth", BYTE),
                ("wYear", WORD),
                ("wHour", WORD),
                ("ucMin", BYTE),
                ("ucSec", BYTE),
                ("wTimeStampMode", WORD),
                ("wRecordStopEventMode", WORD),
                ("dwRecordStopDelayImages", DWORD),
                ("wMetaDataMode", WORD),
                ("wMetaDataSize", WORD),
                ("wMetaDataVersion", WORD),
                ("ZZwDummy[PCO_RECORDINGDUMMY]", WORD*PCO_RECORDINGDUMMY)]

class PCO_SC2_CL_TRANSFER_PARAMS(Structure):
    _fields_= [("baudrate", c_uint), #serial baudrate:9600, 19200, 38400
               ("ClockFrequency", c_uint), #Pixelclock in Hz: 40000000,66000000,80000000
               ("CCline", c_uint),
               ("DataFormat", c_uint),
               ("Transmit", c_uint)] #single or continuous transmitting images, 0-single, 1-continuous


class API:
    '''
    A ctypes based Python wrapper of the Software Development Kit for Cooke pco camera.

    '''

    def __init__(self):
        self.cooke_path = "C:\\Program Files\\Digital Camera Toolbox\\pco.sdk\\bin\\"
        self.cooke = windll.LoadLibrary(self.cooke_path+"SC2_Cam")

        self.hcam = wintypes.HANDLE()
        f_open = self.cooke.__getattr__('PCO_OpenCamera')
        err = f_open(byref(self.hcam), c_int(0))

        self.f_getgeneral = self.cooke.__getattr__('PCO_GetGeneral')
        self.f_clparams = self.cooke.__getattr__('PCO_GetTransferParameter')
        self.f_setclparams = self.cooke.__getattr__('PCO_SetTransferParameter')
        self.f_getstorage = self.cooke.__getattr__('PCO_GetStorageStruct')
        self.f_getrecording = self.cooke.__getattr__('PCO_GetRecordingStruct')
        self.f_setrecording = self.cooke.__getattr__('PCO_SetRecordingStruct')
        self.f_setstoragemode = self.cooke.__getattr__('PCO_SetStorageMode')
        self.f_getstoragemode = self.cooke.__getattr__('PCO_GetStorageMode')
        self.f_getrecordersubmode = self.cooke.__getattr__('PCO_GetRecorderSubmode')
        self.f_setrecordersubmode = self.cooke.__getattr__('PCO_SetRecorderSubmode')
        self.f_settimestampmode = self.cooke.__getattr__('PCO_SetTimestampMode')
        self.f_close = self.cooke.__getattr__('PCO_CloseCamera')
        self.f_getROI = self.cooke.__getattr__('PCO_GetROI')
        self.f_setROI = self.cooke.__getattr__('PCO_SetROI')
        self.f_gettimes = self.cooke.__getattr__('PCO_GetDelayExposureTime')
        self.f_settimes = self.cooke.__getattr__('PCO_SetDelayExposureTime')
        self.f_arm = self.cooke.__getattr__('PCO_ArmCamera')
        self.f_record = self.cooke.__getattr__('PCO_SetRecordingState')
        self.f_getrecord = self.cooke.__getattr__('PCO_GetRecordingState')
        self.f_allocate = self.cooke.__getattr__('PCO_AllocateBuffer')
        self.f_abe = self.cooke.__getattr__('PCO_AddBufferExtern')
        self.f_add = self.cooke.__getattr__('PCO_AddBufferEx')
        self.f_getImage = self.cooke.__getattr__('PCO_GetImageEx')
        self.f_bufstat = self.cooke.__getattr__('PCO_GetBufferStatus')
        self.f_free = self.cooke.__getattr__('PCO_FreeBuffer')
        self.f_getpending = self.cooke.__getattr__('PCO_GetPendingBuffer')
        self.f_rembuff = self.cooke.__getattr__('PCO_RemoveBuffer')
        self.f_camlink = self.cooke.__getattr__('PCO_CamLinkSetImageParameters')
        
        
        

    def getGeneral(self):
        params_gen = PCO_General()
        params_gen.wSize = sizeof(params_gen)
        params_gen.strCamType.wSize = sizeof(params_gen.strCamType)
        err = self.f_getgeneral(self.hcam, byref(params_gen))
        return params_gen

    def getCLTransferParams(self):
        params = PCO_SC2_CL_TRANSFER_PARAMS()
        iSize = sizeof(params)
        err = self.f_clparams(self.hcam, byref(params), c_int(iSize))
        return params

    def setCLTransferParams(self, baudrate, clockfreq, ccline, dataformat, transmit):
        params = PCO_SC2_CL_TRANSFER_PARAMS()
        params.baudrate = c_uint(baudrate)
        params.ClockFrequency = c_uint(clockfreq)
        params.CCline = c_uint(ccline)
        params.DataFormat = c_uint(dataformat)
        params.Transmit = c_uint(transmit)
        iSize = sizeof(params)
        return self.f_setclparams(self.hcam, byref(params), c_int(iSize))

    def getStorageStruct(self):
        params = PCO_Storage()
        params.wSize = WORD(sizeof(params))
        err = self.f_getstorage(self.hcam, byref(params))
        return params

    def getRecordingStruct(self):
        params = PCO_Recording()
        params.wSize = WORD(sizeof(params))
        err = self.f_getrecording(self.hcam, byref(params))
        return params

    def setRecordingStruct(self, storemode, recmode):
        ps = self.getRecordingStruct()
        ps.wStorageMode = WORD(storemode)
        ps.wRecSubmode = WORD(recmode)
        return self.f_setrecording(self.hcam, byref(ps))

    def getStorageMode(self):
        wMode = wintypes.WORD()
        err = self.f_getstoragemode(self.hcam, byref(wMode))
        return (err, wMode.value)

    def setStorageMode(self, mode):
        wMode = WORD(mode)
        err = self.f_setstoragemode(self.hcam, wMode)
        return err

    def getRecorderSubmode(self):
        wMode = wintypes.WORD()
        err = self.f_getrecordersubmode(self.hcam, byref(wMode))
        return (err, wMode.value)

    def setRecorderSubmode(self, mode):
        wMode = WORD(mode)
        err = self.f_setrecordersubmode(self.hcam, wMode)

    def setTimestampMode(self, mode):
        '''
        0x0000: no stamp
        0x0001: BCD stamp in first 14 pixel
        0x0002: BCD stamp in first 14 pixel and ASCII text
        '''
        wMode = WORD(mode)
        err = self.f_settimestampmode(self.hcam, wMode)
        return err

    def closeCamera(self):
        return self.f_close(self.hcam)

    def getROI(self):
        wRoiX0 = wintypes.WORD()
        wRoiY0 = wintypes.WORD()
        wRoiX1 = wintypes.WORD()
        wRoiY1 = wintypes.WORD()
        err = self.f_getROI(self.hcam,
                            byref(wRoiX0), byref(wRoiY0),
                            byref(wRoiX1), byref(wRoiY1))
        return (err, (wRoiX0.value, wRoiY0.value, wRoiX1.value, wRoiY1.value))

    def setROI(self, x0, y0, x1, y1):
        return self.f_setROI(self.hcam, wintypes.WORD(x0), wintypes.WORD(y0),
                             wintypes.WORD(x1), wintypes.WORD(y1))
        

    def getDelayExposureTime(self):
        dwDelay = wintypes.DWORD()
        dwExp = wintypes.DWORD()
        wDelayBase = WORD()
        wExpBase = WORD()
        err = self.f_gettimes(self.hcam,
                              byref(dwDelay), byref(dwExp),
                              byref(wDelayBase), byref(wExpBase))
        if wDelayBase.value == 0:
            delay_base = 1e-9
        elif wDelayBase.value == 1:
            delay_base = 1e-6
        elif wDelayBase.value == 2:
            delay_base = 1e-3
        else:
            delay_base = 0
        if wExpBase.value == 0:
            exp_base = 1e-9
        elif wExpBase.value == 1:
            exp_base = 1e-6
        elif wExpBase.value == 2:
            exp_base = 1e-3
        else:
            exp_base = 0
        return (err, (dwDelay.value*delay_base, dwExp.value*exp_base))

    def setDelayExposureTime(self, delay, exposure, delay_base, exp_base):
        return self.f_settimes(self.hcam, wintypes.DWORD(delay),
                               wintypes.DWORD(exposure),
                               wintypes.WORD(delay_base),
                               wintypes.WORD(exp_base))
        

    def armCamera(self):
        return self.f_arm(self.hcam)

    def setRecordingState(self, state):
        # state = 0x0001 to run; 0x0000 to stop #
        return self.f_record(self.hcam, wintypes.WORD(state))

    def getRecordingState(self):
        state = wintypes.WORD()
        err = self.f_getrecord(self.hcam, byref(state))
        return state.value

    def allocateBuffer(self, xres, yres, buffer_number, num_images=1):
        sBufNum = wintypes.SHORT(buffer_number)
        dwSize = wintypes.DWORD(2*xres*yres*num_images)
        wBuffer = np.zeros((xres*yres*num_images),dtype=np.uint16)
        hEvent1 = wintypes.HANDLE()
        hEvent2 = pywintypes.HANDLE()#
        err = self.f_allocate(self.hcam, byref(sBufNum), dwSize,
                              addressof(c_void_p(wBuffer.ctypes.data)),
                              byref(hEvent1))
        return (err, hEvent1, wBuffer)
        #return wBuffer

    def addBufferExtern(self, xres, yres, num_images,
                        imageFirst, imageLast):
        dwSize = wintypes.DWORD(2*xres*yres*num_images)
        wbuf = np.zeros((xres*yres*num_images),dtype=np.uint16)
        #buf = c_void_p(0)
        hEvent = wintypes.HANDLE(1)
        #hEvent2 = pywintypes.HANDLE()
        status = DWORD()
        err = self.f_abe(self.hcam, hEvent, WORD(4), DWORD(imageFirst), DWORD(imageLast),
                    DWORD(0), c_void_p(wbuf.ctypes.data), dwSize,
                    byref(status))
        return (err, wbuf)

    def addBufferExtern2(self, xres, yres, numImages, event):
        dwSize = wintypes.DWORD(2*xres*yres)
        buf = (c_ushort*xres*yres*numImages)()
        status = DWORD()
        for i in range(numImages-1):
            hEvent = wintypes.HANDLE(1+i)
            err = self.f_abe(self.hcam, hEvent, WORD(4), DWORD(0), DWORD(0),
                        DWORD(0), addressof(buf[i]), dwSize,
                        byref(status))
        err = self.f_abe(self.hcam, event, WORD(4), DWORD(0), DWORD(0),
                        DWORD(0), addressof(buf[numImages-1]), dwSize,
                        byref(status))
        return (err, buf, event)

    def waitThenAdd(self, xres, yres, numImages, buf, eventToWait, newEvent):
        win32event.WaitForSingleObject(eventToWait.value, 10000)
        dwSize = wintypes.DWORD(2*xres*yres)
        status = DWORD()
        for i in range(numImages-1):
            hEvent = wintypes.HANDLE(1+i)
            err = self.f_abe(self.hcam, hEvent, WORD(4), DWORD(0), DWORD(0),
                        DWORD(0), addressof(buf[i]), dwSize,
                        byref(status))
        err = self.f_abe(self.hcam, newEvent, WORD(4), DWORD(0), DWORD(0),
                        DWORD(0), addressof(buf[numImages-1]), dwSize,
                        byref(status))

    def reAddBuffer(self, xres, yres, buf, numImages, event):
        dwSize = wintypes.DWORD(2*xres*yres)
        status = DWORD()
        for i in range(numImages-1):
            hEvent = wintypes.HANDLE(1+i)
            err = self.f_abe(self.hcam, hEvent, WORD(4), DWORD(0), DWORD(0),
                        DWORD(0), addressof(buf[i]), dwSize,
                        byref(status))
        err = self.f_abe(self.hcam, event, WORD(4), DWORD(0), DWORD(0),
                        DWORD(0), addressof(buf[numImages-1]), dwSize,
                        byref(status))
        

    def largeBufferFill(self, xres, yres, numImages, events=None):
        numSegments = int(round(numImages/15.0))
        dwSize = wintypes.DWORD(2*xres*yres)
        status = DWORD()
        buf = (c_ushort*xres*yres*15*numSegments)()
        if events is None:
            event1 = wintypes.HANDLE(5001)
            event2 = wintypes.HANDLE(5002)
            events = [event1, event2]

        ##Add first two segments:
        self.reAddBuffer(xres,yres,buf[0],15,events[0])
        self.reAddBuffer(xres,yres,buf[1],15,events[1])

        for i in range(2,numSegments):
            win32event.WaitForSingleObject(events[i%2].value, 1000)
            self.reAddBuffer(xres,yres,buf[i],15,events[i%2])

        return buf
        
        
        

    def addBuffer(self, imageFirst, imageLast, buffer_number, xres, yres, bpp):
        dwImageFirst = wintypes.DWORD(imageFirst)
        dwImageLast = wintypes.DWORD(imageLast)
        sBuf = wintypes.SHORT(buffer_number)
        wXRes = wintypes.WORD(xres)
        wYRes = wintypes.WORD(yres)
        wBPP = wintypes.WORD(bpp)
        return self.f_add(self.hcam, dwImageFirst, dwImageLast,
                          sBuf, wXRes, wYRes, wBPP)

    '''
    def getBuffer(self, buffer_number, xres, yres):
        f_getBuffer = self.cooke.__getattr__('PCO_GetBuffer')
        sBuf = wintypes.SHORT(buffer_number)
        wBuffer = np.
    '''

    def getImage(self, segment, imageFirst, imageLast, buffer_number,
                 xres, yres, bpp):
        wseg = wintypes.WORD(segment)
        dwFirst = wintypes.DWORD(imageFirst)
        dwLast = wintypes.DWORD(imageLast)
        sBuf = wintypes.SHORT(buffer_number)
        wXRes = wintypes.WORD(xres)
        wYRes = wintypes.WORD(yres)
        wBPP = wintypes.WORD(bpp)
        return self.f_getImage(self.hcam, wseg, dwFirst, dwLast, sBuf,
                               wXRes, wYRes, wBPP)

    def getBufferStatus(self, bufnum):
        sBufNr = SHORT(bufnum)
        dwStatusDll = DWORD()
        dwStatusDrv = DWORD()
        err = self.f_bufstat(self.hcam, sBufNr, byref(dwStatusDll),
                             byref(dwStatusDrv))
        return dwStatusDll.value, dwStatusDrv.value

    def freeBuffer(self, buffer_number):
        return self.f_free(self.hcam, wintypes.SHORT(buffer_number))

    def getPendingBuffer(self):
        icount = wintypes.INT()
        err = self.f_getpending(self.hcam, byref(icount))
        return (err, icount.value)

    def removeBuffer(self):
        return self.f_rembuff(self.hcam)

    def camlinkSetParams(self, xres, yres):
        wXRes = wintypes.WORD(xres)
        wYRes = wintypes.WORD(yres)
        return self.f_camlink(self.hcam, wXRes, wYRes)

queue = Queue.PriorityQueue()
buffers = [0,1]

class ThreadAPI(threading.Thread):
    def __init__(self, queue, cam_api):
        threading.Thread.__init__(self)
        self.queue = queue
        self.cam_api = cam_api
        err, (x0,y0,x1,y1) = self.cam_api.getROI()
        self.xres = x1-x0+1
        self.yres = y1-y0+1

    def run(self):
        while True:
            bufnum = self.queue.get()

            b = self.cam_api.allocateBuffer(self.xres, self.yres, bufnum)
            self.cam_api.getImage(1,0,0,bufnum,self.xres,self.yres,14)
            np.save('im'+str(bufnum),b[1].reshape(self.yres,self.xres))

            self.queue.task_done()
            
'''
if __name__ == '__main__':
    cam_api = API()
    err, (x0,y0,x1,y1) = cam_api.getROI()
    xres = x1-x0+1
    yres = y1-y0+1
    cam_api.camlinkSetParams(xres,yres)
    for i in range(8):
        cam_api.allocateBuffer(xres,yres,-1)
    cam_api.armCamera()
    cam_api.setRecordingState(0x0001)
    time.sleep(0.1)

    for i in range(8):
        cam_api.addBuffer(0,0,i,xres,yres,14)
        t = ThreadAPI(queue, cam_api)
        t.setDaemon(True)
        t.start()

    for buf in buffers:
        queue.put(buf)

    queue.join()

    cam_api.setRecordingState(0x0000)
    for i in range(8):
        cam_api.freeBuffer(i)
    cam_api.closeCamera()
'''



if __name__ == '__main__':
    cam_api = API()
    err, (x0,y0,x1,y1) = cam_api.getROI()
    xres = x1-x0+1
    yres = y1-y0+1
    
    #err = cam_api.setCLTransferParams(9600, PCO_CL_PIXELCLOCK_40MHZ, 0x08, 0x05, 1)
    cam_api.camlinkSetParams(xres,yres)
    pstore = cam_api.getStorageStruct()
    
    cam_api.setRecordingStruct(0,0)

    prec = cam_api.getRecordingStruct()

    pgen = cam_api.getGeneral()

    ''' i don't think storage mode is alterable with pco.edge
    err = cam_api.setStorageMode(1)
    print err
    time.sleep(0.5)
    err,mode = cam_api.getStorageMode()
    print "Storage mode: ", mode
    '''
    err = cam_api.setRecorderSubmode(1)
    print err
    time.sleep(0.2)
    err,mode = cam_api.getRecorderSubmode()
    
    print "Recorder submode: ", mode

    func = pythonapi.PyBuffer_FromMemory
    func.restype = py_object
    

    bt = []

    for i in range(0,2):
        bt.append(cam_api.allocateBuffer(xres,yres,-1,num_images=1))
    #b = cam_api.allocateBuffer(xres,yres,-1,num_images=1)
    print "Buffers allocated..."
    cam_api.armCamera()
    print "Camera armed..."
    #b = cam_api.allocateBuffer(xres,yres,0,num_images=1)
    for k in range(0,1):
        for i in range(0,2):
            cam_api.addBuffer(0,0,i,xres,yres,16)
        #cam_api.addBuffer(i+1,i+1,i,xres,yres,14)
    #exBuf = np.zeros((20,xres*yres),dtype=np.uint16)
    #for i in range(0,20):
        #err,exBuf[i] = cam_api.addBufferExtern(xres,yres,1,0,0)
        #print "External buffer error: ", err
    #ev1 = wintypes.HANDLE(1001)
    #err,exBuf1,ev1a = cam_api.addBufferExtern2(xres,yres,15,ev1)
    #ev2 = wintypes.HANDLE(1002)
    #err,exBuf2,ev2a = cam_api.addBufferExtern2(xres,yres,15,ev2)
    print "External buffer error: ", err
    #stat1,stat2 = cam_api.getBufferStatus(0)

    def waitAndAdd(bufNum1,bufNum2):
        print "Starting..."
        ims = []
        win32event.WaitForSingleObject(bt[bufNum2-1][1].value, 100000)
        for i in range(bufNum1, bufNum2):
            ims.append(bt[i][2])
            cam_api.addBuffer(0,0,i,xres,yres,2)
            print "More added...", i
        np.save('test'+str(bufNum1), ims)
        return
        
    print "Buffers pending: ", cam_api.getPendingBuffer()[1]

    '''
    jobs = []
    for i in [(0,8), (8,16)]:
        p = multiprocessing.Process(target=waitAndAdd, args=(i[0],i[1],))
        jobs.append(p)
        p.start()
        p.join()
        #p.run()

    for p in jobs:
        p.run()
    '''
    
    cam_api.setRecordingState(0x0001)

    time.sleep(5)

    
    #print "Recording on..."

    '''
    while len(bt)<20:
        pend = cam_api.getPendingBuffer()[1]
        print pend
        if pend<8:
            len_bt = len(bt)
            bt_old = bt[0:len_bt-pend]
            bt.append(bt_old)
            for i in range(0,len_bt-pend):
                if i<16:
                    #bt.append(cam_api.allocateBuffer(xres,yres,i,num_images=1))
                    cam_api.addBuffer(0,0,i,xres,yres,14)
    '''
    #goneYet = False
    #print "event1 to use: ", bt[0][1]
    #bufs = cam_api.largeBufferFill(xres,yres,10000,events=[bt[0][1], bt[1][1]])
    #print "Before Wait(0). Buffers pending: ", cam_api.getPendingBuffer()[1]
    #win32event.WaitForSingleObject(ev1.value, 10000)
    #err,exBuf3,ev1b = cam_api.addBufferExtern2(xres,yres,15,ev1)
    #win32event.WaitForSingleObject(ev2.value, 10000)
    #err,exBuf4,ev2b = cam_api.addBufferExtern2(xres,yres,15,ev2)
    #print "After Wait(0). Buffers pending: ", cam_api.getPendingBuffer()[1]
    """
    while cam_api.getPendingBuffer()[1]>8:
        if cam_api.getPendingBuffer()[1]==9 and not goneYet:
            #bt_old = np.array(bt[:7]).copy()
            #np.save(np.array(bt_old),'test.npy')
            goneYet = True
            for i in range(0,7):
                cam_api.addBuffer(0,0,i,xres,yres,14)
    
    """
    '''
    for i in range(10):
        print "Buffers pending: ", cam_api.getPendingBuffer()[1]
        time.sleep(0.01)

    print "Before Wait(-1). Buffers pending: ", cam_api.getPendingBuffer()[1]
    #win32event.WaitForSingleObject(bt[-1][1].value, 10000000)
    print "After Wait(-1). Buffers pending: ", cam_api.getPendingBuffer()[1]
    cam_api.setRecordingState(0x0000)

    print "Recording off..."
    stat1b,stat2b = cam_api.getBufferStatus(0)

    #exBuf2 = np.frombuffer(func(exBuf, 2*bt[0][2].shape[0]),dtype=np.uint16)
    

    for i in range(0,30):
        cam_api.freeBuffer(i)
    cam_api.closeCamera()
    '''
    '''
    b1 = cam_api.allocateBuffer(xres,yres,-1)
    b2 = cam_api.allocateBuffer(xres,yres,-1)
    cam_api.armCamera()
    #b1 = cam_api.allocateBuffer(xres,yres,0)
    #b2 = cam_api.allocateBuffer(xres,yres,1)
    cam_api.setRecordingState(0x0001)
    cam_api.addBuffer(0,0,0,xres,yres,14)
    cam_api.addBuffer(0,0,1,xres,yres,14)
    cam_api.getImage(1,0,0,0,xres,yres,14)
    cam_api.getImage(1,0,0,1,xres,yres,14)
    cam_api.setRecordingState(0x0000)
    '''
    cam_api.freeBuffer(0)
    cam_api.freeBuffer(1)
    cam_api.closeCamera()
    

