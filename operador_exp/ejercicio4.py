import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math


def op_log(img,c):
    if img is not None:
        #mostramos imagen original
        cv2.imshow('Imagen inicial',img)
        cv2.waitKey()
        #calculamos el histograma por cada capa y los mostramos
        col=['r','g','b']
        for i in range(len(img[0][0])):
            h=cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(h,color=col[i%3])
            #mostramos los histogramas
        plt.show()
        
        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        #aplicamos el Histogram equalization en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    vtmp=math.log10(1+img[j][k][i])*c
                    if vtmp>255:
                        vtmp=255
                    out[j][k][i]=vtmp

        
        cv2.imshow('imagen inicial',img)
        cv2.waitKey()
        cv2.imshow('imagen final',out)
        cv2.waitKey()

        return(out,True)
        #guardamos la imagen generada
    else:
        return(None,False)
        
def op_exp(img,b,c):
    if img is not None:
        #mostramos imagen original
        #cv2.imshow('Imagen inicial',img)
        #cv2.waitKey()
        #calculamos el histograma por cada capa y los mostramos
        col=['r','g','b']
        for i in range(len(img[0][0])):
            h=cv2.calcHist([img], [i], None, [256], [0, 256])
            #plt.plot(h,color=col[i%3])
            #mostramos los histogramas
        plt.show()
        
        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        #aplicamos el Histogram equalization en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    vtmp=c*((b**img[j][k][i])-1)
                    if vtmp>255:
                        vtmp=255
                    if vtmp<0:
                        vtmp=0
                    out[j][k][i]=vtmp

        
        #cv2.imshow('imagen inicial',img)
        #cv2.waitKey()
        #cv2.imshow('imagen final',out)
        #cv2.waitKey()

        return(out,True)
        #guardamos la imagen generada
    else:
        return(None,False)

def op_rtp(img,c,r):
    if img is not None:
        #mostramos imagen original
        #cv2.imshow('Imagen inicial',img)
        #cv2.waitKey()
        #calculamos el histograma por cada capa y los mostramos
        col=['r','g','b']
        for i in range(len(img[0][0])):
            h=cv2.calcHist([img], [i], None, [256], [0, 256])
            #plt.plot(h,color=col[i%3])
            #mostramos los histogramas
        plt.show()
        
        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        #aplicamos el Histogram equalization en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    vtmp=c*((img[j][k][i])**r)
                    if vtmp>255:
                        vtmp=255
                    if vtmp<0:
                        vtmp=0
                    out[j][k][i]=vtmp

        
        #cv2.imshow('imagen inicial',img)
        #cv2.waitKey()
        #cv2.imshow('imagen final',out)
        #cv2.waitKey()

        return(out,True)
        #guardamos la imagen generada
    else:
        return(None,False)

def run_lg(folder,cc):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out,ok=op_log(img,cc)
        if ok:
            cv2.imwrite('./out4/out'+str(cc)+'_'+filename,out)

def run_exp(folder,b,c):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out,ok=op_exp(img,b,c)
        if ok:
            cv2.imwrite('./out4/out_exp'+str(b)+'-'+str(c)+'_'+filename,out)
            print("Imagen Transformada")

def run_rtp(folder,c,r):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out,ok=op_rtp(img,c,r)
        if ok:
            cv2.imwrite('./out4/out_rtp'+str(c)+'-'+str(r)+'_'+filename,out)
            print("Imagen Transformada")
        



run_lg('./input4',90)
run_lg('./input4',100) 
run_lg('./input4',120)

run_exp('./input4',1.01,10)
run_exp('./input4',1.01,20) # <- El operador exponencial da mejores resultados para la imagen
run_exp('./input4',1.01,50)

run_rtp('./input4',0.01,1.5)
run_rtp('./input4',0.05,1.5) 
run_rtp('./input4',0.1,1.5) 