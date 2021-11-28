from utils.shaders.static import vertex_shader

vertex_shader = vertex_shader

fragment_shader = '''
#version 450
layout (location = 0) out vec4 color;

in vec3 out_color;
in vec2 texture_coords;
in float out_intensity;

uniform sampler2D _texture;
uniform float _time;
uniform float _zoom;

// Extraído de: https://www.youtube.com/watch?v=8GaZsg8vJUw&list=PL4neAtv21WOmIrTrkNO3xCyrxg4LKkrF7&index=34
float random2d(vec2 coord){
  return fract(sin(dot(coord.xy, vec2(12.9898, 78.2333))) * 43758.5453);
}

void main(){
    float theta = _time*20.0;
    vec3 color = vec3(0, 0, 1);
    vec3 noise_color;
    vec2 coords = gl_FragCoord.xy;

    float noise = random2d(vec2(sin(coords) + 50.0) * theta) - 0.5;

    noise_color = vec3(noise);

    color *= noise_color;
    
    color.r += _zoom;
    color.g -= _zoom;

    gl_FragColor = vec4(color, 0.1) * texture(_texture, texture_coords) * out_intensity;
}
'''