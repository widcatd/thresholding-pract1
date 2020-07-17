import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math

def pixel(lst):
    return((float(lst[0])+float(lst[1])+float(lst[2]))/3)

def aux(imname):
    img = cv2.imread(imname)
    if img is not None:
        return(img)
    else:
        return(None)

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

        return(out)
    else:
        return(None)

def contrast_str(imname,limi):
    img = cv2.imread(imname)
    if img is not None:

        h1 = cv2.calcHist([img], [0], None, [256], [0, 256])
        h1_c=[]
        for i in range (h1.shape[0]):
            if h1[i]!=0:
                h1_c.append(i)
        t=len(h1_c)
        r=int(t/limi)
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

        return(out)
    else:
        return(None)

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
        
        return(out)
    else:
        return(None)

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
        return(out)
    else:
        return(None)
        
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

        return(out)
    else:
        return(None)

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

        return(out)
    else:
        return(None)


def op_sum(imname1,imname2):
    img=cv2.imread(imname1)
    img2=cv2.imread(imname2)
    if img is not None and img2 is not None:
        #ajustamos el tamaño de la imagen 2 a la de la imagen 1
        img2=cv2.resize(img2, (img.shape[1], img.shape[0]))

        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        #aplicamos la suma en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    out[j][k][i]=int(img[j][k][i]/2)+int(img2[j][k][i]/2)

        return(out)
        #guardamos la imagen generada
    else:
        return(None)

def op_div(imname1,imname2):
    img=cv2.imread(imname1)
    img2=cv2.imread(imname2)
    if img is not None and img2 is not None:
        #ajustamos el tamaño de la imagen 2 a la de la imagen 1
        img2=cv2.resize(img2, (img.shape[1], img.shape[0]))

        mini=np.min(img)
        maxi=np.max(img)
        newmin=np.min(img2)
        newmax=np.max(img2)
        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    out[j][k][i]=int((img[j][k][i]/img2[j][k][i])*100)

        return(out)
        #guardamos la imagen generada
    else:
        return(None)

def op_blend(imname1,imname2,x):
    img=cv2.imread(imname1)
    img2=cv2.imread(imname2)
    if img is not None and img2 is not None:
        #mostramos las imagenes originales

        #ajustamos el tamaño de la imagen 2 a la de la imagen 1
        img2=cv2.resize(img2, (img.shape[1], img.shape[0]))

        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    #X ∗ P1(i, j) + (1 − X) ∗ P2(i, j)
                    out[j][k][i]=x*img[j][k][i]+(1-x)*img2[j][k][i]
        
        return(out)
        #guardamos la imagen generada
    else:
        return(None)

def op_multi(imname,c):
    img=cv2.imread(imname)
    if img is not None:

        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        #aplicamos la suma en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    if int(img[j][k][i]*c)>255:
                        out[j][k][i]=255
                    else:
                        out[j][k][i]= int(img[j][k][i]*c)

        return(out)
        #guardamos la imagen generada
    else:
        return(None)

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


def op_binario(imname1,imname2,operacion):
    img=cv2.imread(imname1)
    img2=cv2.imread(imname2)
    if img is not None and img2 is not None:
        #mostramos las imagenes originales


        out=np.zeros(shape=img2.shape,dtype=np.uint8)
        #aplicamos las operaciones binarias
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    if operacion=="and":
                        out[j][k][i]=op_and((img2[j][k][i]),(img[j][k][i]))
                    if operacion=="or":
                        out[j][k][i]=op_or((img2[j][k][i]),(img[j][k][i]))
                    if operacion=="xor":
                        out[j][k][i]=op_xor((img2[j][k][i]),(img[j][k][i]))
                    if operacion=="not":
                        out[j][k][i]=op_not(img[j][k][i])
        #mostramos la imagen resultante

        return(out)
    else:
        return(None)


def op_rotar(imname,angle):
    img=cv2.imread(imname)
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = cv2.getRotationMatrix2D((cols/2,filas/2),angle,1)
        out=cv2.warpAffine(img,M,(cols,filas))
        return(out)
    else:
        return(None)

def op_escala(imname,alto,ancho):
    img=cv2.imread(imname)
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = np.float32([[ancho/cols ,0,0],[0,alto/filas,0]])
        out=cv2.warpAffine(img,M,(ancho,alto))
        return(out)
    else:
        return(None)

def op_trasl(imname,tx,ty):
    img=cv2.imread(imname)
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = np.float32([[1,0,tx],[0,1,ty]])
        out=cv2.warpAffine(img,M,(cols,filas))
        return(out)
    else:
        return(None)

def op_shear(imname,shx,shy):
    img=cv2.imread(imname)
    if img is not None:
        filas, cols = img.shape[0], img.shape[1]
        M = np.float32([[1,shy,0],[shx,1,0]])
        out=cv2.warpAffine(img,M,(filas,cols))
        return(out)
    else:
        return(None)
def thresold_adaptativo(direccion,w_size,cf):#segundo parametro debe ser impar mayor que 1
    img=cv2.imread(direccion)
    if img is not None:
        #mostramos las imagenes originales
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Imagen inicial 1',img)
        cv2.waitKey()
        #ajustamos el tamaño de la imagen 2 a la de la imagen 1
        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)
        #matriz_umbral=np.zeros(shape=img.shape,dtype=np.uint8)
        submatrix=[]
        parametro=int(w_size/2)
        valores=[0,0,0,0]
        tam=[0,0]
        suma=0
        #aplicamos la suma en los 3 canales
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                #obtenemos las coordenadas para generar la submatriz
                if i-parametro>=0:
                    valores[0]=i-parametro
                else:
                    valores[0]=0
                if i+parametro<img.shape[0]:
                    valores[1]=i+parametro+1
                else:
                    valores[1]=img.shape[0]
                if j-parametro>=0:
                    valores[2]=j-parametro
                else:
                    valores[2]=0
                if j+parametro<img.shape[1]:
                    valores[3]=j+parametro+1
                else:
                    valores[3]=img.shape[1]
                #generamos la submatriz
                submatrix=np.zeros(shape=[valores[1]-valores[0]-1,valores[3]-valores[2]-1])
                submatrix=img[valores[0]:valores[1]:1,valores[2]:valores[3]:1].copy()
                #sacamos el promedio
                suma=int(np.sum(submatrix)/(submatrix.shape[0]*submatrix.shape[1]))
                suma=suma-(cf) #restamos con el valor statico
                #aplicamos thresholding
                if img[i][j]>=suma:
                    out[i][j]=255
                else:
                    out[i][j]=0 
        #cv2.imshow('Imagen final',out)
        #cv2.waitKey()
        return(out)
        #guardamos la imagen generada
    else:
        return(None)
