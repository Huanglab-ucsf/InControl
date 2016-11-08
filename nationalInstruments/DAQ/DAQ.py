#!/usr/bin/python


import inLib
import numpy as np
import os, glob
import Queue
import threading

class Control(inLib.Device):
    '''
    The device control of NI DAQ board.
    '''

    def __init__(self, settings):
        inLib.Device.__init__(self, 'nationalInstruments.DAQ.DAQ_api', settings)

        #DAQ properties
        self._props = {}

        self._numChannels = settings['channels']
        self._board = settings['board']
        self._analogout0 = settings['analogoutput0']
        self._analogout1 = settings['analogoutput1']
        self._oversampling = settings['oversampling']
        self._frames = settings['frames']
        self._channelSettings = settings['channel_settings']
        self.frame_time = 0.01

        self.waveform_len = self._frames * self._oversampling

        self.ct_task = 0
        self.wv_task = 0

        self.ao0 = False
        self.ao1 = False

        self.aiSamples = 1000
        self.aiSampleRate = 1000

        self.powerToVoltage = lambda channel,power: 5*power

        self._api.createAnalogOutput(0)
        self._api.createAnalogOutput(1)

        self._api.createAnalogInput(0)
        self.aiData = []

    def _newChannelSettings(self, settings_dict):
        self._channelSettings = settings_dict

    def _newSettings(self, numChannels=0, frames=0,
                     oversampling=0, frame_time=0):
        if numChannels:
            self._numChannels = numChannels
        if frames:
            self._frames = frames
        if oversampling:
            self._oversampling = oversampling
        if frame_time:
            self.frame_time = frame_time

    def _createWaveformOLD(self):
        self.waveforms = []
        for i in range(0,self._numChannels):
            for j in range(0,self._frames):
                power = 0
                if i in self._channelSettings.keys():
                    if j<self._channelSettings[i]['ch_on']:
                        power = 0
                    elif j>=self._channelSettings[i]['ch_off']:
                        power = 0
                    else:
                        power = self._channelSettings[i]['power']
                for k in range(0,self._oversampling):
                        self.waveforms.append(self.powerToVoltage(i, power))

    def _createWaveform(self):
        self.waveforms = self.makeWaveform(self._numChannels,
                                           self._frames,
                                           self._oversampling,
                                           self._channelSettings)
        filename = 'waveform'
        if os.path.exists(filename+'.npy'):
            num = len(glob.glob(filename+'*'))
            filename = filename + str(num).zfill(4)
        np.save(filename, np.array(self.waveforms))

    def makeWaveform(self, numChannels, frames, oversampling, channelSettings):
        i=0
        waveforms = []
        while i<numChannels:
            for j in range(0,frames*oversampling):
                power = 0
                if i in channelSettings.keys():
                    if np.isscalar(channelSettings[i]['ch_on']):
                        if j<int(round(channelSettings[i]['ch_on']*oversampling)):
                            power = 0
                        elif j>=int(round(channelSettings[i]['ch_off']*oversampling)):
                            power = 0
                        else:
                            power = channelSettings[i]['power']
                    else:
                        power = 0
                        for k in range(0,len(channelSettings[i]['ch_on'])):
                            cond_one = (j>=int(round(channelSettings[i]['ch_on'][k]*oversampling)))
                            cond_two = (j<int(round(channelSettings[i]['ch_off'][k]*oversampling)))
                            if cond_one and cond_two:
                                power = channelSettings[i]['power']
                waveforms.append(self.powerToVoltage(i, power))
            i = i+1
        return waveforms

    def setup(self):
        self._createWaveform()
        self.readyShutters(self.frame_time,
                           self._frames,
                           self._oversampling,
                           self._numChannels,
                           self.waveforms)

    def readyShutters(self, frametime, frames, oversampling, numChannels, waveforms, freq=None, noCounter=False):
        frequency = (1.001/frametime) * float(oversampling)
        self._api.createDigWaveformOutput(numChannels,
                                          waveforms,
                                          frequency)
        if not noCounter:
            self._api.createCounterOutput(frames*oversampling)

    def createCounterOnly(self, waveform_len, ch=0, freq=None, counter2=False):
        self._api.createCounterOutput(waveform_len,channel=ch,freq=freq,
                                      counter2=counter2)

    def startCounterOnly(self, counter2=False):
        self._api.startCounter(counter2=counter2)

    def stopCounterOnly(self, counter2=False):
        self._api.stopCounter(counter2=counter2)
        
    def start(self, noCounter=False):
        #starts the waveform and counter tasks
        self._api.startTask(noCounter=noCounter)

    def createWaveformOutput(self, channel, waveform, sample_rate, clock=""):
        self._api.createWaveformOutput(channel, waveform, sample_rate, clock=clock)

    def startWaveformOutput(self):
        self._api.startWaveformOutput()

    def stopWaveformOutput(self):
        self._api.stopWaveformOutput()

    def clearWaveformOutput(self):
        self._api.clearWaveformOutput()

    def createAI(self):
        self._api.createAnalogInput(0)

    def startAI(self):
        self._api.startAI()

    def addAIChannel(self):
        self._api.addAIChannel(1)

    def setAIParams(self, samples, sampleRate):
        self.aiSamples = samples
        self.aiSampleRate = sampleRate

    def configureAI(self):
        self._api.configureAI(self.aiSamples, self.aiSampleRate)

    def getAI(self):
        self.aiData = self._api.getAIData()
        return self.aiData

    def stop(self):
        #stops the waveform and counter tasks
        self._api.stopTask()

    def stopDO(self):
        self._api.clearDO()

    def stopAI(self):
        self._api.stopAI()

    '''
    def setupAnalogOuts(self):
        self._api.createAnalogOutput(0, self._analogout0)
        self._api.createAnalogOutput(1, self._analogout1)
    '''

    def startAnalogOuts(self, channel, voltage):
        setattr(self, "ao"+str(int(channel)), True)
        self._api.startAnalogOutput(channel, voltage)

    def stopAnalogOuts(self, channel):
        self._api.stopAnalogOutput(channel)
        setattr(self, "ao"+str(int(channel)), False)

    def digitalOutput(self, channel, level):
        self._api.digitalOutput(channel, level)

    def shutDown(self):
        self.stop()
        self.stopDO()
        self.stopAI()

    ##Making analog waveforms:
    def createTriangle(self, numPoints, minV, maxV):
        w1 = np.linspace(minV, maxV, numPoints/2, endpoint=False)
        w2 = np.linspace(maxV, minV, numPoints/2, endpoint=False)
        wave = np.hstack((w1,w2))
        return wave

    def createSawtooth(self, numPoints, minV, maxV):
        wave = np.linspace(minV, maxV, numPoints)
        return wave
        

        
