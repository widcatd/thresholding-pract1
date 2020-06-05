import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math

def op_blend(img,img2,x):
    if img is not None and img2 is not None:
        #mostramos las imagenes originales
        cv2.imshow('Imagen inicial 1',img)
        cv2.waitKey()
        cv2.imshow('Imagen inicial 2',img2)
        cv2.waitKey()

        #ajustamos el tamaño de la imagen 2 a la de la imagen 1
        img2=cv2.resize(img2, (img.shape[1], img.shape[0]))

        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    #X ∗ P1(i, j) + (1 − X) ∗ P2(i, j)
                    out[j][k][i]=x*img[j][k][i]+(1-x)*img2[j][k][i]
        
        cv2.imshow('Imagen final',out)
        cv2.waitKey()
        return(out)
        #guardamos la imagen generada
    else:
        return(None)

def run_blend(file1,file2,x):
    #Procesamos todos los elementos de la carpeta indicada
    img = cv2.imread(file1)
    img2=cv2.imread(file2)
    out=op_blend(img,img2,x)
    if out is not None:
        cv2.imwrite('./out2/out_blend'+str(x)+'.jpg',out)
        print("Operacion Realizada")
    else:
        print("Imagenes no compatibles--")

run_blend('./input2/bld_10.jpg','./input2/bld_11.jpg',0.1)
run_blend('./input2/bld_10.jpg','./input2/bld_11.jpg',0.25) 
run_blend('./input2/bld_10.jpg','./input2/bld_11.jpg',0.5) 
run_blend('./input2/bld_10.jpg','./input2/bld_11.jpg',0.9) 