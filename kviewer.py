#!/bin/python

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.uix.image import Image
from database import DatabaseManager

import json

class Viewer(GridLayout):
    def __init__(self):
        super(Viewer, self).__init__()

        self.database = DatabaseManager()
        self.buildInterface()

    def buildInterface(self):
        self.cols = 3
        self.rows = 3

        self.showText = TextInput(multiline=True)
        self.random_button = Button(text="RANDOM", on_press=lambda a:self.randomEntry())
        self.Image = Image()

        # ADDING WIDGETS
        self.add_widget(self.Image)
        self.add_widget(self.showText)
        self.add_widget(self.random_button)

    def randomEntry(self):
        self.database.loadRandom()
        self.changeView()

    def changeView(self):
        data = self.database.getCurrentData()
        imageName = self.database.nameToImageName(data["name"])
        filename = self.database.getImageFilename(imageName)
        self.Image.source = filename
        self.Image.reload()
        self.showText.text = json.dumps(data, indent=2)

class theApp(App):
    def build(self):
        return Viewer()


if __name__ == "__main__":
    theApp().run()
