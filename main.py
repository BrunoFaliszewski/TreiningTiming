from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock
import os
import sys

Times = [5, 4, 3, 2, 1]

class MainWindow(Screen):
    sets = ObjectProperty(None)
    workMinutes = ObjectProperty(None)
    workSeconds = ObjectProperty(None)
    restMinutes = ObjectProperty(None)
    restSeconds = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def AddPressed(self):
        global Times
        for i in range(int(self.sets.text)):
            for j in range(int(self.workMinutes.text) * 60 + int(self.workSeconds.text)):
                Times.append(int(self.workMinutes.text) * 60 + int(self.workSeconds.text) - j)
            for j in range(int(self.restMinutes.text) * 60 + int(self.restSeconds.text)):
                Times.append(int(self.restMinutes.text) * 60 + int(self.restSeconds.text) - j)
    
    def ResetPressed(self):
        global Times
        Times = [5, 4, 3, 2, 1]

class TrainingWindow(Screen):
    seconds = StringProperty()
    i = 0

    def on_enter(self):
        if self.seconds == "":
            self.schedule = Clock.schedule_interval(self.updatelabel, 1)

    def updatelabel(self, dt):
        global Times
        if self.i < len(Times):
            self.seconds = str(Times[self.i])
            self.i += 1
        else:
            self.seconds = "End"
    
    def showrestarttext(self):
        self.schedule.cancel()
        self.seconds = "Restart_app"


        
        

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")

class TrainingTiming(App):
    def build(self):
        return kv

    @staticmethod
    def restart():
        os.execvp(sys.executable, ['python'] + sys.argv)

if __name__ == "__main__":
    TrainingTiming().run()