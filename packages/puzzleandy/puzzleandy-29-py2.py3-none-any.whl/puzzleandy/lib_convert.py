import numpy as np
import PIL
import wand.image
from .comps import num_comps
from .swap import (
	rgb_to_bgr,bgr_to_rgb,
	rgba_to_bgra)
from .type_convert import to_float,to_uint

def to_cv(img):
	match num_comps(img):
		case 3:
			img = rgb_to_bgr(img)
		case 4:
			img = rgba_to_bgra(img)
	return to_uint(img)

def to_pil(img):
	img = to_uint(img)
	return PIL.Image.fromarray(img)

def to_wand(img):
	img = to_uint(img)
	return wand.image.Image.from_array(img)

def from_cv(img):
	img = bgr_to_rgb(img)
	return to_float(img)

def from_pil(img):
	img = np.array(img)
	return to_float(img)

def from_wand(img):
	img = np.array(img)
	return to_float(img)