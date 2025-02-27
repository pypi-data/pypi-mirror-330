import cv2

def rgb_to_hsl(x):
	return cv2.cvtColor(x,cv2.COLOR_RGB2HLS)

def hsl_to_rgb(x):
	return cv2.cvtColor(x,cv2.COLOR_HLS2RGB)

def rgb_to_hsv(x):
	return cv2.cvtColor(x,cv2.COLOR_RGB2HSV)

def rgb_to_lab(x):
	return cv2.cvtColor(x,cv2.COLOR_RGB2LAB)

def hsv_to_rgb(x):
	return cv2.cvtColor(x,cv2.COLOR_HSV2RGB)

def rgb_to_gray(x):
	return cv2.cvtColor(x,cv2.COLOR_RGB2GRAY)

def bgr_to_rgb(x):
	return cv2.cvtColor(x,cv2.COLOR_BGR2RGB)

def rgb_to_lab(x):
	return cv2.cvtColor(x,cv2.COLOR_RGB2LAB)

def lab_to_rgb(x):
	return cv2.cvtColor(x,cv2.COLOR_LAB2RGB)