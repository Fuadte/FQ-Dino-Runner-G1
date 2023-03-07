
import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING


DINO_RUNNING = "running"
DINO_JUMPING = "jumping"
DINO_DUCKING = "ducking"

class Dinosaur(Sprite):
    POSITION_X = 80
    POSITION_Y = 310
    JUMP_VELOCITY = 8.5
    POSITION_Y_DUCK = 340

    def __init__(self):
        self.image = RUNNING[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.POSITION_X
        self.rect.y = self.POSITION_Y
        self.action = DINO_RUNNING
        self.jump_velocity = self.JUMP_VELOCITY
        self.step = 0

    def update(self, user_input):
        if self.action == DINO_RUNNING:
            self.run()
        elif self.action == DINO_DUCKING:
            self.duck()
        elif self.action == DINO_JUMPING:
            self.jump()

        if user_input[pygame.K_DOWN]:
            if self.action == DINO_JUMPING:
                self.jump()
            else:
                self.action = DINO_DUCKING
        elif self.action != DINO_JUMPING:
            if user_input[pygame.K_UP]:
                self.action = DINO_JUMPING
            else:
                self.action = DINO_RUNNING
        
        if self.step >= 10:
            self.step = 0

    def run(self):
        self.update_image(RUNNING[self.step // 5])
        self.step += 1

    def duck(self):
        self.update_image(DUCKING[self.step // 5], pos_y = self.POSITION_Y_DUCK)
        self.step += 1

    def jump(self):
        pos_y = self.rect.y - self.jump_velocity * 4
        self.update_image(JUMPING, pos_y = pos_y)
        self.jump_velocity -= 0.8
        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.jump_velocity = self.JUMP_VELOCITY
            self.action = DINO_RUNNING
            self.rect.y = self.POSITION_Y

    def update_image(self, image:pygame.Surface, pos_x = None, pos_y=None):
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = pos_x or self.POSITION_X
        self.rect.y = pos_y or self.POSITION_Y

    def draw(self, screen):
        screen.blit(self.image,(self.rect.x, self.rect.y))