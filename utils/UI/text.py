"""
    Extraído de: https://gist.github.com/ohsqueezy/2802185
    Adaptado por: Zaray Corado
"""

class Text(object):
    def __init__(self, screen, font, msg, position, color, hover_color=None, center=False):
        self.screen = screen
        self.font = font
        self.msg = msg
        self.color = color
        self.hover_color = hover_color
        self.position = position
        self._hover = False
        self.text = None
        self.rect = None
        self.height = None
        self.center = center
        self.render_text()
        self.draw_text()

    def hover(self):
        if self._hover:
            return self.hover_color
        return self.color

    def render_text(self):
        color = self.hover()
        self.text = self.font.render(self.msg, True, color)
        self.rect = self.text.get_rect()
        if self.center:
            self.rect.center = self.position
        else:
            self.rect.topleft = self.position

    def draw_text(self):
        self.render_text()
        self.screen.blit(self.text, self.rect)
