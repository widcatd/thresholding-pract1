import cv2
import os
import numpy as np
import math
'''
def ces_affine(img,matrix,tam):
    A=matrix[0:2,0:2]
    B=matrix[0:2,2:3]
    out=np.zeros(shape=tam,dtype=np.uint8)
    for f in range(len(img[0][0])):
        for j in range(tam[0]):
            for k in range(tam[1]):
                tmp=(np.dot(A,np.array([[j],[k]])))+B
                x=int(tmp[0][0])
                y=int(tmp[1][0])
                if(x<0 or x>=img.shape[0]):
                    out[j][k][f]=0
                elif(y<0 or y>=img.shape[1]):
                    out[j][k][f]=0
                else:
                    out[j][k][f]=img[x][y][f]
    return (out)

def ces_affine(img,matrix,tam):
    A=matrix[0:2,0:2]
    B=matrix[0:2,2:3]
    out=np.zeros(shape=tam,dtype=np.uint8)
    for f in range(len(img[0][0])):
        for j in range(img.shape[0]):
            for k in range(img.shape[1]):
                tmp=(np.dot(A,np.array([[j],[k]])))+B
                x=math.floor(tmp[0][0])
                y=math.floor(tmp[1][0])
                if(not((x>=tam[0] or x<0)or(y>=tam[1] or y<0))):
                    out[x][y][f]=img[j][k][f]
    return (out)
'''

def ces_affine(img,matrix,tam):
    A=matrix[0:2,0:2]
    B=matrix[0:2,2:3]
    out=np.zeros(shape=tam,dtype=np.uint8)
    for f in range(len(img[0][0])):
        for j in range(img.shape[0]):
            for k in range(img.shape[1]):
                tmp=(np.dot(A,np.array([[j],[k]])))+B
                x=math.floor(tmp[0][0])
                y=math.floor(tmp[1][0])
                if(not((x>=tam[0] or x<0)or(y>=tam[1] or y<0))):
                    out[x][y][f]=img[j][k][f]
    return (out)

def op_rotar(img,angle):
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = cv2.getRotationMatrix2D((cols/2,filas/2),angle,1)
        out=ces_affine(img,M,(filas,cols,3))
        return(out)
    else:
        return(None)

def op_escala(img,alto,ancho):
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = np.float32([[ancho/cols,0,0],[0,alto/filas,0]])
        out=ces_affine(img,M,(ancho,alto,3))
        return(out)
    else:
        return(None)

def op_trasl(img,tx,ty):
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = np.float32([[1,0,tx],[0,1,ty]])
        out=ces_affine(img,M,(cols,filas,3))
        return(out)
    else:
        return(None)

def op_shear(img,shx,shy):
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = np.float32([[1,shy,0],[shx,1,0]])
        out=ces_affine(img,M,(filas,cols,3))
        return(out)
    else:
        return(None)


def run_rot(folder,angle):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out=op_rotar(img,angle)
        if out is not None:
            cv2.imwrite('./out/ceout2_rot'+str(angle)+'_'+filename,out)
            print("Imagen Transformada")

def run_escal(folder,a,an):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out=op_escala(img,a,an)
        if out is not None:
            cv2.imwrite('./out/ceout2_esc'+str(a)+'-'+str(an)+'_'+filename,out)
            print("Imagen Transformada")

def run_trasl(folder,tx,ty):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out=op_trasl(img,tx,ty)
        if out is not None:
            cv2.imwrite('./out/ceout2_tras'+str(tx)+'-'+str(ty)+'_'+filename,out)
            print("Imagen Transformada")

def run_shear(folder,shx,shy):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out=op_shear(img,shx,shy)
        if out is not None:
            cv2.imwrite('./out/ceout2_shear'+str(shx)+'-'+str(shy)+'_'+filename,out)
            print("Imagen Transformada")

if __name__ == "__main__":
    run_rot('./input',90)
    run_escal('./input',200,200)
    run_trasl('./input',50,50)
    run_shear('./input',0.5,0.5)
