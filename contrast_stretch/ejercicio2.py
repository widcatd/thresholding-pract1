import cv2
import numpy as np
import matplotlib.pyplot as plt
image = cv2.imread('imput/img_contrast_stretching.jpg')
cv2.imshow('imagen original', image)
cv2.waitKey()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
a_array = np.asarray(gray)
#agregando un outlier a la imagen
for i in range(20):
    for j in range(20):
        a_array[i][j]=0
im_fin = np.uint8(a_array)
cv2.imshow('image final', im_fin)
cv2.waitKey()
cv2.imwrite('./out/out3_img_contrast_stretching_o.jpg',im_fin)
image = cv2.imread('out/out3_img_contrast_stretching_o.jpg)
hist = cv2.calcHist([image], [0], None, [256], [0, 256])
plt.plot(hist, color='gray' )
plt.show()
