#!/usr/bin/python


import inLib
from PyQt4.QtGui import QImage
import numpy as np
import os, time
    

err_codes = {20072 : 'acquiring',
             20073 : 'idle',
             20024 : 'no_new_data',
             20002 : 'success',
             20074 : 'tempcycle',
             20035 : 'temp_not_stabilized',
             20034 : 'temp_off',
             20036 : 'temp_stabilized',
             20037 : 'temp_not_reached',
             20010 : 'pagelock',
             20075 : 'not_initialized'} 

drv_acquiring = 20072
drv_idle = 20073
drv_no_new_data = 20024
drv_success = 20002
drv_tempcycle = 20074
drv_temp_not_stabilized = 20035
drv_temp_off = 20034
drv_temp_stabilized = 20036
drv_temp_not_reached = 20037
drv_error_pagelock = 20010


class Control(inLib.Device):
    '''
    The device control of an Andor EMCCD camera.
    '''

    def __init__(self, settings):
        inLib.Device.__init__(self, 'andor.camera_api', settings)

        self._initSettings = settings.copy()
       
        # Initialize:
        status = self._api.initialize()

        self._props = {}

        # Size of camera chip:
        status, dimensions = self._api.getDetector()
        self._props['dimensions'] = dimensions
        
        # Number of vs speeds:
        status,n_vs_speeds = self._api.getNumberVSSpeeds()
        self._props['n_vs_speeds'] = n_vs_speeds

        # VS speeds:
        vs_speeds = range(n_vs_speeds)
        for i in range(n_vs_speeds):
            status,vs_speed = self._api.getVSSpeed(i)
            vs_speeds[i] = vs_speed
        self._props['vs_speeds'] = vs_speeds

        # Number of AD channels:
        status,n_ad_channels = self._api.getNumberADChannels()
        self._props['n_ad_channels'] = n_ad_channels

        # Number of HS speeds per AD channel:
        n_hs_speeds = range(n_ad_channels)
        for i in range(n_ad_channels):
            status,n_hs_speeds[i] = self._api.getNumberHSSpeeds(i,0)
        self._props['n_hs_speeds'] = n_hs_speeds

        # HS speeds:
        hs_speeds = range(n_ad_channels)
        for i in range(n_ad_channels):
            hs_speeds[i] = range(n_hs_speeds[i])
            for j in range(n_hs_speeds[i]):
                status,hs_speed = self._api.getHSSpeed(i,0,j)
                hs_speeds[i][j] = hs_speed
        self._props['hs_speeds'] = hs_speeds

        # Temperature range:
        status,temp_range = self._api.getTemperatureRange()
        self._props['temp_range'] = temp_range

        # Number of preamp gains:
        status,n_preamp_gains = self._api.getNumberPreAmpGains()
        self._props['n_preamp_gains'] = n_preamp_gains

        # Preamp gains:
        preamp_gains = range(n_preamp_gains)
        for i in range(n_preamp_gains):
            status,preamp_gains[i] = self._api.getPreAmpGain(i)
        self._props['preamp_gains'] = preamp_gains

        # EM gain range:
        status, em_gain_range = self._api.getEMGainRange()
        self._props['em_gain_range'] = em_gain_range


        # Setting up the camera acquisition:

        self._api.coolerOn()

        self.loadSettings(settings)

        self._getAcquisitionTimings()

        self._api.startAcquisition()
        print 'Camera initialized.'

    def getSettings(self):
        return self._settings

    def getProps(self):
        return self._props

    def loadSettings(self, settings):
        if type(settings) is str:
            if os.path.exists(settings):
                settingsDict = inLib.load_settings(settings)
                settings = settingsDict
        
        if type(settings) is dict:
            self._api.setTemperature(settings['temperature'])
            self._api.setExposureTime(settings['exposure_time'])
            self._setADChannel(settings['ad_channel'])
            self._setROIAndBinning(settings['roi'], settings['binning'])
            self._setHSSpeed(settings['ad_channel'], settings['hs_speed'])
            self._api.setVSAmplitude(settings['vs_amplitude'])
            self._setEMCCDGain(settings['em_gain'])
            self._setVSSpeed(settings['vs_speed'])
            self._setPreAmpGain(settings['preamp_gain'])
            
            self._api.setAcquisitionMode(settings['acquisition_mode'])
            self._api.setReadMode(settings['read_mode'])
            self._api.setTriggerMode(settings['trigger_mode'])
            self._api.setKineticCycleTime(settings['kinetic_time'])
            self._api.setEMGainMode(settings['em_gain_mode'])
            self._api.setBaselineClamp(settings['baseline_clamp'])
            self._api.setFrameTransferMode(settings['frame_transfer_mode'])
            

    def _getAcquisitionTimings(self):
        status, timings = self._api.getAcquisitionTimings()
        self._settings['exposure_time'] = timings[0]
        self._settings['frame_rate'] = 1.0/timings[1]
        self._settings['kinetic_value'] = timings[2]

    def setExposureTime(self, exp_time):
        self._api.setExposureTime(exp_time)
        self._settings['exposure_time'] = exp_time


    def _setADChannel(self, channel):
        if not channel in range(self._props['n_ad_channels']):
            print 'camera: Warning! Invalid AD channel. Setting AD channel to 0.'
            channel = 0
        self._api.setADChannel(channel)
        self._ad_channel = channel


    def _setEMCCDGain(self, gain):
        if gain == 'min':
            gain = self._props['em_gain_range'][0]
        elif gain == 'max':
            gain = self._props['em_gain_range'][1]
        print 'EMCCD: Setting gain to', gain
        self._api.setEMCCDGain(gain)
        self._settings['em_gain'] = gain


    def _setROIAndBinning(self, ROI, binning):
        hbin, vbin = binning
        hstart, hend, vstart, vend = ROI
        status = self._api.setImage(hbin,vbin,hstart,hend,vstart,vend)
        x_pixels = (hend - hstart + 1) / hbin
        y_pixels = (vend - vstart + 1) / vbin
        print 'camera: (x_pixels, y_pixels) =', x_pixels, y_pixels
        self._settings['dimensions'] = (x_pixels, y_pixels)
        self._settings['n_pixels'] = x_pixels*y_pixels
        self._settings['x_start'] = hstart
        self._settings['y_start'] = vstart
        self._settings['roi'] = (hstart, hstart+x_pixels-1,
                                 vstart, vstart+y_pixels-1)


    def _setTemperature(self, temperature):
        if temperature < self._props['temp_range'][0]:
            temperature = self._props['temp_range'][0]
        elif temperature > self._props['temp_range'][1]:
            temperature = self._props['temp_range'][1]
        self._api.setTemperature(temperature)
        return temperature

    def getTemperature(self):
        status, temp = self._api.getTemperature()
        if status==drv_temp_stabilized:
            return [temp, "stable"]
        elif status==drv_temp_off:
            return [temp, "temp_off"]
        elif (status==drv_temp_not_stabilized) or (status==drv_temp_not_reached):
            return [temp, "unstable"]
        else:
            return [0, "error getting temperature"]

    def setFanMode(self,mode):
        if mode=='full' or mode==0:
            self._api.setFanMode(0)
        elif mode=='low' or mode==1:
            self._api.setFanMode(1)
        elif mode=='off' or mode==2:
            self._api.setFanMode(2)

    def _setHSSpeed(self,ad_channel,hs_speed):
        hs_speeds = self._props['hs_speeds'][ad_channel]
        index = 0
        best = abs(hs_speed - hs_speeds[index])
        for i in range(len(hs_speeds)):
            cur = abs(hs_speed - hs_speeds[i])
            if cur < best:
                best = cur
                index = i
        status = self._api.setHSSpeed(0,index)
        self._settings['hs_speed'] = hs_speeds[index]


    def _setVSSpeed(self,vs_speed):
        speeds = self._props["vs_speeds"]
        index = 0
        best = abs(vs_speed - speeds[index])
        for i in range(len(speeds)):
            cur = abs(vs_speed - speeds[i])
            if cur < best:
                best = cur
                index = i
        self._settings['vs_speed'] = speeds[index]
        status = self._api.setVSSpeed(index)


    def _setPreAmpGain(self,preamp_gain):
        gains = self._props["preamp_gains"]
        index = 0
        best = abs(preamp_gain - gains[index])
        for i in range(len(gains)):
            cur = abs(preamp_gain - gains[i])
            if cur < best:
                best = cur
                index = i
        self._settings['preamp_gain'] = gains[index]
        status = self._api.setPreAmpGain(index)

    def getSizeOfCircBuffer(self):
        status, size = self._api.getSizeOfCircularBuffer()
        return size

    def getNumAvailableImages(self):
        status, (first, last) = self._api.getNumberAvailableImages()
        return first,last

    def getROI(self):
        '''
        :Returns:
            *ROI*: array
                Four element array of ROI
        '''
        return self._settings['roi']

    def getDimensions(self):
        '''

        :Returns:
            *dimensions*: tuple
                The dimensions of the current ROI on the camera chip.
        '''
        return self._settings['dimensions']


    def getEMCCDGain(self):
        '''

        :Returns:
            *em_gain*: int
                The current EMCCD gain.
        '''
        return self._settings['em_gain']


    def getEMGainRange(self):
        '''

        :Returns:
            *em_gain_range*: tuple
                The minimumum and maximum EM gain.
        '''
        return self._props['em_gain_range']


    def getNPixels(self):
        '''

        :Returns:
            *n_pixels*: int
                The number of pixels in the current ROI on the camera chip.
        '''
        return self._settings['n_pixels']


    def getFrameRate(self):
        '''

        :Returns:
            *frame_rate*: float
                The frame rate in Hz.
        '''
        return self._settings['frame_rate']

    def getExposureTime(self, use_kinetic=False):
        if use_kinetic:
            return self._settings['kinetic_value']
        return self._settings['exposure_time']

    def getKineticTime(self):
        return self._settings['kinetic_value']

    def getMostRecentImage16(self):
        '''
        
        :Returns:
            *image*: str
                The most recent image as a 16 bit binary string.
        '''
        status,image = self._api.getMostRecentImage16(self._settings['n_pixels'])
        return image

    def getImages16(self):
        [frames, status] = self._api.getImages16(self._settings['n_pixels'])
        return [frames, status]


    def getMostRecentImageNumpy(self):
        '''

        :Returns:
            *image*: numpy.array
                The most recent image as a uint16 Numpy array.
        '''
        buff = self.getMostRecentImage16()
        image = np.fromstring(buff,np.dtype('<u2'))
        return image.reshape(self._settings['dimensions'])


    def saveSnapshot(self, filename):
        '''
        Grabs the most recent image an saves it in Numpy's .npy format.

        :Parameters:
            *filename*: str
                The name of the file to save the image.
        '''
        shot = self.getMostRecentImage16Numpy()
        np.save(filename, shot)


    def setEMCCDGain(self, gain):
        '''
        Sets the EM gain.

        :Parameters:
            *gain*: int or str
                Can be either 'min', 'max' or an int, to set the EM gain to the minimum,
                maximum or a given value, respectively.
        '''
        if gain == 'min':
            gain = self._props['em_gain_range'][0]
        elif gain == 'max':
            gain = self._props['em_gain_range'][1]
        print 'EMCCD: Setting gain to', gain
        self._settings['em_gain'] = gain
        self._api.abortAcquisition()
        self._api.setEMCCDGain(gain)
        self._api.startAcquisition()


    def openShutter(self):
        ''' Opens the camera shutter. '''
        self._api.abortAcquisition()
        self._api.setShutter(0,1,0,0)
        status = self._api.startAcquisition()
        print "OpenShutter: " + err_codes[status]


    def closeShutter(self):
        ''' Closes the camera shutter. '''
        self._api.abortAcquisition()
        self._api.setShutter(0,2,0,0)
        status = self._api.startAcquisition()
        print "CloseShutter: " + err_codes[status]

    def stopCapture(self):
        status = self._api.abortAcquisition()
        print "AbortAcquisition: " + err_codes[status]

    def beginAcquisition(self):
        status = self._api.startAcquisition()
        print "Acquisition start: " + err_codes[status]
        if err_codes[status]=='pagelock':
            self.stopCapture()
            time.sleep(5)
            status = self._api.startAcquisition()
            print "Acquisition start (2nd try): " + err_codes[status]
            #if err_codes[status]=='pagelock':
            #    self.shutDown()
            #    time.sleep(0.5)
            #    self.__init__(self._initSettings)


    def shutDown(self):
        ''' Shuts down the camera. This function is automatically called when the user
        closes InControl. '''
        print 'Shutting down camera...'
        self._api.abortAcquisition()
        self.closeShutter()
        self._api.coolerOff()
        status = self._api.shutDown()
        print err_codes[status]
        print '...done.'

