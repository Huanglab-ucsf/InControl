#!/usr/bin/python


import inLib
from PyQt4.QtGui import QImage
import numpy as np
import Queue
import copy
import threading
import time
from itertools import chain
import libs.imagewriters as writer
import pywintypes, win32event
import multiprocessing
from multiprocessing import Process, Pipe, Queue, Array, Manager
from multiprocessing.sharedctypes import RawArray

globalImageBuffer = []

def bcd_to_int(x):

    binaryString = bin(x).split('b')[1]
    oneDig = binaryString[-4:]
    twoDig = binaryString[:-4].zfill(4)

    oneNum = eval('0b'+oneDig)
    twoNum = eval('0b'+twoDig)

    return oneNum + (10*twoNum)

mpArray = Array('H', 100*256*256, lock=True)

def imageAnalysisTest2(conn):
    print "New process starting..."
    #images = conn.recv()
    print "Got images. Length = "#, len(images)
    time.sleep(5)

def imageAnalysisTest3(framesToGrab,q,qRes,qIms):
    while True:
        doOnce = False
        results = {}
        queuedData = q.get()
        if queuedData is None:
            print "Frame size was: ", frameSize
            print "Nothing left in queue..."
            qRes.put(None)
            break
        frameSize = len(queuedData)/8
        for j in range(0,8):
            if doOnce:
                print "QueuedData: ", queuedData[j*frameSize:(j+1)*frameSize]
                doOnce = False
            #results[j] = np.mean(queuedData[j*frameSize:(j+1)*frameSize][0])
            temp1 = bcd_to_int(queuedData[j*frameSize:(j+1)*frameSize][0][3])
            temp2 = bcd_to_int(queuedData[j*frameSize:(j+1)*frameSize][0][2])
            temp3 = bcd_to_int(queuedData[j*frameSize:(j+1)*frameSize][0][1])
            results[j] = temp3*10000 + temp2*100 + temp1
            if results[j]%framesToGrab == 0:
                qIms.put(queuedData[j*frameSize:(j+1)*frameSize][0])
        qRes.put(results)
        
        '''
        startFrame,endFrame = queuedData
        print "Length of globalImageBuffer: ", len(globalImageBuffer)
        images = copy.deepcopy(globalImageBuffer[startFrame:endFrame])
        print "Length of images: ", len(images)
        '''
        #print "iat3 got: ", queuedData
        #frameLength = len(queuedData)/8
        #print "frame length: ", frameLength
        #for j in range(0,8):
        #    results[j] = np.mean(queuedData[j*frameLength:(j+1)*frameLength])
        #qRes.put(results)
        #print "On processor: ", multiprocessing.current_process().name
        #print "Got images from %i to %i" % (startFrame,endFrame)

def useImageAnalysisResults(sigFrame,qRes, e):
    allRes = {}
    print "Starting useImageAnalysisResults..."
    print "Size of qRes: ", qRes.qsize()
    i=0
    setYet = False
    while True:
        results = qRes.get()
        if i==0:
            print "i=0 results: ", results
            allRes = results.values()
        i=i+1
        if results is None:
            np.save('D:\\Data\\Ryan\\results.npy', allRes)
            break
        #allRes = dict(allRes, **results)
        allRes.extend(results.values())
        if sigFrame in allRes and not setYet:
            e.set()
            setYet = True
    #for key in allRes:
    #    print "Frame %i: mean value = %.1f" % (key, allRes[key])
    
    

