#!/usr/bin/python


from ctypes import *

drv_acquiring = 20072
drv_idle = 20073
drv_no_new_data = 20024
drv_success = 20002
drv_tempcycle = 20074
drv_temp_not_stabilized = 20035
drv_temp_off = 20034
drv_temp_stabilized = 20036
drv_temp_not_reached = 20037


class API(object):
    '''
    A ctypes based Python wrapper of the Software Development Kit for Andor cameras.

    The functions are a direct translation of the SDK functions. Good documentation is
    provided by Andor.
    '''

    def __init__(self):
        self.andor_path = "C:\\Program Files\\Andor SOLIS\\Drivers\\"
        self.andor = oledll.LoadLibrary(self.andor_path+"ATMCD32D")

    def abortAcquisition(self):
        return self.andor.AbortAcquisition()

    def abortIfAcquiring(self):
        findStateStatus,state = self.getStatus()
        if state==drv_acquiring:
            status = self.abortAcquisition

    def coolerOff(self):
        return self.andor.CoolerOFF()

    def coolerOn(self):
        return self.andor.CoolerON()

    def getAcquisitionTimings(self):
        exposure = c_float()
        accumulate = c_float()
        kinetic_time = c_float()
        status = self.andor.GetAcquisitionTimings(byref(exposure),
                                                  byref(accumulate),
                                                  byref(kinetic_time))
        return (status,(exposure.value,accumulate.value,kinetic_time.value))

    def getDetector(self):
        x_pixels = c_long()
        y_pixels = c_long()
        status = self.andor.GetDetector(byref(x_pixels),byref(y_pixels))
        return (status,(x_pixels.value,y_pixels.value))

    def getEMCCDGain(self):
        gain = c_int()
        status = self.andor.GetEMCCDGain(byref(gain))
        return (status,gain)

    def getEMGainRange(self):
        low = c_int()
        high = c_int()
        status = self.andor.GetEMGainRange(byref(low),byref(high))
        return (status,(low.value,high.value))

    def getHSSpeed(self,channel,typ,index):
        channel = c_int(channel)
        typ = c_int(typ)
        index = c_int(index)
        speed = c_float()
        status = self.andor.GetHSSpeed(channel,typ,index,byref(speed))
        return (status,speed.value)

    def getMostRecentImage16(self,nPixels):
        buff = create_string_buffer(2 * nPixels)
        status = self.andor.GetMostRecentImage16(buff,c_ulong(nPixels))
        return (status,buff)

    def getNumberADChannels(self):
        channels = c_int()
        status = self.andor.GetNumberADChannels(byref(channels))
        return status,channels.value

    def getNumberAvailableImages(self):
        first = c_long()
        last = c_long()
        status = self.andor.GetNumberAvailableImages(byref(first),byref(last))
        return (status,(first.value,last.value))

    def getNumberHSSpeeds(self,channel,typ):
        channel = c_int(channel)
        typ = c_int(typ)
        speeds = c_int()
        status = self.andor.GetNumberHSSpeeds(channel,typ,byref(speeds))
        return (status,speeds.value)

    def getNumberPreAmpGains(self):
        noGains = c_int()
        status = self.andor.GetNumberPreAmpGains(byref(noGains))
        return (status,noGains.value)

    def getNumberVSSpeeds(self):
        speeds = c_int()
        status = self.andor.GetNumberVSSpeeds(byref(speeds))
        return (status,speeds.value)

    def getOldestImage16(self,nPixels):
        buff = create_string_buffer(2 * nPixels)
        status = self.andor.GetOldestImage16(buff,c_ulong(nPixels))
        return (status,buff)

    def getImages16(self, nPixels):
        frames = []
        first = c_long(0)
        last = c_long(0)
        status = self.andor.GetNumberNewImages(byref(first), byref(last))
        if status == drv_success:
            diff = last.value - first.value + 1
            buffer_size = nPixels * diff
            buffer = create_string_buffer(2*buffer_size)
            valid_first = c_long(0)
            valid_last = c_long(0)
            status == self.andor.GetImages16(first,last,buffer,c_ulong(buffer_size),
                                             byref(valid_first), byref(valid_last))
            if (first.value != valid_first.value) or (last.value != valid_last.value):
                print "getImages16 first or last value problem"
            if status==drv_success:
                for i in range(diff):
                    frames.append(buffer[2*i*nPixels:2*(i+1)*nPixels])
                return [frames, "acquiring"]
            elif status==drv_no_new_data:
                findStateStatus,state = self.getStatus()
                if state==drv_idle:
                    return [frames, "idle"]
                else:
                    return [frames, "acquiring"]
            else:
                print "getImages16 failed... " + str(status)

        elif status==drv_no_new_data:
            findStateStatus,state = self.getStatus()
            if state==drv_idle:
                return [frames, "idle"]
            else:
                return [frames, "acquiring"]

        else:
            print "getImages16 failed... " + str(status)

    def getPreAmpGain(self,index):
        index = c_int(index)
        gain = c_float()
        status = self.andor.GetPreAmpGain(index,byref(gain))
        return (status,gain.value)

    def getSizeOfCircularBuffer(self):
        size = c_long(0)
        status = self.andor.GetSizeOfCircularBuffer(byref(size))
        return (status,size.value)

    def getStatus(self):
        i_state = c_int()
        status = self.andor.GetStatus(byref(i_state))
        return (status,i_state.value)

    def getTemperature(self):
        temperature = c_int()
        status = self.andor.GetTemperature(byref(temperature))
        return (status,temperature.value)

    def getTemperatureRange(self):
        low = c_int()
        high = c_int()
        status = self.andor.GetTemperatureRange(byref(low),byref(high))
        return (status,(low.value,high.value))

    def getVSSpeed(self,index):
        index = c_int(index)
        speed = c_float()
        status = self.andor.GetVSSpeed(index,byref(speed))
        return (status,speed.value)

    def initialize(self):
        return self.andor.Initialize(self.andor_path + "Detector.ini")

    def setAccumulationCycleTime(self,time):
        time = c_float(time)
        return self.andor.SetAccumulationCycleTime(time)

    def setAcquisitionMode(self,mode):
        mode = c_int(mode)
        return self.andor.SetAcquisitionMode(mode)

    def setNumberAccumulations(self,numAccs):
        num = c_int(num)
        return self.andor.SetNumberAccumulations(num)

    def setADChannel(self,channel):
        channel = c_int(channel)
        return self.andor.SetADChannel(channel)

    def setBaselineClamp(self,state):
        state = c_int(state)
        return self.andor.SetBaselineClamp(state)

    def setEMCCDGain(self,gain):
        gain = c_int(gain)
        return self.andor.SetEMCCDGain(gain)

    def setEMGainMode(self,mode):
        mode = c_int(mode)
        return self.andor.SetEMGainMode(mode)

    def setExposureTime(self,time):
        time = c_float(time)
        return self.andor.SetExposureTime(time)

    def setFrameTransferMode(self,mode):
        mode = c_int(mode)
        return self.andor.SetFrameTransferMode(mode)

    def setHSSpeed(self,typ,index):
        typ = c_int(typ)
        index = c_int(index)
        return self.andor.SetHSSpeed(typ,index)

    def setImage(self,hbin,vbin,hstart,hend,vstart,vend):
        hbin = c_int(hbin)
        vbin = c_int(vbin)
        hstart = c_int(hstart)
        hend = c_int(hend)
        vstart = c_int(vstart)
        vend = c_int(vend)
        return self.andor.SetImage(hbin,vbin,hstart,hend,vstart,vend)

    def setKineticCycleTime(self,time):
        time = c_float(time)
        return self.andor.SetKineticCycleTime(time)

    def setNumberKinetics(self, numFrames):
        num = c_int(numFrames)
        return self.andor.SetNumberKinetics(num)

    def setPreAmpGain(self,index):
        index = c_int(index)
        return self.andor.SetPreAmpGain(index)

    def setReadMode(self,mode):
        mode = c_int(mode)
        return self.andor.SetReadMode(mode)

    def setFanMode(self,mode):
        '''
        0=full, 1=low, 2=off
        '''
        return self.andor.SetFanMode(c_int(mode))

    def setShutter(self,typ,mode,closingtime,openingtime):
        return self.andor.SetShutter(typ,mode,closingtime,openingtime)

    def setTemperature(self,temperature):
        i_temp = c_int(temperature)
        return self.andor.SetTemperature(i_temp)

    def setTriggerMode(self,mode):
        mode = c_int(mode)
        return self.andor.SetTriggerMode(mode)

    def setVSAmplitude(self,state):
        state = c_int(state)
        return self.andor.SetVSAmplitude(state)

    def setVSSpeed(self,index):
        index = c_int(index)
        return self.andor.SetVSSpeed(index)

    def shutDown(self):
        return self.andor.ShutDown()

    def startAcquisition(self):
        return self.andor.StartAcquisition()


