#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform vec3 iResolution;

out vec3 fragColor;

float inv_compand(float x)
{
	if (x <= 0.04045)
		return x/12.92;
	else
		return pow((x+0.055)/1.055,2.4);
}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	vec3 c = texture(iChannel0,uv).rgb;
	fragColor = vec3(
		inv_compand(c.r),
		inv_compand(c.g),
		inv_compand(c.b));
}