
import pygame

from dino_runner.utils.constants import FONT_STYLE, SCREEN_HEIGHT, SCREEN_WIDTH


class Text:
    def show(self, screen, size, message, pos_x = SCREEN_WIDTH // 2, pos_y = SCREEN_HEIGHT // 2, color = (0,0,0), font = FONT_STYLE):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(message, True, color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (pos_x, pos_y)
        screen.blit(self.text, self.text_rect)
