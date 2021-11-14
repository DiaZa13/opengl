import numpy as np
import pygame
from pygame.locals import *
import sys
from gl import Renderer
from model import Model
from camera import Camera
from shaders.multicolor import *

width = 960
height = 540
delta_time = 0.0
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption('OPENGL')
clock = pygame.time.Clock()

camera = Camera()
render = Renderer(screen, width, height, camera)
render.setShaders(vertex_shader, fragment_shader)

'''
* Posiciones
* Color
'''
verts = np.array([-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                  0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                  0.0, 0.5, 0.0, 0.0, 0.0, 1.0], dtype=np.float32)

cube_data = np.array([-0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
                      -0.5, 0.5, 0.5, 0.0, 1.0, 0.0,
                      0.5, 0.5, 0.5, 0.0, 0.0, 1.0,
                      0.5, -0.5, 0.5, 1.0, 1.0, 0.0,
                      -0.5, -0.5, -0.5, 1.0, 0.0, 1.0,
                      -0.5, 0.5, -0.5, 0.0, 1.0, 1.0,
                      0.5, 0.5, -0.5, 1.0, 1.0, 1.0,
                      0.5, -0.5, -0.5, 0.0, 0.0, 0.0], dtype=np.float32)

index_data = np.array([0, 1, 3, 1, 2, 3,
                       1, 5, 2, 5, 6, 2,
                       4, 5, 0, 5, 1, 0,
                       3, 2, 7, 6, 2, 7,
                       4, 0, 7, 0, 3, 7,
                       5, 4, 6, 4, 7, 6], dtype=np.uint32)

cube = Model(cube_data, index_data)

cube.position.z = -5.0

render.scene.append(cube)
while 1:
    render.time += delta_time
    keys = pygame.key.get_pressed()

    if keys[K_d]:
        render.camPosition.x += 1 * delta_time
    if keys[K_a]:
        render.camPosition.x -= 1 * delta_time
    if keys[K_w]:
        render.camPosition.z += 1 * delta_time
    if keys[K_s]:
        render.camPosition.z -= 1 * delta_time

    if keys[K_q]:
        render.camRotation.y -= 5 * delta_time
    if keys[K_e]:
        render.camRotation.y += 5 * delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == K_1:
                render.filledMode()
            if event.key == K_2:
                render.wireframeMode()

    render.render()
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
