import numpy as np
import cv2
# Función para dibujar el eje
def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 5)
    return img
IMAGE_NAME = 'imagenes/group5_15_left.jpg'
PARA_SAVE_PATH = "parametros/parameters_left.yaml"

cv_file = cv2.FileStorage(PARA_SAVE_PATH, cv2.FILE_STORAGE_READ)

mtx = cv_file.getNode("camera_matrix").mat()
dist = cv_file.getNode("dist_coeff").mat()
cv_file.release()

#Criterios de terminación (cada cuadrado pequeño en nuestro tablero de ajedrez es de 20 mm x 20 mm)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

objp = np.zeros((7*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

img = cv2.imread(IMAGE_NAME)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, corners = cv2.findChessboardCorners(gray, (9,7),None)

if ret == True:
    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    if np.linalg.norm(corners2[0,0,:]) > np.linalg.norm(corners2[62,0,:]):
        corners2 = corners2[::-1,:,:]
    # Encuentra los vectores de rotación y traslación.
    _,rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)
    # proyectar puntos 3D al plano de la imagen
    imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

    img = draw(img,corners2,imgpts)
    cv2.imshow('img',img)
    k = cv2.waitKey(5000)

cv2.destroyAllWindows()
print("rvecs")
print(str(rvecs))
print("tvecs")
print(str(tvecs))
