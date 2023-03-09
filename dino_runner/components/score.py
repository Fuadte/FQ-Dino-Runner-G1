import pygame
from dino_runner.components.text import Text
from dino_runner.utils.constants import HEART


class Score:
    def __init__(self):
        self.score = 0
        self.max_score = 0
        self.text = Text()
        self.heart = 0

    def update(self, game):
        self.score += 1
        if self.score % 200 == 0:
            game.game_speed += 2

        if self.score % 500 == 0:
            game.player.hearts += 1
            self.heart = game.player.hearts
        self.update_max_score()

    def update_max_score(self):
        if self.score > self.max_score:
            self.max_score = self.score

    def reset(self):
        self.score = 0

    def draw(self, screen):
        screen.blit(HEART, (100, 20))
        self.text.show(screen, 16, f" x {self.heart}", pos_x = 150, pos_y = 30)
        self.text.show(screen, 16, f"Score: {self.score}", pos_x = 1000, pos_y = 30)
        self.text.show(screen, 16, f"HI: {self.max_score}", pos_x = 800, pos_y = 30)