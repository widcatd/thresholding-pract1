import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math
def dec_to_bin(numero1,numero2):
    #los 2 primeros valores no son parte del numero binario
    bin1=bin(numero1)[2:]
    bin2=bin(numero2)[2:]
    #en caso los nros binarios no sean de la misma longitud
    while len(bin1)<len(bin2):
        bin1="0"+bin1
    while len(bin1)>len(bin2):
        bin2="0"+bin2
    return bin1,bin2
def bin_to_dec(t_cadena):
    return int(t_cadena,2)
def op_or(pixel1,pixel2):
    #convertimos a binario los pixeles
    cadena1,cadena2=dec_to_bin(pixel1,pixel2)
    temp_cadena=""
    #realizamos las operacion or
    for i in range(len(cadena1)):
        if cadena1[i]=="1"or cadena2[i]=="1":
            temp_cadena=temp_cadena+"1"
        else:
            temp_cadena=temp_cadena+"0"
    return bin_to_dec(temp_cadena)
def op_binario(imname1,imname2,operacion):
    img=cv2.imread(imname1)
    img2=cv2.imread(imname2)
    if img is not None and img2 is not None:
        #mostramos las imagenes originales
        cv2.imshow('Imagen inicial 1',img)
        cv2.waitKey()
        cv2.imshow('Imagen inicial 2',img2)
        cv2.waitKey()

        out=np.zeros(shape=img2.shape,dtype=np.uint8)
        #aplicamos las operaciones binarias
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    out[j][k][i]=op_or((img2[j][k][i]),(img[j][k][i]))
        #mostramos la imagen resultante
        cv2.imshow('Imagen final',out)
        cv2.waitKey()
        return(out)
    else:
        return(None)

operacion="or"
out=op_binario('./input1/img1.jpeg','./input1/img2.jpeg',operacion)
cv2.imwrite('./output/out_'+str(operacion)+'.jpeg',out)