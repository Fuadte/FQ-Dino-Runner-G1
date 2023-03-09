
import pygame

from dino_runner.utils.constants import FONT_STYLE, SCREEN_HEIGHT, SCREEN_WIDTH


class Text:
    def show(self, screen, size, message, *center):
        self.font = pygame.font.Font(FONT_STYLE, size)
        self.text = self.font.render(message, True, (0,0,0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (center)
        screen.blit(self.text, self.text_rect)
