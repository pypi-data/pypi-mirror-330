#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform vec3 iResolution;

out vec3 fragColor;

float color_burn(float b, float t)
{
	if (b == 1)
		return 1;
	else if (t == 0)
		return 0;
	else
		return 1-min((1-b)/t,1);
}

float color_dodge(float b, float t)
{
	if (b == 0)
		return 0;
	else if (t == 1)
		return 1;
	else
		return min(b/(1-t),1);
}

float vivid_light(float b, float t)
{
	if (t <= 0.5)
		return color_burn(b,2*t);
	else
		return color_dodge(b,2*(t-0.5));
}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	vec3 b = texture(iChannel0,uv).rgb;
	vec3 t = texture(iChannel1,uv).rgb;
	fragColor = vec3(
		vivid_light(b.r,t.r),
		vivid_light(b.g,t.g),
		vivid_light(b.b,t.b));
}