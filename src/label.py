import pygame


class Label:
    STYLE_SHADOW = 'shadow'

    def __init__(self, text="", font_size=10, font_face='cartwheel.otf'):
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(font_face, font_size)
        self.color = (255, 255, 255)
        self.style = None

    def set_text(self, text):
        self.text = text
        return self

    def set_color(self, color=(0, 0, 0)):
        self.color = color
        return self

    def with_shadow(self):
        self.style = self.STYLE_SHADOW
        return self

    def set_font_size(self, font_size):
        self.font_size = font_size
        return self

    def display(self, screen, position=(0, 0)):
        if self.style == self.STYLE_SHADOW:
            self.__display_shadow(screen, position)
        else:
            text = self.font.render(self.text, 1, self.color)
            screen.blit(text, position)

    def get_size(self):
        width = len(self.text) * self.font_size
        height = self.font_size
        return width, height

    def __display_shadow(self, screen, position):
        top_text = self.font.render(self.text, 1, self.color)
        shadow_text = self.font.render(self.text, 1, (0, 0, 0))
        shadow_offset = self.font_size * 0.1
        screen.blit(shadow_text, (position[0]+shadow_offset, position[1]+shadow_offset))
        screen.blit(top_text, position)