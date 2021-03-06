from utils.shaders.heatmap import vertex_shader

vertex_shader = vertex_shader

fragment_shader = '''
#version 450

in vec3 out_color;
in vec2 texture_coords;
in vec3 out_normal;
in float out_intensity;

uniform sampler2D _texture;
uniform float _time;
uniform float _zoom;

void main(){
  vec3 color;
  
  vec3 diffuse_color = out_normal * vec3(15,15 * _zoom,0.1 * _zoom);
 
  if (mod(gl_FragCoord.x, 10.0) >= 5.0 && mod(gl_FragCoord.y, 10.0) >= 5.0) {
    color = vec3(1,0,0);
  } else {
    color = vec3(1,0,cos(_time * 5));
  }
  
  gl_FragColor = vec4(color + diffuse_color , 1.0) *  texture(_texture, texture_coords) * out_intensity;
}
'''