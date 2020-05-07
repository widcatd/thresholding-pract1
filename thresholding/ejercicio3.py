import cv2
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread('imgs2/thresh3.png')
cv2.imshow('imagen original', image)
cv2.waitKey()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
a = np.asarray(gray)
datos=np.zeros(256)
for i in range(len(a)):
    for j in range(len(a[i])):
        datos[a[i][j]]=datos[a[i][j]]+1
x=[]
for i in range(256):
    x.append(i)
#plt.plot(x,datos)
#plt.show()
limi=192 #limite inicial
limf=207 #limite final
for i in range(len(a)):
    for j in range(len(a[i])):
        if a[i][j]>=limi and a[i][j]<=limf:
            a[i][j]=0
        else:
            a[i][j]=255
im_fin = np.uint8(a)
cv2.imshow('image final', im_fin)
cv2.waitKey()
cv2.imwrite('./out/e2out_thresh3.png',im_fin)
