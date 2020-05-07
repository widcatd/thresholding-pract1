import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 


def pixel(lst):
    return((float(lst[0])+float(lst[1])+float(lst[2]))/3)


def run(folder):
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:

            cv2.imshow('imagen inicial',img)
            cv2.waitKey()

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
            
            cv2.imshow('imagen inicial',img)
            cv2.waitKey()
            cv2.imshow('imagen final',out)
            cv2.waitKey()

            cv2.imwrite('./out/out3_'+filename,out)

run('./imput')