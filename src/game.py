import sys
import pygame
from src.title_screen import TitleScreen
from src.level import Level
from src.level_profile import LevelProfile


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Angry Clones")

        self.fps = 30
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.screen_size = (1024, 652)
        self.screen = pygame.display.set_mode(self.get_screen_size())
        self.levels = self.load_levels()
        self.current_level_number = 0
        self.current_level = self.levels[self.current_level_number]

    def start(self):
        while not self.game_over:
            for event in pygame.event.get():
                self.current_level.handle_event(event)

            self.current_level.calculate()
            self.current_level.display(self.screen)

            pygame.display.flip()
            pygame.display.update()

            self.clock.tick(self.fps)

        self.exit()

    def get_screen_size(self):
        return self.screen_size
    
    def complete_game(self):
        print('Game Complete!')
        self.exit()

    def go_to_next_level(self):
        if (self.current_level_number + 1) < len(self.levels):
            self.current_level_number += 1
            self.current_level = self.levels[self.current_level_number]
        else:
            self.complete_game()

    def handle_quit(self, event):
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.exit()

    def exit(self, code=0):
        pygame.quit()
        sys.exit(code)

    def load_levels(self):
        return [
            TitleScreen(self),
            Level(self, profile=LevelProfile.for_level_1())
        ]
