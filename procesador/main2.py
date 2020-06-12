from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
Builder.load_string('''
<CustButton@Button>:
    text_size: self.size
    halign: 'center'
    valign: 'middle'

<DropFile@Image>:
<Box>:

    BoxLayout:  
        DropFile:
            id: img

        DropFile:
            id: img2

    BoxLayout:
        size_hint: 1, .3
        spacing: 10

        CustButton:
            text: "Aplicar Histogram Equalitation"

        CustButton:
            text: "Aplicar Thresholding"

        BoxLayout:
            size_hint: 2, 1
            canvas:
                Color:
                    rgba: 0.2,0.2,0.2,1
                Line:
                    rectangle: self.x, self.y, self.width+1, self.height+1

            TextInput:
                id: entry
                font_size: 20
                multiline: False
                hint_text: "Rango"
            CustButton:
                text: "Aplicar contrast Stretching"
                on_release: root.reduced_image()
            

        BoxLayout:
            size_hint: 2, 1
            canvas:
                Color:
                    rgba: 0.2,0.2,0.2,1
                Line:
                    rectangle: self.x, self.y, self.width+1, self.height+1

            TextInput:
                id: entry2
                font_size: 20
                multiline: False
                hint_text: "Valor C"
            CustButton:
                text: "Aplicar Op. Log"

        
            
''')

class Box(BoxLayout):
    pass

class Test(App):
    def build(self):
        self.drops = []
        Window.bind(on_dropfile=self.handledrops)
        return Box()
    def handledrops(self, *args):
        for i in self.drops:
            i(*args)

class Helper:
    pass

class DropFile(Label):
    filePath = StringProperty('')
    def __init__(self, **kwargs):
        super(DropFile, self).__init__(**kwargs)
        Window.bind(mouse_pos=lambda w, p: setattr(Helper, 'mpos', p))
        app = App.get_running_app()
        app.drops.append(self.on_dropfile)

    def on_dropfile(self, *args):
        self.filePath = args[0].decode("utf-8")      # convert byte to string
        self.id.source = self.filePath
        self.id.reload()   # reload image


Test().run()