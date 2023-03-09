import random
import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import HAMMER_TYPE


class Obstacle_manager:
    def __init__(self):
        self.obstacles = []
        self.is_playing_sound = False
    
    def update(self, game_speed, player, on_death):
        if not self.obstacles:
            probability = random.randint(0, 10)
            if probability <= 7:
                self.obstacles.append(Cactus()) 
            else:
                self.obstacles.append(Bird())

        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)
            if player.rect.colliderect(obstacle.rect):
                on_death()
                self.is_playing_sound = True
            else:
                self.is_playing_sound = False

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
    
    def reset(self):
        self.obstacles = []

