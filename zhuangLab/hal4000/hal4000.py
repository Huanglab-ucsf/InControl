#!/usr/bin/python


import inLib
import json


class Control(inLib.Device):
    '''
    The device control for Hazen Babcock's HAL4000.
    '''

    def __init__(self, settings):
        inLib.Device.__init__(self, 'zhuangLab.hal4000.hal4000_api', settings)


    def abortMovie(self):
        ''' Aborts a running movie. '''
        self._api.send('abortMovie')


    def getStagePosition(self):
        '''
        Retrieves the current position of Hal4000's stage.

        :Returns:
            *position*: list
                The coordinate list of the current position, commonly
                as [x, y, z].
        '''
        return json.loads(self._api.send('getStagePosition'))


    def getWorkingDirectory(self):
        '''
        Retrieve Hal4000's current working directory.

        :Returns:
            *directory*: str
        '''
        return self._api.send('getWorkingDirectory')


    def findSum(self):
        self._api.send('findSum')


    def incPower(self, channel, increment):
        '''
        Increase the power of an illumination channel.

        :Parameters:
            *channel*: int
                The channel number. To figure out which number corresponds
                to a channel, take a look at Hal4000's illumination user interface.
                The channel numbers are counted from left, starting with 0.
            *increment*: float
                The power increment on the scale of the unit interval (0, 1.0),
                where 1.0 is maximum power.
        '''
        self._api.send('incPower,{0},{1}'.format(channel, increment))


    def moveTo(self, position):
        '''
        Moves Hal4000's stage.

        :Parameters:
            *position*: tuple of floats
                A three-dimensional position as in (x, y, z).
        '''
        x, y, z = position
        self._api.send('moveTo,{0},{1}'.format(x, y))


    def movie(self, name, length):
        '''
        Records a STORM movie.

        :Parameters:
            *name*: str
                The name of the movie, which will be use for saving
                the data in the working directory.
            *length*: int
                The length of the movie in frames.
        '''
        self._api.send('movie,{0},{1}'.format(name, length))


    def parameters(self, index):
        '''
        Chooses a pre-loaded Hal4000 settings file.

        :Parameters:
            *index*: int
                The index of the settings file as in the list of the
                user interface, counting from top to bottom, starting
                with 0.
        '''
        self._api.send('parameters,{0}'.format(index))


    def recenterPiezo(self):
        self._api.send('recenterPiezo')


    def setLockTarget(self, target):
        self._api.send('setLockTarget,{0}'.format(target))


    def setPower(self, channel, power):
        '''
        Sets the power of an illumination channel.

        :Parameters:
            *channel*: int
                The illumination channel number. See :func:`incPower` for
                more details.
            *power*: float
                The new power in the interval (0, 1.0), where 1.0 is the
                maximal power.
        '''
        self._api.send('setPower,{0},{1}'.format(channel, power))


    def setRunShutters(self, flag):
        '''
        Controls whether the shutter sequence should be used when
        recording a movie.

        :Parameters:
            *flag*: bool
                If *True*, shutters will be used, if *False*, not.
        '''
        self._api.send('setRunShutters,{0}'.format(flag))


    def toggleChannel(self, channel, flag):
        '''
        Turns an illumination channel on or off.

        :Parameters:
            *channel*: int
                The illumination channel number. See :func:`incPower` for
                more details.
            *flag*: bool
                If *True*, channel is turned on, if *False*, it is turned off.
        '''
        self._api.send('toggleChannel,{0},{1}'.format(channel, flag))
