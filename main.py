from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import numpy


class MyArray(GridLayout):
    """Genere un tableau de labels ( couleurs ) a partir d'un numpy"""

    __size = 5
    __colors = [Label(text="0") for x in range(__size*__size)]

    def __init__(self, **kwargs):
        super(MyArray, self).__init__(**kwargs)
        # il n'y a que 5 valeurs dans la palette
        self.palette = [b"\x00\x00\x00", b"\xff\x00\x00", b"\x00\xff\x00", b"\x00\x00\xff", b"\xff\xff\xff"]
        self.refresh()
        self.cols = self.__size
        for x in range(self.__size*self.__size):
            self.add_widget(self.__colors[x])

    def refresh(self):
        """Regenere le tableau numpy et les couleurs ( textes des labels )"""
        # 5 valeurs pour correspondre à la palette ( limitee )
        numpy_array = numpy.random.randint(0, 4, size=(self.__size*self.__size), dtype=numpy.uint16)
        for x in range(self.__size*self.__size):
            self.__colors[x].text = str(self.palette[numpy_array[x]])


class WidgetContainer(GridLayout):
    """Gere affichage et refresh auto du layout principal"""

    def __init__(self, **kwargs):
        super(WidgetContainer, self).__init__(**kwargs)
        self.cols = 1

        self.my_array = MyArray()

        self.mySlider = Slider(min=30, max=60, value=30)
        self.mySlider.bind(value=self.on_frequency)
        self.mySliderValue = Label(text='30 Hz')

        self.myButton = Button(text="Quit")
        self.myButton.bind(on_press=self.click_exit)

        self.add_widget(self.my_array)
        self.add_widget(self.mySlider)
        self.add_widget(self.mySliderValue)
        self.add_widget(self.myButton)

        self.auto_refresh = Clock.schedule_interval(self.refresh_array, 1/30)

    def refresh_array(self, _):
        # le layout est redessine automatiquement
        self.my_array.refresh()

    def on_frequency(self, _, value):
        self.mySliderValue.text = "%d Hz" % value
        period = 1/value
        self.auto_refresh.cancel()  # Precedent schedule annule
        self.auto_refresh = Clock.schedule_interval(self.refresh_array, period)

    @staticmethod
    def click_exit():
        exit(0)


class MyApp(App):

    def build(self):
        widget_container = WidgetContainer()
        return widget_container


if __name__ == '__main__':
    MyApp().run()
