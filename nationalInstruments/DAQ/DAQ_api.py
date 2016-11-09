#!/usr/bin/python
#
# Communicates with the National Instrument card(s).
#
# This is geared primarly towards doing retriggerable analog
# output. Since the analog channels are not themselves retriggerable
# the default is they run in continous mode and get clocked
# by one of the counters, which are retriggerable.
#
# Based on Hazen 3/09 by Ryan 6/12
#

#import inLib
import numpy as np
from ctypes import *
import time

# Load the NIDAQmx driver library.
nidaqmx = windll.nicaiu

# Constants
DAQmx_Val_ChanPerLine = 0
DAQmx_Val_ChanForAllLines = 1
DAQmx_Val_ContSamps = 10123
DAQmx_Val_Falling = 10171
DAQmx_Val_FiniteSamps = 10178
DAQmx_Val_GroupByChannel = 0
DAQmx_Val_High = 10192
DAQmx_Val_Hz = 10373
DAQmx_Val_Low = 10214
DAQmx_Val_Rising = 10280
DAQmx_Val_Volts = 10348
DAQmx_Val_RSE = 10083
DAQmx_Val_NRSE = 10078
DAQmx_Val_Diff = 10106
DAQmx_Val_PseudoDiff = 12529

TaskHandle = c_ulong


#
# Utility functions
#

def checkStatus(status):
    if status < 0:
        buf_size = 1000
        buf = create_string_buffer(buf_size)
        nidaqmx.DAQmxGetErrorString(c_long(status), buf, buf_size)
        raise RuntimeError('nidaq call failed with error %d: %s'%(status, buf.value))


#
# NIDAQ functions
#

# Return DAQ board info.
def getDAQBoardInfo():
    daq_boards = []
    devices_len = 100
    devices = create_string_buffer(devices_len)
    checkStatus(nidaqmx.DAQmxGetSysDevNames(devices, devices_len))
    devices_string = devices.value
    for dev in devices_string.split(", "):
        dev_data_len = 100
        dev_data = create_string_buffer(dev_data_len)
        c_dev = c_char_p(dev)
        checkStatus(nidaqmx.DAQmxGetDevProductType(c_dev, dev_data, dev_data_len))
        daq_boards.append([dev_data.value, dev[-1:]])
    return daq_boards

# Return the device number that corresponds to a given board
# This assumes that you do not have two identically named boards.
def getBoardDevNumber(board):
    available_boards = getDAQBoardInfo()
    index = 1
    device_number = 0
    for available_board in available_boards:
        if board == available_board[0]:
            device_number = available_board[1]
        index += 1
        
    #assert device_number != 0, str(board) + " is not available."

    return device_number

#
# DAQ communication classes
#

#
# NIDAQmx task class
#
class NIDAQTask():
    def __init__(self, board):
        self.board_number = getBoardDevNumber(board)
        self.taskHandle = TaskHandle(0)
        checkStatus(nidaqmx.DAQmxCreateTask("", byref(self.taskHandle)))

    def clearTask(self):
        checkStatus(nidaqmx.DAQmxClearTask(self.taskHandle))

    def startTask(self):
        checkStatus(nidaqmx.DAQmxStartTask(self.taskHandle))

    def stopTask(self):
        checkStatus(nidaqmx.DAQmxStopTask(self.taskHandle))

    def taskIsDoneP(self):
        done = c_long(0)
        checkStatus(nidaqmx.DAQmxIsTaskDone(self.taskHandle, byref(done)))
        return done.value


