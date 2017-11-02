#!/usr/bin/python

from PyQt5 import QtCore,QtWidgets


class dropWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.__class__.dragEnterEvent = self.dragEnterEvent
        self.__class__.dragMoveEvent = self.dragEnterEvent
        self.__class__.dropEvent = self.dropEvent
        self.setAcceptDrops(True)

        print("initialized dropWidget...")

        self.show()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        event.accept()
        print("Drag enter event...")

    def dropEvent(self, event):
        print("Drop event...")

    
