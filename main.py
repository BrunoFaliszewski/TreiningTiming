from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

Times = [5, 4, 3, 2, 1]
Names = ["Start"]

class MainWindow(Screen):
    sets = ObjectProperty(None)
    workMinutes = ObjectProperty(None)
    workSeconds = ObjectProperty(None)
    restMinutes = ObjectProperty(None)
    restSeconds = ObjectProperty(None)
    timesLabel = StringProperty()

    def on_pre_enter(self):
        Window.clearcolor = (33/255, 172/255, 47/255, 1)

    def AddPressed(self):
        global Times, Names, Colors
        if int(self.sets.text) > 0 and (int(self.workMinutes.text) * 60 + int(self.workSeconds.text) > 0 or int(self.restMinutes.text) * 60 + int(self.restSeconds.text) > 0):
            for i in range(int(self.sets.text)):
                for j in range(int(self.workMinutes.text) * 60 + int(self.workSeconds.text)):
                    if int(self.workMinutes.text) * 60 + int(self.workSeconds.text) > 0:
                        Times.append(int(self.workMinutes.text) * 60 + int(self.workSeconds.text) - j)
                if int(self.workMinutes.text) * 60 + int(self.workSeconds.text) > 0:
                    Names.append("Work")
                for j in range(int(self.restMinutes.text) * 60 + int(self.restSeconds.text)):
                    if int(self.restMinutes.text) * 60 + int(self.restSeconds.text) > 0:
                        Times.append(int(self.restMinutes.text) * 60 + int(self.restSeconds.text) - j)
                if int(self.restMinutes.text) * 60 + int(self.restSeconds.text) > 0:
                    Names.append("Rest")
            self.timesLabel += f"{self.sets.text}x Work: {self.workMinutes.text}:{self.workSeconds.text} Rest: {self.restMinutes.text}:{self.restSeconds.text}\n"
    
    def ResetPressed(self):
        global Times
        Times = [5, 4, 3, 2, 1]
        self.timesLabel = ""

    def SavePressed(self):
        pass

class TrainingWindow(Screen):
    seconds = StringProperty()
    names = StringProperty()
    color = StringProperty()
    oneSound = SoundLoader.load('Sounds\sone.wav')
    twoSound = SoundLoader.load('Sounds\stwo.wav')
    threeSound = SoundLoader.load('Sounds\sthree.wav')
    workSound = SoundLoader.load('Sounds\swork.wav')
    restSound = SoundLoader.load('Sounds\srest.wav')
    endSound = SoundLoader.load('Sounds\send.wav')
    isFirst = False

    def on_pre_enter(self):
        Window.clearcolor = (223/255, 227/255, 9/255, 1)
        self.secondsnum = 0
        self.namesnum = 0
        self.schedule = Clock.schedule_interval(self.updatelabel, 1)

    def updatelabel(self, dt):
        global Times, Names
        if self.secondsnum < len(Times):
            self.seconds = str(Times[self.secondsnum])
            self.names = Names[self.namesnum]
            if self.names == "Work":
                Window.clearcolor = (33/255, 172/255, 47/255, 1)
                if self.isFirst == True:
                    self.workSound.play()
                    self.isFirst = False
            elif self.names == "Rest":
                Window.clearcolor = (230/255, 11/255, 11/255, 1)
                if self.isFirst == True:
                    self.restSound.play()
                    self.isFirst = False
            if Times[self.secondsnum]  == 3:
                self.threeSound.play()
            elif Times[self.secondsnum]  == 2:
                self.twoSound.play()
            elif Times[self.secondsnum]  == 1:
                self.namesnum += 1
                self.oneSound.play()
                self.isFirst = True
            self.secondsnum += 1
        else:
            self.seconds = "End"
            if self.isFirst == True:
                self.endSound.play()
                self.isFirst = False
            self.names = ""
    
    def BackPressed(self):
        Clock.unschedule(self.schedule)

class MySetsWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")

class TrainingTiming(App):
    def build(self):
        self.icon = "Images\chronometer.png"
        return kv

if __name__ == "__main__":
    TrainingTiming().run()