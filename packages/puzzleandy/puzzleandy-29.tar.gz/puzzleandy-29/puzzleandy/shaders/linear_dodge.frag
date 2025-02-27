#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform sampler2D iChannel1;
uniform vec3 iResolution;

out vec3 fragColor;

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	vec3 b = texture(iChannel0,uv).rgb;
	vec3 t = texture(iChannel1,uv).rgb;
	fragColor = min(b+t,1);
}