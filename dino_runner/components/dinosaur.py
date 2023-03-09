
import pygame
from pygame.sprite import Sprite
from dino_runner.components.text import Text

from dino_runner.utils.constants import DEFAULT_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING, JUMPING, DUCKING, RUNNING_SHIELD, SHIELD_TYPE


DINO_RUNNING = "running"
DINO_JUMPING = "jumping"
DINO_DUCKING = "ducking"

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}

class Dinosaur(Sprite):
    POSITION_X = 80
    POSITION_Y = 310
    JUMP_VELOCITY = 8.5
    POSITION_Y_DUCK = 340

    def __init__(self):
        self.type = DEFAULT_TYPE
        self.power_up_time_up = 0
        self.update_image(RUN_IMG[self.type][0])
        self.action = DINO_RUNNING
        self.jump_velocity = self.JUMP_VELOCITY
        self.step = 0
        self.text = Text()

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
        self.update_image(RUN_IMG[self.type][self.step // 5])
        self.step += 1

    def duck(self):
        self.update_image(DUCK_IMG[self.type][self.step // 5], pos_y = self.POSITION_Y_DUCK)
        self.step += 1

    def jump(self):
        pos_y = self.rect.y - self.jump_velocity * 4
        self.update_image(JUMP_IMG[self.type], pos_y = pos_y)
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

    def on_pick_power_up(self, power_up):
        self.type = power_up.type
        self.power_up_time_up = power_up.start_time + (power_up.duration * 1000)

    def check_power_up(self, screen):
        if self.type == SHIELD_TYPE:
            time_to_show = round((self.power_up_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.text.show(screen, 24,f"{self.type.capitalize()} enabled for {time_to_show} seconds", (500, 50))
            else:
                self.type = DEFAULT_TYPE
                self.power_up_time_up = 0