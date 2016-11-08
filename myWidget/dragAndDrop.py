#!/usr/bin/python

from PyQt4 import QtCore,QtGui,Qwt5


class dropWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.__class__.dragEnterEvent = self.dragEnterEvent
        self.__class__.dragMoveEvent = self.dragEnterEvent
        self.__class__.dropEvent = self.dropEvent
        self.setAcceptDrops(True)

        print "initialized dropWidget..."

        self.show()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        event.accept()
        print "Drag enter event..."

    def dropEvent(self, event):
        print "Drop event..."

    
