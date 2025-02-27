#version 330

vec2 fragCoord = gl_FragCoord.xy;
uniform sampler2D iChannel0;
uniform vec3 iResolution;
uniform int num_cols;
uniform float col_locs[10];
uniform vec3 cols[10];
uniform float col_mids[9];
uniform int num_alphas;
uniform float alpha_locs[10];
uniform float alphas[10];
uniform float alpha_mids[9];

out vec4 fragColor;

float unlerp(float fx, float f0, float f1)
{
	return (fx-f0)/(f1-f0);
}

int idx(float x,float y[10],int n)
{
	if (x <= y[0])
		return 0;
	else if (x >= y[n-1])
		return n;
	else
		for (int i = 0; i < n; i++)
			if (x < y[i])
				return i;
}

vec3 lookup(
	float loc, float locs[10],
	vec3 vals[10], float mids[9], int n)
{
	int i = idx(loc,locs,n);
	if (i == 0)
		return vals[0];
	else if (i == n)
		return vals[n-1];
	else
	{
		float t = unlerp(loc,locs[i-1],locs[i]);
		float u = pow(t,log(0.5)/log(mids[i-1]));
		return mix(vals[i-1],vals[i],u);
	}
}

float lookup(
	float loc, float locs[10],
	float vals[10], float mids[9], int n)
{
	int i = idx(loc,locs,n);
	if (i == 0)
		return vals[0];
	else if (i == n)
		return vals[n-1];
	else
	{
		float t = unlerp(loc,locs[i-1],locs[i]);
		float u = pow(t,log(0.5)/log(mids[i-1]));
		return mix(vals[i-1],vals[i],u);
	}
}

void main()
{
	vec2 uv = fragCoord/iResolution.xy;
	float loc = texture(iChannel0, uv).r;
	vec3 col = lookup(loc,col_locs,cols,col_mids,num_cols);
	float alpha = lookup(loc,alpha_locs,alphas,alpha_mids,num_alphas);
	fragColor = vec4(col,alpha);
}