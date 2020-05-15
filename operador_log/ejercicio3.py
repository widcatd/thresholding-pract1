import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math


def op_log(img,c):
    if img is not None:
        #mostramos imagen original
        cv2.imshow('Imagen inicial',img)
        cv2.waitKey()
        #calculamos el histograma por cada capa y los mostramos
        col=['r','g','b']
        for i in range(len(img[0][0])):
            h=cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(h,color=col[i%3])
            #mostramos los histogramas
        plt.show()
        
        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        #aplicamos el Histogram equalization en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                #aplicamos la formula de raiz
                for k in range(img.shape[1]):
                    vtmp=math.sqrt(1+img[j][k][i])*c
                    if vtmp>255:
                        vtmp=255
                    out[j][k][i]=vtmp

        
        cv2.imshow('imagen inicial',img)
        cv2.waitKey()
        for i in range(len(out[0][0])):
            h=cv2.calcHist([out], [i], None, [256], [0, 256])
            plt.plot(h,color=col[i%3])
        plt.show()
        cv2.imshow('imagen final',out)
        cv2.waitKey()

        return(out,True)
        #guardamos la imagen generada
    else:
        return(None,False)
        


def run(folder,cc):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out,ok=op_log(img,cc)
        if ok:
            cv2.imwrite('./out/out'+str(cc)+'_'+filename,out)

        #Si el archivo es imagen:
        
run('./input3',25)
run('./input3',30)#<- segun analisis visual el mejor valor
run('./input3',35) 
