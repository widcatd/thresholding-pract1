import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty
import functions

Window.clearcolor = (0.5, 0.5, 0.5, 1)

fil_pt=''

class CalcGridLayout(GridLayout):
    filePath = StringProperty('')

    def __init__(self, **kwargs):
        super(CalcGridLayout, self).__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)

    def reduced_image(self):
        print(self.filePath)

    def _on_file_drop(self, window, file_path):
        print(file_path)
        fil_pt=file_path.decode("utf-8") 
        self.filePath = file_path.decode("utf-8")    # convert byte to string
        self.ids.img.source = self.filePath
        self.ids.img.reload()   # reload image

    def _on_file_drop2(self, window, file_path):
        print(file_path)
        fil_pt=file_path.decode("utf-8") 
        self.filePath = file_path.decode("utf-8")    # convert byte to string
        self.ids.img2.source = self.filePath
        self.ids.img2.reload()   # reload image

def callback(instance):
    functions.hist_eq(fil_pt)


class DragDropApp(App):
    def build(self):
        return CalcGridLayout()


if __name__ == "__main__":
    DragDropApp().run()