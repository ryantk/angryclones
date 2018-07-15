import pygame
from src.image import Image
from src.label import Label
from src.coords import Coords


class TitleScreen:
    def __init__(self, game):
        self.game = game
        self.background_image = Image('background-dim.jpg')
        self.title_message = Label('Angry Clones', font_size=55).with_shadow()
        self.press_space_message = Label('Press SPACE to start!', font_size=30).with_shadow()

    def handle_event(self, event):
        self.game.handle_quit(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game.go_to_next_level()

    def calculate(self):
        pass

    def display(self, screen):
        self.background_image.display(screen)
        self.title_message.display(screen, self.title_message_coords())
        self.press_space_message.display(screen, self.press_space_message_coords())

    def title_message_coords(self):
        return Coords.centered_label(self.game.get_screen_size(), self.title_message)

    def press_space_message_coords(self):
        x, y = Coords.centered_label(self.game.get_screen_size(), self.press_space_message)
        return x, y + 30
