import glm
from importlib.resources import files
import moderngl
import numpy as np
from .basic import *

class Stop:
	def __init__(self,loc,val):
		self.loc = loc
		self.val = val

def var_cmap(img,
	col_locs,cols,col_mids,
	alpha_locs,alphas,alpha_mids):
	w = img.shape[1]
	h = img.shape[0]
	shaders_path = files()/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/'var_cmap.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		contents(vert_path),contents(frag_path))
	prog['iChannel0'] = 0
	tex = ctx.texture((w,h),1,img.tobytes(),dtype='f4')
	tex.use(0)
	uni = prog['iResolution']
	uni.value = (w,h,1)

	prog['num_cols'].value = len(col_stops)
	col_locs = [0]*10
	cols = [None]*10
	for i in range(len(col_stops)):
		col_locs[i] = col_stops[i].loc
		cols[i] = col_stops[i].val
	for i in range(len(col_stops),10):
		cols[i] = glm.vec3()
	prog['col_locs'].value = col_locs
	prog['cols'].value = cols
	zeros = [0]*(10-len(col_stops))
	prog['col_mids'].value = col_mids+zeros

	prog['num_alphas'].value = len(alpha_stops)
	alpha_locs = [0]*10
	alphas = [0]*10
	for i in range(len(alpha_stops)):
		alpha_locs[i] = alpha_stops[i].loc
		alphas[i] = alpha_stops[i].val
	prog['alpha_locs'].value = alpha_locs
	prog['alphas'].value = alphas
	zeros = [0]*(10-len(alpha_stops))
	prog['alpha_mids'].value = alpha_mids+zeros

	col = ctx.texture((w,h),3,dtype='f4')
	fbo = ctx.framebuffer([col])
	fbo.use()
	fbo.clear(0,0,0,0)
	verts = ((-1,-1),(1,-1),(1,1),(-1,1))
	verts = np.array(verts, np.float32)
	vbo = ctx.buffer(verts.tobytes())
	vao = ctx.simple_vertex_array(prog,vbo,'pos')
	vao.render(moderngl.TRIANGLE_FAN)
	img = np.frombuffer(fbo.read(dtype='f4'),dtype=np.float32)
	img = img.reshape((h,w,3))
	return img