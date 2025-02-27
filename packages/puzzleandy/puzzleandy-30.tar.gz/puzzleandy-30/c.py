import ctypes
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from puzzleandy import *
ctypes.windll.shcore.SetProcessDpiAwareness(1)

font = ImageFont.truetype('arial.ttf',200)
txt = 'Whatever O!'
bbox = font.getbbox(txt)
w = bbox[2]-bbox[0]
h = bbox[3]-bbox[1]
img = Image.new('RGBA',(w,h))
draw = ImageDraw.Draw(img)
draw.text((-bbox[0],-bbox[1]),txt,font=font)
img = np.array(img)
print(img.shape)
img = to_float(img)
write(img,'out.png')
show(img)