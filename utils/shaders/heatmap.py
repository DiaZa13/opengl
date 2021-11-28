vertex_shader = '''
#version 450
layout (location = 0) in vec3 _position;
layout (location = 1) in vec2 _textures;
layout (location = 2) in vec3 _normal;

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

uniform vec3 _light;
uniform float _zoom;

out vec3 out_color;
out vec2 texture_coords;
out vec3 out_normal;
out float out_intensity;

void main(){ 

    vec4 light = vec4(_light, 1.0);
    vec4 normal = vec4(_normal, 0.0);
    vec4 position = vec4(_position, 1.0);
    position = model_matrix * position;

    // Intensidad
    vec4 lightning = normalize(light - position);
    out_intensity = dot(model_matrix * normal, lightning);

    out_color = vec3(1.0, 1.0, 1.0) * out_intensity;
    // Coordenadas de textura
    texture_coords = _textures;
    // Posición
    gl_Position = projection_matrix * view_matrix * position;
    out_normal = _normal;
}
'''

fragment_shader = '''
#version 450

in vec3 out_color;
in vec2 texture_coords;
in vec3 out_normal;

uniform sampler2D _texture;
uniform float _time;

void main(){
    vec3 color;
    
    vec3 direction = vec3(cos(_time),0,sin(_time)); 
    
    float diffuse1 = pow(dot(out_normal,direction),2.0);
    float diffuse2 = pow(dot(out_normal,direction),2.0);
    
    vec3 diffuse_color = diffuse1 * vec3(1,25,0) + diffuse2 * vec3(15,0,6);
    
    if (mod(gl_FragCoord.x, 10.0) >= 1.0 || mod(gl_FragCoord.y, 2.0) >= 2.0) {
    color = vec3(1,0,0);
    } else {
    color = vec3(1,0,1);
    }
    
    gl_FragColor = vec4(color + diffuse_color , 1.0);
}
'''