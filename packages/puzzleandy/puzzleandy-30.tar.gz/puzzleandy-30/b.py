import ctypes
import cv2
import glm
import matplotlib.pyplot as plt
import numpy as np
from skimage import data
import sys
from puzzleandy import *
ctypes.windll.shcore.SetProcessDpiAwareness(1)



c = glm.vec2(256,256)
b = glm.vec2(50,50)
img = sd_box(512,512,c,b)
img = np.maximum(img,0)
img = np.absolute(img)
img = norm(img)
img = rainbow(img)
show(img)
sys.exit(0)

img = rgb_to_gray(img)
print(img.shape)
img = ocean(img)
show(img)
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
eps = 0.001
auto = auto_min_max(img,eps)
if auto is not None:
	show(auto)
man = man_min_max(img,0.2,0.7)
show(man)