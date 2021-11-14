import glm


class Camera(object):
    def __init__(self, position=glm.vec3(0, 0, 0), rotation=glm.vec3(0, 0, 0)):
        # View matrix
        self.position = position
        self.rotation = rotation  # pitch, yaw, roll

    def cameraMatrix(self):
        identity = glm.mat4(1)
        translate = glm.translate(identity, self.position)

        pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        rotation = pitch * yaw * roll

        return translate * rotation
