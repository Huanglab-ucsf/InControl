#!/usr/bin/python

from PyQt4 import QtCore
import inLib
import time
import functools


class UI(inLib.DeviceUI):
    
    def __init__(self, control):
        design_path = 'nationalInstruments.DAQ.DAQ_design'
        print 'DAQ: Initializing UI.'
        inLib.DeviceUI.__init__(self, control, design_path)

        #Filling in data:
        self._ui.lineEdit_frames.setText("%i" % self._control._frames)
        self._ui.lineEdit_numChannels.setText("%i" % self._control._numChannels)
        self._ui.lineEdit_oversampling.setText("%i" % self._control._oversampling)
        self._ui.lineEdit_frameTime.setText("%.3f" % self._control.frame_time)

        #Filling in channel data
        channelSettings = self._control._channelSettings
        for i in range(0,len(channelSettings)):
            channel = channelSettings.keys()[i]
            powerLineEdit = getattr(self._ui, "lineEdit_power"+str(channel))
            onLineEdit = getattr(self._ui, "lineEdit_on"+str(channel))
            offLineEdit = getattr(self._ui, "lineEdit_off"+str(channel))
            powerLineEdit.setText("%.2f" % channelSettings[channel]['power'])
            onLineEdit.setText("%.2f" % channelSettings[channel]['ch_on'])
            offLineEdit.setText("%.2f" % channelSettings[channel]['ch_off'])

        #Filling in analog output data:
        self._ui.lineEdit_analogout0.setText("%.2f" % self._control._analogout0)
        self._ui.lineEdit_analogout1.setText("%.2f" % self._control._analogout1)

        #Connecting buttons to functions:
        self._ui.setup_pushButton.clicked.connect(self._setup)
        self._ui.start_pushButton.clicked.connect(self._start)
        self._ui.stop_pushButton.clicked.connect(self._stop)
        self._ui.pushButton_analog0.clicked.connect(functools.partial(self._analogOnOff,int(0)))
        self._ui.pushButton_analog1.clicked.connect(functools.partial(self._analogOnOff,int(1)))
        self._ui.pushButton_updateTDO.clicked.connect(self._updateTDO)

        #Connecting checkboxes:
        self._ui.checkBox_ch0.stateChanged.connect(functools.partial(self._doCheck, 0))
        self._ui.checkBox_ch1.stateChanged.connect(functools.partial(self._doCheck, 1))
        self._ui.checkBox_ch2.stateChanged.connect(functools.partial(self._doCheck, 2))
        self._ui.checkBox_ch3.stateChanged.connect(functools.partial(self._doCheck, 3))
        self._ui.checkBox_ch4.stateChanged.connect(functools.partial(self._doCheck, 4))
        self._ui.checkBox_ch5.stateChanged.connect(functools.partial(self._doCheck, 5))
        self._ui.checkBox_ch6.stateChanged.connect(functools.partial(self._doCheck, 6))
        self._ui.checkBox_ch7.stateChanged.connect(functools.partial(self._doCheck, 7))

        #Analog waveform
        self._ui.pushButton_waveformSetup.clicked.connect(self._setupAnalogWaveform)
        self._ui.pushButton_waveformStart.clicked.connect(self._startWaveform)
        self._ui.pushButton_waveformStop.clicked.connect(self._stopWaveform)
        self._ui.pushButton_waveformClear.clicked.connect(self._clearWaveform)

        ##Counter only
        self._ui.pushButton_counterSet.clicked.connect(self._setupCounter)
        self._ui.pushButton_counterStart.clicked.connect(self._startCounter)
        self._ui.pushButton_counterStop.clicked.connect(self._stopCounter)

        #Quick confocal buttons
        self._ui.confocal10_pushButton.clicked.connect(self._confocal10)
        self._ui.confocal40_pushButton.clicked.connect(self._confocal40)
        

    def _doCheck(self, channel):
        checkBox = getattr(self._ui, "checkBox_ch"+str(channel))
        isOn = checkBox.checkState()
        if not isOn:
            self._control.digitalOutput(channel, 0)
        else:
            self._control.digitalOutput(channel, 1)

    def _updateTDO(self):
        numChannels = int(self._ui.lineEdit_numChannels.text())
        frames = int(self._ui.lineEdit_frames.text())
        oversampling = int(self._ui.lineEdit_oversampling.text())
        frametime = float(self._ui.lineEdit_frameTime.text())
        newChannelSettings = {}
        for i in range(0,6):
            ch_str = str(int(i))
            powerLineEdit = getattr(self._ui, "lineEdit_power"+ch_str)
            onLineEdit = getattr(self._ui, "lineEdit_on"+ch_str)
            offLineEdit = getattr(self._ui, "lineEdit_off"+ch_str)
            temp_str = powerLineEdit.text()
            if not (temp_str == None or temp_str == '' or temp_str == '0'):
                newChannelSettings[i] = {}
                newChannelSettings[i]['power'] = float(temp_str)
                ch_on = float(onLineEdit.text())
                newChannelSettings[i]['ch_on'] = ch_on
                ch_off = float(offLineEdit.text())
                newChannelSettings[i]['ch_off'] = ch_off
        self._control._newChannelSettings(newChannelSettings)
        self._control._newSettings(numChannels = numChannels,
                                   frames = frames,
                                   oversampling = oversampling,
                                   frame_time = frametime)
        

    def _analogOnOff(self, channel):
        if channel==1:
            ch_str = '1'
            ao = self._control.ao1
        else:
            ch_str = '0'
            ao = self._control.ao0
        lineEdit = getattr(self._ui, "lineEdit_analogout"+ch_str)
        pushButton = getattr(self._ui, "pushButton_analog"+ch_str)
        if not ao:
            outvoltage = float(lineEdit.text())
            pushButton.setText('Turn OFF')
            pushButton.setStyleSheet("QPushButton { color: red }")
            self._control.startAnalogOuts(int(channel), outvoltage)
            setattr(self._control, "ao"+ch_str, True)
        else:
            pushButton.setText('Turn ON')
            pushButton.setStyleSheet("QPushButton { color: black }")
            self._control.stopAnalogOuts(int(channel))
            setattr(self._control, "ao"+ch_str, False)

    def _setupAnalogWaveform(self):
        numSamples = int(self._ui.lineEdit_waveformNumSamples.text())
        freq = int(self._ui.lineEdit_waveformFrequency.text())
        sampleRate = numSamples*freq
        print "Sample rate for analog waveform: ", sampleRate
        minV = float(self._ui.lineEdit_waveformMin.text())
        maxV = float(self._ui.lineEdit_waveformMax.text())
        clock_item = int(self._ui.comboBox_waveformClock.currentIndex())
        ch0 = self._ui.radioButton_waveformCh0.isChecked()
        if ch0:
            channel = 0
        else:
            channel = 1
        if clock_item == 0:
            clck = ""
        elif clock_item == 1:
            clck = "ctr0out"
        elif clock_item == 2:
            clck = "ctr0InternalOutput"
        elif clock_item == 3:
            clck = "ctr1InternalOutput"
        if self._ui.radioButton_sawtooth.isChecked():
            wave = self._control.createSawtooth(numSamples, minV, maxV)
        else:
            wave = self._control.createTriangle(numSamples, minV, maxV)
        self._control.createWaveformOutput(channel, wave, sampleRate, clock=clck)

    def _setupCounter(self):
        ch0 = self._ui.radioButton_counterCh0.isChecked()
        if ch0:
            channel = 0
        else:
            channel = 1
        numSamples = int(self._ui.lineEdit_waveformNumSamples.text())
        freq = int(self._ui.lineEdit_counterFreq.text())
        useCounterTask2 = self._ui.checkBox_counter2.isChecked()
        self._control.createCounterOnly(numSamples, ch=channel, freq=freq, counter2=useCounterTask2)

    def _startCounter(self):
        useCounterTask2 = self._ui.checkBox_counter2.isChecked()
        self._control.startCounterOnly(counter2=useCounterTask2)

    def _stopCounter(self):
        useCounterTask2 = self._ui.checkBox_counter2.isChecked()
        self._control.stopCounterOnly(counter2=useCounterTask2)

    def _startWaveform(self):
        self._control.startWaveformOutput()

    def _stopWaveform(self):
        self._control.stopWaveformOutput()

    def _clearWaveform(self):
        self._control.clearWaveformOutput()

    def _confocal10(self):
        useCounterTask2 = self._ui.checkBox_counter2.isChecked()
        self._control.stopWaveformOutput()
        self._control.stopCounterOnly(counter2=useCounterTask2)

        minV = float(self._ui.lineEdit_waveformMin.text())
        maxV = float(self._ui.lineEdit_waveformMax.text())
        
        self._control.createCounterOnly(1000, ch=0, freq=10*1000)
        self._control.startCounterOnly(counter2=useCounterTask2)
        wave = self._control.createTriangle(1000, minV, maxV)
        self._control.createWaveformOutput(0, wave, 10*1000, clock="ctr0InternalOutput")
        self._control.startWaveformOutput()

    def _confocal40(self):
        useCounterTask2 = self._ui.checkBox_counter2.isChecked()
        self._control.stopWaveformOutput()
        self._control.stopCounterOnly(counter2=useCounterTask2)

        minV = float(self._ui.lineEdit_waveformMin.text())
        maxV = float(self._ui.lineEdit_waveformMax.text())
        
        self._control.createCounterOnly(1000, ch=0, freq=40*1000)
        self._control.startCounterOnly(counter2=useCounterTask2)
        wave = self._control.createTriangle(1000, minV, maxV)
        self._control.createWaveformOutput(0, wave, 40*1000, clock="ctr0InternalOutput")
        self._control.startWaveformOutput()


    def _setup(self):
        print "setting up daq..."
        self._control.setup()

    def _start(self):
        print "starting..."
        self._control.start()

    def _stop(self):
        print "stopping..."
        self._control.stop()

    def shutDown(self):
        self._control.stop()
        self._control.stopAnalogOuts(0)
        self._control.stopAnalogOuts(1)
        self._control.stopDO()
