#!/usr/bin/python


import inLib


class Control(inLib.Device):
    '''
    The device control for the Motorizer.
    '''

    def __init__(self, settings):
        inLib.Device.__init__(self, 'huangLab.motorizer.motorizer_api', settings)


    def setOD(self, od):
        '''
        Sets the OD of a 'Motorizer'-controlled filter wheel.

        :Parameters:
            *od*: float
                The OD to which the filter wheel should turn. Accepts
                only ODs given in the settings file.
        '''
        if od in self._settings['ODs']:
            index = self._settings['ODs'].index(od)
            self._api.send('filter={0}'.format(index))
        else:
            print 'motorizer: Invalid OD. Available:', self._settings['ODs']


    def setTIRF(self, position):
        '''
        Sets the OD of a 'Motorizer'-controlled TIRF stage.

        :Parameters:
            *position*: float
                The new TIRF stage position.
        '''
        self._api.send('tirpos={0:05.2f}'.format(position))


    def stepTIRF(self, amount):
        '''
        Steps a 'Motorizer'-controlled TIRF stage.

        :Parameters:
            *amount*: '-', '--', '+' or '++'
                '-' and '--': decrease by 0.02 mm or 0.1 mm, respectively.
                '+' and '++' works accordingly as increase.
        '''
        if amount in ['-', '--', '+', '++']:
            self._api.send('tirpos'+amount)
        else:
            print "motorizer: Invalid amount. Use '-', '--', '+'  or '++'."
