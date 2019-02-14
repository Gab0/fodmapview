#!/bin/python

import json
import random
import os
from google_images_download import google_images_download

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap


class Viewer(QApplication):
    def __init__(self):
        QApplication.__init__(self, [])
        window = QWidget()
        layout = QVBoxLayout()

        Buttons = QHBoxLayout()

        self.btn_Random = QPushButton("RANDDM")
        self.btn_Random.clicked.connect(lambda: self.changeView(random.choice(range(len(self.database)))))
        nav_r = QPushButton('<-')
        nav_r.clicked.connect(lambda: self.cycleDatabaseIndex(-1))
        Buttons.addWidget(nav_r)

        Buttons.addWidget(self.btn_Random)

        nav_l = QPushButton('->')
        nav_l.clicked.connect(lambda: self.cycleDatabaseIndex(1))
        Buttons.addWidget(nav_l)

        self.Image = QLabel()
        self.textBox = QPlainTextEdit()
        layout.addWidget(self.Image)
        layout.addWidget(self.textBox)

        layout.addLayout(Buttons)


        window.setLayout(layout)

        window.show()

        self.imagesFolder = "Images"
        self.database = json.load(open("fodmap_list/fodmap_repo.json"))



        self.exec_()

    def cycleDatabaseIndex(self, Value):
        targetIdx = int(self.data["id"]) -1 + Value
        self.changeView(targetIdx)

    def changeView(self, viewIndex):
        self.data = self.database[viewIndex]
        self.showImage(self.data['name'].replace(",", "").replace("/", ""))

        self.textBox.setPlainText(json.dumps(self.data, indent=4))

    def showImage(self, imageName):
        folderPath = os.path.join(self.imagesFolder, imageName)
        if not os.path.isdir(folderPath):
            filename = self.downloadImage(imageName)[imageName][0]
        else:
            filename = os.path.join(folderPath, os.listdir(folderPath)[0])
        pixmap = QPixmap(filename)

        self.Image.setPixmap(pixmap.scaled(800, 600))
        self.Image.resize(200, 100)

    def downloadImage(self, keyword):
        image = google_images_download.googleimagesdownload()

        arguments = {
            "keywords": keyword,
            "limit": 1,
            "output_directory": self.imagesFolder
        }

        paths = image.download(arguments)
        print(paths)
        return paths


a = Viewer()
