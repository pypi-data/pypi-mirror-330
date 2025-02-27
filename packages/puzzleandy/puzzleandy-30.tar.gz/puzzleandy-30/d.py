import colour.difference
import ctypes
import glm
from puzzleandy import *
ctypes.windll.shcore.SetProcessDpiAwareness(1)

x = cow()
w = x.shape[1]
h = x.shape[0]
y = solid_color(w,h,glm.vec3(120,178,250)/255)
textiles = False
z1 = delta_e_2000(x,y)
#print(np.allclose(z1,z2,0.0001))
z1 = clamp(remap(z1,0,20,0,1))
show(z1)