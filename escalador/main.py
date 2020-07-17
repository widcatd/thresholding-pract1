from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.behaviors import DragBehavior
import functions
from cv2 import imwrite as sav
import numpy as np

root_kv = '''
<CustButton@Button>:
    text_size: self.size
    halign: 'center'
    valign: 'middle'
<DragLabel>:
    drag_rectangle: self.x, self.y, self.width*2, self.height*2
    drag_timeout: 10000000
    drag_distance: 0

BoxLayout:
    orientation:'vertical'

    MDToolbar:
        title: 'Ajustador de Imágenes'
        md_bg_color: .2, .2, .2, 1
        specific_text_color: 1, 1, 1, 1

    MDBottomNavigation:
        panel_color: .2, .2, .2, 1

        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Imagen de entrada'
            icon: 'file-import'

            MDLabel:
                halign: 'center'
                Image:
                    size: 500,500
                    id: img0

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Transformacion'
            icon: 'file-eye'

            MDLabel:
                orientation:'vertical'
                align: 'center'
                BoxLayout:
                    size: 500,500
                    Image:
                        size: 500,500
                        id: img
                        DragLabel:
                            id:u_l
                            text: '+'
                        DragLabel:
                            id:u_r
                            size_hint: 1, 1
                            text: '+'
                        DragLabel:
                            id:d_l
                            size_hint: 1, 1
                            text: '+'
                        DragLabel:
                            id:d_r
                            size_hint: 1, 1
                            text: '+'
                CustButton:
                    id:bott
                    text: "Transformar"
                    on_press: 


        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'Salida'
            icon: 'file-export'       

            MDLabel:
                BoxLayout:
                    size: 500,500
                    orientation:'vertical'
                    spacing: 10
                    rows: 3
                    BoxLayout:
                        orientation:'horizontal'
                        Image:
                            id: imgtmp
                        Image:
                            id: imgfn
                    BoxLayout:
                        size_hint: 1, .3
                        CustButton:
                            text: "Aplicar Histogram Equalitation"

                        CustButton:
                            text: "Aplicar Contrast Stretching"
'''
class DragLabel(DragBehavior, Label):
    pass

class MainApp(MDApp):
    filePath = StringProperty('')
    def __init__(self, **kwargs):
        self.title = "Transformador"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.filePath=""
        self.cont=1
        Window.bind(on_dropfile=self._on_file_drop)
        super().__init__(**kwargs)


    def build(self):
        self.root = Builder.load_string(root_kv)
        self.root.ids.u_l.x=0
        self.root.ids.u_l.y=0
        self.root.ids.bott.bind(on_press=self.f1)
        #self.root.ids.bott.on_press=self.f1()
        
    
    def _on_file_drop(self, window, file_path):
        print(file_path)
        self.filePath = file_path.decode("utf-8")
        self.root.ids.img0.source = self.filePath
        self.root.ids.img0.reload()
        self.root.ids.img.source = self.filePath
        self.root.ids.img.reload()
        rec=functions.puntos(self.filePath)
        self.act_extr(rec)
        self.cont+=1
        #self.root.switch_tab(self, "screen1")

    def act_extr(self,points):
        w,h=functions.get_dim(self.filePath)
        l=functions.transform_in(points[0][0],points[0][1],w,h,500,500) #(0,0,900,450,500,500) =0,125
        #self.root.ids.u_l.x=0
        #self.root.ids.u_l.y=0
        self.root.ids.u_l.x=int(l[0])
        self.root.ids.u_l.y=int(l[1])
        l=functions.transform_in(points[1][0],points[1][1],w,h,500,500)
        self.root.ids.u_r.x=int(l[0])
        self.root.ids.u_r.y=int(l[1])
        l=functions.transform_in(points[2][0],points[2][1],w,h,500,500)
        self.root.ids.d_l.x=int(l[0])
        self.root.ids.d_l.y=int(l[1])
        l=functions.transform_in(points[3][0],points[3][1],w,h,500,500)
        self.root.ids.d_r.x=int(l[0])
        self.root.ids.d_r.y=int(l[1])

    def f1(self,instance):
        a=functions.puntos(self.filePath)
        temporal=np.array(a)
        img=functions.aux(self.filePath)
        b=functions.four_point_transform(img,temporal)
        sav("./tmp/process.jpg",b)
        self.root.ids.imgtmp.source = "./tmp/process.jpg"
        self.root.ids.imgtmp.reload()

    def f2(self):
        sav("./out/"+str(self.cont)+".jpg",functions.aux("./tmp/process.jpg"))



if __name__ == "__main__":
    MainApp().run()
