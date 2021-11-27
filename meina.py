import math

import pygame
from pygame import image, Color, transform
from pygame.locals import *
import sys
from utils.libs.texture import Texture
from utils.libs.gl import Renderer
from utils.libs.obj import Obj
from utils.libs.model import Model
from utils.libs.camera import Camera
from utils.shaders import heatmap_pattern, static, toon, internal_shadow, multicolor

shaders = [(multicolor.vertex_shader, multicolor.fragment_shader),
           (static.vertex_shader, static.fragment_shader),
           (heatmap_pattern.vertex_shader, heatmap_pattern.fragment_shader),
           (internal_shadow.vertex_shader, internal_shadow.fragment_shader)]

width = 960
height = 540

delta_time = 0.0
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
# Window title
pygame.display.set_caption('Visualizador de modelos')
clock = pygame.time.Clock()

camera = Camera()
render = Renderer(screen, width, height, camera)

model = Obj('utils/models/face.obj')
texture = Texture('utils/textures/face.bmp')
face = Model(model, texture)
face.position.z = -5
# face.scale.x = 2
# face.scale.y = 2
# face.scale.z = 2

render.scene.append(face)
face.setShaders(shaders[0][0], shaders[0][1])
orbit = False
mouse_clicked = False
while 1:
    keys = pygame.key.get_pressed()
    render.time += delta_time
    # render.camera.angle += 15 * delta_time
    render.camera.radius = render.scene[0].position.z
    render.camera.mouse_sensitivity = delta_time

    # Camera translation
    if keys[K_d]:
        render.camera.angle -= 15 * delta_time
        render.camera.orbitMovement(render.scene[0].position)
    if keys[K_a]:
        render.camera.angle += 15 * delta_time
        render.camera.orbitMovement(render.scene[0].position)
    if keys[K_q]:
        render.camera.position.y -= 1 * delta_time
    if keys[K_e]:
        render.camera.position.y += 1 * delta_time
    if keys[K_w]:
        render.camera.position.z += 1 * delta_time
    if keys[K_s]:
        render.camera.position.z -= 1 * delta_time

    # Será que pongo rotación
    # if keys[K_LEFT]:
    #     render.camera.rotation.x -= 10 * delta_time
    # if keys[K_RIGHT]:
    #     render.camera.rotation.x += 10 * delta_time

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
            if event.key == K_3 or event.key == K_KP3:
                face.setShaders(shaders[0][0], shaders[0][1])
            if event.key == K_4 or event.key == K_KP4:
                face.setShaders(shaders[1][0], shaders[1][1])
            if event.key == K_5 or event.key == K_KP5:
                face.setShaders(shaders[2][0], shaders[2][1])
            if event.key == K_6 or event.key == K_KP6:
                face.setShaders(shaders[3][0], shaders[3][1])

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True
            # Zoom in/out with mouse
            elif event.button == 4:
                if render.scene[0].scale.x < -render.scene[0].position.z:
                    render.scene[0].scale.x += 5 * delta_time
                    render.scene[0].scale.y += 5 * delta_time
                    render.scene[0].scale.z += 5 * delta_time
            elif event.button == 5:
                if render.scene[0].scale.x > 1:
                    render.scene[0].scale.x -= 5 * delta_time
                    render.scene[0].scale.y -= 5 * delta_time
                    render.scene[0].scale.z -= 5 * delta_time

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_clicked = False

        elif event.type == pygame.MOUSEMOTION:
            if mouse_clicked:
                mouse_x, mouse_y = event.rel
                render.camera.mouseMovement(mouse_x, mouse_y, render.scene[0].position)

    # render.camera.update(render.scene[0].position)
    render.render(True)
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
