import pygame
from dino_runner.components.text import Text


class Score:
    def __init__(self):
        self.score = 0
        self.max_score = 100
        self.text = Text()

    def update(self, game):
        self.score += 1
        if self.score % 100 == 0:
            game.game_speed += 2
        self.update_max_score()

    def update_max_score(self):
        if self.score > self.max_score:
            self.max_score = self.score

    def reset(self):
        self.score = 0

    def draw(self, screen):
        self.text.show(screen, 24, f"Score: {self.score}", (1000, 30))
        self.text.show(screen, 24, "HI: " + str(self.max_score), (850, 30))