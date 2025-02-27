#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform vec3 iResolution;

out vec3 fragColor;

float color_dodge(float b, float t)
{
	if (b == 0)
		return 0;
	else if (t == 1)
		return 1;
	else
		return min(b/(1-t),1);
}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	vec3 b = texture(iChannel0,uv).rgb;
	vec3 t = texture(iChannel1,uv).rgb;	
	fragColor = vec3(
		color_dodge(b.r,t.r),
		color_dodge(b.g,t.g),
		color_dodge(b.b,t.b));
}