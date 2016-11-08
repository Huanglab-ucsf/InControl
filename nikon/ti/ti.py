#!/usr/bin/python
import sys
import os
sys.path.append(os.getcwd())

import inLib
import time
import numpy as np


class Control(inLib.Device):
    '''
    The device control for a Nikon Ti Eclipse microscope. An instance of this class will
    contain sub-classing for present accessories. For example, if an instance of this class
    is called *scope*, the PFS accessory can be accessed by calling *scope.PFS*.
    '''

    def __init__(self, settings):
        inLib.Device.__init__(self, 'nikon.ti.ti_api', settings)
       
        if self._api.isMounted('zDrive'):
            self.zDrive = Positioner(self._api, 'zDrive')
        if self._api.isMounted('PFS'):
            self.PFS = Positioner(self._api, 'PFS')

        self._zCalibration = None


    def calibrateFocalPlanePosition(self, max_depth, simulation=False):
        '''
        If a PFS is present, this function calibrates the PFS offset to the focal plane position
        above the coverslip. When this function is called, the PFS has to be enabled and the objective
        has to focus on the coverslip.

        :Parameters:
            *max_depth*: float
                The maximal depth into the sample to which the calibration should be performed.
                The unit is the same as the unit of the zDrive (see 
                :func:`Positioner.getUnit`).

        :Returns:
            *zCalibration*: tuple
                A tuple with three elements: 1) a list of the PFS offsets of the
                calibration curve, 2) a list of the focal plane positions of the calibration curve,
                3) *p*, a numpy.poly1d instance. For any PFS offset within [0, *max_depth*], the focal
                plane position can be retrieved with p(offset).
        '''
        z = [0]
        PFS_position = [self.PFS.getPosition()]
        print 'scope: PFS position:', PFS_position[-1]
        print 'scope: Focal plane position:', z[-1]
        zDrive_coverglass = self.zDrive.getPosition()
        while z[-1] <= max_depth:
            self.PFS.moveRelative(100)
            if simulation:
                self.zDrive.moveRelative(0.1)
            time.sleep(1.0)
            PFS_position.append(self.PFS.getPosition())
            z.append(self.zDrive.getPosition() - zDrive_coverglass)
            print 'scope: PFS position:', PFS_position[-1]
            print 'scope: Focal plane position:', z[-1]
        coeffs = np.polyfit(PFS_position, z, 7)
        z_pol = np.poly1d(coeffs)
        self._zCalibration = (PFS_position, z, z_pol)
        self.PFS.setPosition(PFS_position[0])
        return self._zCalibration


    def getFocalPlanePosition(self):
        '''
        Retrieves the current focal plane position above the coverslop.

        :Returns: float or None
            The focal plane position if a calibration was done with :func:`calibrateFocalPlanePosition`,
            None otherwise.
        '''
        if self._zCalibration:
            PFS, z, z_pol = self._zCalibration
            PFS_current = self.PFS.getPosition()
            return z_pol(PFS_current)
        else:
            return None


    def getFocalPlaneCalibration(self):
        '''
        :Returns: tuple
            The same tuple as :func:`calibrateFocalPlanePosition` for a previously performed
            calibration.
        '''
        return self._zCalibration


    def shutDown(self):
        ''' Shuts down the connection to the Nikon Ti microscope. '''
        self._api.shutDown()




class Positioner:
    ''' A class for any one-dimensional positioners in a Nikon Ti microscope, e.g. PFS or zDrive. '''
    def __init__(self, api, name):
        self._api = api
        self._name = name
        self._scale = self._api.getScale(self._name)
        self._offset = self._api.getOffset(self._name)
        self._unit = self._api.getUnit(self._name)


    def getPosition(self):
        '''
        Returns the position of the accessory.
        
        :Returns:
            *position*: int or float
                The current position of the accessory in units of the
                accessory's DisplayString (see Nikon Ti docs for more
                information). Use :func:`getUnits` to retrieve the unit.
        '''
        raw = self._api.getPosition(self._name)
        return self._scale*raw + self._offset


    def getUnit(self):
        ''' Returns the units of the accessory. '''
        return self._unit


    def setPosition(self, position):
        '''
        Sets the position of the accessory.

        :Parameters:
            *position*: int or float
                The postion to which the accessory should move in units
                of the accessory's DisplayString (see Nikon Ti docs for
                more information). Use :func:`getUnits` to retrieve the unit.
        '''
        raw = int(round((position - self._offset)/self._scale))
        self._api.setPosition(self._name, raw)


    def moveRelative(self, step):
        '''
        Moves the accessory relative to its current position.

        :Parameters:
            *step*: int or float
                The step by which the accessory should move. Use :func:`getUnits`
                to retrieve the units used for this positioner.
        '''
        current = self.getPosition()
        self.setPosition(current + step)


if __name__ == '__main__':
    control = Control({})
    print control.PFS.getPosition()
    print control.zDrive.getPosition()
    control.PFS.moveRelative(200)
    print control.PFS.getPosition()
    print control.zDrive.getPosition()

    control.shutDown()
