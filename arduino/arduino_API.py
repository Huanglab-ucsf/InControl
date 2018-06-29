# Created by Dan on 06/29/2018
import time
import serial

class API():
    def __init__(self, port, timeout = None):
        ser = serial.Serial()
