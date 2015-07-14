# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 13:38:01 2015

@author: Matt B Rowley
"""
import sys
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import Home_Manager_Ui


def main():
    window = Home_Manager_Ui.mainWindow()
    window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    window.showMaximized()
    return window

# Instantiate the application
app = QtGui.QApplication(sys.argv)

# Create the GUI and start the application
window = main()
app.exec_()
