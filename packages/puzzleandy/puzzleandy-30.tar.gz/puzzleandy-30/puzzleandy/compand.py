from importlib.resources import files
import moderngl
import numpy as np
from .util import *

def _contents(path):
	with open(path) as f:
		return f.read()

def _compand(x,stem):
	w = x.shape[1]
	h = x.shape[0]
	shaders_path = files()/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/f'{stem}.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		_contents(vert_path),_contents(frag_path))
	prog['iChannel0'] = 0
	tex = ctx.texture((w,h),3,x.tobytes(),dtype='f4')
	tex.use(0)
	uni = prog['iResolution']
	uni.value = (w,h,1)
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

def compand(x):
	return _compand(x,'compand')

def inv_compand(x):
	return _compand(x,'inv_compand')