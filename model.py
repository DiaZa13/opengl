import glm
from numpy import array, float32
from OpenGL.GL import *


class Model(object):
    def __init__(self, model, texture):
        self.model = model
        self.vertex = None
        self.createVertex()

        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)

        # Textura
        self.texture = texture
        self.gl_texture = glGenTextures(1)
        # Si el modelo tiene más texturas o se desea agregar un mapa normal hay que generar otro buffer de texturas

    def createVertex(self):

        buffer = []
        # TODO mejorar para que se puedan agregar modelos con más caras
        for face in self.model.faces:
            for i in range(3):
                # positions
                position = self.model.vertices[face[i][0] - 1]
                buffer.append(position[0])
                buffer.append(position[1])
                buffer.append(position[2])

                # texture coordinates
                texture = self.model.textures[face[i][1] - 1]
                buffer.append(texture[0])
                buffer.append(texture[1])

                # normals
                normal = self.model.normals[face[i][2] - 1]
                buffer.append(normal[0])
                buffer.append(normal[1])
                buffer.append(normal[2])

        self.vertex = array(buffer, dtype=float32)

        # Vertex buffer → posición en memoria donde guardaré los vértices
        self.VBO = glGenBuffers(1)
        # Vertex array object → donde se guardan los buffers
        self.VAO = glGenVertexArrays(1)
        # # Buffer que guardara los indices del objeto → Element array object
        # self.EAO = glGenBuffers(1)

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
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EAO)
        glBindTexture(GL_TEXTURE_2D, self.gl_texture)

        # Cuál es la información que yo quiero ingresar al buffer
        '''
        * ID de lo que quiero guardar
        * Buffer size
        * Buffer data
        * Usage 
        '''
        glBufferData(GL_ARRAY_BUFFER, self.vertex.nbytes, self.vertex, GL_STATIC_DRAW)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.index.nbytes, self.index, GL_STATIC_DRAW)

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
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(0))
        # Textura
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(4 * 3))
        # Normal
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 4 * 8, ctypes.c_void_p(4 * 5))
        # Textura
        '''
        * Tipo de textura
        * Nivel
        * Formato
        * Ancho de textura
        * Alto
        * Borde
        * Formato
        * Tipo
        * Data de textura
        '''
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.texture.width, self.texture.height, 0, GL_RGB, GL_UNSIGNED_BYTE,
                     self.texture.data)
        # Mip mapping → usar distintas resoluciones dependiendo de la distancia
        glGenerateMipmap(GL_TEXTURE_2D)

        # Activar un atributo específico
        glEnableVertexAttribArray(0)  # Activando el atributo de posición
        glEnableVertexAttribArray(1)  # Activando el atributo de normales
        glEnableVertexAttribArray(2)  # Activando el atributo de coordenadas de textura

        '''
        * Modo en el que dibuja
        * Indice en el que empieza a dibujar
        * Cantidad de índices a los que se hace referencia
        '''
        glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces) * 3)
        # Función para que dibuje con base a índices
        # glDrawElements(GL_TRIANGLES, len(self.index), GL_UNSIGNED_INT, None)
