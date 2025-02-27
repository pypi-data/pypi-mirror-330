from math import *
from PIL import Image
import skimage
from puzzleandy import *

def sgn(x):
	if x < 0:
		return -1
	elif x == 0:
		return 0
	else:
		return 1

def trim(img):
	bbox = np.nonzero(img[:,:,3])
	top = bbox[0].min()
	bot = bbox[0].max()
	left = bbox[1].min()
	right = bbox[1].max()
	return img[top:bot,left:right,:]

img = skimage.data.chelsea()
img = to_float(img)
img = rgb_to_rgba(img)

h1,w1 = img.shape[:2]
t = 15*pi/180
a = atan2(h1,w1)
k = hypot(w1,h1)
q = floor(2*t/pi)
s = -2*sgn(q%2)+1
w2 = k*abs(cos(t-s*a))
h2 = k*abs(sin(t+s*a))
img2 = rotate1(img,t)
img3 = rotate2(img,t)
img4 = rotate3(img,t)
h3,w3 = img2.shape[:2]
print(w1,h1)
print(w2,h2)
print(w3,h3)
write(img2,'pil.png')
write(img3,'skimage.png')
write(img4,'wand.png')
