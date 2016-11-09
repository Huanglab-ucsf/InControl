#!/usr/bin/python


import socket


class API:

    def send(self, message):
        print 'hal4000: Sending command:', message
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9000))
        s.send(message + '\n')
        response = self.waitForComplete(s)
        s.close()
        return response

    def waitForComplete(self, s):
        ack = ''
        while ack[-4:] != 'Ack\n':
            ack += s.recv(1)
        response = ''
        while response[-9:] != 'Complete\n':
            response += s.recv(1)
        print 'hal4000: Command completed.'
        response = response.splitlines()
        if len(response) > 1:
            return response[0]


