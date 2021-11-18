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
  vec3 color = vec3(0,0,1);
  
  vec3 dir1 = vec3(sin(_time),5,cos(_time * 20)); 
  vec3 dir2 = vec3(cos(_time),0,sin(_time));
  
  float diffuse1 = pow(dot(out_normal,dir1),2.0);
  float diffuse2 = pow(dot(out_normal,dir2),2.0);
  
  vec3 diffuse_color = diffuse1 * vec3(15,0,0)  + diffuse2 * vec3(12,12,12);
  
  gl_FragColor = vec4(color * diffuse_color, 0.8) ;
}
'''