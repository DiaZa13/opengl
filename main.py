import pygame
from pygame.locals import *
import sys
from gl import Renderer
from model import Model
from camera import Camera
from shaders.textures import *
from obj import Obj
from texture import Texture

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

model = Obj('models/face.obj')
texture = Texture('textures/face.bmp')
among = Model(model, texture)
among.position.z = -5
# among.scale.x = 100
# among.scale.y = 100
# among.scale.z = 100

render.scene.append(among)

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

    render.camera.position.x += 1 * delta_time
    # render.camera.position.y += 1 * delta_time
    # render.camera.position.z += 1 * delta_time
    render.scene[0].position.x -= 1 * delta_time
    # render.scene[0].rotation.y += 10 * delta_time
    # render.scene[0].rotation.z += 10 * delta_time

    # Camera rotation
    if keys[K_UP]:
        # render.camera.rotation.y += 10 * delta_time
        if render.zoom < 0.5:
            render.zoom += 1 * delta_time
    if keys[K_DOWN]:
        # render.camera.rotation.y -= 10 * delta_time
        if render.zoom > 0:
            render.zoom -= 1 * delta_time
    if keys[K_LEFT]:
        render.camera.rotation.x -= 10 * delta_time
    if keys[K_RIGHT]:
        render.camera.rotation.x += 10 * delta_time

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
