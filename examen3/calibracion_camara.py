import numpy as np
import cv2
import todas

IMAGENES_RUTA = 'image/*left.jpg'
GUARDAR_RUTA = "parameters/parameters_left.yaml"

# Ingrese todas las imágenes desde una cámara 
imagenes = todas.todas(IMAGENES_RUTA)

# Criterios de terminación 
criterio = (cv2.TERM_CRITERIO_EPS + cv2.TERM_CRITERIO_MAX_ITER, 20, 0.001)

# preparar puntos de objeto
objp = np.zeros((7*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)

# Matrices para almacenar puntos de objeto y puntos de imagen de todas las imágenes
objpoints = [] # 3D puntos en el espacio del mundo real
imgpoints = [] # 2D puntos en el plano de la imagen
correct_idx = []

print("Verifique manualmente si las esquinas son correctas")
print("presione 'a' para corregir o espere 5 segundos para error")

for idx, fname in enumerate(imagenes):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Encuentra las esquinas 
    ret, corners = cv2.findChessboardCorners(gray, (9,7),None)

    # Si lo encuentra, agregue puntos de objeto
    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criterio)
        # Dibujar y mostrar las esquinas
        img = cv2.drawChessboardCorners(img, (9,7), corners2,ret)
        cv2.putText(img, str(idx), (40, 50), cv2.FUENTE, 2.0, (0, 0, 255), 2)
        cv2.imshow('img',img)
        key = cv2.waitKey(5000)
        if key & 0xFF == ord('a'):
            correct_idx.append(idx)
            objpoints.append(objp)
            imgpoints.append(corners2)
            continue
        else:
            continue

print(correct_idx)
# Utilice solo las imágenes con las esquinas "correctas" para la calibración
cv2.destroyAllWindows()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

# ---------- Guardar la calibración -----------------
cv_file = cv2.FileStorage(GUARDAR_RUTA, cv2.FILE_ARCHIVO_ESCRIBIR)
cv_file.write("camera_matrix", mtx)
cv_file.write("dist_coeff", dist)
cv_file.release()
