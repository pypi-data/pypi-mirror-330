from importlib.resources import files
from .basic import *
from .apply_cmap import *

def _cmap(img,basename):
	path = files()/'cmaps'/basename
	M = read(path)
	return apply_cmap(img,M)

def autumn(img):
	return _cmap(img,'autumn.jpg')

def bone(img):
	return _cmap(img,'bone.jpg')

def cividis(img):
	return _cmap(img,'cividis.jpg')

def cool(img):
	return _cmap(img,'cool.jpg')

def deep_green(img):
	return _cmap(img,'deep_green.jpg')

def hot(img):
	return _cmap(img,'hot.jpg')

def hsv(img):
	return _cmap(img,'hsv.jpg')

def inferno(img):
	return _cmap(img,'inferno.jpg')

def jet(img):
	return _cmap(img,'jet.jpg')

def magma(img):
	return _cmap(img,'magma.jpg')

def ocean(img):
	return _cmap(img,'ocean.jpg')

def parula(img):
	return _cmap(img,'parula.jpg')

def pink(img):
	return _cmap(img,'pink.jpg')

def plasma(img):
	return _cmap(img,'plasma.jpg')

def rainbow(img):
	return _cmap(img,'rainbow.jpg')

def spring(img):
	return _cmap(img,'spring.jpg')

def summer(img):
	return _cmap(img,'summer.jpg')

def turbo(img):
	return _cmap(img,'turbo.jpg')

def twilight(img):
	return _cmap(img,'twilight.jpg')

def twilight_shifted(img):
	return _cmap(img,'twilight_shifted.jpg')

def viridis(img):
	return _cmap(img,'viridis.jpg')

def winter(img):
	return _cmap(img,'winter.jpg')
