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
            hist = cv2.calcHist([img], [1], None, [256], [0, 256])
            cv2.imshow('imagen inicial',img)
            cv2.waitKey()

            plt.plot(hist)
            plt.show()

            lim=185 #valor calculado con aproximaciones
            out=np.zeros(shape=img.shape,dtype=np.uint8)

            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    t=pixel(img[i][j])
                    if (pixel(img[i][j])<lim):
                        out[i][j]=img[i][j]
            
            cv2.imshow('imagen inicial',img)
            cv2.waitKey()
            cv2.imshow('imagen final',out)
            cv2.waitKey()

            cv2.imwrite('./out/out_'+filename,out)

run('./img')