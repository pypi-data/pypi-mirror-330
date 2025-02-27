#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform vec3 iResolution;

out vec3 fragColor;

float linear_burn(float b, float t)
{
	return max(b+t-1,0);
}

float linear_dodge(float b, float t)
{
	return min(b+t,1);
}

float linear_light(float b, float t)
{
	if (t <= 0.5)
		return linear_burn(b,2*t);
	else
		return linear_dodge(b,2*(t-0.5));
}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	vec3 b = texture(iChannel0,uv).rgb;
	vec3 t = texture(iChannel1,uv).rgb;
	fragColor = vec3(
		linear_light(b.r,t.r),
		linear_light(b.g,t.g),
		linear_light(b.b,t.b));
}