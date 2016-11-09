#!/usr/bin/python


import socket


class API:


    def send(self, message):
        print 'motorizer: Sending command:', message
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9001))
        s.send(message)
        s.close()

