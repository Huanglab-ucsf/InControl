"""
Last modification: 11/01/2016 by Dan.
# simulate the deformable mirror
# No calculation for the pupil function
"""

import numpy as np
import libtim.zern as lzern
from scipy.ndimage import interpolation

# ---------------Below is a simulation of deformable mirror
class DM(object):

    def __init__(self, nseg = 12, nPixels = 256, pattern=None, mask = False):
        self.nSegments = nseg
        self.nPixels = nPixels
        self.radius = nPixels/2
        self.DMsegs = np.zeros((self.nSegments, self.nSegments))
        self.borders = np.linspace(0,self.nPixels,num=self.nSegments+1).astype(int)
        self.useMask = mask

        if pattern is None:
            self.pattern = np.zeros((nPixels,nPixels))
        else:
            """
            scale up or down the pattern
            """
            zoom = 256./np.float(pattern.shape[0])
            MOD = interpolation.zoom(pattern,zoom,order=0,mode='nearest')
            self.pattern = MOD


    def findSeg(self):
        for ii in np.arange(self.nSegments):
            for jj in np.arange(self.nSegments):
                xStart = self.borders[ii]
                xEnd = self.borders[ii+1]
                yStart = self.borders[jj]
                yEnd = self.borders[jj+1]

                av = np.mean(self.pattern[xStart:xEnd, yStart:yEnd])
                self.DMsegs[ii,jj] = av

        DMsegs = np.copy(self.DMsegs) # create a copy of self.segs
        return DMsegs


    def readSeg(self, raw_seg):
        """
        load a 1-d array and represent it with a segments
        return a matrix
        """
        seg=raw_seg[:140]
        seg = np.insert(seg,0,0)
        seg = np.insert(seg,11,0)
        seg = np.insert(seg,132,0)
        seg = np.insert(seg, 143, 0)
        rseg = np.flipud(seg.reshape(self.nSegments,self.nSegments).transpose())
        return rseg


    def zernSeg(self, z_ampli):
        """
        Take amplitudes of zernike modes and synthesize into a pattern;
        convert into segment patterns.
        """
        self.pattern = lzern.calc_zernike(z_ampli, self.radius, mask = self.useMask, zern_data = {})
        self.findSeg()
        # done with zernSeg

    def setPattern(self, newPattern):
        """
        update Pattern with new pattern
        """
        self.pattern = newPattern.copy()
    # done with setPattern


    def clearPattern(self):
        """
        clear the pattern.
        """
        self.pattern[:] = 0
        print("Pattern cleared.")
        # done with clearPattern

    def exportSegs(self, filename):
        allSegments = self.DMsegs.astype(np.int16).flatten()
        forMirror = np.zeros((160),dtype=np.int16)
        forMirror[0:10] = allSegments[1:11]
        forMirror[10:130] = allSegments[12:132]
        forMirror[130:140] = allSegments[133:143]
        segs = np.append(forMirror, np.zeros((16),dtype=np.int16))
        #segs = np.append(self.segOffsets.astype(np.int16).flatten(),np.zeros((16),dtype=np.int16))
        np.savetxt(filename, segs, fmt='%i', delimiter='\n')


    def getPattern(self):
        return self.pattern
        # done with getPattern

    def getSegs(self):
        return self.DMsegs
        # done with getSegs



    #---------------------------OK it's still good to add some visualizetion function. ------------------------



"""
The following codes are just for testing the function
"""

def main():
    pass

if __name__ =="__main__":
    main()
