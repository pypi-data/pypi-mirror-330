import cv2
from .comps import num_comps

def gray_to_bgr(x):
	assert num_comps(x) == 1
	return cv2.cvtColor(x,cv2.COLOR_GRAY2BGR)

def gray_to_bgra(x):
	assert num_comps(x) == 1
	return cv2.cvtColor(x,cv2.COLOR_GRAY2BGRA)

def rgb_to_gray(x):
	assert num_comps(x) == 3
	return cv2.cvtColor(x,cv2.COLOR_RGB2GRAY)

def rgba_to_gray(x):
	assert num_comps(x) == 3
	return cv2.cvtColor(x,cv2.COLOR_RGBA2GRAY)

def rgb_to_rgba(x):
	assert num_comps(x) == 3
	return cv2.cvtColor(x,cv2.COLOR_RGB2RGBA)

def rgb_to_bgr(x):
	assert num_comps(x) == 3
	return cv2.cvtColor(x,cv2.COLOR_RGB2BGR)

def rgba_to_bgr(x):
	assert num_comps(x) == 3
	return cv2.cvtColor(x,cv2.COLOR_RGBA2BGR)

def rgba_to_bgra(x):
	assert num_comps(x) == 4
	return cv2.cvtColor(x,cv2.COLOR_RGBA2BGRA)

def bgra_to_rgba(x):
	assert num_comps(x) == 4
	return cv2.cvtColor(x,cv2.COLOR_BGRA2RGBA)

def bgr_to_rgb(x):
	assert num_comps(x) == 3
	return cv2.cvtColor(x,cv2.COLOR_RGB2BGR)