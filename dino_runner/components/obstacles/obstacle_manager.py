import pygame
from dino_runner.components.obstacles.cactus import Cactus


class Obstacle_manager:
    def __init__(self):
        self.obstacles = []
    
    def update(self, game_speed, player, game):
        if not self.obstacles:
            self.obstacles.append(Cactus())
        
        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)
            if player.rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

