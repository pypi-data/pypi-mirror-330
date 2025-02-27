import cv2
from .lib_convert import from_cv,to_cv

def read(path):
	x = cv2.imread(path)
	return from_cv(x)

def write(x,path):
	x = to_cv(x)
	cv2.imwrite(path,x)