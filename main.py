from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from glob import glob
from os import listdir
from os.path import isfile, join
import os
import shutil

Times = [5, 4, 3, 2, 1]
Names = ["Start"]
Sets = glob(os.path.join('Sets', "*", ""))
for i in range(len(Sets)):
    Sets[i] = Sets[i].replace('Sets', '')
    Sets[i] = Sets[i].replace('\\', '')
CurrentSet = ''
TrainingText = ''
print(Sets)

class SavePopupWindow(Popup):
    popuptextinput = ObjectProperty(None)

    def PopupSavePressed(self):
        global Sets, Times, Names, TrainingText
        if len(Sets) < 9:
            try:
                Sets.append(self.popuptextinput.text)

                os.mkdir(f'Sets\{self.popuptextinput.text}')

                with open(f'Sets\{self.popuptextinput.text}\{self.popuptextinput.text}.txt', 'w') as self.file:
                    for i in range(len(Times)):
                        self.file.write(f'{Times[i]}\n')

                with open(f'Sets\{self.popuptextinput.text}\{self.popuptextinput.text}names.txt', 'w') as self.file:
                    for i in range(len(Names)):
                        self.file.write(f'{Names[i]}\n')

                with open(f'Sets\{self.popuptextinput.text}\{self.popuptextinput.text}trainingtext.txt', 'w') as self.file:
                    self.file.write(TrainingText)

                self.dismiss()
            except FileExistsError:
                self.popuptextinput.text = "There already is that set"
        else:
            self.popuptextinput.text = "You already have 9 Sets"

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
        global Times, Names, Colors, TrainingText
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
            TrainingText = self.timesLabel
    
    def ResetPressed(self):
        global Times
        Times = [5, 4, 3, 2, 1]
        self.timesLabel = ""

    def SavePressed(self):
        self.popup = SavePopupWindow()
        self.popup.open()

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

class SetPopupWindow(Popup):
    currentset = StringProperty()
    timesLabel = StringProperty()

    def on_open(self):
        global CurrentSet
        self.currentset = CurrentSet
        with open(f'Sets\{CurrentSet}\{CurrentSet}trainingtext.txt', 'r') as self.file:
            self.timesLabel = self.file.read()
    
    def RemovePressed(self):
        global CurrentSet, Sets
        shutil.rmtree(f'Sets\{CurrentSet}')
        Sets.remove(f'{CurrentSet}')
        self.dismiss()
    
    def StartPressed(self):
        global Times, Names
        Times = []
        Names = []
        with open(f'Sets\{CurrentSet}\{CurrentSet}.txt', 'r') as self.file:
            self.line = self.file.readline()
            while self.line:
                Times.append(int(self.line.strip('\n')))
                self.line = self.file.readline()
        with open(f'Sets\{CurrentSet}\{CurrentSet}names.txt', 'r') as self.file:
            self.line = self.file.readline()
            while self.line:
                Names.append(self.line.strip('\n'))
                self.line = self.file.readline()
        self.dismiss()

class MySetsWindow(Screen):
    setsnames = ListProperty([])
    currentset = StringProperty()

    def on_pre_enter(self):
        Clock.schedule_interval(self.update, 1)
    
    def update(self, dt):
        global Sets
        self.setsnames = Sets
    
    def SetPressed(self, instance):
        global CurrentSet
        CurrentSet = instance.text
        self.popup = SetPopupWindow()
        self.popup.open()

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")

class TrainingTiming(App):
    def build(self):
        self.icon = "Images\chronometer.png"
        return kv

if __name__ == "__main__":
    TrainingTiming().run()