#                    
# Simple analog output class
#
class VoltageOutput(NIDAQTask):
    def __init__(self, board, channel, min_val = -10.0, max_val = 10.0):
        print "NIDAQ voltage output"
        NIDAQTask.__init__(self, board)
        self.channel = channel
        self.dev_and_channel = "Dev" + str(self.board_number) + "/ao" + str(self.channel)
        print "VoltageOutput: " + self.dev_and_channel
        checkStatus(nidaqmx.DAQmxCreateAOVoltageChan(self.taskHandle, 
                                                     c_char_p(self.dev_and_channel),
                                                     "", 
                                                     c_double(min_val), 
                                                     c_double(max_val), 
                                                     c_int(DAQmx_Val_Volts), 
                                                     ""))

    # output a single voltage more or less as soon as it is called, 
    # assuming that no other task is running.
    def outputVoltage(self, voltage):
        c_samples_written = c_long(0)
        c_voltage = c_double(voltage)
        checkStatus(nidaqmx.DAQmxWriteAnalogF64(self.taskHandle, 
                                                c_long(1),
                                                c_long(1),
                                                c_double(10.0),
                                                c_long(DAQmx_Val_GroupByChannel),
                                                byref(c_voltage),
                                                byref(c_samples_written), 
                                                c_long(0)))
        assert c_samples_written.value == 1, "outputVoltage failed: " + str(c_samples_written.value) + " 1"

    def outputVoltageWave(self, waveform, sampleRate):
        periodLength = len(waveform)
        checkStatus(nidaqmx.DAQmxCfgSampClkTiming(self.taskHandle,
                                                  "",
                                                  c_double(sampleRate),
                                                  c_long(DAQmx_Val_Rising),
                                                  c_long(DAQmx_Val_FiniteSamps),
                                                  c_ulonglong(periodLength)))
        checkStatus(nidaqmx.DAQmxWriteAnalogF64(self.taskHandle, 
                                                c_long(periodLength),
                                                c_long(0),
                                                c_double(-1),
                                                c_long(DAQmx_Val_GroupByChannel),
                                                waveform.ctypes.data,
                                                None,None))
        


#
# Analog waveform output class
#
class WaveformOutput(NIDAQTask):
    def __init__(self, board, channel, min_val = -10.0, max_val = 10.0):
        NIDAQTask.__init__(self, board)
        self.c_waveform = 0
        self.dev_and_channel = "Dev" + str(self.board_number) + "/ao" + str(channel)
        self.min_val = min_val
        self.max_val = max_val
        self.channels = 1
        print "Waveform: " + self.dev_and_channel
        checkStatus(nidaqmx.DAQmxCreateAOVoltageChan(self.taskHandle, 
                                                     c_char_p(self.dev_and_channel),
                                                     "", 
                                                     c_double(self.min_val), 
                                                     c_double(self.max_val), 
                                                     c_int(DAQmx_Val_Volts), 
                                                     ""))



    def addChannel(self, channel, board = None):
        self.channels += 1
        board_number = self.board_number
        if board:
            board_number = getBoardDevNumber("PCIe-6323")
        self.dev_and_channel = "Dev" + str(board_number) + "/ao" + str(channel)
        checkStatus(nidaqmx.DAQmxCreateAOVoltageChan(self.taskHandle, 
                                                     c_char_p(self.dev_and_channel),
                                                     "", 
                                                     c_double(self.min_val), 
                                                     c_double(self.max_val), 
                                                     c_int(DAQmx_Val_Volts), 
                                                     ""))

    def setWaveform(self, waveform, sample_rate, finite = 0, clock = "", rising = True):
        #
        # The output waveforms for all the analog channels are stored in one 
        # big array, so the per channel waveform length is the total length 
        # divided by the number of channels.
        #
        # You need to add all your channels first before calling this.
        #
        waveform_len = len(waveform)/self.channels

        clock_source = ""
        if len(clock) > 0:
            clock_source = "/Dev" + str(self.board_number) + "/" + str(clock)

        # set the timing for the waveform.
        sample_mode = DAQmx_Val_ContSamps
        if finite:
            sample_mode = DAQmx_Val_FiniteSamps
        c_rising = c_long(DAQmx_Val_Rising)
        if (not rising):
            c_rising = c_long(DAQmx_Val_Falling)
        checkStatus(nidaqmx.DAQmxCfgSampClkTiming(self.taskHandle,
                                                  c_char_p(clock_source),
                                                  c_double(sample_rate),
                                                  c_rising,
                                                  c_long(sample_mode),
                                                  c_ulonglong(waveform_len)))

        # transfer the waveform data to the DAQ board buffer.
        data_len = len(waveform)
        c_samples_written = c_long(data_len)
        c_wave_form_type = c_double * data_len
        self.c_waveform = c_wave_form_type()
        for i in range(data_len):
            self.c_waveform[i] = c_double(waveform[i])
        '''
        checkStatus(nidaqmx.DAQmxWriteAnalogF64(self.taskHandle, 
                                                c_long(waveform_len),
                                                c_long(0),
                                                c_double(10.0),
                                                c_long(DAQmx_Val_GroupByChannel),
                                                byref(self.c_waveform), 
                                                byref(c_samples_written), 
                                                c_long(0)))
        '''
        checkStatus(nidaqmx.DAQmxWriteAnalogF64(self.taskHandle, 
                                                c_long(waveform_len),
                                                c_long(0),
                                                c_double(-1),
                                                c_long(DAQmx_Val_GroupByChannel),
                                                waveform.ctypes.data, 
                                                None,None))
        assert c_samples_written.value == waveform_len, "Failed to write the right number of samples " + str(c_samples_written.value) + " " + str(waveform_len)


