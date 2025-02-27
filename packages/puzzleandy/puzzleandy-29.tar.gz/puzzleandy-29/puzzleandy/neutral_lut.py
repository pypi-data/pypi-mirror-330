from importlib.resources import files
import math
import moderngl
import numpy as np

def _contents(path):
	with open(path) as f:
		return f.read()

def neutral_lut(n):
	shaders_path = files()/'shaders'
	vert_path = shaders_path/'default.vert'
	frag_path = shaders_path/'neutral_lut.frag'
	ctx = moderngl.create_standalone_context()
	prog = ctx.program(
		_contents(vert_path),_contents(frag_path))
	uni = prog['n']
	uni.value = n
	s = n*int(math.sqrt(n))
	col = ctx.texture((s,s),3,dtype='f4')
	fbo = ctx.framebuffer([col])
	fbo.use()
	fbo.clear(0,0,0,0)
	verts = ((-1,-1),(1,-1),(1,1),(-1,1))
	verts = np.array(verts, np.float32)
	vbo = ctx.buffer(verts.tobytes())
	vao = ctx.simple_vertex_array(prog,vbo,'pos')
	vao.render(moderngl.TRIANGLE_FAN)
	img = np.frombuffer(fbo.read(dtype='f4'),dtype=np.float32)
	img = img.reshape((s,s,3))
	return img