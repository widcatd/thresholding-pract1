import cv2 as cv2
image = cv2.imread('data/thresh3.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow('Original image',image)
cv2.imshow('Gray image', gray)
cv2.waitKey(0)