#
# Analog input class
#
# Geared towards acquiring a fixed number of samples at a predefined rate,
# asynchronously timed off the internal clock.
#
class AnalogInput(NIDAQTask):
    def __init__(self, board, channel, min_val = -10.0, max_val = 10.0):
        NIDAQTask.__init__(self, board)
        self.c_waveform = 0
        self.dev_and_channel = "Dev" + str(self.board_number) + "/ai" + str(channel)
        self.min_val = min_val
        self.max_val = max_val
        self.channels = 1
        checkStatus(nidaqmx.DAQmxCreateAIVoltageChan(self.taskHandle, 
                                                     c_char_p(self.dev_and_channel),
                                                     "",
                                                     c_int(DAQmx_Val_RSE),
                                                     c_double(self.min_val), 
                                                     c_double(self.max_val), 
                                                     c_int(DAQmx_Val_Volts),
                                                     c_long(0)))

    def addChannel(self, channel):
        self.channels += 1
        self.dev_and_channel = "Dev" + str(self.board_number) + "/ai" + str(channel)        
        checkStatus(nidaqmx.DAQmxCreateAIVoltageChan(self.taskHandle, 
                                                     c_char_p(self.dev_and_channel),
                                                     "",
                                                     c_int(DAQmx_Val_RSE),
                                                     c_double(self.min_val), 
                                                     c_double(self.max_val), 
                                                     c_int(DAQmx_Val_Volts),
                                                     c_long(0)))

    def configureAcquisition(self, samples, sample_rate_Hz):
        # set the sample timing and buffer length.
        self.samples = samples
        checkStatus(nidaqmx.DAQmxCfgSampClkTiming(self.taskHandle,
                                                  "",
                                                  c_double(sample_rate_Hz),
                                                  c_long(DAQmx_Val_Rising),
                                                  c_long(DAQmx_Val_FiniteSamps),
                                                  c_ulonglong(self.samples)))

    def getData(self):
        # allocate space to store the data.
        c_data_type = c_double * (self.samples * self.channels)
        data = c_data_type()
        # acquire the data.
        c_samples_read = c_long(0)
        checkStatus(nidaqmx.DAQmxReadAnalogF64(self.taskHandle,
                                               c_long(self.samples),
                                               c_double(10.0),
                                               c_long(DAQmx_Val_GroupByChannel),
                                               byref(data),
                                               c_ulong(self.channels*self.samples),
                                               byref(c_samples_read),
                                               c_long(0)))
        assert c_samples_read.value == self.samples, "Failed to read the right number of samples " + str(c_samples_read.value) + " " + str(self.samples)
        return data


