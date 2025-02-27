from importlib.resources import files
import moderngl
import numpy as np

def _contents(path):
	with open(path) as f:
		return f.read()

def circular_qualifier(x,ux,uw,dx,dw):
	w = x.shape[1]
	h = x.shape[0]
	shaders_path = files()/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/'circular_qualifier.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		_contents(vert_path),_contents(frag_path))
	prog['iChannel0'] = 0
	tex = ctx.texture((w,h),1,x.tobytes(),dtype='f4')
	tex.use(0)
	uni = prog['iResolution']
	uni.value = (w,h,1)
	uni = prog['ux']
	uni.value= ux
	uni = prog['uw']
	uni.value= uw
	uni = prog['dx']
	uni.value= dx
	uni = prog['dw']
	uni.value= dw
	col = ctx.texture((w,h),1,dtype='f4')
	fbo = ctx.framebuffer([col])
	fbo.use()
	fbo.clear(0,0,0,0)
	verts = ((-1,-1),(1,-1),(1,1),(-1,1))
	verts = np.array(verts, np.float32)
	vbo = ctx.buffer(verts.tobytes())
	vao = ctx.simple_vertex_array(prog,vbo,'pos')
	vao.render(moderngl.TRIANGLE_FAN)
	x = np.frombuffer(fbo.read(components=1,dtype='f4'),dtype=np.float32)
	x = x.reshape((h,w,1))
	return x