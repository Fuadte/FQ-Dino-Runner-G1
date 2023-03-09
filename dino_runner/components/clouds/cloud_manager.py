import random
import pygame
from dino_runner.components.clouds.cloud import Cloud


class CloudManager:
    def __init__(self):
        self.clouds = []

    def update(self, game_speed):
        if not self.clouds:
            self.clouds.append(Cloud())

        for cloud in self.clouds:
            cloud.update(game_speed, self.clouds)

    def draw(self, screen):
        for cloud in self.clouds:
            cloud.draw(screen)

    def reset(self):
        self.clouds = []