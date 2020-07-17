import cv2
import numpy as np
import math

def aux(imname):
    img = cv2.imread(imname)
    if img is not None:
        return(img)
    else:
        return(None)

#(0,0,900,450,500,500) =0,125
#(0,0,450,900,500,500) =125,0
def get_dim(path):
    img = cv2.imread(path)
    h, w, c = img.shape
    return w,h

def transform_in(cx,cy,x,y,nx,ny):
    o=[]
    if(x>y):
        trx=nx/x
        o.append(cx*trx)
        o.append(ny-(((y/trx)/2)+(cy*trx)))
    else:
        trx=ny/y
        o.append(((x-nx)/2)+(cx*trx))
        o.append(ny-(cy*trx))
    return o

def transform_out(cx,cy,x,y,nx,ny):
    o=[]
    if(x>y):
        trx=nx/x
        o.append(cx*trx)
        o.append(ny-(((y/trx)/2)+(cy*trx)))
    else:
        trx=ny/y
        o.append(((x-nx)/2)+(cx*trx))
        o.append(ny-(cy*trx))
    return o


def puntos(direccion):
	imagen = cv2.imread(direccion)
	gray = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
	_,th = cv2.threshold(gray,140,255,cv2.THRESH_BINARY)
	contours,hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(imagen, contours, -1, (0,255,0), 3)
	xx=yy=ww=hh=0
	i=d=s=inf=[]
	for cnt in contours:
		#print(c)
		area = cv2.contourArea(cnt)
		(x, y, w, h) = cv2.boundingRect(cnt)
		if ww<w and hh<h:
			cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 255, 0), 1, cv2.LINE_AA)
			izquierdo = tuple(cnt[cnt[:,:,0].argmin()][0])
			derecho = tuple(cnt[cnt[:,:,0].argmax()][0])
			superior = tuple(cnt[cnt[:,:,1].argmin()][0])
			inferior = tuple(cnt[cnt[:,:,1].argmax()][0])
			i=[izquierdo[0],izquierdo[1]]
			d=[derecho[0],derecho[1]]
			s=[superior[0],superior[1]]
			inf=[inferior[0],inferior[1]]
			ww=w
			hh=h
			yy=y
			xx=x
	return[i,d,s,inf]
