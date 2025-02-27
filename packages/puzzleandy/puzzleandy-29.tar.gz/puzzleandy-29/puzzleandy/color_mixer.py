import cv2
import numpy as np

def color_mixer(img,m):
	m = np.array(m)
	m = m.reshape(3,3)
	return cv2.transform(img,m.T,None)