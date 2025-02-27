import ctypes
import glm
import platform
from puzzleandy import *
if platform.system() == 'Windows':
	ctypes.windll.shcore.SetProcessDpiAwareness(1)

col_stops = [
	Stop(0,glm.vec3(0,0,0)/255),
	Stop(1,glm.vec3(43,177,236)/255)
]
col_mids = [0.68]
alpha_stops = [
	Stop(0,1),
	Stop(1,1)
]
alpha_mids = [0.5]

x = subway()
x = rgb_to_gray(x)
x = var_cmap(x,col_stops,col_mids,alpha_stops,alpha_mids)
show(x)