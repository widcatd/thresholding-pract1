import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math

def pixel(lst):
    return((float(lst[0])+float(lst[1])+float(lst[2]))/3)


def hist_eq(imname):
    img = cv2.imread(imname)
    #Si el archivo es imagen:
    if img is not None:
        #mostramos imagen original
        #calculamos el histograma por cada capa y los mostramos
        lh=[]
        ll=[]
        for i in range(len(img[0][0])):
            h=cv2.calcHist([img], [i], None, [256], [0, 256])
            lh.append(h)
            #calculamos los P(n)
            ph=[0]*256
            for i in range (len(h)):
                ph[i]=h[i]/(img.shape[0]*img.shape[1])
            
            #calculamos los s(n)
            sn=[]
            for i in range(256):
                t=0
                for i in range(i):
                    t+=ph[i]
                sn.append(math.floor(256*t))
            ll.append(sn)
        
        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        #aplicamos el Histogram equalization en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    out[j][k][i]=ll[i][img[j][k][i]]

        #return(out)

        cv2.imwrite('./out_'+imname,out)

def contrast_str(imname):
    img = cv2.imread(imname)
    if img is not None:

        h1 = cv2.calcHist([img], [0], None, [256], [0, 256])
        h1_c=[]
        for i in range (h1.shape[0]):
            if h1[i]!=0:
                h1_c.append(i)
        t=len(h1_c)
        r=int(t/10)
        l1=h1_c[0+r]
        u1=h1_c[len(h1_c)-1-r]
        
        h2 = cv2.calcHist([img], [1], None, [256], [0, 256])
        h2_c=[]
        for i in range (h2.shape[0]):
            if h2[i]!=0:
                h2_c.append(i)
        t=len(h2_c)
        r=int(t/10)
        l2=h2_c[0+r]
        u2=h2_c[len(h2_c)-1-r]

        h3 = cv2.calcHist([img], [2], None, [256], [0, 256])
        h3_c=[]
        for i in range (h3.shape[0]):
            if h3[i]!=0:
                h3_c.append(i)
        t=len(h3_c)
        r=int(t/10)
        l3=h3_c[0+r]
        u3=h3_c[len(h3_c)-1-r]

        out=np.zeros(shape=img.shape,dtype=np.uint8)

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                tt=img[i][j][0]-l1
                if(tt<0):
                    out[i][j][0]=0
                else:
                    out[i][j][0]=tt*int(255/(u1-l1))
                
                tt=img[i][j][1]-l2
                if(tt<0):
                    out[i][j][1]=0
                else:
                    out[i][j][1]=tt*int(255/(u2-l2))

                tt=img[i][j][2]-l3
                if(tt<0):
                    out[i][j][2]=0
                else:
                    out[i][j][2]=tt*int(255/(u3-l3))
        
        #return(out)

        cv2.imwrite('./out_'+imname,out)

def threshold(imname):
    img = cv2.imread(imname)
    if img is not None:
        hist = cv2.calcHist([img], [1], None, [256], [0, 256])
        cv2.imshow('imagen inicial',img)
        cv2.waitKey()

        lim=185 #valor calculado con aproximaciones
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                t=pixel(img[i][j])
                if (pixel(img[i][j])<lim):
                    out[i][j]=img[i][j]
        
        cv2.imwrite('./out_'+imname,out)

def op_log(imname,c):
    img = cv2.imread(imname)
    if img is not None:
        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        #aplicamos el Histogram equalization en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                #aplicamos la formula de raiz
                for k in range(img.shape[1]):
                    vtmp=math.sqrt(1+img[j][k][i])*c
                    if vtmp>255:
                        vtmp=255
                    out[j][k][i]=vtmp
        cv2.imwrite('./out_'+imname,out)
        
def op_exp(imname,b,c):
    img = cv2.imread(imname)
    if img is not None:
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

        cv2.imwrite('./out_'+imname,out)

def op_rtp(imname,c,r):
    img = cv2.imread(imname)
    if img is not None:
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

        cv2.imwrite('./out_'+imname,out)


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
                    out[j][k][i]=int(img[j][k][i]/2)+int(img2[j][k][i]/2)

        cv2.imshow('Imagen final',out)
        cv2.waitKey()
        return(out)
        #guardamos la imagen generada
    else:
        return(None)

def op_div(img,img2):
    if img is not None and img2 is not None:
        #mostramos las imagenes originales
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Imagen inicial 1',img)
        cv2.waitKey()
        cv2.imshow('Imagen inicial 2',img2)
        cv2.waitKey()

        #ajustamos el tamaño de la imagen 2 a la de la imagen 1
        img2=cv2.resize(img2, (img.shape[1], img.shape[0]))

        mini=np.min(img)
        maxi=np.max(img)
        newmin=np.min(img2)
        newmax=np.max(img2)

        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        
        for j in range(img.shape[0]):
            for k in range(img.shape[1]):
                #out[j][k]=((img[j][k]-mini)*((newmax-newmin)/(maxi-mini)))+newmin
                out[j][k]=int((img[j][k]/img2[j][k])*100)
        
        cv2.imshow('Imagen final',out)
        cv2.waitKey()
        return(out)
        #guardamos la imagen generada
    else:
        return(None)

def op_blend(img,img2,x):
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

        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    #X ∗ P1(i, j) + (1 − X) ∗ P2(i, j)
                    out[j][k][i]=x*img[j][k][i]+(1-x)*img2[j][k][i]
        
        cv2.imshow('Imagen final',out)
        cv2.waitKey()
        return(out)
        #guardamos la imagen generada
    else:
        return(None)
        