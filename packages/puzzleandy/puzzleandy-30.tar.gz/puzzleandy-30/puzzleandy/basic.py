import cv2
import numpy as np
from pathlib import Path
from .lib_convert import to_cv

def contents(path):
	return Path(path).read_text()

def solid_color(w,h,c):
	c = np.array(c,np.float32)
	return np.full((h,w,len(c)),c,np.float32)

def show(x):
	x = to_cv(x)
	cv2.imshow('',x)
	cv2.waitKey()