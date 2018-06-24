#!/usr/bin/python

#
#	InControl's library
#
#	Joerg 01/2012
#

'''
This module is InControl's library for miscellaneous utilities.
'''


from PyQt5 import QtWidgets, QtCore
import functools
import threading
import sys
sys.path.append('D:\\Dan\\Programs\\InControl\\')
import numpy as np
import traceback
import os
import yaml
import importlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def import_module(path):
    '''
    Imports a module.

    :Parameters:
        *path*: str
            The path to the module relative to InControl's main directory in Python package
            style, e.g. 'andor.emccd.emccd'

    :Returns:
        *module*: module
            In instance of the imported module.
    '''
    file_m = path.split('.')[-1]
    return importlib.import_module(path)
    return __import__(path, globals(), locals(), [file_m], 0)


def get_device_path(device):
    return device['manufacturer'] + 2*('.' + device['model'])


def get_module_path(module):
    return 'modules' + 2*('.' + module)


def get_device_ui_path(name):
    return get_device_path(name) + '_ui'


def get_module_ui_path(name):
    return get_module_path(name) + '_ui'


def get_nested_attr(obj, attr):
    attributes = attr.split('.')
    for i in attributes:
        try:
            obj = getattr(obj, i)
        except AttributeError:
            raise
    return obj


def load_settings(path):
    file_settings = open(path)
    settings = yaml.load(file_settings)
    file_settings.close()
    return settings


class _UI:
    def __init__(self, control, design_path):
        self._control = control
        self._window = QtWidgets.QWidget()
        '''
        if design_path=='modules.testing.testing2_design':
            self._window = QtWidgets.QMainWindow()
            print "testing..."
        else:
            self._window = QtWidgets.QWidget()
            '''
        ui_module = import_module(design_path)
        self._ui = ui_module.Ui_Form()
        try:
            self._ui.setupUi(self._window)
        except:
            self._window = QtWidgets.QMainWindow()
            self._ui.setupUi(self._window)
        self._window.closeEvent = self._hide_window

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        event.accept()
        print("Drag enter event...")

    def dropEvent(self, event):
        print("Drop event...")

    def _hide_window(self, event):
            self._window.hide()
            event.ignore()

    def shutDown(self):
            pass

DeviceUI = _UI



class ModuleUI(_UI):
    def __init__(self, control, ui_control, design_path):
        _UI.__init__(self, control, design_path) # this is where the problem emerges
        self._ui_control = ui_control



class Device:
    def __init__(self, api_path, settings, *args):
        self._settings = settings
        api_module = import_module(api_path)
        api = api_module.API(*args)
        self._api = CommandQueue(api)


    def shutDown(self):
        ''' Shuts down the device. '''
        pass


class Module:
    def __init__(self, control, settings):
        self._control = control
        self._settings = settings

    def shutDown(self):
        pass



class CommandQueue:

    def __init__(self, control):

        self.__lock = threading.RLock()

        attributes = {}
        for attribute in dir(control):
            Obj = getattr(control, attribute)
            if callable(Obj):
                attributes[attribute] = functools.partial(self.__addTask, Obj)
            else:
                attributes[attribute] = Obj
        self.__dict__.update(attributes)

    def __addTask(self, function, *args, **kwargs):

        self.__lock.acquire()
        try:
            response = function(*args, **kwargs)
        except:
            etype, value, tb = sys.exc_info()
            print((''.join(traceback.format_exception(etype, value, tb))))
            response = None
        self.__lock.release()
        return response


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, figsize=(5,4), dpi=72):
        self.figure = Figure(figsize, dpi)
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MplCanvasAxes(MplCanvas):

    def __init__(self, parent=None, figsize=(5,4), dpi=72):
        MplCanvas.__init__(self, parent, figsize, dpi)
        self.axes = self.figure.add_subplot(111)
