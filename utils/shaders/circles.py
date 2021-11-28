vertex_shader = '''
#version 450
layout (location = 0) in vec3 _position;
layout (location = 1) in vec2 _textures;
layout (location = 2) in vec3 _normal;

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

uniform float _zoom;
uniform vec3 _light;

out float out_intensity;
out vec2 texture_coords;

void main(){ 

    vec4 light = vec4(_light, 1.0);
    vec4 normal = vec4(_normal, 0.0);
    vec4 position = vec4(_position, 1.0) + normal * _zoom;
    position = model_matrix * position;

    vec4 lightning = normalize(light - position);
    out_intensity = dot(model_matrix * normal, lightning);

    gl_Position = projection_matrix * view_matrix * position;
    texture_coords = _textures;
}
'''

fragment_shader = '''
#version 450
in vec2 texture_coords;
in float out_intensity;

uniform sampler2D _texture;
uniform vec2 _resolution;
uniform float _time;

void main(){
    vec3 color = vec3(0.0);
    vec2 coords = gl_FragCoord.xy / _resolution;
    vec2 translate = vec2(-0.5);
    coords += translate;
    
    color.r += abs(0.1 + length(coords) - 0.6 * abs(sin(_time * 0.9 / 12.0)));
    color.g += abs(0.1 + length(coords) - 0.6 * abs(sin(_time * 0.6 / 4.0)));
    color.b += abs(0.1 + length(coords) - 0.6 * abs(sin(_time * 0.3 / 9.0)));
    
    gl_FragColor = vec4(0.2 / color, 1.0) * texture(_texture, texture_coords) * out_intensity;
}
'''