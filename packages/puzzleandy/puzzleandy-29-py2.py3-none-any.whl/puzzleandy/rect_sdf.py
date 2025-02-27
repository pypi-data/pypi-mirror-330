from importlib.resources import files
import moderngl
import numpy as np
from .basic import *

def sd_box(w,h,c,b):
	shaders_path = files()/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/'sd_box.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		contents(vert_path),contents(frag_path))
	prog['c'] = c
	prog['b'] = b
	col = ctx.texture((w,h),1,dtype='f4')
	fbo = ctx.framebuffer([col])
	fbo.use()
	fbo.clear(0,0,0,0)
	verts = ((-1,-1),(1,-1),(1,1),(-1,1))
	verts = np.array(verts, np.float32)
	vbo = ctx.buffer(verts.tobytes())
	vao = ctx.simple_vertex_array(prog,vbo,'pos')
	vao.render(moderngl.TRIANGLE_FAN)
	img = np.frombuffer(
		fbo.read(dtype='f4',components=1),dtype=np.float32)
	img = img.reshape((h,w,1))
	return img