#
# Counter output class
#
class CounterOutput(NIDAQTask):
    def __init__(self, board, channel, frequency, duty_cycle, initial_delay = 0.0):
        NIDAQTask.__init__(self, board)
        self.channel = channel
        self.dev_and_channel = "Dev" + str(self.board_number) + "/ctr" + str(self.channel)
	checkStatus(nidaqmx.DAQmxCreateCOPulseChanFreq(self.taskHandle,
                                                       c_char_p(self.dev_and_channel),
                                                       "",
                                                       c_long(DAQmx_Val_Hz),
                                                       c_long(DAQmx_Val_High), #was LOW
                                                       c_double(initial_delay),
                                                       c_double(frequency),
                                                       c_double(duty_cycle)))

    def setCounter(self, number_samples):
        checkStatus(nidaqmx.DAQmxCfgImplicitTiming(self.taskHandle,
                                                   c_long(DAQmx_Val_FiniteSamps),
                                                   c_ulonglong(number_samples)))

    def setTrigger(self, trigger_source, retriggerable = 1):
        if retriggerable:
            checkStatus(nidaqmx.DAQmxSetStartTrigRetriggerable(self.taskHandle, 
                                                               c_long(1)))
        else:
            checkStatus(nidaqmx.DAQmxSetStartTrigRetriggerable(self.taskHandle, 
                                                               c_long(0)))
        trigger = "/Dev" + str(self.board_number) + "/PFI" + str(trigger_source)
	checkStatus(nidaqmx.DAQmxCfgDigEdgeStartTrig(self.taskHandle,
                                                     c_char_p(trigger),
                                                     c_long(DAQmx_Val_Rising)))

# ----------------------------------------------------------------------------       
#                                DIGITAL
#
# Digital output task (for simple non-triggered digital output)
#
class DigitalOutput(NIDAQTask):
    def __init__(self, board, channel):
        NIDAQTask.__init__(self, board)
        self.channel = channel
        self.dev_and_channel = "Dev" + str(self.board_number) + "/port0/line" + str(self.channel)
        #print "CREATING DIGITAL LINE"
        checkStatus(nidaqmx.DAQmxCreateDOChan(self.taskHandle,
                                              c_char_p(self.dev_and_channel),
                                              "",
                                              c_long(1)))           #DAQmx_Val_ChanPerLine

    def output(self, high):
        if high:
            c_data = c_byte(1)
        else:
            c_data = c_byte(0)
        c_written = c_long(0)
        #print "WRITING DIGITAL LINES"
        checkStatus(nidaqmx.DAQmxWriteDigitalLines(self.taskHandle,
                                                   c_long(1),
                                                   c_long(1),
                                                   c_double(10.0),
                                                   c_long(DAQmx_Val_GroupByChannel),
                                                   byref(c_data),
                                                   byref(c_written),
                                                   c_long(0)))
        assert c_written.value == 1, "Digital output failed"

class DigitalOutput32(NIDAQTask):
    def __init__(self, board, channel):
        NIDAQTask.__init__(self, board)
        self.channel = channel
        self.dev_and_channel = "Dev" + str(self.board_number) + "/port0"
        checkStatus(nidaqmx.DAQmxCreateDOChan(self.taskHandle,
                                              c_char_p(self.dev_and_channel),
                                              "",
                                              c_long(DAQmx_Val_ChanForAllLines)))

    def Digoutput(self, high):
        #potential buffer size problem, might need to make c_data a larger array
        if high:
            c_data = c_uint(1)
        else:
            c_data = c_uint(0)
        c_written = c_long(0)
        checkStatus(nidaqmx.DAQmxWriteDigitalU32(self.taskHandle,
                                                   c_long(1),
                                                   c_long(1),
                                                   c_double(10.0),
                                                   c_long(DAQmx_Val_GroupByChannel),
                                                   byref(c_data),
                                                   byref(c_written),
                                                   c_long(0)))
        assert c_written.value == 1, "Digital output failed"

