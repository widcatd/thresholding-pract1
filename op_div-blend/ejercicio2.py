import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math

def op_division(img,img2):
    if img is not None and img2 is not None:
        #mostramos las imagenes originales
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Imagen inicial 1',img)
        cv2.waitKey()
        cv2.imshow('Imagen inicial 2',img2)
        cv2.waitKey()
        #sacamos los valores minimos y maximos
        mini=np.min(img)
        maxi=np.max(img)
        newmin=np.min(img2)
        newmax=np.max(img2)
        #ajustamos el tamaño de la imagen 2 a la de la imagen 1
        img2=cv2.resize(img2, (img.shape[1], img.shape[0]))

        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)
        #creamos una constante
        const=190
        #aplicamos la suma en los 3 canales
        for j in range(img.shape[0]):
            for k in range(img.shape[1]):
                out[j][k]=((((img[j][k]/img2[j][k])*const)-mini)*((newmax-newmin)/(maxi-mini)))+newmin
        cv2.imshow('Imagen final',out)
        cv2.waitKey()
        return(out)
        #guardamos la imagen generada
    else:
        return(None)

def run_exp(file1,file2):
    #Procesamos todos los elementos de la carpeta indicada
    img = cv2.imread(file1)
    img2=cv2.imread(file2)
    out=op_division(img,img2)
    if out is not None:
        cv2.imwrite('./out1/out_div_1.jpg',out)
        print("Imagenes Sumadas")
    else:
        print("Imagenes no compatibles--")
run_exp('./input1/sub_1.jpg','./input1/sub_2.jpg') # <- Operador B optimo para
