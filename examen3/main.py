from autograd import numpy as np
from math import tan, radians
from autograd import value_and_grad

def reprojeccion_error(points, camera, views, observations):
    assert len(views) == len(observations)
    ret = 0.0
    camera_matrix = calibracion_camara(camera)
    for view, (pointids, observed_pixels) in zip(views, observations):
        position, orientation = view[:3], view[3:]
        camera_centric = rotacion(points[pointids], orientation) - position
        expected_pixels = proyeccion(camera_centric, camera_matrix)
        ret = ret + np.linalg.norm(observed_pixels - expected_pixels, axis=1)
    return ret

def rotacion(points, q):
    rot = quat2mat(q)
    return np.dot(points, rot)

_FLOAT_EPS = np.finfo(np.float).eps
def quat2mat(q):
    w, x, y, z = q
    Nq = w*w + x*x + y*y + z*z
    if Nq < _FLOAT_EPS:
        return np.eye(3)
    s = 2.0/Nq
    X = x*s
    Y = y*s
    Z = z*s
    wX = w*X; wY = w*Y; wZ = w*Z
    xX = x*X; xY = x*Y; xZ = x*Z
    yY = y*Y; yZ = y*Z; zZ = z*Z
    return np.array(
           [[ 1.0-(yY+zZ), xY-wZ, xZ+wY ],
            [ xY+wZ, 1.0-(xX+zZ), yZ-wX ],
            [ xZ-wY, yZ+wX, 1.0-(xX+yY) ]])

def calibracion_camara(camera):
    fovh, width, height = camera
    f = width/2 * tan(radians(fovh)/2)
    cx, cy = width/2, height/2
    return np.array(
        ((f, 0, cx),
         (0, f, cy),
         (0, 0,  1)))

def proyeccion(points, camera_matrix):
    projected = np.dot(points, camera_matrix.T)
    divided = projected / projected[:,2].reshape((len(projected),1))
    assert (divided[:,2] == 1).all()
    return divided[:,0:2]

def t_proyeccion():
    w, h = 1280, 962
    camera_matrix = calibracion_camara((90, w, h))
    res = np.array([
        [ w/2,    0,  w/2 ],
        [   0,  w/2,  h/2 ],
        [   0,    0,    1 ]])
    assert np.allclose(camera_matrix, res)
    test_set = np.array([
        [ 0, 0,1,    w/2, h/2],
        [ 1, 0,1,      w, h/2],
        [-1, 0,1,      0, h/2],
        [ 0, h/w,1,  w/2,   h],
        [ 0,-h/w,1,  w/2,   0],
    ], dtype=float)
    points = test_set[:,0:3]
    pixels = proyeccion(points, camera_matrix)
    assert np.allclose(pixels, test_set[:,3:5])

def t_rotacion():
    points = np.ones((1,3))
    e = np.array([1,0,0,0]) # indentidad
    eye = quat2mat(e)
    assert np.allclose(np.identity(3), eye)
    assert (rotacion(points, e) == points).all()
    quat = [0, 1, 0, 0]
    mat = quat2mat(quat) # Rotación de 180 grados alrededor del eje x
    assert np.allclose(mat, np.diag([1, -1, -1]))
    rotaciond = rotacion(points, quat) #modificar y y z
    assert np.allclose(rotaciond, [[ 1, -1, -1]])

t_proyeccion()
t_rotacion()