#
# Digital waveform output class
#
class DigWaveformOutput(NIDAQTask):
    def __init__(self, board, channel, min_val = -10.0, max_val = 10.0):
        NIDAQTask.__init__(self, board)
        self.c_waveform = 0
        self.dev_and_channel = "Dev" + str(self.board_number) + "/port0"
        self.min_val = min_val
        self.max_val = max_val
        self.channels = 1
        checkStatus(nidaqmx.DAQmxCreateDOChan(self.taskHandle,
                                              c_char_p(self.dev_and_channel),
                                              "",
                                              c_long(DAQmx_Val_ChanForAllLines)))       #This means we write our data to all 32 lines in the port

    def addDigChannel(self, channel, board = None):
        self.channels += 1
        # --- We group all lines to one Channel (initialized above)
        # Additional "channels" only tell us to divide the waveform further
        
        #board_number = self.board_number
        #if board:
        #    board_number = getBoardDevNumber("PCIe-6323")
        #self.dev_and_channel = "Dev" + str(board_number) + "/port0/line" + str(channel)
        #checkStatus(nidaqmx.DAQmxCreateDOChan(self.taskHandle,
        #                                      c_char_p(self.dev_and_channel),
        #                                      "",
        #                                      c_long(DAQmx_Val_ChanPerLine)))

    def setDigWaveform(self, waveform, sample_rate, finite = 0, clock = "ctr0InternalOutput", rising = True):
        #
        # The output waveforms for all the analog channels are stored in one 
        # big array, so the per channel waveform length is the total length 
        # divided by the number of channels.
        #
        # You need to add all your channels first before calling this.
        #
        print "SET DIGWAVEFORM"
        waveform_len = len(waveform)/self.channels

        clock_source = ""
        if len(clock) > 0:
            clock_source = "/Dev" + str(self.board_number) + "/" + str(clock)

        # set the timing for the waveform.
        sample_mode = DAQmx_Val_ContSamps
        if finite:
            sample_mode = DAQmx_Val_FiniteSamps
        c_rising = c_long(DAQmx_Val_Rising)
        if (not rising):
            c_rising = c_long(DAQmx_Val_Falling)
        print "SET DIGWAVEFORM TIMING"
        checkStatus(nidaqmx.DAQmxCfgSampClkTiming(self.taskHandle,
                                                  c_char_p(clock_source),
                                                  c_double(sample_rate),
                                                  c_rising,
                                                  c_long(sample_mode),
                                                  c_ulonglong(waveform_len)))

        # transfer the waveform data to the DAQ board buffer.
        data_len = len(waveform)/self.channels
        c_samples_written = c_long(data_len)

        # converting the waveform into 8-bit integer format, by Bo
        U8_waveform = []
        for i in range(waveform_len):
            U8_waveform.append(int(0))
        bitmask = int(1)    
        for i in range(self.channels):
            for j in range(waveform_len):
                if waveform[i*waveform_len + j] > 0:
                    U8_waveform[j] = U8_waveform[j] | bitmask
            bitmask = bitmask << 1
        #print U8_waveform

        # converting the python data format to c data format (c_uint is 32 bit unsigned integer)    
        c_wave_form_type = c_uint * data_len
        self.c_waveform = c_wave_form_type()
        for i in range(data_len):
            self.c_waveform[i] = c_uint(U8_waveform[i])
        print "WRITE DIGWAVEFORM"
        checkStatus(nidaqmx.DAQmxWriteDigitalU32(self.taskHandle, 
                                                c_long(waveform_len),
                                                c_long(0),
                                                c_double(10.0),
                                                c_long(DAQmx_Val_GroupByChannel),
                                                byref(self.c_waveform), 
                                                byref(c_samples_written), 
                                                c_long(0)))
        assert c_samples_written.value == waveform_len, "Failed to write the right number of samples " + str(c_samples_written.value) + " " + str(waveform_len)

#                                   DIGITAL
#--------------------------------------------------------------------------------------------


#
# Digital input task (for simple non-triggered digital input)
#
class DigitalInput(NIDAQTask):
    def __init__(self, board, channel):
        NIDAQTask.__init__(self, board)
        self.channel = channel
        self.dev_and_channel = "Dev" + str(self.board_number) + "/port0/line" + str(self.channel)
        checkStatus(nidaqmx.DAQmxCreateDIChan(self.taskHandle,
                                              c_char_p(self.dev_and_channel),
                                              "",
                                              c_long(DAQmx_Val_ChanPerLine)))
    def input(self):
        c_read = c_byte(0)
        c_samps_read = c_long(0)
        c_bytes_per_samp = c_long(0)
        checkStatus(nidaqmx.DAQmxReadDigitalLines(self.taskHandle,
                                                  c_long(-1),
                                                  c_double(10.0),
                                                  c_long(DAQmx_Val_GroupByChannel),
                                                  byref(c_read),
                                                  c_long(1),
                                                  byref(c_samps_read),
                                                  byref(c_bytes_per_samp),
                                                  c_long(0)))
        assert c_samps_read.value == 1, "Digital input failed"
        if c_read.value == 1:
            return 1
        else:
            return 0


