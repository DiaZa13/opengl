import numpy as np
from OpenGL.GL import *

import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Triangle(object):
    def __init__(self, verts):
        self.vertex = verts
        # Vertex buffer → posición en memoria donde guardaré los vértices
        self.VBO = glGenBuffers(1)
        # Vertex array object → donde se guardan los buffers
        self.VAO = glGenVertexArrays(1)

    def render(self):
        # "Guardando" en OpenGl el vertex array
        glBindVertexArray(self.VAO)
        # "Atando" a OpenGL el vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # Cuál es la información que yo quiero ingresar al buffer
        '''
        * ID de lo que quiero guardar
        * Buffer size
        * Buffer data
        * Usage 
        '''
        glBufferData(GL_ARRAY_BUFFER, self.vertex.nbytes, self.vertex, GL_STATIC_DRAW)

        # Atributos → Cómo quiero que lea la información (los vertex que paso)
        '''
        * Attribute number
        * Size 
        * Type
        * Is normalize?
        * Stride → lo recibe en bytes (Desplazamiento, cada cuánto se lee el siguiente atributo)
        * Offset → posición en la que inicia la información (simulado como un pointer en la posicion 0)
        '''
        # Posición
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(0))
        # Color
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(4 * 3))

        # Activar un atributo específico
        glEnableVertexAttribArray(0)  # Activando el atributo de posición
        glEnableVertexAttribArray(1)  # Activando el atributo de color

        '''
        * Modo en el que dibuja
        * Indice en el que empieza a dibujar
        * Cantidad de índices a los que se hace referencia
        '''
        glDrawArrays(GL_TRIANGLES, 0, 3)
