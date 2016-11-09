#!/usr/bin/python


import comtypes.client
import threading
import Queue


class API(object):
    def __init__(self):
        # Multithreading support for COM objects is complicated.
        # Therefore, we run the Ti COM in a seperate thread and communicate
        # thread-safe through a queue:
        self._cmdQ = Queue.Queue()
        self._runner = threading.Thread(target=self._run, args=(self._cmdQ,))
        self._runner.start()

    def getPosition(self, obj):
        returnQ = Queue.Queue()
        self._cmdQ.put(('getPosition', obj, returnQ))
        return returnQ.get()

    def getScale(self, obj):
        returnQ = Queue.Queue()
        self._cmdQ.put(('getScale', obj, returnQ))
        return returnQ.get()

    def getOffset(self, obj):
        returnQ = Queue.Queue()
        self._cmdQ.put(('getOffset', obj, returnQ))
        return returnQ.get()
    
    def getUnit(self, obj):
        returnQ = Queue.Queue()
        self._cmdQ.put(('getUnit', obj, returnQ))
        return returnQ.get()

    def isMounted(self, obj):
        returnQ = Queue.Queue()
        self._cmdQ.put(('isMounted', obj, returnQ))
        return returnQ.get()

    def setPosition(self, obj, position):
        self._cmdQ.put(('setPosition', obj, position))

    def shutDown(self):
        self._cmdQ.put(('stop',))
        self._runner.join()

    def _run(self, cmdQ):
        active = True
        comtypes.CoInitialize()
        ti = comtypes.client.CreateObject('Nikon.TiScope.NikonTi')

        while active:
            cmd = cmdQ.get()

            if cmd[0] == 'getPosition':
                obj, returnQ = cmd[1:3]
                obj = getattr(ti, obj)
                # Due to a quirk in the Ti SDK, the zDrive position does not
                # update when PFS is engaged. A call to isMounted solves it though.
                if obj.isMounted.RawValue:
                    returnQ.put(obj.Position.RawValue)
                else:
                    returnQ.put(None)

            elif cmd[0] == 'getScale':
                obj, returnQ = cmd[1:3]
                obj = getattr(ti, obj)
                returnQ.put(obj.Position.DisplayScale)

            elif cmd[0] == 'getOffset':
                obj, returnQ = cmd[1:3]
                obj = getattr(ti, obj)
                returnQ.put(obj.Position.DisplayOffset)

            elif cmd[0] == 'getUnit':
                obj, returnQ = cmd[1:3]
                obj = getattr(ti, obj)
                returnQ.put(obj.Position.Unit)

            elif cmd[0] == 'isMounted':
                obj, returnQ = cmd[1:3]
                obj = getattr(ti, obj)
                returnQ.put(obj.isMounted.RawValue)

            elif cmd[0] == 'setPosition':
                obj, position = cmd[1:3]
                obj = getattr(ti, obj)
                obj.Position.RawValue = position

            elif cmd[0] == 'stop':
                active = False
                del ti
                comtypes.CoUninitialize()

            else:
                print 'Nikon Ti API: Do not understand command:', cmd
