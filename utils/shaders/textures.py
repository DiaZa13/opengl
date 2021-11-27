
vertex_shader = '''
#version 450
layout (location = 0) in vec3 _position;
layout (location = 1) in vec2 _textures;
layout (location = 2) in vec3 _normal;

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

uniform float tiempo;
uniform float _zoom;
uniform vec3 _light;

out vec3 out_color;
out vec2 texture_coords;

void main(){ 

    vec4 light = vec4(_light, 1.0);
    vec4 normal = vec4(_normal, 0.0);
    vec4 position = vec4(_position, 1.0) + normal * _zoom;
    position = model_matrix * position;
    
    vec4 lightning = normalize(light - position);
    float intensity = dot(model_matrix * normal, lightning);
    
    gl_Position = projection_matrix * view_matrix * position;
    
    out_color = vec3(1.0, 1.0 -_zoom, 1.0 - _zoom) * intensity;
    texture_coords = _textures;
}
'''

fragment_shader = '''
#version 450
layout (location = 0) out vec4 color;

in vec3 out_color;
in vec2 texture_coords;

uniform sampler2D _texture;

void main(){
    color = vec4(out_color, 1) * texture(_texture, texture_coords);
}
'''