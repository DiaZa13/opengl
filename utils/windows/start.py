from utils.UI.text import Text
import os
import sys
from pygame import font, Color, Surface, SRCALPHA, mixer


class StartWindow(object):
    def __init__(self, screen, image, transform, width, height):
        self.screen = screen
        self.image = image
        self.transform = transform
        self.width = width
        self.height = height
        # self.song = song
        self.x = None
        self.start = None
        self.exit = None

        self.background()
        self.tittle()
        self.option_menu()
        self.options()
        # self.background_music()

    # def background_music(self):
    #     mixer.music.load(self.song)
    #     mixer.music.set_volume(0.05)
    #     mixer.music.play(-1)

    def background(self):
        bck = self.image.load(os.path.join('utils/textures', 'space.png'))
        bck = self.transform.scale(bck, (self.width, self.height))
        self.screen.blit(bck, [0, 0])

    def tittle(self):
        fnt = font.Font('utils/fonts/Pixel.ttf', 100)
        maze_pos = (20, 1 / 2 * self.height)
        maze = Text(self.screen, fnt, 'MAZE', maze_pos, Color('white'))
        camping_pos = (20, self.height - 25 - maze.rect[3])
        Text(self.screen, fnt, 'CAMPING', camping_pos, Color('white'))

    def option_menu(self):
        # Menu de opciones
        self.x = self.width - int(1 / 3 * self.width) - 100
        self.menu_bck = Surface((int(2 / 5 * self.width), int(3 / 4 * self.height)), SRCALPHA)
        self.menu_bck.fill((229, 236, 231, 102))

    def logo(self):
        # Logo
        logo = self.image.load(os.path.join('utils/textures', 'logo.png'))
        logo = self.transform.scale(logo, (180, 150))
        rectangle = logo.get_rect().move(self.menu_bck.get_width() / 2 - 90, 10)
        self.menu_bck.blit(logo, rectangle)
        self.screen.blit(self.menu_bck, (self.x, 0))

    def options(self):
        # Opciones
        fnt = font.Font('utils/fonts/Pixel.ttf', 70)
        start_pos = (self.x + 60, int(1 / 2 * self.height) - 50)
        self.start = Text(self.screen, fnt, 'PLAY', start_pos, Color('black'), Color(255, 193, 0, 255))
        self.start._hover = True
        exit_pos = (self.x + 60, int(1 / 2 * self.height) + 40)
        self.exit = Text(self.screen, fnt, 'EXIT', exit_pos, Color('black'), Color('chartreuse'))

    def move_options(self, event, pygame):
        playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.start._hover = True
                self.exit._hover = False
            elif event.key == pygame.K_DOWN:
                self.start._hover = False
                self.exit._hover = True
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self.start._hover:
                    playing = True
                elif self.exit._hover:
                    sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            if self.start.rect.collidepoint(event.pos):
                self.start._hover = True
                self.exit._hover = False
            if self.exit.rect.collidepoint(event.pos):
                self.start._hover = False
                self.exit._hover = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start.rect.collidepoint(event.pos):
                playing = True
            if self.exit.rect.collidepoint(event.pos):
                sys.exit()

        self.start.draw_text()
        self.exit.draw_text()

        return playing
