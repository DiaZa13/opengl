import glm
import numpy
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

class Renderer(object):
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        # Objetos que se renderizarán en mi escena
        self.scene = []
        # Shader
        self.active_shader = None
        # Activando del z-buffer
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)


    def set_shaders(self, vertex, fragment):
        self.active_shader = compileProgram(compileShader(vertex, GL_VERTEX_SHADER),
                                            compileShader(fragment, GL_FRAGMENT_SHADER))



    # Función que se llamará una vez cada cuadro
    def render(self):
        # Color para hacer el clear
        glClearColor(0.2, 0.2, 0.2, 1)
        # Clear al fondo y al buffer de profundidad
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.active_shader)

        for figure in self.scene:
            figure.render()


