#!/usr/bin/python


import inLib
import serial 


class Control(inLib.Device):
    def __init__(self,settings):
        print('Initializing filter wheels.')
        port = settings['port']
        inLib.Device.__init__(self, 'arduino.arduino_API', settings, port)



