import random
import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus


class Obstacle_manager:
    def __init__(self):
        self.obstacles = []
        self.obstacle_type = [Cactus(), Bird()]
    
    def update(self, game_speed, player, game):
        if not self.obstacles:
            probability = random.randint(0, 10)
            self.obstacles.append(Cactus()) if probability <= 7 else self.obstacles.append(Bird())
        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)
            if player.rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

