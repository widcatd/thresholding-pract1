import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math

def op_sum(img,img2):
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

        #aplicamos la suma en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    out[j][k][i]=abs(int(img[j][k][i])-int(img2[j][k][i])+100)
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
    out=op_sum(img,img2)
    if out is not None:
        cv2.imwrite('./out1/out_ejercicio3.jpg',out)
        print("Imagenes Sumadas")
    else:
        print("Imagenes no compatibles--")

run_exp('./input1/sub_1.jpg','./input1/sub_2.jpg') # <- Operador B optimo para