import pygame
from pygame.locals import *
from pygame import mixer
import sys
from utils.libs.texture import Texture
from utils.libs.gl import Renderer
from utils.libs.obj import Obj
from utils.libs.model import Model
from utils.libs.camera import Camera
from utils.shaders import heatmap_pattern, static, toon, internal_shadow, multicolor, floor

shaders = [(toon.vertex_shader, toon.fragment_shader),
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

# Music
mixer.init()
background_music = mixer.Sound('utils/fonts/background_music.mp3')
flip = mixer.Sound('utils/fonts/flip.mp3')
mixer.Channel(0).set_volume(0.8)
mixer.Channel(0).play(background_music, -1, 0, 1)

# Floor shader
render.floorShader(floor.vertex_shader, floor.fragment_shader)

models = [Model(Obj('utils/models/alien.obj'), Texture('utils/textures/alien.bmp')),
          Model(Obj('utils/models/spaceship.obj'), Texture('utils/textures/spaceship.bmp')),
          Model(Obj('utils/models/hero.obj'), Texture('utils/textures/hero.bmp')),
          Model(Obj('utils/models/among_us.obj'), Texture('utils/textures/among_us.bmp'))]

# Default shader
for x in models:
    x.setShaders(shaders[0][0], shaders[0][1])

model = 0
# Renderizando el primer modelo
render.figure = models[model]

mouse_clicked = False
while 1:
    keys = pygame.key.get_pressed()
    render.time += delta_time
    render.camera.radius = render.figure.position.z
    render.camera.mouse_sensitivity = delta_time

    # Orbit movement
    if keys[K_d]:
        render.camera.angle -= 15 * delta_time
        render.camera.orbitMovement(render.figure.position)
    if keys[K_a]:
        render.camera.angle += 15 * delta_time
        render.camera.orbitMovement(render.figure.position)
    # Camera translation
    # if keys[K_q]:
    #     render.camera.position.y -= 1 * delta_time
    #     render.camera.update(render.figure.position)
    # if keys[K_e]:
    #     render.camera.position.z = -5
    #     render.camera.position.y += 1 * delta_time
    #     render.camera.update(render.figure.position)
    # if keys[K_w]:
    #     render.camera.position.z = -5
    #     render.camera.position.z += 1 * delta_time
    #     render.camera.update(render.figure.position)
    # if keys[K_s]:
    #     render.camera.position.z = -5
    #     render.camera.position.z -= 1 * delta_time
    #     render.camera.update(render.figure.position)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            # Changing the actual model
            elif event.key == K_LEFT:
                model = (model - 1) % len(models)
                mixer.Channel(1).play(flip)
            elif event.key == K_RIGHT:
                model = (model - 1) % len(models)
                mixer.Channel(1).play(flip)
            # Changing the filled mode
            elif event.key == K_1:
                render.filledMode()
            elif event.key == K_2:
                render.wireFrame()
            # Changing the actual shader
            elif event.key == K_3 or event.key == K_KP3:
                models[model].setShaders(shaders[0][0], shaders[0][1])
            elif event.key == K_4 or event.key == K_KP4:
                models[model].setShaders(shaders[1][0], shaders[1][1])
            elif event.key == K_5 or event.key == K_KP5:
                models[model].setShaders(shaders[2][0], shaders[2][1])
            elif event.key == K_6 or event.key == K_KP6:
                models[model].setShaders(shaders[3][0], shaders[3][1])

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True
            # Zoom in/out with mouse
            elif event.button == 4:
                if render.figure.scale.x < -render.figure.position.z:
                    render.figure.scale.x += 5 * delta_time
                    render.figure.scale.y += 5 * delta_time
                    render.figure.scale.z += 5 * delta_time
            elif event.button == 5:
                if render.figure.scale.x > 1:
                    render.figure.scale.x -= 5 * delta_time
                    render.figure.scale.y -= 5 * delta_time
                    render.figure.scale.z -= 5 * delta_time
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_clicked = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_clicked:
                mouse_x, mouse_y = event.rel
                render.camera.mouseMovement(mouse_x, mouse_y, render.figure.position)
                # render.camera.mouseMovement(mouse_x, mouse_y, render.figure.position)

    render.figure = models[model]
    render.render(True)
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
