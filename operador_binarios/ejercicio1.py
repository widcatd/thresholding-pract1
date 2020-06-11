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
def op_not(pixel):
    return (255-pixel)
def op_and(pixel1,pixel2):
    #convertimos a binario los pixeles
    cadena1,cadena2=dec_to_bin(pixel1,pixel2)
    temp_cadena=""
    #realizamos la operacion and
    for i in range(len(cadena1)):
        if cadena1[i]=="1"and cadena2[i]=="1":
            temp_cadena=temp_cadena+"1"
        else:
            temp_cadena=temp_cadena+"0"
    return bin_to_dec(temp_cadena)
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
def op_xor(pixel1,pixel2):
    #convertimos a binario los pixeles
    cadena1,cadena2=dec_to_bin(pixel1,pixel2)
    temp_cadena=""
    #realizamos las operacion xor
    for i in range(len(cadena1)):
        if cadena1[i]!= cadena2[i]:
            temp_cadena=temp_cadena+"1"
        else:
            temp_cadena=temp_cadena+"0"
    return bin_to_dec(temp_cadena)
def op_binario(img,img2,operacion):
    if img is not None and img2 is not None:
        #mostramos las imagenes originales
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Imagen inicial 1',img)
        cv2.waitKey()
        cv2.imshow('Imagen inicial 2',img2)
        cv2.waitKey()
        out=np.zeros(shape=img2.shape,dtype=np.uint8)
        #aplicamos las operaciones binarias
        for j in range(img.shape[0]):
            for k in range(img.shape[1]):
                if operacion=="and":
                    out[j][k]=op_and((img2[j][k]),(img[j][k]))
                if operacion=="or":
                    out[j][k]=op_or((img2[j][k]),(img[j][k]))
                if operacion=="xor":
                    out[j][k]=op_xor((img2[j][k]),(img[j][k]))
        #mostramos la imagen resultante
        cv2.imshow('Imagen final',out)
        cv2.waitKey()
        return(out)
    else:
        return(None)

def run_exp(file1,file2):
    img = cv2.imread(file1)
    img2=cv2.imread(file2)
    operacion="and"#definimos con que operador vamos a usar
    out=op_binario(img,img2,operacion)
    if out is not None:
        cv2.imwrite('./output/out_'+str(operacion)+'.jpeg',out)
        print("Imagenes Sumadas")
    else:
        print("Imagenes no compatibles--")

run_exp('./input1/img1.jpeg','./input1/img2.jpeg') # <- Operador B optimo para