class API():
    '''
    Python wrapper of NI DAQ Board
    '''
    def __init__(self):

        #self.frequency = (1.001/kinetic_cycle_time) * float(self.oversampling)
        self.wv_task = 0
        self.ct_task = 0
        self.ct_task2 = 0
        self.input_task = 0
        
        self.ao0 = 0
        self.ao1 = 0

        self.wfo = 0

        self.do0 = 0
        self.do1 = 0
        self.do2 = 0
        self.do3 = 0
        self.do4 = 0
        self.do5 = 0
        self.do6 = 0
        self.do7 = 0

        self.digitalOuts = [self.do0, self.do1, self.do2, self.do3,
                            self.do4, self.do5, self.do6, self.do7]

        self.frequency = 1000
        self.board = 'PCIe-6353'

        self.clearDO()


    def createDigWaveformOutput(self, numChannels, waveform, frequency):
        self.frequency = frequency
        if self.wv_task==0:
            self.wv_task = DigWaveformOutput(self.board,0)
            self.wv_task.channels = numChannels
            self.wv_task.setDigWaveform(waveform, self.frequency)
            print "API's frequency: ", self.frequency
        else:
            print "WaveformOutput task needs to be cleared..."

    def createCounterOutput(self, waveform_len, channel=0, freq=None, counter2=False):
        if freq is None:
            freq=self.frequency
        if self.ct_task==0 and counter2==False:
            self.ct_task = CounterOutput(self.board, channel, freq, 0.5)
            self.ct_task.setCounter(waveform_len)
            self.ct_task.setTrigger(0)
        elif (self.ct_task!=0 and counter2==False) or (self.ct_task2!=0 and counter2):
            print "CounterOutput task needs to be cleared..."
        elif self.ct_task2==0 and counter2:
            self.ct_task2 = CounterOutput(self.board,channel, freq, 0.5)
            self.ct_task2.setCounter(waveform_len)
            self.ct_task2.setTrigger(0)

    def startCounter(self, counter2=False):
        if counter2:
            self.ct_task2.startTask()
        else:
            self.ct_task.startTask()

    def stopCounter(self, counter2=False):
        if counter2:
            self.ct_task2.stopTask()
            self.ct_task2.clearTask()
            self.ct_task2 = 0
        else:
            self.ct_task.stopTask()
            self.ct_task.clearTask()
            self.ct_task = 0

    def createAnalogOutput(self, channel):
        if channel==0:
            self.ao0 = VoltageOutput(self.board, 0)
            #self.ao0.outputVoltage(voltage)
        elif channel==1:
            self.ao1 = VoltageOutput(self.board, 1)
            #self.ao1.outputVoltage(voltage)

    def createAnalogOutputWaveform(self, channel, waveform, samplerate):
        if channel==0:
            self.ao0 = VoltageOutput(self.board, 0)
            self.ao0.outputVoltageWave(waveform, samplerate)
        elif channel==1:
            self.ao1 = VoltageOutput(self.board, 1)
            self.ao1.outputVoltageWave(waveform, samplerate)

    def createWaveformOutput(self, channel, waveform, sample_rate, clock=""):
        self.wfo = WaveformOutput(self.board,channel)
        self.wfo.setWaveform(waveform, sample_rate, finite = 0, clock = clock, rising = True)

    def startWaveformOutput(self):
        self.wfo.startTask()

    def stopWaveformOutput(self):
        self.wfo.stopTask()
        self.wfo.clearTask()

    def clearWaveformOutput(self):
        self.stopWaveformOutput()
        self.wfo = 0
        

    def startAnalogOutputWaveform(self, channel):
        if channel == 0:
            self.ao0.startTask()
        elif channel == 1:
            self.ao1.startTask()

    def createAnalogInput(self, channel):
        if self.input_task == 0:
            self.input_task = AnalogInput(self.board, channel)
        else:
            print "AnalogInput task needs to be cleared..."

    def configureAI(self, samples, sampleRate):
        if self.input_task:
            self.input_task.configureAcquisition(samples, sampleRate)

    def addAIChannel(self, channel):
        if self.input_task:
            self.input_task.addChannel(channel)
        else:
            print "AnalogInput task needs to be created..."
            

    def digitalOutput(self, channel, high):
        do = getattr(self, "do"+str(channel))
        if not do:
            print do
            setattr(self,"do"+str(channel),DigitalOutput(self.board, channel))
            do = getattr(self, "do"+str(channel))
            do.output(high)
            if high==0:
                setattr(self,"do"+str(channel),0)
        else:
            do.output(0)
            setattr(self,"do"+str(channel),0)


    '''
    def startDigOut(self, channel, high):
        do = getattr(self, "do"+str(channel))
        if not do:
            do.startTask()
        '''

    def clearDO(self):
        for channel in range(0,len(self.digitalOuts)):
            self.digitalOutput(channel,0)

    def startAnalogOutput(self, channel, voltage):
        analogout = getattr(self, "ao"+str(int(channel)))
        analogout.outputVoltage(voltage)

    def stopAnalogOutput(self, channel):
        analogout = getattr(self, "ao"+str(int(channel)))
        analogout.outputVoltage(0)
        
    def startTask(self, noCounter=False):
        self.wv_task.startTask()
        if not noCounter:
            self.ct_task.startTask()

    def startAI(self):
        if self.input_task:
            self.input_task.startTask()

    def getAIData(self):
        if self.input_task:
            return self.input_task.getData()

    def stopAI(self):
        if self.input_task:
            self.input_task.stopTask()
            self.input_task.clearTask()
            self.input_task = 0            

    def stopTask(self):
        if self.ct_task:
            print "CT Task: ", self.ct_task
            self.ct_task.stopTask()
            self.ct_task.clearTask()
            self.ct_task = 0
        if self.wv_task:
            self.wv_task.stopTask()
            self.wv_task.clearTask()
            self.wv_task = 0

    def stopAnalogOutputWaveform(self, channel):
        if channel == 0:
            self.ao0.stopTask()
            self.ao0.clearTask()
        elif channel == 1:
            self.ao1.stopTask()
            self.ao1.clearTask()

        
    

