import cv2
import numpy as np
from .space_convert import rgb_to_lab

def delta_e_1994(x,y,textiles=False):

	x = rgb_to_lab(x)
	y = rgb_to_lab(y)

	L1,a1,b1 = cv2.split(x)
	L2,a2,b2 = cv2.split(y)

	C1 = np.hypot(a1,b1)
	C2 = np.hypot(a2,b2)

	da = a1-a2
	db = b1-b2
	dC = C1-C2
	K1 = 0.048 if textiles else 0.045
	K2 = 0.014 if textiles else 0.015

	dL = L1-L2
	dH = np.sqrt(np.maximum(da**2+db**2-dC**2,0))
	KL = 2 if textiles else 1
	KC = 1
	KH = 1
	SL = 1
	SC = 1+K1*C1
	SH = 1+K2*C1

	return np.sqrt(
		(dL/(KL*SL))**2+
		(dC/(KC*SC))**2+
		(dH/(KH*SH))**2)