#version 330
#define PI (2*acos(0))

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform vec3 iResolution;
uniform float ux,uw,dx,dw;

out float fragColor;

float min3(float x,float y,float z)
{
	return min(min(x,y),z);
}

float max3(float x,float y,float z)
{
	return max(max(x,y),z);
}

float unlerp(float fx,float f0,float f1)
{
	return (fx-f0)/(f1-f0);
}

float clamp(float x)
{
	return min(max(x,0),1);
}

float s(float x,float e1,float e2)
{
	return clamp(unlerp(x,e1,e2));
}

float us(float x,float ux,float uw)
{
	if (uw == 0)
		return int(x >= ux);
	else
		return s(x,ux-uw/2,ux+uw/2);			
}

float ds(float x,float ux,float uw)
{
	if (dw == 0)
		return int(x <= dx);
	else
		return s(x,dx+dw/2,dx-dw/2);
}

float qualifier_circ(
	float x,float ux,float uw,float dx,float dw)
{
	if (ux <= dx)
		return max3(
			min(us(x+2*PI,ux,uw),ds(x+2*PI,dx,dw)),
			min(us(x,ux,uw),ds(x,dx,dw)),
			min(us(x-2*PI,ux,uw),ds(x-2*PI,dx,dw))
		);
	else
		return min3(
			max(us(x+2*PI,ux,uw),ds(x+2*PI,dx,dw)),
			max(us(x,ux,uw),ds(x,dx,dw)),
			max(us(x-2*PI,ux,uw),ds(x-2*PI,dx,dw))
		);
}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	float x = texture(iChannel0, uv).r;
	fragColor = qualifier_circ(x,ux,uw,dx,dw);
}