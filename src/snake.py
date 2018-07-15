from src.image import Image

class Snake:
    def __init__(self, position=(0, 0)):
        self.image = Image('snake.png')
        self.position = position

    def display(self, screen):
        self.image.display(screen, self.position)