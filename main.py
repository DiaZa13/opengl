import numpy as np
import pygame
import sys
from gl import Renderer
from model import Model
from camera import Camera
from shaders.multicolor import *

width = 960
height = 540
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
verts = np.array([-0.5, -0.5, -10.0, 1.0, 0.0, 0.0,
                   0.5, -0.5, -10.0, 0.0, 1.0, 0.0,
                   0.0,  0.5, -10.0, 0.0, 0.0, 1.0], dtype=np.float32)
triangle = Model(verts)

render.scene.append(triangle)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    render.render()
    clock.tick()
    pygame.display.flip()
