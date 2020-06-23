import cv2
import os
import numpy as np
import math

def op_rotar(img,angle):
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = cv2.getRotationMatrix2D((cols/2,filas/2),angle,1)
        out=cv2.warpAffine(img,M,(cols,filas))
        return(out)
    else:
        return(None)

def op_escala(img,alto,ancho):
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = np.float32([[ancho/cols ,0,0],[0,alto/filas,0]])
        out=cv2.warpAffine(img,M,(ancho,alto))
        return(out)
    else:
        return(None)

def op_trasl(img,tx,ty):
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = np.float32([[1,0,tx],[0,1,ty]])
        out=cv2.warpAffine(img,M,(cols,filas))
        return(out)
    else:
        return(None)

def op_shear(img,shx,shy):
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = np.float32([[1,shy,0],[shx,1,0]])
        out=cv2.warpAffine(img,M,(filas,cols))
        return(out)
    else:
        return(None)



def run_rot(folder,angle):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out=op_rotar(img,angle)
        if out is not None:
            cv2.imwrite('./out/out1_rot'+str(angle)+'_'+filename,out)
            print("Imagen Transformada")

def run_escal(folder,a,an):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out=op_escala(img,a,an)
        if out is not None:
            cv2.imwrite('./out/out1_esc'+str(a)+'-'+str(an)+'_'+filename,out)
            print("Imagen Transformada")

def run_trasl(folder,tx,ty):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out=op_trasl(img,tx,ty)
        if out is not None:
            cv2.imwrite('./out/out1_tras'+str(tx)+'-'+str(ty)+'_'+filename,out)
            print("Imagen Transformada")

def run_shear(folder,shx,shy):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out=op_shear(img,shx,shy)
        if out is not None:
            cv2.imwrite('./out/out1_shear'+str(shx)+'-'+str(shy)+'_'+filename,out)
            print("Imagen Transformada")

if __name__ == "__main__":
    run_rot('./input',90)
    run_escal('./input',200,200)
    run_trasl('./input',50,50)
    run_shear('./input',0.5,0.5)
