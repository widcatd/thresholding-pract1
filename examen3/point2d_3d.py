import numpy as np
import cv2

points = [
[598.563,	436.873,	525.596,	380.127], 
[631.825,	427.795,	557.187,	383.776],
]

# matriz intriseca de la camara derecha e izquierda 
intrinsec_l = np.array([[948.209,0,617.72],[0,960.912,374.665],[0,0,1]])
intrinsec_r = np.array([[960.613,0,653.568],[0,968.804,369.677],[0,0,1]])

distortion_left = np.array([0.0487857,-0.279364,0.00329971,-0.0073942,0.367614])
distortion_right = np.array([0.0400987,-0.218146,0.00793717,0.00552612,0.133228])

# matriz de rotacion y translacion de lac camaras 1y2 respecto al plano
Rl = cv2.Rodrigues(np.array([-0.78103995,-0.30358092,-0.05871129]))[0]
Tl = [[2.9147771],[0.09855708],[26.59388227]]

Rr = cv2.Rodrigues(np.array([-0.83922768, 0.19875148, 0.47898573]))[0]
Tr = [[0.261736697],[0.0165916331],[29.8146047]]

def point2d_3d(ul, vl, ur, vr):

    # Zc_left * [[ul],[vl],[1]] = Pl * [[X],[Y],[Z],[1]]
    Pl = np.dot(intrinsec_l, np.hstack((Rl, Tl)))
    Pr = np.dot(intrinsec_r, np.hstack((Rr, Tr)))

    #solucion de AX = B
    A_eq = [[ul*Pl[2][0]-Pl[0][0], ul*Pl[2][1]-Pl[0][1], ul*Pl[2][2]-Pl[0][2]],\
        [vl*Pl[2][0]-Pl[1][0], vl*Pl[2][1]-Pl[1][1], vl*Pl[2][2]-Pl[1][2]],\
        [ur*Pr[2][0]-Pr[0][0], ur*Pr[2][1]-Pr[0][1], ur*Pr[2][2]-Pr[0][2]],\
        [vr*Pr[2][0]-Pr[1][0], vr*Pr[2][1]-Pr[1][1], vr*Pr[2][2]-Pr[1][2]]] 
    B_eq = [Pl[0][3]-ul*Pl[2][3], Pl[1][3]-vl*Pl[2][3], Pr[0][3]-ur*Pr[2][3], Pr[1][3]-vr*Pr[2][3]]

    res = np.linalg.lstsq(A_eq, B_eq, rcond=-1)
    X = 20*res[0][0]
    Y = 20*res[0][1]
    Z = 20*res[0][2]


    return X, Y, Z

def undistort_image(img, intrinsic, distortion):
    h, w = img.shape[:2]
    newcam, roi=cv2.getOptimalNewCameraMatrix(intrinsic,distortion,(w,h),0,(w,h))
    dst = cv2.undistort(img, intrinsic, distortion, None, newcam)
    # recorta la imagen
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

def distance_3D(point0_2d, point1_2d):
    X0, Y0, Z0 = point2d_3d(point0_2d[0],point0_2d[1],point0_2d[2],point0_2d[3])
    X1, Y1, Z1 = point2d_3d(point1_2d[0],point1_2d[1],point1_2d[2],point1_2d[3])

    dist = np.sqrt((X0 - X1)*(X0 - X1) + (Y0 - Y1)*(Y0 - Y1) + (Z0 - Z1)*(Z0 - Z1))
    print(dist) 

def main():
    print("Distancia en 3D (mm)") 
    for point_2d in points[1:]:
        distance_3D(points[0], point_2d)


if __name__ == '__main__':
    main()
    