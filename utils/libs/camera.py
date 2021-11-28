import glm
from math import sin, cos, acos, asin
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera(object):
    def __init__(self, position=glm.vec3(0, 0, 0), rotation=glm.vec3(0, 0, 0)):
        # View matrix
        self.position = position
        self.rotation = rotation  # pitch, yaw, roll
        self.angle = 0
        self.radius = -5

        self.view_matrix = glm.inverse(self.cameraMatrix())

        self.mouse_sensitivity = 0

    def cameraMatrix(self):
        identity = glm.mat4(1)
        translate = glm.translate(identity, self.position)

        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        rotation = pitch * yaw * roll

        return translate * rotation

    def orbitMovement(self, center=glm.vec3(0, 0, 0)):
        self.position.x = sin(glm.radians(self.angle)) * self.radius
        self.position.z = cos(glm.radians(self.angle)) * self.radius

        self.view_matrix = glm.lookAt(center - self.position, center, glm.vec3(0, 1, 0))

    # def mouseMovement(self, x_axis, y_axis, center=glm.vec3(0.0, 0.0, 0.0)):
    #     # self.angle += y_axis + x_axis
    #
    #     # if x_axis != 0 and y_axis != 0:
    #     #     if yaw > 45:
    #     #         yaw = 45
    #     #     elif yaw < -45:
    #     #         yaw = -45
    #     #     self.position.y = sin(glm.radians(yaw)) * self.radius
    #         # self.position.y = sin(glm.radians(self.angle)) * self.radius
    #     if x_axis == 0:
    #         self.position.y += 1 * self.mouse_sensitivity * y_axis
    #         self.view_matrix = glm.lookAt(self.position, center, glm.vec3(0.0, 1.0, 0.0))
    #     elif y_axis == 0:
    #         self.angle += x_axis
    #         self.position.x = sin(glm.radians(self.angle)) * self.radius
    #         self.position.z = cos(glm.radians(self.angle)) * self.radius
    #         self.view_matrix = glm.lookAt(center - self.position, center, glm.vec3(0, 1, 0))

    def mouseMovement(self, mouse_x, mouse_y, center=glm.vec3(0.0, 0.0, 0.0)):
        self.position.x -= 1 * self.mouse_sensitivity * mouse_x
        self.position.y += 1 * self.mouse_sensitivity * mouse_y
        self.view_matrix = glm.lookAt(self.position, center, glm.vec3(0, 1, 0))

    def update(self, center=glm.vec3(0, 0, 0)):
        self.view_matrix = glm.lookAt(self.position, center, glm.vec3(0.0, 1.0, 0.0))
