import cv2
import os
import numpy as np
import math

def op_rotar(img,angle):
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]

        aux1= (1-math.cos(angle))*(filas/2)-math.sin(angle)*(cols/2)+((filas*math.cos(angle)+cols*math.sin(angle))/2)-(filas/2)
        aux2= math.sin(angle)*(filas/2)+(1-math.cos(angle))*(cols/2)+((cols*math.cos(angle)+filas*math.sin(angle))/2)-(cols/2)
        M = np.float32([[math.cos(angle),math.sin(angle),aux1],[-math.sin(angle),math.cos(angle),aux2]])
        out=cv2.warpAffine(img,M,(int(filas*math.cos(angle)+cols*math.sin(angle)),int(cols*math.cos(angle)+filas*math.sin(angle))))
        
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

if __name__ == "__main__":
    run_rot('./input',45)