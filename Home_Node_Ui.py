# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 13:40:44 2015

@author: Matt B Rowley
"""

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import sys
import time
import os
import json


class mainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setFont(button_font)
        self.setWindowTitle("Home Node Controller")
        self.frames = QtGui.QStackedWidget(self)
        self.frames.addWidget(homeFrame(self))
        self.frames.addWidget(plantsFrame(self))
        # self.home_frame = homeFrame(self)
        # self.plants_frame = plantsFrame(self)
        self.setCentralWidget(self.frames)
        signals.frame_change.connect(self.changeFrame)
        self.frames_dict = {"home": 0,
                            "plants": 1}

    def changeFrame(self):
        global frame_mutex
        set_frame = self.frames_dict[frame_mutex.read()]
        self.frames.setCurrentIndex(set_frame)

    def closeEvent(self, evt):
        QtGui.QMainWindow.closeEvent(self, evt)


class homeFrame(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.generateObjects()

    def generateObjects(self):
        self.vertical_layout = QtGui.QVBoxLayout(self)
        self.title_layout = QtGui.QHBoxLayout()
        self.name_layout = QtGui.QVBoxLayout()
        self.name_label = QtGui.QLabel(self)
        self.name_label.setFont(QtGui.QFont("Aegyptus", pointSize=60))
        self.name_label.setText("Rowley Family")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label = QtGui.QLabel(self)
        self.title_label.setFont(QtGui.QFont("Brill", pointSize=40))
        self.title_label.setText("Home Node Controller")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.title_label)
        self.title_layout.addLayout(self.name_layout)
        self.title_layout.addWidget(verticalLine(self))
        self.clock_label = clockWidget(self)
        self.title_layout.addWidget(self.clock_label)
        self.vertical_layout.addLayout(self.title_layout)
        self.vertical_layout.addWidget(horizontalLine(self))
        self.vertical_layout.addItem(verticalSpacer())
        self.plants_button = frameButton("plants", self)
        self.plants_button.setText("Plants")
        self.vertical_layout.addWidget(self.plants_button)
        self.vertical_layout.addItem(verticalSpacer())


class verticalSpacer(QtGui.QSpacerItem):

    def __init__(self):
        QtGui.QSpacerItem.__init__(self, 20, 20, QtGui.QSizePolicy.Minimum,
                                   QtGui.QSizePolicy.Expanding)


class horizontalSpacer(QtGui.QSpacerItem):

    def __init__(self):
        QtGui.QSpacerItem.__init__(self, 20, 20, QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Minimum)


class verticalLine(QtGui.QFrame):

    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setFrameShape(QtGui.QFrame.VLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)


class horizontalLine(QtGui.QFrame):

    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.setFrameShape(QtGui.QFrame.HLine)
        self.setFrameShadow(QtGui.QFrame.Sunken)


class homeButton(QtGui.QPushButton):

    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)
        self.home_icon = QtGui.QIcon(QtGui.QPixmap("Images/home.png"))
        self.setIcon(self.home_icon)
        self.clicked.connect(self.goHome)
        self.target_frame = "home"

    def goHome(self):
        global frame_mutex, signals
        frame_mutex.write(self.target_frame)
        signals.frame_change.emit()


class frameButton(QtGui.QPushButton):

    def __init__(self, target_frame, parent=None):
        QtGui.QPushButton.__init__(self, parent)
        self.setText("frameButton")
        self.target_frame = target_frame
        self.clicked.connect(self.gotoFrame)

    def gotoFrame(self):
        global frame_mutex, signals
        frame_mutex.write(self.target_frame)
        signals.frame_change.emit()


class plantsFrame(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        with open('plants.json') as plant_file:
            self.plants = json.load(plant_file)
        self.layout = QtGui.QVBoxLayout(self)
        self.plants_layout = QtGui.QHBoxLayout(self)
        for i, plant in enumerate(self.plants):
            plant_widget = plantWidget(i, self.plants, self)
            self.plants_layout.addWidget(plant_widget)
            if i < len(self.plants)-1:
                self.plants_layout.addWidget(verticalLine(self))
        self.layout.addLayout(self.plants_layout)
        self.home_layout = QtGui.QHBoxLayout()
        self.home_layout.addItem(horizontalSpacer())
        self.home_button = homeButton(self)
        self.home_layout.addWidget(self.home_button)
        self.layout.addLayout(self.home_layout)


class plantWidget(QtGui.QWidget):

    def __init__(self, plant_index, plants, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.plant_index = plant_index
        self.plants = plants
        self.notification_sent = False
        self.my_values = self.plants[self.plant_index]

        # Generate GUI objects
        self.layout = QtGui.QVBoxLayout(self)
        self.name_label = QtGui.QLabel(self)
        self.name_label.setText(self.my_values["Name"])
        self.layout.addWidget(self.name_label)
        self.button_layout = QtGui.QHBoxLayout(self)
        self.button_layout.addItem(horizontalSpacer())
        self.picture = QtGui.QLabel(self)
        self.pixmap = (QtGui.QPixmap(self.my_values["Filename"]).
                       scaled(225, 225, QtCore.Qt.KeepAspectRatio))
        self.picture.setPixmap(self.pixmap)
        self.button_layout.addWidget(self.picture)
        self.button = QtGui.QPushButton(self)
        self.watering_icon = QtGui.QIcon(QtGui.QPixmap("Images/watering.png"))
        self.button.setIcon(self.watering_icon)
        self.button_layout.addWidget(self.button)
        self.progress = QtGui.QProgressBar(self)
        self.progress.setRange(0, self.my_values["Watering Time (s)"])
        self.progress.setOrientation(QtCore.Qt.Orientation(2))
        self.button_layout.addWidget(self.progress)
        self.button_layout.addItem(horizontalSpacer())
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(horizontalLine(self))
        self.info = QtGui.QLabel(self)
        self.info.setText(self.my_values["Info"])
        self.layout.addWidget(self.info)
        self.layout.addItem(verticalSpacer())
        self.button.clicked.connect(self.waterMe)
        self.setProgress()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.setProgress)
        self.timer.start(1000)
        # self.timer.start(2000000)  # 33 minutes or so

    def waterMe(self):
        current_time = time.time()
        self.plants[self.plant_index]["Last Watering"] = current_time
        with open('plants.json', 'w') as f:
            json.dump(self.plants, f, indent=4, ensure_ascii=False)
        self.setProgress()
        if self.notification_sent:
            notification_mutex.remove(self.my_values["Name"])
            self.notification_sent = False

    def setProgress(self):
        current_time = time.time()
        last_watering = self.my_values["Last Watering"]
        elapsed_time = current_time - last_watering
        watering_time = self.my_values["Watering Time (s)"]
        self.progress.setValue(watering_time - elapsed_time)
        if elapsed_time > watering_time:
            print("TODO: Send a notification")
            self.notification_sent = True


class clockWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QVBoxLayout(self)
        self.time_label = QtGui.QLabel(self)
        self.time_font = QtGui.QFont("Analecta", pointSize=40)
        self.time_font.setBold(True)
        self.time_label.setFont(self.time_font)
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.date_label = QtGui.QLabel(self)
        self.date_font = QtGui.QFont("Atavyros", pointSize=40)
        self.date_label.setFont(self.date_font)
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.date_label)
        self.setTime()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.setTime)
        self.timer.start(10000)

    def setTime(self):
        self.time_label.setText(time.strftime("%I:%M %p"))
        self.date_label.setText(time.strftime("%A %B %d, %Y"))


class notificationMutex(QtCore.QMutex):
    def __init__(self):
        QtCore.QMutex.__init__(self)
        self.notifications = {}

    def read(self):
        return self.notifications

    def add(self, new_name, new_value):
        self.lock()
        self.notifications[new_name] = new_value
        self.unlock()

    def remove(self, name):
        self.lock()
        if name in self.notifications:
            del self.notifications[name]
        self.unlock()


class frameMutex(QtCore.QMutex):
    def __init__(self):
        QtCore.QMutex.__init__(self)
        self.frame_name = "home_frame"

    def read(self):
        return self.frame_name

    def write(self, new_frame):
        self.lock()
        self.frame_name = new_frame
        self.unlock()


class Signals(QtCore.QObject):
    frame_change = QtCore.pyqtSignal()
    notification_update = QtCore.pyqtSignal()

# A few global variables
signals = Signals()
frame_mutex = frameMutex()
notification_mutex = notificationMutex()
button_font = QtGui.QFont("Brill", pointSize=40)
