Image processing library. Images are float32 NumPy arrays.

```
import ctypes
import platform
from puzzleandy import *
if platform.system() == 'Windows':
  ctypes.windll.shcore.SetProcessDpiAwareness(1)

x = horses()
y = flip_hor(x)
z = multiply(y,x)
z = gamma(z,0.7)
show(z)
```

## Photos

```bones()```\
```building()```\
```horses()```\
```mountains()```\
```pelican()```\
```subway()```\
```woman_1()```\
```woman_2()```

## Adjustments

```bright(x,b)```\
x is an image.\
b in \[-1,1\].\
\
```contrast(x,c)```\
```sig_contrast(x,c)```\
x is an image.\
c in \[-1,1\].\
\
```gamma(x,c)```\
x is an image.\
g in \[-inf,inf\].\
\
```flip_hor(x)```\
```flip_vert(x)```\
x is an image.

## Blend Modes

b = bottom\
t = top\
\
```normal(b,t)```\
```darken(b,t)```\
```multiply(b,t)```\
```color_burn(b,t)```\
```linear_burn(b,t)```\
```darker_color(b,t)```\
```lighten(b,t)```\
```screen(b,t)```\
```color_dodge(b,t)```\
```linear_dodge(b,t)```\
```lighter_color(b,t)```\
```overlay(b,t)```\
```soft_light(b,t)```\
```hard_light(b,t)```\
```vivid_light(b,t)```\
```linear_light(b,t)```\
```pin_light(b,t)```\
```hard_mix(b,t)```\
```difference(b,t)```\
```exclusion(b,t)```\
```subtract(b,t)```\
```divide(b,t)```\
```hue(b,t)```\
```saturation(b,t)```\
```color(b,t)```\
```luminosity(b,t)```