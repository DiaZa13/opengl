# Los shaders de OPenGL se escriben en GLSL
'''
* Version
* Atributos
* gl_Position → existe por default
'''
vertex_shader = '''
#version 450
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 _color;

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

out vec3 out_color;

void main(){ 
    vec4 pos = vec4(position, 1.0);
    gl_Position = projection_matrix * view_matrix * model_matrix * pos;
    out_color = _color;
}
'''

fragment_shader = '''
#version 450
layout (location = 0) out vec4 color;

in vec3 out_color;

void main(){
    color = vec4(out_color, 1);
}
'''