import numpy as np
from .comps import num_comps
from .swap import (
	rgb_to_gray,rgba_to_gray,
	gray_to_bgr,rgb_to_bgr,rgba_to_bgr
)

def to_uint(img):
	img = np.clip(img*255,0,255)
	return img.astype(np.uint8)

def to_float(img):
	img = np.clip(img/255,0,1)
	return img.astype(np.float32)

def to_gray(x):
	assert num_comps(x) in [1,3,4]
	match num_comps(x):
		case 1:
			return x
		case 3:
			return rgb_to_gray(x)
		case 4:
			return rgba_to_gray(x)

def to_bgr(x):
	assert num_comps(x) in [1,3,4]
	match num_comps(x):
		case 1:
			return gray_to_bgr(x)
		case 3:
			return rgb_to_bgr(x)
		case 4:
			return rgba_to_bgr(x)