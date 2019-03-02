#!/bin/python

import json
import random
import os
from google_images_download import google_images_download

import collections
import threading
import time
import fodmap_repo


class DatabaseManager():
    def __init__(self, dataDirectory=None, Async=True):

        self.maxCachedImages = 5
        self.cachedImages = collections.deque()

        self.imagesFolder = dataDirectory

        databaseFilename = "fodmaplist.json"
        databaseFilepath = os.path.join(dataDirectory, databaseFilename)

        if not os.path.isfile(databaseFilepath):
            fodmap_repo.downloadDatabase(databaseFilepath)

        self.database = json.load(open(databaseFilepath))

        self.Async = Async

        self.currentIndex = 0

        if self.Async:
            n = threading.Thread(target=self.imageCacheControl)
            n.start()

    def getCurrentData(self):
        return self.database[self.currentIndex]

    def loadRandom(self):
        if self.Async and len(self.cachedImages):
            cacheEntry = self.cachedImages.pop()
            self.currentIndex = cacheEntry
        else:
            self.currentIndex = self.initializeRandom()

    def initializeRandom(self):
        viewIndex = random.randrange(len(self.database))
        data = self.database[viewIndex]
        #imageName = self.nameToImageName(data['name'])
        #IMG = self.downloadImage(imageName)

        return viewIndex
    """

    This should run countinuously in the background, keeping the cache filled.

    """
    def imageCacheControl(self):
        while True:
            if len(self.cachedImages) <= self.maxCachedImages:
                cacheEntryIndex = self.initializeRandom()
                self.cachedImages.append(cacheEntryIndex)
            else:
                time.sleep(4)

    def nameToImageName(self, name):
        return name.replace(",", "").replace("/", "")

    def getImageFilename(self, imageName):
        if not os.path.isdir(self.imagesFolder):
            os.mkdir(self.imagesFolder)
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
            "output_directory": self.imagesFolder,
            "print_urls": True
        }

        paths = image.download(arguments)
        imagePath = paths[keyword][0]
        print("Downloaded %s" % imagePath)
        return paths



