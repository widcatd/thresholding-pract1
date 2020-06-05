import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math

def op_sum(img,c):
    if img is not None:
        #mostramos las imagenes originales
        cv2.imshow('Imagen inicial 1',img)
        cv2.waitKey()
        #ajustamos el tamaño de la imagen 2 a la de la imagen 1
        
        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        #aplicamos la suma en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    if int(img[j][k][i]*c)>255:
                        out[j][k][i]=255
                    else:
                        out[j][k][i]= int(img[j][k][i]*c)

        cv2.imshow('Imagen final',out)
        cv2.waitKey()
        return(out)
        #guardamos la imagen generada
    else:
        return(None)

def run_exp(file1):
    #Procesamos todos los elementos de la carpeta indicada
    img = cv2.imread(file1)
    c=7 #constante
    out=op_sum(img,c)
    if out is not None:
        cv2.imwrite('./out1/out_mul_4_7.jpg',out)
        print("Imagenes Sumadas")
    else:
        print("Imagenes no compatibles--")

run_exp('./input1/mul_4.jpg') 