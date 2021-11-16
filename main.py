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
cube_data = np.array([ 0,    1.5,   0.5, 1.0, 0.0, 0.0,
                      -0.5,  0.5,   0.5, 0.0, 1.0, 0.0,
                       0.5,  0.5,   0.5, 0.0, 0.0, 1.0,
                      -1.5,  0.5,   0.5, 1.0, 1.0, 0.0,
                       1.5,  0.5,   0.5, 1.0, 0.0, 1.0,
                      -0.7, -0.2, 0.5, 1.0, 1.0, 0.0,
                       0.7,  0.2, 0.5, 1.0, 0.0, 1.0,
                      -1,   -1.3, 0.5, 0.0, 1.0, 1.0,
                       1,   -1.3, 0.5, 1.0, 0.0, 0.0,
                       0,   -0.8, 0.5, 1.0, 1.0, 0.0,

                       0,    1.5,   0, 0.0, 0.0, 0.0,
                      -0.5,  0.5,   0, 0.0, 1.0, 0.0,
                       0.5,  0.5,   0, 0.0, 0.0, 1.0,
                      -1.5,  0.5,   0, 1.0, 1.0, 0.0,
                       1.5,  0.5,   0, 1.0, 0.0, 1.0,
                      -0.7, -0.2, 0, 1.0, 1.0, 0.0,
                       0.7, -0.2, 0, 1.0, 0.0, 1.0,
                      -1,   -1.3, 0, 0.0, 1.0, 1.0,
                       1,   -1.3, 0, 1.0, 0.0, 0.0,
                       0,   -0.8, 0, 1.0, 1.0, 0.0,
                       ], dtype=np.float32)

index_data = np.array([0, 1, 2,
                       5, 1, 3,
                       2, 4, 6,
                       5, 7, 9,
                       9, 8, 6,
                       1, 9, 5,
                       1, 2, 6,
                       1, 6, 9,
                       10, 11, 12,
                       15, 11, 13,
                       12, 14, 16,
                       15, 17, 19,
                       19, 18, 16,
                       11, 19, 15,
                       11, 12, 16,
                       11, 16, 19,
                       0, 1, 11,
                       0, 10, 11,
                       0, 2, 12,
                       0, 10, 12,
                       3, 5, 15,
                       3, 13, 15,
                       4, 2, 12,
                       4, 12, 14,
                       4, 6, 16,
                       4, 14, 16,
                       8, 16, 18,
                       8, 6, 16,
                       8, 18, 19,
                       8, 9, 19,
                       7, 17, 19,
                       7, 9, 17,
                       7, 5, 15,
                       7, 17, 15], dtype=np.uint32)

cube = Model(cube_data, index_data)

cube.position.z = -10

render.scene.append(cube)
while 1:
    render.time += delta_time
    keys = pygame.key.get_pressed()

    # Camera translation
    if keys[K_d]:
        render.camera.position.x += 1 * delta_time
    if keys[K_a]:
        render.camera.position.x -= 1 * delta_time
    if keys[K_q]:
        render.camera.position.y -= 1 * delta_time
    if keys[K_e]:
        render.camera.position.y += 1 * delta_time
    if keys[K_w]:
        render.camera.position.z += 1 * delta_time
    if keys[K_s]:
        render.camera.position.z -= 1 * delta_time

    # render.scene[0].rotation.x += 10 * delta_time
    # render.scene[0].rotation.y += 10 * delta_time
    # render.scene[0].rotation.z += 10 * delta_time
    # render.camera.rotation.y += 5 * delta_time
    # render.camera.position.x -= render.camera.rotation.y * delta_time
    # render.scene[0].rotation.y -= render.camera.rotation.y * delta_time
    # render.scene[0].position.x = render.camera.rotation.y * delta_time
    # render.scene[0].position.x += 10 * delta_time

    # Camera rotation
    if keys[K_UP]:
        if render.scene[0].scale.x < 5:
            render.scene[0].scale.x += 1 * delta_time
            render.scene[0].scale.y += 1 * delta_time
            render.scene[0].scale.z += 1 * delta_time
    if keys[K_DOWN]:
        if render.scene[0].scale.x > 1:
            render.scene[0].scale.x -= 1 * delta_time
            render.scene[0].scale.y -= 1 * delta_time
            render.scene[0].scale.z -= 1 * delta_time
    if keys[K_LEFT]:
        render.camera.rotation.y += 5 * delta_time
        render.camera.position.x -= 5 * delta_time
        render.scene[0].position.x -= render.camera.position.x / 2 * delta_time
        render.scene[0].position.z += 5 * delta_time
        render.camera.position.x += 5 * delta_time
    if keys[K_RIGHT]:
        render.camera.rotation.y += 5 * delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == K_1:
                render.filledMode()
            if event.key == K_2:
                render.wireFrame()

    render.render()
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
