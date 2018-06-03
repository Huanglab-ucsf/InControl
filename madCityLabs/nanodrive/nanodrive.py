#!/usr/bin/python


import inLib
import numpy as np
import time


class Control(inLib.Device):
    
    def __init__(self, settings):
        inLib.Device.__init__(self, 'madCityLabs.nanodrive.nanodrive_api', settings)
        self._toPrint = True
        # Store axis ranges:
        self._axis_range = [0,
                           self._api.getCalibration(1),
                           self._api.getCalibration(2),
                           self._api.getCalibration(3)]
        # Move to center positions:
        if self._settings['n_axis'] in (1,3):
            if 'initial_z' in self._settings:
                self.moveTo(3,self._settings['initial_z'])
            else:
                self.moveTo(3, self._axis_range[3]/2.0)
        if self._settings['n_axis'] in (2,3):
            self.moveTo(1, self._axis_range[1]/2.0)
            self.moveTo(2, self._axis_range[2]/2.0)

        

    def _axisCheck(self, axis):
        if axis in (1,2) and self._settings['n_axis'] in (2,3):
            return True
        if axis == 3 and self._settings['n_axis'] in (1,3):
            return True
        print('piezo: Warning! Invalid axis number.')
        return False

    def _positionCheck(self,axis,position):
        if (position >= 0) & (position <= self._axis_range[axis]):
            return True
        else:
            print('piezo: Warning! Invalid position.')


    def shutDown(self):
        '''Shuts down the stage.'''
        self._api.releaseHandle()


    def moveTo(self, axis, position, waitForConvergence=True):
        '''
        Moves an axis to a position. It checks if the axis is valid and if the new position
        is within the range of the axis.

        :Parameters:
            *axis*: int
                The axis index (1,2 or 3).
            *position*: float
                The new position in micrometers.
        '''
        if self._axisCheck(axis) and self._positionCheck(axis, position):
            if self._toPrint:
                print('piezo: Moving axis {0} to {1} um.'.format(axis, position))
            self._api.singleWriteN(position,axis)
            pos = self._api.singleReadN(axis)
            print("New Position:", pos)
            if waitForConvergence:
                self._waitUntilConverge(axis)


    def getPosition(self, axis):
        '''
        Probes the position of an axis.

        :Parameters:
            *axis*: int
                The axis index (1,2 or 3).

        :Returns:
            *position*: float
                The position of the axis in micrometers.
        '''
        if self._axisCheck(axis):
            return self._api.singleReadN(axis)
        else:
            return None


    def getAxisRange(self):
        '''

        :Returns:
            *axis_range*: list
                A list with four items. The item with index 0 is redundant, items with indices
                1,2 and 3 are the ranges of the respective axis.
        '''
        return self._axis_range


    def step(self, axis, step, verbose = True):
        '''
        Performs a step movement of an axis.

        :Parameters:
            *axis*: int
                The axis index (1,2 or 3).
            *step*: float
                The stepsize in micrometers, can be negative.
        '''
        position = self.getPosition(axis)+step
        self.moveTo(axis,position)
        if(verbose):
            position = self.getPosition(axis)
            print("")


    def getNAxis(self):
        '''

        :Returns:
            *nAxis*: int
                The number of axis of this device.
        '''
        return self._settings['n_axis']


    def moveHomeXY(self):
        ''' Moves axis 1 and 2 home, which is the center of the axis ranges. '''
        self.moveTo(1,self._axis_range[1]/2.0)
        szzelf.moveTo(2,self._axis_range[2]/2.0)


    def moveHomeZ(self):
        ''' Moves axis 3 home, which is the center of the axis range. '''
        self.moveTo(3,self._axis_range[3]/2.0)


    def _waitUntilConverge(self, axis):
        if self._toPrint:
            print('piezo: Waiting until axis {0} position converges.'.format(axis))
        positions = np.array(self.getPosition(axis))
        time.sleep(self._settings['response_time'])
        positions = np.append(positions, self.getPosition(axis))
        m = np.std(positions)
        i = 0
        while m > self._settings['precision']:
            positions = np.append(positions, self.getPosition(axis))
            m = np.std(positions[-5:])
            i += 1
            if self._toPrint:
                print('piezo: Axis {0} standard deviation: {1}'.format(axis, m))
            time.sleep(self._settings['response_time'])

