from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
import numpy


class MyPic:

    __tab_size = 50

    def __init__(self):
        self.texture = Texture.create(size=(self.__tab_size, self.__tab_size))
        self.palette = [b"\x00\x00\x00", b"\xff\x00\x00", b"\x00\xff\x00", b"\x00\x00\xff", b"\xff\xff\xff"]
        self.refresh()

    def refresh(self):
        """Regénère le tableau numpy et le buffer à afficher translaté avec la palette"""
        tab = numpy.random.randint(0, 5, size=(self.__tab_size*self.__tab_size), dtype=numpy.uint16)
        buf = b""
        for x in range(self.__tab_size*self.__tab_size):
            buf += self.palette[tab[x]]
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')


class WidgetContainer(GridLayout):

    def __init__(self, **kwargs):
        super(WidgetContainer, self).__init__(**kwargs)
        self.cols = 1

        self.my_pic = MyPic()
        self.pic = Widget()
        self.pic.canvas = Rectangle(texture=self.my_pic.texture, pos=(10, 10), size=(50, 50))

        self.mySlider = Slider(min=30, max=60, value=30)
        self.mySlider.bind(value=self.on_frequency)
        self.mySliderValue = Label(text='30 Hz')

        self.myButton = Button(text="Quit")
        self.myButton.bind(on_press=self.click_exit)

        self.add_widget(self.mySlider)
        self.add_widget(self.mySliderValue)
        self.add_widget(self.myButton)
        self.add_widget(self.pic)

        self.auto_refresh = Clock.schedule_interval(self.refresh_pic, 1/30)

    def refresh_pic(self, dt):
        self.my_pic.refresh()
        self.pic.canvas.texture = self.my_pic.texture

    def on_frequency(self, instance, value):
        self.mySliderValue.text = "%d Hz" % value
        period = 1/value
        self.auto_refresh.cancel()
        self.auto_refresh = Clock.schedule_interval(self.refresh_pic, period)

    @staticmethod
    def click_exit(self):
        exit(0)


class MyApp(App):

    def build(self):
        widget_container = WidgetContainer()
        return widget_container


if __name__ == '__main__':
    MyApp().run()
