#!/bin/python

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color

from kivy.uix.image import Image
from database import DatabaseManager
import json

import ssl

# this makes https work on android;
ssl._create_default_https_context = ssl._create_unverified_context


class Sphere(Widget):
    def __init__(self, layout):
        Widget.__init__(self)
        layout.bind(pos=self.update, size=self.update)

        self.w = Ellipse(pos=self.pos, size=self.size)

        self.Color = Color(rgb=(1,1,1))
        self.canvas.add(self.Color)
        self.canvas.add(self.w)

        self.bind(pos=self.update, size=self.update)

    def update(self, instance, value):
        self.w.pos = instance.pos
        self.w.size = instance.size
        print(value)

    def changecolor(self, color):
        self.Color.rgb = color


class AttributeViewer(GridLayout):
    def __init__(self):
        super(AttributeViewer, self).__init__()
        self.Name = Label()
        self.Category = Label(text="")

        self.cols = 1
        self.rows = 6

        Spheres = GridLayout()
        Spheres.rows = 1
        Spheres.cols = 4
        self.coloredSpheres = {
            "oligos": Sphere(Spheres),
            "fructose": Sphere(Spheres),
            "polyols": Sphere(Spheres),
            "lactose": Sphere(Spheres)
        }
        Spheres.add_widget(self.coloredSpheres['oligos'])
        Spheres.add_widget(self.coloredSpheres['fructose'])
        Spheres.add_widget(self.coloredSpheres['polyols'])
        Spheres.add_widget(self.coloredSpheres['lactose'])

        subtitles = Label(text="oligos/fructose/polyols/lactose")

        self.add_widget(self.Name)
        self.add_widget(self.Category)
        self.add_widget(Label())
        self.add_widget(Label(text="Content:"))
        self.add_widget(subtitles)
        self.add_widget(Spheres)

    def changeView(self, data):
        self.Name.text = data["name"]
        self.Category.text = data["category"]

        Values = {
            "low": 10,
            "high": 90
        }

        cm = 0.2
        cM = 0.8

        ballColorMap = {
            0: (cm, cM, cm), # GREEN
            1: (cm, cM, cM), # YELLOW
            2: (cM, cm, cm)  # RED
        }
        for k in self.coloredSpheres.keys():
            try:
                self.coloredSpheres[k].changecolor(ballColorMap[data["details"][k]])
            except KeyError as e:
                print('fail')
            except Exception as e:
                raise


class Viewer(GridLayout):
    def __init__(self, dataDirectory=None):
        super(Viewer, self).__init__()

        self.database = DatabaseManager(dataDirectory=dataDirectory, Async=False)
        self.buildInterface()

    def buildInterface(self):
        self.cols = 3
        self.rows = 3

        self.showText = TextInput(multiline=True)
        self.random_button = Button(text="RANDOM", on_press=lambda a: self.randomEntry())
        self.Image = Image()

        self.foodView = AttributeViewer()

        # ADDING WIDGETS
        self.add_widget(self.Image)
        #self.add_widget(self.showText)
        self.add_widget(self.foodView)
        self.add_widget(self.random_button)

    def randomEntry(self):
        self.database.loadRandom()
        self.changeView()

    def changeView(self):
        data = self.database.getCurrentData()
        try:
            imageName = self.database.nameToImageName(data["name"])
            filename = self.database.getImageFilename(imageName)
            self.Image.source = filename
            self.Image.reload()
        except Exception as e:
            print("Failure to connect")
            print(str(e))
        self.showText.text = json.dumps(data, indent=2)

        self.foodView.changeView(data)


class fodmapApp(App):
    def build(self):
        return Viewer(dataDirectory=self.user_data_dir)


if __name__ == "__main__":
    fodmapApp().run()
