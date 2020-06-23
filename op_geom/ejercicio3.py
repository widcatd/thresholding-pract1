import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math

def scalematrix(m, scale):
  # Crear matriz con ceros del tamaño apropiado
  r = np.zeros(((m.shape[0]-1)*scale+1, (m.shape[1]-1)*scale+1))

  # Rellenar filas multiplo de scale (interpolando entre valores de los elementos de la fila)
  for fil in range(m.shape[0]):
    for col in range(m.shape[1]-1):
      r[fil*scale, col*scale:(col+1)*scale+1] = np.linspace(m[fil,col], m[fil,col+1], scale+1)

  # Rellenar resto de ceros, interpolando entre elementos de las columnas
  for fil in range(m.shape[0]-1):
    for col in range(r.shape[1]):
      r[fil*scale:(fil+1)*scale + 1, col] = np.linspace(r[fil*scale,col], r[(fil+1)*scale, col], scale+1)
  return r
def cofcof(img,scale):
    if img is not None:
        #mostramos las imagenes originales
        cv2.imshow('Imagen inicial 1',img)
        cv2.waitKey()
        #creamos una imagen en negro
        out = np.zeros(((img.shape[0]-1)*scale+1,(img.shape[1]-1)*scale+1,3),dtype=np.uint8)
        temp_a=img[:,:,2]
        for i in range(out.shape[2]):
            temp_a=img[:,:,i].copy()
            temp_a=scalematrix(temp_a,scale)
            temp_a=temp_a.astype(int)
            for j in range(out.shape[0]):
                for k in range(out.shape[1]):
                    out[j][k][i]=temp_a[j][k]

        #for i in range(img.shape[2]):

        cv2.imshow('Imagen final',out)
        cv2.waitKey()
        return(out)
        #guardamos la imagen generada
    else:
        return(None)
def run_exp(file1):
    #Procesamos todos los elementos de la carpeta indicada
    img = cv2.imread(file1)
    escalar=2
    out=cofcof(img,escalar)
    if out is not None:
        cv2.imwrite('./out/out_meme1.jpg',out)
        print("Imagenes Sumadas")
    else:
        print("Imagenes no compatibles--")
run_exp('./input/meme1.jpg') 
