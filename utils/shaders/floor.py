# Los shaders de OPenGL se escriben en GLSL
"""
* Version
* Atributos
* gl_Position → existe por default
"""

vertex_shader = '''
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 _color;
out vec3 out_color;
void main(){
    gl_Position = vec4(position.x, position.y, position.z, 1.0);
    out_color = _color;
}
'''

fragment_shader = '''
#version 460
layout (location = 0) out vec4 color;
in vec3 out_color;
void main(){
    color = vec4(out_color, 1);
}
'''
