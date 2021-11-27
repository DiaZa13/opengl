import pygame
from pygame import image, Color, transform
from pygame.locals import *
import sys
from utils.windows.start import StartWindow

width = 960
height = 540
delta_time = 0.0
pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
# Window title
pygame.display.set_caption('Visualizador de modelos')
clock = pygame.time.Clock()

start_page = StartWindow(screen, image, transform, width, height)
pygame.display.flip()

visualize = False

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not visualize:
            visualize = start_page.move_options(event, pygame)
        elif visualize:
            visualize = False

    pygame.display.flip()
