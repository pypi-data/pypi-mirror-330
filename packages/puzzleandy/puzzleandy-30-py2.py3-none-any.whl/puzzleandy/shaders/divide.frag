#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform vec3 iResolution;

out vec3 fragColor;

float divide(float b, float t)
{

}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	vec3 b = texture(iChannel0,uv).rgb;
	vec3 t = texture(iChannel1,uv).rgb;
	if 
	fragColor = vec3(
		divide(b.r,t.r),
		divide(b.g,t.g),
		divide(b.b,t.b);
}