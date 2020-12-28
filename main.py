from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock

Times = [5, 4, 3, 2, 1]
Names = ["Start"]
Colors = ['#dfe309']

class MainWindow(Screen):
    sets = ObjectProperty(None)
    workMinutes = ObjectProperty(None)
    workSeconds = ObjectProperty(None)
    restMinutes = ObjectProperty(None)
    restSeconds = ObjectProperty(None)
    timesLabel = StringProperty()

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def AddPressed(self):
        global Times, Names, Colors
        if int(self.sets.text) > 0 and (int(self.workMinutes.text) * 60 + int(self.workSeconds.text) > 0 or int(self.restMinutes.text) * 60 + int(self.restSeconds.text) > 0):
            for i in range(int(self.sets.text)):
                for j in range(int(self.workMinutes.text) * 60 + int(self.workSeconds.text)):
                    if int(self.workMinutes.text) * 60 + int(self.workSeconds.text) > 0:
                        Times.append(int(self.workMinutes.text) * 60 + int(self.workSeconds.text) - j)
                if int(self.workMinutes.text) * 60 + int(self.workSeconds.text) > 0:
                    Names.append("Work")
                    Colors.append('#21ac2f')
                for j in range(int(self.restMinutes.text) * 60 + int(self.restSeconds.text)):
                    if int(self.restMinutes.text) * 60 + int(self.restSeconds.text) > 0:
                        Times.append(int(self.restMinutes.text) * 60 + int(self.restSeconds.text) - j)
                if int(self.restMinutes.text) * 60 + int(self.restSeconds.text) > 0:
                    Names.append("Rest")
                    Colors.append('#e60b0b')
            self.timesLabel += f"{self.sets.text}x Work: {self.workMinutes.text}:{self.workSeconds.text} Rest: {self.restMinutes.text}:{self.restSeconds.text}\n"
    
    def ResetPressed(self):
        global Times
        Times = [5, 4, 3, 2, 1]
        self.timesLabel = ""

class TrainingWindow(Screen):
    seconds = StringProperty()
    names = StringProperty()
    color = StringProperty()

    def on_pre_enter(self):
        self.secondsnum = 0
        self.namesnum = 0
        self.colorsnum = 0

        if self.seconds == "":
            self.schedule = Clock.schedule_interval(self.updatelabel, 1)

    def updatelabel(self, dt):
        global Times, Names, Colors
        if self.secondsnum < len(Times):
            self.seconds = str(Times[self.secondsnum])
            self.names = Names[self.namesnum]
            self.color = Colors[self.colorsnum]
            if Times[self.secondsnum]  == 1:
                self.namesnum += 1
                self.colorsnum += 1
            self.secondsnum += 1
        else:
            self.seconds = "End"
            self.names = ""
            self.color = Colors[-1]

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")

class TrainingTiming(App):
    def build(self):
        return kv

if __name__ == "__main__":
    TrainingTiming().run()