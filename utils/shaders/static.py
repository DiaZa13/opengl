vertex_shader = '''
#version 450
layout (location = 0) in vec3 _position;
layout (location = 1) in vec2 _textures;
layout (location = 2) in vec3 _normal;

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;
uniform float _time;

uniform vec3 _light;
uniform float _zoom;

out vec3 out_color;
out vec2 texture_coords;
out float out_intensity;

void main(){ 

    vec4 light = vec4(_light, 1.0);
    vec4 normal = vec4(_normal, 0.0);
    vec4 position = vec4(_position, 1.0) + normal * sin(_time / 3.0);
    position = model_matrix * position;

    // Intensidad
    vec4 lightning = normalize(light - position);
    out_intensity = dot(model_matrix * normal, lightning);

    out_color = vec3(1.0, 1.0, 1.0) * out_intensity;
    // Coordenadas de textura
    texture_coords = _textures;
    // Posición
    gl_Position = projection_matrix * view_matrix * position;
}
'''

fragment_shader = '''
#version 450
layout (location = 0) out vec4 color;

in vec3 out_color;
in vec2 texture_coords;
in float out_intensity;

uniform sampler2D _texture;
uniform float _time;

// Extraído de: https://www.youtube.com/watch?v=8GaZsg8vJUw&list=PL4neAtv21WOmIrTrkNO3xCyrxg4LKkrF7&index=34
float random2d(vec2 coord){
  return fract(sin(dot(coord.xy, vec2(12.9898, 78.2333))) + 152893.9);
}

void main(){
    float theta = _time*20.0;
    vec3 color;
    vec3 noise_color;
    vec2 coords = gl_FragCoord.xy;
    
    float residuo = mod(gl_FragCoord.x, 80.0);
    
    if (residuo >= 0.0 && residuo < 10.0) {
    color = vec3(1,1,1);
    }else if (residuo >= 10.0 && residuo < 20.0) {
    color = vec3(236,236,0);
    }else if (residuo >= 20.0 && residuo < 30.0) {
    color = vec3(0,237,238);
    }else if (residuo >= 30.0 && residuo < 40.0) {
    color = vec3(0,219,0);
    }else if (residuo >= 40.0 && residuo < 50.0) {
    color = vec3(234,0,226);
    }else if (residuo >= 50.0 && residuo < 60.0) {
    color = vec3(236,0,0);
    }else if (residuo >= 60.0 && residuo < 70.0) {
    color = vec3(0,0,232);
    } else {
    color = vec3(0,0,0);
    }
    
    float noise = random2d(vec2(sin(coords)) * theta) - 0.3;
    
    noise_color = vec3(noise);
    
    color *= noise_color;
    
    color.r += sin(_time);
    color.g += sin(_time);
    
    gl_FragColor = vec4(color, 0.1) * texture(_texture, texture_coords) * out_intensity;
}
'''