import numpy as np
from .comps import (
	num_comps,
	get_lab_l,set_lab_l)
from .type_convert import to_float,to_uint
from .util import remap

def hist(x,n=256):
	H = np.zeros(n,np.uint32)
	for i in range(len(x)):
		H[x[i]] += 1
	return H

def cum_sum(x):
	S = np.empty(len(x))
	S[0] = x[0]
	for i in range(1,len(x)):
		S[i] = S[i-1]+x[i]
	return S

def norm_cdf(x,n):
	x = x.flatten()
	H = hist(x,n)
	cdf = cum_sum(H)
	m = np.min(cdf[np.argmax(cdf > 0)])
	M = np.max(cdf)
	cdf = remap(cdf,m,M,0,255)
	return cdf.astype('uint8')

def eq_hist(x,n=256,M=1):
	assert(num_comps(x) in [1,3])
	match num_comps(x):
		case 1:
			w = x.shape[1]
			h = x.shape[0]
			x /= M
			x = to_uint(x)
			cdf = norm_cdf(x,n)
			x = cdf[x]
			x = x.reshape(h,w)
			x = to_float(x)
			return M*x
		case 3:
			l = get_lab_l(x)
			l = eq_hist(l,n,100)
			return set_lab_l(x,l)

def match_hist(x,y,n=256,M=1):
	assert(num_comps(x) == num_comps(y)
		and num_comps(x) in [1,3])
	match num_comps(x):
		case 1:
			w = x.shape[1]
			h = x.shape[0]
			x /= M
			y /= M
			x = to_uint(x)
			y = to_uint(y)
			cdf_x = norm_cdf(x,n)
			cdf_y = norm_cdf(y,n)
			f = np.zeros(n,np.uint8)
			for i in range(n):
				f[i] = np.argmax(cdf_x[i] <= cdf_y)
			x = f[x]
			x = x.reshape(h,w)
			x = to_float(x)
			return M*x
		case 3:
			xl = get_lab_l(x)
			yl = get_lab_l(y)
			xl = match_hist(xl,yl,n,100)
			return set_lab_l(x,xl)