def get_PerspectiveTransform(origen, destino):
	M = np.ndarray((3, 3), dtype=float)
	R = np.ndarray((8, 8), dtype=float)
	T = np.ndarray((8, 1), dtype=float)
	X = np.ndarray((8, 1), dtype=float)
	for i in range(len(origen)):
		R[i, 0] = R[i+4, 3] = origen[i, 0]
		R[i, 1] = R[i + 4, 4] = origen[i, 1]
		R[i, 2] = R[i + 4, 5] = 1
		R[i, 3] = R[i, 4] = R[i, 5] = R[i + 4, 0] = R[i + 4, 1] = R[i + 4, 2] = 0
		R[i, 6] = -origen[i, 0] * destino[i, 0]
		R[i, 7] = -origen[i, 1] * destino[i, 0]
		R[i + 4, 6] = -origen[i, 0] * destino[i, 1]
		R[i + 4, 7] = -origen[i, 1] * destino[i, 1]
		T[i] = destino[i, 0]
		T[i + 4] = destino[i, 1]
	cv2.solve(R, T, X, cv2.DECOMP_LU)
	for i in range(len(X)):
		M[i//3, i % 3] = X[i]
	M[2, 2] = 1.
	return M
def warpperspective_(imagen, matriz, tam_salida):
	out = np.ndarray((tam_salida[1], tam_salida[0], 3), dtype=float)
	filas, columnas = (tam_salida[0], tam_salida[1])
	for k in range(filas):
		for i in range(columnas):
			out[i, k] = (255, 255, 255)
	matriz_in = np.ndarray((2, 1), dtype=float)
	valores = np.ndarray((2, 1), dtype=float)
	for x in range(1, filas):
		for y in range(1, columnas):
		#temp_matriz=matriz.copy()
			temp_matriz = np.copy(matriz)
			temp_matriz[0, :] = temp_matriz[0, :] / float(x)
			temp_matriz[0, :2] = temp_matriz[0, :2] - temp_matriz[2, :2]
			temp_matriz[1, :] = temp_matriz[1, :] / float(y)
			temp_matriz[1, :2] = temp_matriz[1, :2] - temp_matriz[2, :2]
			matriz_in[0, 0] = temp_matriz[2, 2] - temp_matriz[0, 2]
			matriz_in[1, 0] = temp_matriz[2, 2] - temp_matriz[1, 2]
			cv2.solve(temp_matriz[:2, :2], matriz_in, valores)
			valor_x = valores[0, 0]
			valor_y = valores[1, 0]
			if 0 <= valor_x < imagen.shape[1] and 0 <= valor_y < imagen.shape[0]:
				out[y, x] = imagen[int(valor_y), int(valor_x)]
	return out
def order_points(pts):
	rect = np.zeros((4, 2), dtype = "float32")
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	return rect
def four_point_transform(image, pts):
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	dst = np.array([[0, 0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")
	M = get_PerspectiveTransform(rect, dst)
	#warped = warpperspective_(image, M, (maxWidth, maxHeight))
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))# return the warped image
	return warped
#a=[[211,388],[721,995],[608,365],[263,1061],]


def hist_eq(imname):
    img = cv2.imread(imname)
    #Si el archivo es imagen:
    if img is not None:
        #mostramos imagen original
        #calculamos el histograma por cada capa y los mostramos
        lh=[]
        ll=[]
        for i in range(len(img[0][0])):
            h=cv2.calcHist([img], [i], None, [256], [0, 256])
            lh.append(h)
            #calculamos los P(n)
            ph=[0]*256
            for i in range (len(h)):
                ph[i]=h[i]/(img.shape[0]*img.shape[1])
            
            #calculamos los s(n)
            sn=[]
            for i in range(256):
                t=0
                for i in range(i):
                    t+=ph[i]
                sn.append(math.floor(256*t))
            ll.append(sn)
        
        #creamos una imagen en negro
        out=np.zeros(shape=img.shape,dtype=np.uint8)

        #aplicamos el Histogram equalization en los 3 canales
        for i in range(len(img[0][0])):
            for j in range(img.shape[0]):
                for k in range(img.shape[1]):
                    out[j][k][i]=ll[i][img[j][k][i]]

        #return(out)

        return(out)
    else:
        return(None)


def contrast_str(imname,limi):
    img = cv2.imread(imname)
    if img is not None:

        h1 = cv2.calcHist([img], [0], None, [256], [0, 256])
        h1_c=[]
        for i in range (h1.shape[0]):
            if h1[i]!=0:
                h1_c.append(i)
        t=len(h1_c)
        r=int(t/limi)
        l1=h1_c[0+r]
        u1=h1_c[len(h1_c)-1-r]
        
        h2 = cv2.calcHist([img], [1], None, [256], [0, 256])
        h2_c=[]
        for i in range (h2.shape[0]):
            if h2[i]!=0:
                h2_c.append(i)
        t=len(h2_c)
        r=int(t/10)
        l2=h2_c[0+r]
        u2=h2_c[len(h2_c)-1-r]

        h3 = cv2.calcHist([img], [2], None, [256], [0, 256])
        h3_c=[]
        for i in range (h3.shape[0]):
            if h3[i]!=0:
                h3_c.append(i)
        t=len(h3_c)
        r=int(t/10)
        l3=h3_c[0+r]
        u3=h3_c[len(h3_c)-1-r]

        out=np.zeros(shape=img.shape,dtype=np.uint8)

        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                tt=img[i][j][0]-l1
                if(tt<0):
                    out[i][j][0]=0
                else:
                    out[i][j][0]=tt*int(255/(u1-l1))
                
                tt=img[i][j][1]-l2
                if(tt<0):
                    out[i][j][1]=0
                else:
                    out[i][j][1]=tt*int(255/(u2-l2))

                tt=img[i][j][2]-l3
                if(tt<0):
                    out[i][j][2]=0
                else:
                    out[i][j][2]=tt*int(255/(u3-l3))
        
        #return(out)

        return(out)
    else:
        return(None)

if __name__ == "__main__":
    a=[]
    a=puntos('./input/p6.jpg')
    temporal=np.array(a)
    img=cv2.imread('./input/p6.jpg')
    b=four_point_transform(img,temporal)
    cv2.imshow('adad',b)
    cv2.waitKey(0)
    cv2.destroyAllWindows()