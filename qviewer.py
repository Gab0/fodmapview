#!/bin/python

import json
import random
import os
from google_images_download import google_images_download

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from database import DatabaseManager


class Viewer(QApplication):
    def __init__(self):
        QApplication.__init__(self, [])

        self.database = DatabaseManager()
        self.buildInterface()
        self.exec_()

    def btn_random(self):
        self.database.loadRandom()
        self.changeView()

    def buildInterface(self):
        self.window = QWidget()
        layout = QVBoxLayout()

        Buttons = QHBoxLayout()

        self.btn_Random = QPushButton("RANDDM")
        self.btn_Random.clicked.connect(self.btn_random)
        nav_r = QPushButton('<-')
        nav_r.clicked.connect(lambda: self.cycleDatabaseIndex(-1))
        Buttons.addWidget(nav_r)

        Buttons.addWidget(self.btn_Random)

        nav_l = QPushButton('->')
        nav_l.clicked.connect(lambda: self.cycleDatabaseIndex(1))
        Buttons.addWidget(nav_l)

        self.Image = QLabel()
        self.Image.setFixedSize(800, 600)
        self.textBox = QPlainTextEdit()
        layout.addWidget(self.Image)
        layout.addWidget(self.textBox)

        layout.addLayout(Buttons)

        self.window.setLayout(layout)

        self.window.show()

    def cycleDatabaseIndex(self, Value):

        # Checando se a variavel data existe.
        try:
            print(self.data['id'])
            self.database.currentIndex += Value
            self.changeView()
        except:
            self.database.currentIndex = random.randint(0, 99)
            self.changeView()

    def changeView(self):
        data = self.database.getCurrentData()
        imageName = self.database.nameToImageName(data["name"])
        self.showImage(imageName)
        self.textBox.setPlainText(json.dumps(data, indent=4))

    def showImage(self, imageName):
        filename = self.database.getImageFilename(imageName)
        pixmap = QPixmap(filename)

        self.Image.setPixmap(pixmap.scaledToHeight(
            600, Qt.TransformationMode(Qt.FastTransformation)))
        self.Image.resize(200, 100)


a = Viewer()