#
# Testing.
#

if __name__ == "__main__":
    print getDAQBoardInfo()
    print getBoardDevNumber("PCIe-6321")
    print getBoardDevNumber("PCI-6722")
    

    if 0:
        waveform = [5.0, 4.0, 3.0, 2.0, 1.0, 0.5]
        frequency = 31.3 * len(waveform) * 0.5
        wv_task = WaveformOutput("PCI-MIO-16E-4", 0)
        wv_task.setWaveform(waveform, frequency)
        wv_task.startTask()
        
        ct_task = CounterOutput("PCI-MIO-16E-4", 0, frequency, 0.5)
        ct_task.setCounter(len(waveform))
        ct_task.setTrigger(0)
        ct_task.startTask()
        foo = raw_input("Key Return")
        ct_task.stopTask()
        ct_task.clearTask()
        
        wv_task.stopTask()
        wv_task.clearTask()
    if 0:
        d_task = DigitalOutput("PCI-6722", 0)
        d_task.output(1)
        time.sleep(2)
        d_task.output(0)
    if 0:
        samples = 10
        a_task = AnalogInput("PCIe-6321", 0)
        a_task.addChannel(1)
        a_task.configureAcquisition(samples, 1000)
        a_task.startTask()
        data = a_task.getData()
        for i in range(2 * samples):
            print data[i]
        a_task.stopTask()
        a_task.clearTask()


#
# The MIT License
#
# Copyright (c) 2009 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
