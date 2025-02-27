#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform vec3 iChannelResolution[2];

out vec4 fragColor;

vec4 lerp(float x, vec4 f0, vec4 f1)
{
	vec4 fx = (1-x)*f0+x*f1;
	return fx;
}

vec4 lookup(int x)
{
	vec2 uv = vec2(x+0.5,0.5)/iChannelResolution[1].xy;
	return texture(iChannel1,uv);
}

void main()
{
	vec2 uv = fragCoord/iChannelResolution[0].xy;
	vec3 c = texture(iChannel0,uv).rgb;
	int w = int(iChannelResolution[1].x);
	int x0 = int(min(floor(c.r*w),w-1));
	int x1 = int(min(ceil(c.r*w),w-1));
	vec4 c0 = lookup(x0);
	vec4 c1 = lookup(x1);
	vec4 res = lerp(c.r,c0,c1);
	fragColor = res;
}