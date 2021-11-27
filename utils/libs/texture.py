from pygame import image


class Texture(object):
    def __init__(self, file):
        self.surface = image.load(file)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.data = image.tostring(self.surface, 'RGB', True)
