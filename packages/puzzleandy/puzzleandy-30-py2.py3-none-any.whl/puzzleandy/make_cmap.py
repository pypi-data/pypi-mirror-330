from coloraide import Color
import numpy as np
from scipy.interpolate import (
	LinearNDInterpolator,
	PchipInterpolator)
from .util import unlerp

def idx(x,y):
	n = len(x)
	if y <= x[0]:
		return 0;
	elif x[-1] <= y:
		return n-1
	else:
		for i in range(n):
			if x[i] > y:
				return i

def lookup(locs,vals,loc_interps,val_interps,loc):
	n = len(locs)
	i = idx(locs,loc);
	if i == 0:
		return vals[0]
	elif i == n:
		return vals[-1]
	else:
		t = unlerp(loc,locs[i-1],locs[i]);
		t = loc_interps[i-1](t)
		return val_interps[i-1](t)

def make_cmap(
	w,h,
	col_locs,cols,col_mids,
	alpha_locs,alphas,alpha_mids):

	n = len(col_locs)

	col_loc_interps = [None]*(n-1)
	col_interps = [None]*(n-1)
	for i in range(n-1):
		x = [0,col_mids[i],1]
		y = [0,0.5,1]
		col_loc_interps[i] = PchipInterpolator(x,y)
		col_interps[i] = Color.interpolate(
			[Color('srgb',cols[i]),Color('srgb',cols[i+1])],
			space='srgb')

	alpha_loc_interps = [None]*(n-1)
	alpha_interps = [None]*(n-1)
	for i in range(n-1):
		xp = [0,alpha_mids[i],1]
		fp = [0,0.5,1]
		alpha_loc_interps[i] = PchipInterpolator(xp,fp)
		xp = [0,1]
		fp = [alphas[i-1],alphas[i]]
		alpha_interps[i] = lambda x: np.interp(x,xp,fp)

	img = np.empty((1,w,4),np.float32)
	for i in range(w):
		loc = i/(w-1)
		col = lookup(col_locs,cols,col_loc_interps,col_interps,loc)
		alpha = lookup(alpha_locs,alphas,alpha_loc_interps,alpha_interps,loc)
		img[0,i] = (col[0],col[1],col[2],alpha)
	return np.tile(img,(h,1,1))