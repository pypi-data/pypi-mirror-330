from math import pi
from .util import *

def hue_shift(x,s):
	H = get_hsl_h(x)
	H = np.mod(H+s,360)
	return set_hsl_h(x,H)

def bright(x,b):
	return clamp(x+b,0,1)

def gamma(x,g):
	return x**g

def contrast(x,c):
	t = remap(c,-1,1,0,0.5*pi)
	return clamp(pt_angle(x,0.5,0.5,t))