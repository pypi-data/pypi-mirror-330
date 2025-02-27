def lerp(x,f0,f1):
	fx = (1-x)*f0+x*f1
	return fx

def unlerp(fx,f0,f1):
	x = (fx-f0)/(f1-f0)
	return x