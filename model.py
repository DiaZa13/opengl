import glm
from OpenGL.GL import *

class Model(object):
    def __init__(self, verts, index):
        self.vertex = verts
        self.index = index
        # Vertex buffer → posición en memoria donde guardaré los vértices
        self.VBO = glGenBuffers(1)
        # Vertex array object → donde se guardan los buffers
        self.VAO = glGenVertexArrays(1)
        # Buffer que guardara los indices del objeto → Element array object
        self.EAO = glGenBuffers(1)

        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)

    def modelMatrix(self):
        identity = glm.mat4(1)
        translate = glm.translate(identity, self.position)

        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        rotation = pitch * yaw * roll

        scale = glm.scale(identity, self.scale)

        return translate * rotation * scale

    def render(self):
        # "Guardando" en OpenGl el vertex array
        glBindVertexArray(self.VAO)
        # "Atando" a OpenGL el vertex buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EAO)

        # Cuál es la información que yo quiero ingresar al buffer
        '''
        * ID de lo que quiero guardar
        * Buffer size
        * Buffer data
        * Usage 
        '''
        glBufferData(GL_ARRAY_BUFFER, self.vertex.nbytes, self.vertex, GL_STATIC_DRAW)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.index.nbytes, self.index, GL_STATIC_DRAW)

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
        # glDrawArrays(GL_TRIANGLES, 0, 3)
        # Función para que dibuje con base a índices
        glDrawElements(GL_TRIANGLES, len(self.index), GL_UNSIGNED_INT, None)
