import glm
from puzzleandy import *

w = 512
h = 60
col_locs = [0,1]
cols = [
	glm.vec3(0,0,0)/255,
	glm.vec3(43,177,236)/255
]
col_mids = [0.68]
alpha_locs = [0,1]
alphas = [1,1]
alpha_mids = [0.5]
cmap = make_cmap(
	w,h,
	col_locs,cols,col_mids,
	alpha_locs,alphas,alpha_mids)

img = subway()
img = rgb_to_gray(img)
img = apply_cmap(img,cmap)
show(img)