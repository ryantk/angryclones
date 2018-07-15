from src.snake import Snake

class LevelProfile:
    def __init__(self, snakes=[], crates=[]):
        self.snakes = snakes
        self.crates = crates

    def get_snakes(self):
        return self.snakes

    def get_crates(self):
        return self.crates


    @staticmethod
    def empty_level():
        return LevelProfile(snakes=[], crates=[])

    @staticmethod
    def for_level_1():
        snakes = [
            Snake((20, 20)),
            Snake((40, 20)),
            Snake((60, 20)),
            Snake((80, 20)),
            Snake((100, 20)),
            Snake((120, 20)),
        ]
        crates = []

        return LevelProfile(snakes=snakes, crates=crates)