class Control(inLib.Device):
    '''
    The device control of pco.edge sCMOS camera.
    '''

    def __init__(self, settings):
        inLib.Device.__init__(self, 'cooke.pcoedge.camera_api', settings)

        #Camera properties
        self._props = {}

        #Loaded yaml settings
        self.loadedSettings = settings
        self.saved_settings = []
        self.newSettings('no_file', settings_dict=settings)

        #Sensor settings
        self._bpp = 14
        status, (x0,y0,x1,y1) = self._api.getROI()
        self._props['dimensions'] = x1-x0+1,y1-y0+1
        self._props['x_start'] = x0
        self._props['y_start'] = y0

        self._initializedBuffers = 0
        self._lastBuffer = 0

        self.buffer0_allocd = False
        self.buffer1_allocd = False

        self._buffersAllocated = np.ones((16),dtype=bool)*False
        self._buffersQueued = np.ones((16),dtype=bool)*False
        self._buffers = []
        self._bufferEvents = []

        self._images = np.array([])
        self._fillBottom = True

        self._alternatingBuffer = 0

        self.daxfile = 0

        self._api.setRecorderSubmode(1)

        self.fastImages = None


        #Multiprocessing tests
        self.grabFrames = 100
        self.emitSignalFrame = 4000

        self.initFramesMP = 100
        self.subProcessStart = False
        self.subProcess2Start = False
        self.parent_conn, self.child_conn = Pipe()
        self.mgr = Manager()
        self.q = self.mgr.Queue()
        self.qIms = self.mgr.Queue()
        self.resultsQueue = self.mgr.Queue()
        self.resultsEvent = self.mgr.Event()
        self.p = Process(target=imageAnalysisTest3, args=(self.grabFrames,self.q,self.resultsQueue,self.qIms,))

        self.furtherAnalysis = Process(target=useImageAnalysisResults, args=(self.emitSignalFrame,self.resultsQueue,self.resultsEvent,))
        

        self.image1 = 0
        self.image2 = 100

        self.point1 = 0
        self.point2 = 0

        


    def newSettings(self, filename, settings_dict=None):
        if settings_dict is None:
            settings_dict = inLib.load_settings(filename)
            if settings_dict.has_key('devices'):
                settings_dict = settings_dict['devices']['camera']
            settings_dict['settings_filename'] = filename
        self.saved_settings = [settings_dict] + self.saved_settings

    def updateSettings(self, settings_dict):
        try:
            roi = settings_dict['roi']
            self._setROI(roi)
        except:
            print "Unable to set new ROI"
        try:
            exposure_time = settings_dict['exposure_time']
            delay_time = settings_dict['delay_time']
            self._setDelayExposureTime(delay_time, exposure_time,
                                       'ms','ms')
        except:
            print "Unable to set new timings"

    def unSetEvent(self):
        self.resultsEvent.clear()

    def whenToEmitAndCapture(self):
        return self.emitSignalFrame, self.grabFrames

    def changeWhenToEmitAndCapture(self, sig, capt):
        self.emitSignalFrame = sig
        self.grabFrames = capt

    def getRecordingStruct(self):
        prec = self._api.getRecordingStruct()
        return prec
         
    def _setROI(self, ROI):
        x0,x1,y0,y1 = ROI
        status = self._api.setROI(x0,y0,x1,y1)

    def _getROI(self):
        status, (x0,y0,x1,y1) = self._api.getROI()
        return x0,x1,y0,y1

    def _getResolution(self):
        status, (x0,y0,x1,y1) = self._api.getROI()
        return x1-x0+1,y1-y0+1

    def _getDelayExposureTime(self):
        err, times = self._api.getDelayExposureTime()
        self._props['exposure_time'] = times[1]
        return times[0], times[1]

    def _setDelayExposureTime(self, delay, exposure,
                              delay_units, exp_units):
        if delay_units == 'ns':
            delay_base = 0
        elif delay_units == 'us':
            delay_base = 1
        elif delay_units == 'ms':
            delay_base = 2
        else:
            delay_base = 2
        
        if exp_units == 'ns':
            exp_base = 0
        elif exp_units == 'us':
            exp_base = 1
        elif exp_units == 'ms':
            exp_base = 2
        else:
            exp_base = 2

        status = self._api.setDelayExposureTime(delay, exposure,
                                                delay_base,
                                                exp_base)


    def _initBuffers(self, num_to_init=16):
        xres,yres = self._props['dimensions']
        self._buffers = []
        for i in range(0,num_to_init):
            self._buffers.append(np.zeros((xres*yres),dtype=np.uint16))
        for i in range(0,num_to_init):
            if self._buffersAllocated[i]:
                status, eHandler, self._buffers[i] = self._api.allocateBuffer(xres,yres,i)
                #self._bufferEvents[i] = eHandler
                print "Buffer size: ", (i, self._buffers[i].shape)
            else:
                status, eHandler, self._buffers[i] = self._api.allocateBuffer(xres,yres,-1)
                self._bufferEvents.append(eHandler)
                print "Buffer size: ", (i, self._buffers[i].shape)
                print "Init buff status: ", (i, status)
                print "Event: ", self._bufferEvents[i].value
            if status==0:
                self._buffersAllocated[i] = True

    def _initImages(self):
        self._fillBottom = True
        self._images = np.array([])

    def _addBuffers(self, start=0, end=16):
        xres,yres = self._props['dimensions']
        for i in range(start,end):
            if self._buffersAllocated[i]:
                self._api.addBuffer(0,0,i,xres,yres,self._bpp)
                self._buffersQueued[i] = True

    def addManyBuffers(self, total):
        self._initBuffers()
        i=0
        j=0
        xres,yres = self._props['dimensions']
        while i<total:
            err = self._api.addBuffer(0,0,j,xres,yres,self._bpp)
            if err != 0:
                print "error on ", i
                print "j=",j
                print "addBuffer error: ", err
            i += 1
            j += 1
            if j==16:
                j=0
        print "Pending buffers: ", self._buffersPending()

    def beginDAXRecording(self, filename):
        self.daxfile = writer.DaxFile(filename, self._props)
        self.recordedFrames = 0

    def endDAX(self):
        if self.daxfile != 0:
            self.daxfile.closeFile([0,0,0],0)
            print "Closing DAX file " + str(self.daxfile.filename)

    def writeMemoryToDAX(self, filename):
        self.beginDAXRecording(filename)
        print "Length of self._images: ", len(self._images)
        for i in range(0,len(self._images)):
            temp = self._images[i].astype(np.dtype('>H'))
            self.daxfile.saveFrames(temp.tostring(),1)
            self.recordedFrames += 1
        self.endDAX()    

    def captureFast(self, numImages):

        #Stop camera if it is recording
        if self._api.getRecordingState() > 0:
            self.stopRecording()
        else:
            self._api.removeBuffer()
        xres,yres = self._getResolution()

        #First need to create valid events
        err, event1, buf1 = self._api.allocateBuffer(xres,yres,-1)
        err, event2, buf2 = self._api.allocateBuffer(xres,yres,-1)

        #Add buffers to queue
        self._api.addBuffer(0,0,0,xres,yres,14)
        self._api.addBuffer(0,0,1,xres,yres,14)

        #Set recording to on to fill those two buffers:
        self._api.camlinkSetParams(xres,yres)
        self._api.armCamera()
        self._api.setRecordingState(0x0001)

        #Wait for 2nd buffer to fill, then close
        win32event.WaitForSingleObject(event1.value, 5000) #Waits for event1 or for 5 seconds

        #Stop recording
        self.stopRecording()

        #Fill with numImages:
        self._api.camlinkSetParams(xres,yres)
        self._api.armCamera()
        self._api.setRecordingState(0x0001)
        self.fastImages = self._api.largeBufferFill(xres,yres,numImages,events=[event1,event2])
        '''
        self.fastImages will be an array of np.uint16
        Dimensions of xres,yres,15,variable  (variable = totalnumberofframes/15)
        '''

        #Wait for event2:
        win32event.WaitForSingleObject(event2.value, 5000)

        self.stopRecording()

    def getFastImageFrame(self, frameNumber):
        yres = self.fastImages[0][0][0]._length_
        xres = self.fastImages[0][0]._length_
        print "Dimensions: ", [xres,yres]
        num1 = frameNumber/15
        num2 = frameNumber%15
        image = np.frombuffer(self.fastImages[num1][num2],dtype=np.uint16).reshape(yres,xres)
        print "max: ", image.max()
        print "min: ", image.min()
        return image

    def setInitFramesMP(self, frames):
        self.initFramesMP = frames
        

    def _transferOutOfBuffer(self, start=0, end=8, toDAX=False, verbose=False):
        global mpArray
        if verbose:
            print "Size of image buffer: ", len(self._images)
        #self._images = copy.deepcopy(self._buffers[start:end])
        if toDAX:
            for i in range(start,end):
                temp = self._buffers[i].astype(np.dtype('>H')).copy()
                self.daxfile.saveFrames(temp.tostring(),1)
                self.recordedFrames += 1
            self._images = np.array(self._buffers[start:end]).copy()
            #print "Shape of _images: ", self._images.shape
            return self.recordedFrames
        numImages = len(self._images)
        '''
        if self.image1 == 0:
            self.image2 = self.initFramesMP
        if numImages == 0:
            self._images = copy.deepcopy(self._buffers[start:end])
            globalImageBuffer = copy.deepcopy(self._buffers[start:end])
            self.p.start()
            self.image1 = 0
            self.image2 = self.initFramesMP
        else:
            self._images.extend(copy.deepcopy(self._buffers[start:end]))
            globalImageBuffer = copy.deepcopy(self._images)
            print "Length of globImageBuffer from inside: ", len(globalImageBuffer)
            if numImages > self.initFramesMP:
                if self.p.is_alive():  
                    self.q.put([self.image1,self.image2])
                    self.image1 = self.image2
                    self.image2 = numImages
        '''
        if len(self._images)==0:
            self._images = copy.deepcopy(self._buffers[start:end])
        else:
            self._images.extend(copy.deepcopy(self._buffers[start:end]))

        #arrData = self.mgr.Array('H',list(chain.from_iterable(self._buffers[start:end])),lock=False)

        if not self.subProcessStart and not self.p.is_alive():
            self.p.start()
            self.subProcessStart = True

        self.q.put(self._buffers[start:end])

        if not self.subProcess2Start:
            self.furtherAnalysis.start()
            self.subProcess2Start = True
            
        return numImages

    def flushImQ(self):
        while not self.qIms.empty():
            self.qIms.get()

    def endMP(self):
        print "in EndMP: ", mpArray
        self.q.put(None)
        #if not self.subProcess2Start:
        #    self.furtherAnalysis.start()
        self.subProcess2Start = True
        print "Ending q...\n"
        self.q.put(None)
        #self.q.close()
        time.sleep(3)
        #self.p.terminate()
        if self.furtherAnalysis.is_alive():
            self.furtherAnalysis.join()
        if self.p.is_alive():
            self.p.join()
        
        self.subProcessStart = False
        self.subProcess2Start = False
        #self.furtherAnalysis.terminate()
        #self.q.close()
        del self.mgr
        self.mgr = Manager()
        del self.q
        del self.resultsQueue
        #del self.resultsEvent
        self.q = self.mgr.Queue()
        self.resultsQueue = self.mgr.Queue()
        #self.resultsEvent = self.mgr.Event()
        del self.p
        self.p = Process(target=imageAnalysisTest3, args=(self.grabFrames,self.q,self.resultsQueue,self.qIms,))
        del self.furtherAnalysis
        self.furtherAnalysis = Process(target=useImageAnalysisResults, args=(self.emitSignalFrame,self.resultsQueue,self.resultsEvent,))
        

        #self.furtherAnalysis.start()
        #self.furtherAnalysis.join()

    def stateOfProcesses(self):
        print "imageAnalysisTesting process: ", self.p.is_alive()
        print "Further analysis proces: ", self.furtherAnalysis.is_alive()
        

    def imageAnalysisTest(self, conn):
        print "New process starting..."
        #images = conn.recv()
        #print "Got images. Length = ", len(images)
                                    

    def getImageBuffer(self):
        return self._images

    def _fillImages(self, toDAX=False):
        
        num_pending = self._buffersPending()
        nIms = -1
        if num_pending<=8:
            if self._fillBottom:
                nIms = self._transferOutOfBuffer(0,8,toDAX=toDAX)
                self._addBuffers(0,8)
            else:
                nIms = self._transferOutOfBuffer(8,16,toDAX=toDAX)
                self._addBuffers(8,16)
            self._fillBottom = not self._fillBottom
        return nIms, num_pending
        '''
        #print self._bufferEvents
        numIms = 0
        while numIms<400:
            if self._fillBottom:
                win32event.WaitForSingleObject(self._bufferEvents[8].value, 5000)
                nIms = self._transferOutOfBuffer(0,8,toDAX=toDAX)
                #self._addBuffers(0,8)
            else:
                win32event.WaitForSingleObject(self._bufferEvents[0].value, 5000)
                nIms = self._transferOutOfBuffer(8,16,toDAX=toDAX)
                #self._addBuffers(8,16)
            self._fillBottom = not self._fillBottom
            numIms = self._images.shape[0]
        return self._images.shape[0]
        '''
        
    def _saveImages(self):
        if self._images.shape[0] > 0:
            np.save("D:\\Data\\test_images_out.npy", self._images)

    def getNumberInImages(self):
        return self._images.shape[0]

    def _buffersPending(self):
        return self._api.getPendingBuffer()[1]

    def getImageForPreview(self):
        xres,yres = self._props['dimensions']
        pending = self._buffersPending()
        #print "Pending buffers: ", pending
        if pending < 2:
            im = self._buffers[self._alternatingBuffer].reshape(xres,yres)
            self._addBuffers(self._alternatingBuffer, self._alternatingBuffer+1)
            self._alternatingBuffer = 1 * (not self._alternatingBuffer)
            #print "Image returned for preview."
            return im
        else:
            return None
            
    def _freeBuffers(self):
        for i in range(0,16):
            if self._buffersAllocated[i]:
                self._api.freeBuffer(i)

    def beginPreview(self):
        if self._api.getRecordingState() > 0:
            self.stopRecording()
        xres,yres = self._getResolution()
        self._props['dimensions'] = xres,yres
        print "Resolution ", (xres, yres)
        self._api.camlinkSetParams(xres,yres)
        self._api.armCamera()
        self._initBuffers(2)
        self._addBuffers(0,2)
        self._api.setRecordingState(0x0001)
        print "Preview started..."

    def stopPreview(self):
        if self._api.getRecordingState() > 0:
            self.stopRecording()
        self._api.freeBuffer(0)
        self._api.freeBuffer(1)
        self._buffersAllocated[0] = False
        self._buffersAllocated[1] = False        

    def beginBufferFill(self):
        self.stopRecording()
        self._api.armCamera()
        self._initBuffers(16)
        self._addBuffers(0,16)
        #self.addManyBuffers(20)
        self._api.setRecordingState(0x0001)
        print "Recording started..."

    def stopRecording(self):
        self._api.setRecordingState(0x0000)
        self._api.removeBuffer()

    def shutDown(self):
        print 'Shutting down pco.edge camera...'
        self.stopRecording()
        self._freeBuffers()
        self._api.closeCamera()
        #self.furtherAnalysis.terminate()

