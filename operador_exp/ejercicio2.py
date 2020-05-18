import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math
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
        return(out,True)
    else:
        return(None,False)

def run_rtp(folder,c,r):
    #Procesamos todos los elementos de la carpeta indicada
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        out,ok=op_rtp(img,c,r)
        if ok:
            cv2.imwrite('./out1_2/out_rtp'+str(c)+'-'+str(r)+'_'+filename,out)
            print("Imagen Transformada")
run_rtp('./input1_2',0.05,1.5) #  <- r optimo para operar