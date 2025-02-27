from importlib.resources import files
import math
import moderngl
import numpy as np

def _contents(path):
	with open(path) as f:
		return f.read()

def apply_lut(img,lut,factor=1):
	img_w = img.shape[1]
	img_h = img.shape[0]
	lut_w = lut.shape[1]
	lut_h = lut.shape[0]
	shaders_path = files()/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/'apply_lut.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		_contents(vert_path),_contents(frag_path))
	prog['iChannel0'] = 0
	tex = ctx.texture(
		(img_w,img_h),3,img.tobytes(),dtype='f4')
	tex.use(0)
	prog['iChannel1'] = 1
	tex = ctx.texture(
		(lut_w,lut_h),3,lut.tobytes(),dtype='f4')
	tex.use(1)
	uni = prog['iResolution']
	uni.value = (img_w,img_h,1)
	uni = prog['n']
	uni.value = int(math.cbrt(lut_w**2))
	uni = prog['factor']
	uni.value = factor
	col = ctx.texture((img_w,img_h),3,dtype='f4')
	fbo = ctx.framebuffer([col])
	fbo.use()
	fbo.clear(0,0,0,0)
	verts = ((-1,-1),(1,-1),(1,1),(-1,1))
	verts = np.array(verts, np.float32)
	vbo = ctx.buffer(verts.tobytes())
	vao = ctx.simple_vertex_array(prog,vbo,'pos')
	vao.render(moderngl.TRIANGLE_FAN)
	img = np.frombuffer(fbo.read(dtype='f4'),dtype=np.float32)
	img = img.reshape((img_h,img_w,3))
	return img