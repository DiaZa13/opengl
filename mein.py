import pygame
from pygame import Color, image, mixer
import sys
from utils.windows.game import GameWindow
from utils.windows.start import StartWindow
from utils.const import *

textures = [L1_TEXTURES, L2_TEXTURES, L3_TEXTURES]
enemies = [L1_ENEMIES, L2_ENEMIES, L3_ENEMIES]

# Pygame setup
width = 600
height = 500
pygame.init()
draw = pygame.draw
transform = pygame.transform
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL)
screen.set_alpha(None)
# Window tittle
pygame.display.set_caption('Raycaster')
# Referencia al reloj de pygame
clock = pygame.time.Clock()

song = 'utils/music/nightmare.mp3'
start_page = StartWindow(screen, image, transform, width, height, song)

''' LEVELS '''
levels = ['./utils/maps/maze.txt', './utils/maps/level2.txt', './utils/maps/level3.txt']
game = GameWindow(screen, draw, transform, clock, image)

# Validar en qué ventana está
playing = False

while 1:
    if not playing:
        if game.re_render:
            start_page = StartWindow(screen, image, transform, width, height, song)
            game.re_render = False
            game.pause = False
    elif playing:
        game.floor_roof(Color('gray'), Color('darkgray'), Color('black '))
        game.render(Color('navy'), Color('darkorchid'), textures[game.level], levels[game.level], enemies[game.level])
        game.clock_update(100, Color('black'), Color('white'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not playing:
            playing = start_page.move_options(event, pygame)
        elif playing:
            playing = game.move_options(event, pygame)

    if game.pause:
        game.pause_menu()
        game.resume.draw_text()
        game.start.draw_text()
        game.exit.draw_text()

    pygame.display.update()
