import random
import pygame

from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.components.power_ups.shield import Shield


class PowerUpManager:
    def __init__(self):
        self.power_ups: list[PowerUp] = []
        self.when_appears = 0
        self.power_up_type = (Hammer(), Shield())
    def update(self,game_speed, score, player):
        if not self.power_ups and score == self.when_appears:
            self.when_appears += random.randint(200, 400)
            self.power_ups.append(random.choice(self.power_up_type))

        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if power_up.rect.colliderect(player.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.on_pick_power_up(power_up)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 400)