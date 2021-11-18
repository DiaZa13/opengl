from shaders.heatmap import vertex_shader

vertex_shader = vertex_shader

fragment_shader = '''
#version 450

in vec3 out_color;
in vec2 texture_coords;
in vec3 out_normal;

uniform sampler2D _texture;
uniform float _time;

void main(){
  vec3 color;
  
  vec3 diffuse_color = out_normal * vec3(5,10,0.1);
 
  if (mod(gl_FragCoord.x, 6.0) >= 3.0 && mod(gl_FragCoord.y, 6.0) >= 3.0) {
    color = vec3(1,0,1);
  } else {
    color = vec3(1,0,0);
  }
  
  gl_FragColor = vec4(color + diffuse_color , 1.0) *  texture(_texture, texture_coords);
}
'''