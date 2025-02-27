#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform vec3 iResolution;

out vec3 fragColor;

float D(float c)
{
	if (c <= 0.25)
		return ((16*c-12)*c+4)*c;
	else
		return sqrt(c);
}

float soft_light(float b, float t)
{
	if (t <= 0.5)
		return b-(1-2*t)*b*(1-b);
	else
		return b+(2*t-1)*(D(b)-b);
}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	vec3 b = texture(iChannel0,uv).rgb;
	vec3 t = texture(iChannel1,uv).rgb;
	fragColor = vec3(
		soft_light(b.r,t.r),
		soft_light(b.g,t.g),
		soft_light(b.b,t.b));
}