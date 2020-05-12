import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math

def pixel(lst):
    return((float(lst[0])+float(lst[1])+float(lst[2]))/3)


def run(folder):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        
        if img is not None:
            #mostramos imagen original
            cv2.imshow('imagen inicial',img)
            cv2.waitKey()
            #fijamos las coordenadas,el alto y ancho que tendra la sub-imagen
            x=150
            y=190
            w=120
            h=220
            #sacando una parte de la imagen
            sub_imagen= img[y:y+h, x:x+w]
            #calculamos el histograma por cada capa y los mostramos
            lh=[]
            ll=[]
            for i in range(len(sub_imagen[0][0])):
                h=cv2.calcHist([sub_imagen], [i], None, [256], [0, 256])
                lh.append(h)
                plt.plot(h)
                plt.show()
                
                ph=[0]*256
                for i in range (len(h)):
                    ph[i]=h[i]/(sub_imagen.shape[0]*sub_imagen.shape[1])
                
                sn=[]
                for i in range(256):
                    t=0
                    for i in range(i):
                        t+=ph[i]
                    sn.append(math.floor(256*t))
                ll.append(sn)
            
            
            #creamos una imagen en negro
            out=np.zeros(shape=img.shape,dtype=np.uint8)

            #aplicamos contrast stretching con los topes en los 3 canales
            for i in range(len(img[0][0])):
                for j in range(img.shape[0]):
                    for k in range(img.shape[1]):
                        out[j][k][i]=ll[i][img[j][k][i]]

            
            cv2.imshow('imagen inicial',img)
            cv2.waitKey()
            cv2.imshow('imagen final',out)
            cv2.waitKey()

            hf = cv2.calcHist([out], [0], None, [256], [0, 256])
            plt.plot(hf)
            plt.show()

            #guardamos la imagen generada
            cv2.imwrite('./out/out3_'+filename,out)

run('./imput2')
