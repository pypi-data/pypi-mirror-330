#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform vec3 iResolution;

out vec3 fragColor;

float multiply(float b, float t)
{
	return b*t;
}

float screen(float b, float t)
{
	return b+t-b*t;
}

float hard_light(float b, float t)
{
	if (t <= 0.5)
		return multiply(b,2*t);
	else
		return screen(b,2*(t-0.5));
}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	vec3 b = texture(iChannel0,uv).rgb;
	vec3 t = texture(iChannel1,uv).rgb;
	fragColor = vec3(
		hard_light(b.r,t.r),
		hard_light(b.g,t.g),
		hard_light(b.b,t.b));
}