import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty
import functions
from cv2 import imwrite as sav

Window.clearcolor = (0.5, 0.5, 0.5, 1)

ready="<-- Elegir Slot donde Cargar -->"
ok="Imagen cargada"
ups="No hay imagenes para cargar"
upsall="No hay imagenes cargadas"
ups2="Falta cargar imagen 2"
upsf="Valores invalidos"

imgtmp="./tmp/tmp.jpg"
out="./tmp/out.jpg"

class CalcGridLayout(GridLayout):
    filePath = StringProperty('')

    def __init__(self, **kwargs):
        super(CalcGridLayout, self).__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)
        self.status="Iniciado correctamente"
        self.ids.status.text=self.status
        self.ids.status.texture_update()
        self.ld1=False
        self.rt2=''
        self.ld2=False

    def set_stat(self,strr):
        self.ids.status.text=strr
        self.ids.status.texture_update()


    def _on_file_drop(self, window, file_path):
        print(file_path)
        self.filePath = file_path.decode("utf-8")
        self.set_stat(ready)
        
    def load1(self):
        self.ids.img.source = self.filePath
        self.ids.img.reload()
        sav(imgtmp,functions.aux(self.filePath))
        self.ids.imgt.source=imgtmp
        self.ids.imgt.reload()
        self.ld1=True
        self.set_stat(ok)

    def load2(self):
        self.ids.img2.source = self.filePath
        self.rt2=self.filePath
        self.ids.img2.reload()
        self.ld2=True
        self.set_stat(ok)

    def save(self):
        if self.ld1:
            sav(out,functions.aux(imgtmp))
            self.set_stat("Imagen guardada correctamente")
        else:
            self.set_stat("No hay imagenes para guardar")

    def load(self):
        sav(imgtmp,functions.aux(out))
        self.set_stat("Imagen cargada correctamente")

    def f1(self):
        if self.ld1:
            sav(imgtmp,functions.hist_eq(imgtmp))
            self.ids.imgt.reload()
            self.set_stat("Listo")
        else:
            self.set_stat(upsall)
        
    def f2(self):
        if self.ld1:
            vlu=self.ids.entry.text
            if vlu=='' or vlu=='0':
                self.set_stat(upsf)
            else:
                sav(imgtmp,functions.contrast_str(imgtmp,int(vlu)))
                self.ids.imgt.reload()
                self.set_stat("Listo")
        else:
            self.set_stat(upsall)

    def f3(self):
        if self.ld1:
            sav(imgtmp,functions.threshold(imgtmp))
            self.ids.imgt.reload()
            self.set_stat("Listo")
        else:
            self.set_stat(upsall)

    def f4(self):
        if self.ld1:
            vlu=self.ids.entry2.text
            if vlu=='' or vlu=='0':
                self.set_stat(upsf)
            else:
                sav(imgtmp,functions.op_log(imgtmp,int(vlu)))
                self.ids.imgt.reload()
                self.set_stat("Listo")
        else:
            self.set_stat(upsall)

    def f5(self):
        if self.ld1:
            vlu=self.ids.entry3.text
            vlu2=self.ids.entry4.text
            if (vlu=='' or vlu=='0') or (vlu2=='' or vlu2=='0') :
                self.set_stat(upsf)
            else:
                sav(imgtmp,functions.op_exp(imgtmp,int(vlu),int(vlu2)))
                self.ids.imgt.reload()
                self.set_stat("Listo")
        else:
            self.set_stat(upsall)

    def f6(self):
        if self.ld1:
            vlu=self.ids.entry5.text
            vlu2=self.ids.entry6.text
            if (vlu=='' or vlu=='0') or (vlu2=='' or vlu2=='0') :
                self.set_stat(upsf)
            else:
                sav(imgtmp,functions.op_rtp(imgtmp,int(vlu),int(vlu2)))
                self.ids.imgt.reload()
                self.set_stat("Listo")
        else:
            self.set_stat(upsall)

    def f7(self):
        if self.ld1 and self.ld2:
            sav(imgtmp,functions.op_sum(imgtmp,self.rt2))
            self.ids.imgt.reload()
            self.set_stat("Listo")

        elif self.ld1 or self.ld2:
            self.set_stat(ups2)
        else:
            self.set_stat(upsall)

    def f8(self):
        if self.ld1 and self.ld2:
            sav(imgtmp,functions.op_div(imgtmp,self.rt2))
            self.ids.imgt.reload()
            self.set_stat("Listo")

        elif self.ld1 or self.ld2:
            self.set_stat(ups2)
        else:
            self.set_stat(upsall)

    
    
class DragDropApp(App):
    def build(self):
        return CalcGridLayout()


if __name__ == "__main__":
    DragDropApp().run()