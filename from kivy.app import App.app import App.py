from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

Colors = ['#f6f946', '#21ac2f', '#d31010']

class TrainingWindow(FloatLayout):
    color = StringProperty()

    def on_enter(self):
        self.colorsnum = 0
        self.schedule = Clock.schedule_interval(self.updatelabel, 5)

    def updatelabel(self, dt):
        global Colors
        if self.colorsnum < len(Colors):
            self.color = Colors[self.colorsnum]
            self.colorsnum += 1

kv = Builder.load_string('''
#:import C kivy.utils.get_color_from_hex
<TrainingWindow>
    FloatLayout:
            canvas.before:
                Color:
                    rgba: C(root.color)
                Rectangle:
                    pos: self.pos
                    size: self.size
''')

class MyApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyApp().run()