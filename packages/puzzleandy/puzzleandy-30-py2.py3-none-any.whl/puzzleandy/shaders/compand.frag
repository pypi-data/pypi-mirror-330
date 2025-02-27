#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform vec3 iResolution;

out vec3 fragColor;

float compand(float x)
{
	if (x <= 0.0031308)
		return 12.92*x;
	else
		return 1.055*pow(x,1/2.4)-0.055;
}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	vec3 c = texture(iChannel0,uv).rgb;
	fragColor = vec3(
		compand(c.r),
		compand(c.g),
		compand(c.b));
}