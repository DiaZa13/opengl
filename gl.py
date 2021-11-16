import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram


class Renderer(object):
    def __init__(self, screen, width, height, camera):
        self.screen = screen
        self.width = width
        self.height = height
        # Activando del z-buffer
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)

        # Objetos que se renderizarán en mi escena
        self.scene = []
        # Shader
        self.active_shader = None
        self.time = 0
        self.camera = camera

        '''
        * fov → radians
        * Aspect ratio 
        * Near plane distance → distancia a la cual se empieza a dibujar objetos
        * Far plane distance → distancia máxima a la cual dibuja (más lejos de esto, no dibuja)
        '''
        # Projection Matrix
        self.projection_matrix = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)

    # viewport_matrix (opengl ya lo hace) * projection_matrix * view_matrix * model_matrix * pos
    def viewMatrix(self):
        return glm.inverse(self.camera.cameraMatrix())

    def orbitMovement(self):
        return self.camera.orbitMovement(self.scene[0].position)

    def wireFrame(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def setShaders(self, vertex, fragment):
        self.active_shader = compileProgram(compileShader(vertex, GL_VERTEX_SHADER),
                                            compileShader(fragment, GL_FRAGMENT_SHADER))

    # Función que se llamará una vez cada cuadro
    def render(self, orbit=False):
        # Color para hacer el clear
        glClearColor(0.2, 0.2, 0.2, 1)
        # Clear al fondo y al buffer de profundidad
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.active_shader)

        if self.active_shader:
            '''
            * Uniform location
            * Cantidad de parámetros a pasar
            * Transpose
            '''
            if orbit:
                glUniformMatrix4fv(glGetUniformLocation(self.active_shader, 'view_matrix'), 1, GL_FALSE,
                                   glm.value_ptr(self.orbitMovement()))
            else:
                glUniformMatrix4fv(glGetUniformLocation(self.active_shader, 'view_matrix'), 1, GL_FALSE,
                                   glm.value_ptr(self.viewMatrix()))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, 'projection_matrix'), 1, GL_FALSE,
                               glm.value_ptr(self.projection_matrix))
            glUniform1f(glGetUniformLocation(self.active_shader, 'tiempo'), self.time)

        for figure in self.scene:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, 'model_matrix'), 1, GL_FALSE,
                               glm.value_ptr(figure.modelMatrix()))
            figure.render()
