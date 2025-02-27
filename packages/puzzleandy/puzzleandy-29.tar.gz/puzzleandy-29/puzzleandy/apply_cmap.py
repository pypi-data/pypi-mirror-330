from importlib.resources import files
import moderngl
import numpy as np
from .basic import *

def apply_cmap(img,cmap):
	img_w = img.shape[1]
	img_h = img.shape[0]
	cmap_w = cmap.shape[1]
	cmap_h = cmap.shape[0]
	shaders_path = files()/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/'apply_cmap.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		contents(vert_path),contents(frag_path))
	prog['iChannel0'] = 0
	tex = ctx.texture(
		(img_w,img_h),1,img.tobytes(),dtype='f4')
	tex.use(0)
	prog['iChannel1'] = 1
	tex = ctx.texture(
		(cmap_w,cmap_h),4,cmap.tobytes(),dtype='f4')
	samp = ctx.sampler(False,texture=tex)
	samp.use(1)
	uni = prog['iChannelResolution']
	uni.value = (
		(img_w,img_h,1),
		(cmap_w,cmap_h,1))
	col = ctx.texture((img_w,img_h),4,dtype='f4')
	fbo = ctx.framebuffer([col])
	fbo.use()
	fbo.clear(0,0,0,0)
	verts = ((-1,-1),(1,-1),(1,1),(-1,1))
	verts = np.array(verts, np.float32)
	vbo = ctx.buffer(verts.tobytes())
	vao = ctx.simple_vertex_array(prog,vbo,'pos')
	vao.render(moderngl.TRIANGLE_FAN)
	img = np.frombuffer(
		fbo.read(components=4,dtype='f4'),dtype=np.float32)
	img = img.reshape((img_h,img_w,4))
	return img