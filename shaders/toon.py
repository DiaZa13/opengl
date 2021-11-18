vertex_shader = '''
#version 450
layout (location = 0) in vec3 _position;
layout (location = 1) in vec2 _textures;
layout (location = 2) in vec3 _normal;

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

uniform float _time;
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
layout (location = 0) out vec4 color;

in float out_intensity;
in vec2 texture_coords;

uniform sampler2D _texture;

void main(){
    float intensity = 0;
     if (out_intensity > 0.7){
        intensity = 1;
    }else if (out_intensity > 0.4){
        intensity = 0.5;
    }else{
        intensity = 0.1;
    }
    color = texture(_texture, texture_coords) * intensity;
}
'''