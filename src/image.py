import pygame
import os


class Image:
    loaded_images = {}

    @staticmethod
    def get_image_from_cache_or_load(path):
        fullpath = os.path.join(os.path.dirname(__file__), 'images', path)

        if fullpath not in Image.loaded_images:
            image_to_cache = pygame.image.load(fullpath)
            Image.loaded_images[fullpath] = image_to_cache

        return Image.loaded_images[fullpath]

    def __init__(self, image_path):
        self.image = Image.get_image_from_cache_or_load(image_path)
        self.rectangle = self.image.get_rect()
        self.current_position = (0, 0)

    def display(self, screen, position=None):
        self.move(position)
        screen.blit(self.image, self.rectangle)

    def move(self, position):
        if position and position != self.current_position:
            self.current_position = position
            self.rectangle = self.rectangle.move(position)

    def get_size(self):
        return self.image.get_width(), self.image.get_height()