import cv2
from math import exp
from puzzleandy import *
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# https://github.com/opencv/opencv/blob/6a6a5a765d68c40174f42cf9f68291b33d770226/modules/imgproc/src/smooth.dispatch.cpp#L289C9-L289C31
# https://github.com/opencv/opencv/blob/6a6a5a765d68c40174f42cf9f68291b33d770226/modules/imgproc/src/smooth.dispatch.cpp#L152

def box_blur(x,n):
	k = np.ones(n)/n
	return cv2.sepFilter2D(x,-1,k,k)

# x in Z
def ceil_odd(x):
	return 2*(x//2)+1

def gauss_blur(x,n=None,s=None):
	if not n:
		if num_comps(x) == 1:
			n = round(6*s+1)
		else:
			n = round(8*s+1)
		n = ceil_odd(n)
	if not s:
		s = 0.15*n+0.35
	k = np.empty(n)
	for i in range(0,n):
		k[i] = exp(-(i-(n-1)/2)**2/(2*s**s))
	k /= np.sum(k)
	return cv2.sepFilter2D(x,-1,k,k)

def box_sharpen(x,n):
	y = box_blur(x,n)
	return x-y+x

def gauss_sharpen(x,n=None,s=None):
	y = gauss_blur(x,n,s)
	return x-y+x

x = mountains()
show(x)
x = gauss_sharpen(x,31)
show(x)