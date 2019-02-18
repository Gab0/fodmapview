#!/bin/python

import json
import random
import os
from google_images_download import google_images_download

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QPlainTextEdit, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

import collections
import threading
import time

class DatabaseManager():
    def __init__(self):

        self.maxCachedImages = 5
        self.cachedImages = collections.deque()

        self.imagesFolder = "Images"
        self.database = json.load(open("fodmap_list/fodmap_repo.json"))

        self.currentIndex = 0

        n = threading.Thread(target=self.imageCacheControl)
        n.start()

    def getCurrentData(self):
        return self.database[self.currentIndex]

    def loadRandom(self):
        if len(self.cachedImages):
            cacheEntry = self.cachedImages.pop()
            self.currentIndex = cacheEntry

    """

    This should run countinuously in the background, keeping the cache filled.

    """
    def imageCacheControl(self):
        while True:
            if len(self.cachedImages) <= self.maxCachedImages:
                viewIndex = random.randrange(len(self.database))
                data = self.database[viewIndex]
                imageName = self.nameToImageName(data['name'])
                IMG = self.downloadImage(imageName)
                cacheEntryIndex = viewIndex
                self.cachedImages.append(cacheEntryIndex)
            else:
                time.sleep(4)

    def nameToImageName(self, name):
        return name.replace(",", "").replace("/", "")

    def getImageFilename(self, imageName):
        folderPath = os.path.join(self.imagesFolder, imageName)
        if not os.path.isdir(folderPath):
            filename = self.downloadImage(imageName)[imageName][0]
        else:
            filename = os.path.join(folderPath, os.listdir(folderPath)[0])
        return filename

    def downloadImage(self, keyword):
        image = google_images_download.googleimagesdownload()

        arguments = {
            "keywords": keyword,
            "limit": 1,
            "output_directory": self.imagesFolder
        }

        paths = image.download(arguments)
        imagePath = paths[keyword][0]
        print("Downloaded %s" % imagePath)
        return paths



