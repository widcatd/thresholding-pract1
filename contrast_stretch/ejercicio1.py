import cv2
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread('imput/img_contrast_stretching.jpg')
cv2.imshow('imagen original', image)
cv2.waitKey()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
a_array = np.asarray(gray)
datos=np.zeros(256)
hist = cv2.calcHist([image], [0], None, [256], [0, 256])
plt.plot(hist, color='gray' )
plt.show()
extremos=np.zeros(256)
for i in range(len(a_array)):
    for j in range(len(a_array[i])):
        if a_array[i][j]!=0:
            extremos[a_array[i][j]]=1
a=0.0
b=255.0
c=0.0
d=0.0
for i in range(len(extremos)):
    if extremos[i]!=0:
        c=float(i)
        break
for i in range(len(extremos)):
    if extremos[len(extremos)-1-i]!=0:
        d=float(len(extremos)-1-i)
        break
#aplicando la formula de Contrast stretching
for i in range(len(a_array)):
    for j in range(len(a_array[i])):
        a_array[i][j]=(a_array[i][j]-c)*(((b-a)/(d-c))+a)
im_fin = np.uint8(a_array)
cv2.imshow('image final', im_fin)
cv2.waitKey()
cv2.imwrite('./out/e2out_1.png',im_fin)
image = cv2.imread('out/e2out_1.png')
hist = cv2.calcHist([image], [0], None, [256], [0, 256])
plt.plot(hist, color='gray' )
plt.show()
