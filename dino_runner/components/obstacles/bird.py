
import random
from dino_runner.components.obstacles.obstacles import Obstacle
from dino_runner.utils.constants import BIRD


class Bird(Obstacle):
    def __init__(self):
        image = BIRD[0]
        super().__init__(image)
        positions = [100, 250, 50]
        self.rect.y = positions[random.randint(0,2)]
        self.step = 0

    def update(self, game_speed, obstacles):
        super().update(game_speed, obstacles)
        self.image = BIRD[self.step // 10]
        self.step += 1
        if self.step >= 20:
            self.step = 0
            
        