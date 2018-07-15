from src.image import Image
from src.label import Label
from src.coords import Coords
from src.snake import Snake
from src.level_profile import LevelProfile


class Level:
    def __init__(self, game, profile=LevelProfile.empty_level()):
        self.game = game
        self.background_image = Image('background.jpg')
        self.trebuchet = Image('trebuchet.png')

        self.snakes = profile.get_snakes()
        self.crates = profile.get_crates()
        self.snakes_remaining = len(self.snakes)
        self.snakes_remaining_message = Label(font_size=20).with_shadow()

    def handle_event(self, event):
        self.game.handle_quit(event)

    def calculate(self):
        self.snakes_remaining_message.set_text(f"Snakes Remaining: {self.snakes_remaining}")

    def display(self, screen):
        self.background_image.display(screen)
        self.snakes_remaining_message.display(screen, self.snakes_remaining_message_coords())
        self.trebuchet.display(screen, self.trebuchet_coords())

        for snake in self.snakes:
            snake.display(screen)

        for crate in self.crates:
            crate.display(screen)

    def snakes_remaining_message_coords(self):
        return Coords.bottom_left_label(self.game.get_screen_size(), self.snakes_remaining_message)

    def trebuchet_coords(self):
        return 20, 450
