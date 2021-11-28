import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from numpy import array, float32


class Renderer(object):
    def __init__(self, screen, width, height, camera):
        self.screen = screen
        self.width = width
        self.height = height
        # Activando del z-buffer
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)

        # Objetos que se renderizarán en mi escena
        self.figure = None

        self.time = 0
        self.zoom = 0
        self.camera = camera
        self.point_light = glm.vec3(-1, 0, 0)

        '''
        * fov → radians
        * Aspect ratio 
        * Near plane distance → distancia a la cual se empieza a dibujar objetos
        * Far plane distance → distancia máxima a la cual dibuja (más lejos de esto, no dibuja)
        '''
        # Projection Matrix
        self.projection_matrix = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)

        # Floor
        self.floor_data = array([10, -2, 3, 1.0, 0.0, 0.0,
                                 -10, -2, 3, 0.0, 1.0, 0.0,
                                 -10, -2, -5, 0.0, 0.0, 1.0,
                                 10, -2, -5, 1.0, 1.0, 0.0], dtype=float32)
        self.floor_shader = None
        # Vertex buffer → posición en memoria donde guardaré los vértices
        self.VBO = glGenBuffers(1)
        # Vertex array object → donde se guardan los buffers
        self.VAO = glGenVertexArrays(1)

    # viewport_matrix (opengl ya lo hace) * projection_matrix * view_matrix * model_matrix * pos

    def wireFrame(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def floorShader(self, vertex, fragment):
        self.floor_shader = compileProgram(compileShader(vertex, GL_VERTEX_SHADER),
                                           compileShader(fragment, GL_FRAGMENT_SHADER))

    def drawFloor(self):
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        glBufferData(GL_ARRAY_BUFFER, self.floor_data.nbytes, self.floor_data, GL_STATIC_DRAW)

        # Posición
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(0))
        # Color
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(4 * 3))

        # Activar un atributo específico
        glEnableVertexAttribArray(0)  # Activando el atributo de posición
        glEnableVertexAttribArray(1)  # Activando el atributo de color

        glDrawArrays(GL_QUADS, 0, 4)

    # Función que se llamará una vez cada cuadro
    def render(self, orbit=False):
        # Color para hacer el clear
        glClearColor(0.2, 0.2, 0.2, 1)
        # Clear al fondo y al buffer de profundidad
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.figure:
            glUseProgram(self.figure.active_shader)

            glUniformMatrix4fv(glGetUniformLocation(self.figure.active_shader, 'model_matrix'), 1, GL_FALSE,
                               glm.value_ptr(self.figure.modelMatrix()))

            if self.figure.active_shader:
                '''
                * Uniform location
                * Cantidad de parámetros a pasar
                * Transpose
                '''

                glUniformMatrix4fv(glGetUniformLocation(self.figure.active_shader, 'view_matrix'), 1, GL_FALSE,
                                   glm.value_ptr(self.camera.view_matrix))
                glUniformMatrix4fv(glGetUniformLocation(self.figure.active_shader, 'projection_matrix'), 1, GL_FALSE,
                                   glm.value_ptr(self.projection_matrix))
                glUniform1f(glGetUniformLocation(self.figure.active_shader, '_time'), self.time)
                glUniform1f(glGetUniformLocation(self.figure.active_shader, '_zoom'), self.zoom)

                glUniform3f(glGetUniformLocation(self.figure.active_shader, '_light'), self.point_light.x,
                            self.point_light.y,
                            self.point_light.z)

                glUniform1f(glGetUniformLocation(self.figure.active_shader, '_zoom'), self.zoom)

                glUniform2f(glGetUniformLocation(self.figure.active_shader, '_resolution'), self.width, self.height)

            self.figure.render()

            # TODO hacer que el floor tenga su propio shader
            self.drawFloor()
