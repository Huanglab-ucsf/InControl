import inLib
import time
import numpy as np
import libtim
import libtim.zern
from modules.adaptiveOptics import pupil_forInControl as pupil
import subprocess
from scipy.ndimage import rotate

class Control(inLib.Device):
    def __init__(self, settings):

        self.pixels = settings['pixels']
        self.segments = settings['segments']
        self.executable = settings['executable']

        self.mirror = Mirror(self.pixels, self.segments)

        self.pad_mirror = Mirror(self.pixels, self.segments)

        self.dummy_mirror = Mirror(256,12)
        self.setup_dummy_mirror()

        self._geometry = self.mirror.geometry

        self.tempfilename = 'mirrorSegs.txt'
        self.multiplier = 1.0

        self.preMultiplier = 80
        self.zernike = None
        self.group = []
        self.padding = False
        self.proc = None

    def getGeometry(self):
        return self._geometry

    def getGeoParams(self):
        '''Returns npixels, cx, cy'''
        return self.mirror.getGeo()

    def setup_dummy_mirror(self):
        pass

    def highlight_dummy_mirror_segs(self, segs):
        self.group = segs
        for i in range(len(segs)):
            self.dummy_mirror.addOffset(segs[i], 1)
        return self.dummy_mirror.pattern

    def clearDummyMirror(self):
        self.dummy_mirror.clear()

    def returnDummyMirror(self):
        return self.dummy_mirror.pattern, self.dummy_mirror.segOffsets
        

    def loadPattern(self, pattern_filename, mult=1.0):
        self.mirror.pattern = np.load(str(pattern_filename)) * mult
        return self.mirror.pattern

    def loadSegments(self, filename):
        msegs = np.loadtxt(filename) 
        self.mirror.inputMirrorSegs(msegs)
        
    def patternRot90(self):
        if self.mirror.pattern is not None:
            self.mirror.pattern = np.rot90(self.mirror.pattern)
        return self.mirror.pattern

    def patternFlipLR(self):
        if self.mirror.pattern is not None:
            self.mirror.pattern = np.fliplr(self.mirror.pattern)
        return self.mirror.pattern

    def patternFlipUD(self):
        if self.mirror.pattern is not None:
            self.mirror.pattern = np.flipud(self.mirror.pattern)
        return self.mirror.pattern

    def patternRotate(self, deg):
        if self.mirror.pattern is not None:
            self.mirror.pattern = rotate(self.mirror.pattern, deg)
        return self.mirror.pattern

    def pokeGroup(self, group, offset, quiet=False):
        for s in group:
            self.pokeSegment(s, offset)
            
    def pokeSegment(self, seg, value, pokeAll = False):
        '''
        Add value to a given segment or to all segments
        '''
        if pokeAll:
            self.mirror.addOffset(-1,value)
        else:
            self.mirror.addOffset(seg,value)

    def reconfigGeo(self, cx, cy, npixels):
        self.mirror.initGeo(npixels)
        half_px = npixels/2
        if self.mirror.pattern is not None:
            if self.mirror.pattern.shape[0] > npixels:
                pattern = self.mirror.pattern[cx-half_px:cx+half_px,
                                              cy-half_px:cy+half_px]
                if (pattern.shape[0] == npixels) and (pattern.shape[1]==npixels):
                    self.mirror.pattern = pattern.copy()
                else:
                    print("Problem cropping pattern for DM.")
            if self.mirror.pattern.shape[0] < npixels:
                pattern = np.zeros((npixels,npixels))
                origShape = self.mirror.pattern.shape[0]
                pattern[cx-origShape/2:cx+origShape/2, cy-origShape/2:cy+origShape/2] = self.mirror.pattern
                self.mirror.pattern = pattern.copy()
        self._geometry = self.mirror.geometry
        return self.returnPattern()

    def padZeros(self, border, always=False):
        '''
        Pad pattern with zeros
        '''
        currentPixels = self.mirror.pattern.shape[0]
        newPattern = np.zeros((currentPixels+2*border, currentPixels+2*border))
        newPattern[border:-1*border,border:-1*border] = self.mirror.pattern
        self.mirror.initGeo(newPattern.shape[0])
        self.mirror.setPattern(newPattern)
        return self.returnPattern()

    def findSegments(self):
        self.mirror.findSegOffsets()

    def setMultiplier(self,mult):
        self.multiplier = mult

    def setPreMultiplier(self,mult):
        self.preMultiplier = mult

    def getSegments(self):
        return self.mirror.returnSegs()
        #return self.mirror.segOffsets

    def returnSegments(self):
        return self.mirror.returnSegs()
        #return self.mirror.segOffsets

    def returnPattern(self):
        return self.mirror.pattern

    def clear(self):
        self.mirror.clear()

    def setZernMode(self, mode):
        self.zernMode = mode
    
    def calcZernike(self, mode, amp, radius=None, useMask=True):
        if radius is None:
            radius = self.mirror.nPixels/2
        modes = np.zeros((mode))
        modes[mode-1]=amp
        self.zernike = libtim.zern.calc_zernike(modes, radius, mask=useMask,
                                                zern_data = {})
        return self.zernike

    def addZernike(self, zernike_pattern=None):
        if zernike_pattern is not None:
            zern = zernike_pattern
        else:
            if self.zernike is None:
                return 0
            else:
                zern = self.zernike
        if self.zernike is not None:
            p=self.mirror.addToPattern(zern * self.preMultiplier)
        return self.returnPattern()


    def advancePipe(self):
        print("The process:", self.proc)
        if self.proc is not None:
            print(self.proc.communicate())
            self.proc = None


    def applyToMirror(self, wtime=-1):
        #First save mirror
        self.mirror.outputSegs(self.tempfilename)
        wTimeStr = str(wtime)
        self.proc = subprocess.Popen([self.executable, self.tempfilename, str(self.multiplier),"1", wTimeStr] , stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        
        for ir in range(11):
            line = self.proc.stdout.readline()
            dec_line = line.rstrip().decode()
            print(dec_line)
            if line == '':
                print('Finished reading.')
                break
        print("The pattern is added to the mirror.")

# ---------------------------------The class of Deformable Mirror--------------------------

class Mirror():
    def __init__(self, nPixels, nSegments, pattern=None):

        if pattern is None:
            self.pattern = np.zeros((nPixels,nPixels))
        else:
            self.pattern = pattern

        self.nPixels = nPixels
        self.nSegments = nSegments

        self.segOffsets = np.zeros((nSegments, nSegments))
        self.segTilts = np.zeros((nSegments, nSegments))

        #self.setPupilGeometry(nPixels/2,nPixels/2,nPixels)

        self.initGeo(self.nPixels)

    def initGeo(self, npixels):
        self.nPixels = npixels
        self.borders = np.linspace(0,self.nPixels,num=self.nSegments+1).astype('uint16')
        self.pixInSeg = self.borders[1]-self.borders[0]
        self.setPupilGeometry(npixels/2, npixels/2, npixels)
        

    def setPupilGeometry(self, cx, cy, d):
        '''
        Sets geometry on pixellated grid
        '''
        self.geometry = pupil.Geometry((self.nPixels,
                                         self.nPixels),
                                        cx,cy,d)

    def getGeo(self):
        return [self.geometry.nx, self.geometry.cx, self.geometry.cy]


    def setPattern(self, data):
        self.pattern = data.copy()
        return self.pattern

    def addToPattern(self, data):
        if self.pattern.shape == data.shape:
            self.pattern += data
        elif data.shape < self.pattern.shape:
            diffx = self.pattern.shape[0] - data.shape[0]
            diffy = self.pattern.shape[1] - data.shape[1]
            if diffx != diffy:
                print("Mirror.addToPattern: Something's not square...")
            else:
                border = diffx/2
                self.pattern[border:-1*border,border:-1*border] += data
        else:
            print("Mirror.addToPattern: Shape mismatch...")
            print("Mirror.addToPattern: Data to add has shape: ", data.shape)
            print("Mirror.addToPattern: Pattern  has shape: ", self.pattern.shape)
        return self.pattern
        

    def whereSegment(self, seg):
        temp = np.zeros_like(self.pattern)
        unraveled = np.unravel_index(seg, [self.nSegments, self.nSegments])
        xStart = self.borders[unraveled[0]]
        xStop = self.borders[unraveled[0]+1]
        yStart = self.borders[unraveled[1]]
        yStop = self.borders[unraveled[1]+1]
        temp[xStart:xStop,yStart:yStop] = -1
        return np.where(temp==-1)

    def addOffset(self, seg, value):
        #print "adding %i to segment %i." % (value,seg)
        if seg<0:
            self.segOffsets += value
            self.pattern += value
        else:
            unraveled = np.unravel_index(seg, [self.nSegments, self.nSegments])
            self.segOffsets[unraveled[0],unraveled[1]] += value
            w = self.whereSegment(seg)
            self.pattern[w] += value

    def findSegOffsets(self):
        for i in range(self.nSegments*self.nSegments):
            w = self.whereSegment(i)
            av = np.mean(self.pattern[w])
            unraveled = np.unravel_index(i, [self.nSegments, self.nSegments])
            self.segOffsets[unraveled[0],unraveled[1]]=av

    def findTilt(self, tilt):
        temp = tilt * np.arange(self.pixInSeg)
        toAdd = temp.repeat(self.pixInSeg).reshape(self.pixInSeg,self.pixInSeg)
        return toAdd

    def addXTilt(self, seg, tilt):
        w = self.whereSegment(seg)
        toAdd = self.findTilt(tilt)
        print("toAdd shape:", toAdd.shape)
        print("pattern segment shape:", self.pattern[w].shape)
        self.pattern[w] += toAdd
        
    def addYTilt(self, seg, tilt):
        w = self.whereSegment(seg)
        toAdd = self.findTilt(tilt)
        self.pattern[w] += toAdd.swapaxes(0,1)


    def clear(self):
        self.pattern = np.zeros((self.nPixels,self.nPixels))
        self.segOffsets = np.zeros((self.nSegments, self.nSegments))

    def addZernikes(self, zernModes, clear_first = False):
        if clear_first:
            self.clear()
        z = self.calcZernikes(self, zernModes)
        self.pattern += z
        self.findSegOffsets()

    def pokeSegment(self, seg, amount):
        '''
        pokeSegment #seg
        '''
        pass

    def outputSegs(self, filename):
        print("Filename:", filename)
        allSegments = self.segOffsets.astype(np.int16).flatten()
        forMirror = np.zeros((160),dtype=np.int16)
        forMirror[0:10] = allSegments[1:11]
        forMirror[10:130] = allSegments[12:132]
        forMirror[130:140] = allSegments[133:143]
        segs = np.append(forMirror, np.zeros((16),dtype=np.int16))

        np.savetxt(filename, segs, fmt='%i', delimiter="\r\n", newline = " ")
        return segs

    def inputMirrorSegs(self, msegs):
        print(msegs.shape)
        newSegs = np.zeros((144))
        newSegs[1:11] = msegs[0:10]
        newSegs[12:132] = msegs[10:130]
        newSegs[133:143] = msegs[130:140]
        self.segOffsets = newSegs.reshape(12,12)

    def returnSegs(self):
        return self.segOffsets

        
#++++++++++++++++++++++++++++++++ The test function +++++++++++++++++++++++++++++
        
if __name__ == "__main__":

    pixels = 512
    segments = 12
    toSaveDir = "Z:\\Ryan\\BMC_Mirror\\seg\\"
    m = Mirror(pixels, segments)
    allFiles = []
    for i in range(0,segments*segments):
        m.addOffset(i,1000)
        fname = toSaveDir+"poked"+str(i).zfill(3)+".txt"
        m.outputSegs(fname)
        allFiles.append(fname)
        m.clear()
