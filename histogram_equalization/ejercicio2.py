import cv2
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread('imput/hist10_1.jpg')
cv2.imshow('imagen original', image)
cv2.waitKey()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
a_array = np.asarray(gray)
datos=np.zeros(256)
hist = cv2.calcHist([image], [0], None, [256], [0, 256])
x=160
y=200
w=90
h=180
#sacando una parte de la imagen
sub_imagen= image[y:y+h, x:x+w]
datos=np.zeros(256)
for i in range(len(sub_imagen)):
    for j in range(len(sub_imagen[i])):
        datos[sub_imagen[i][j]]=datos[sub_imagen[i][j]]+1
#print(datos)
print(datos)
l=8
histograma=np.zeros(l)
height,width=sub_imagen.shape[:2]
for i in range(l):
    for j in range(len(datos)):
        if i==0:
            if j<=2**i:
                histograma[i]=histograma[i]+datos[j]
        elif j>2**(i) and j<=2**(i+1):
            histograma[i]=histograma[i]+datos[j]
for i in range(len(histograma)):
    histograma[i]=histograma[i]/(height*width)
print(histograma)
#aplicamos la formula
s=np.zeros(l)
sumatoria=0
for i in range(l):
        s[i]=(l-1)*(sumatoria+histograma[i])
        sumatoria=sumatoria+histograma[i]
print(s)
cv2.imwrite('./out/e2out_1.png',sub_imagen)