#version 410 core

in vec2 uv;

uniform vec4 color;
uniform sampler2D tex;

out vec4 frag_color;

void main()
{
    vec4 sampled = vec4(1.0, 1.0, 1.0, texture(tex, uv).r);
    frag_color = color * sampled;
}