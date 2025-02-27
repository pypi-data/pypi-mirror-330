from .lib_convert import *

def flip_hor(img):
	return cv2.flip(img,1)

def flip_vert(img):
	return cv2.flip(img,0)

def rot(img,theta):
	img = to_wand(img)
	theta = -rad_to_deg(theta)
	img.rotate(theta)
	return from_wand(img)

def rot_90(img):
	return cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)

def rot_180(img):
	return cv2.rotate(img,cv2.ROTATE_180)

def rot_270(img):
	return cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)