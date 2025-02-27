#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform vec3 iResolution;

out vec3 fragColor;

float Y(vec3 c)
{
	return 0.299*c.r+0.587*c.g+0.114*c.b;
}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	vec3 b = texture(iChannel0,uv).rgb;
	vec3 t = texture(iChannel1,uv).rgb;
	if (Y(b) < Y(t))
		fragColor = t;
	else
		fragColor = b;
}