import pygame
from dino_runner.components.clouds.cloud_manager import CloudManager
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import Obstacle_manager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.score import Score
from dino_runner.components.text import Text

from dino_runner.utils.constants import AMBIENT_MUSIC, BG, DEATH_SOUND, DINO_DEAD, DINO_START, EXPLOSION, EXPLOSION_SOUND, GAME_OVER, HAMMER_TYPE, ICON, RESET, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.executing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380

        self.player = Dinosaur()
        self.cloud_manager = CloudManager()
        self.obstacle_manager = Obstacle_manager()
        self.score = Score()
        self.text = Text()
        self.death_count = 0
        self.death_sound = pygame.mixer.Sound(DEATH_SOUND)
        self.explosion_sound = pygame.mixer.Sound(EXPLOSION_SOUND)
        self.ambient_sound = pygame.mixer.Sound(AMBIENT_MUSIC)
        self.power_up_manager = PowerUpManager()

    def run(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()

        pygame.quit()

    def start_game(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset()
        self.score.reset()
        self.game_speed = 20
        self.power_up_manager.reset()
        self.ambient_sound.play()
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.ambient_sound.stop()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.obstacle_manager.update(self.game_speed, self.player, self.on_death)
        self.power_up_manager.update(self.game_speed, self.score.score, self.player)
        self.player.update(user_input)
        self.cloud_manager.update(self.game_speed)
        self.score.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.cloud_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.player.check_power_up(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def on_death(self):
        is_invincible = self.player.type == SHIELD_TYPE
        is_on_smash =self.player.type == HAMMER_TYPE
        if is_invincible:
            pass
        elif is_on_smash:
            self.obstacle_manager.obstacles[0].image = EXPLOSION
            if not self.obstacle_manager.is_playing_sound:
                self.explosion_sound.play()
        else:
            self.ambient_sound.stop()
            self.player.update_image(DINO_DEAD)
            self.death_sound.play()
            pygame.time.delay(1500)
            self.playing = False
            self.death_count += 1

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        if not self.death_count:
            self.text.show(self.screen, 24, "Welcome, press any key to start!")
            self.screen.blit(DINO_START, (half_screen_width - 40, half_screen_height - 140))
        else:
            self.screen.blit(RESET, (half_screen_width - 40, half_screen_height - 140))
            self.screen.blit(GAME_OVER, (half_screen_width - 180, half_screen_height - 50))
            self.text.show(self.screen, 25, "press any key to start again", pos_y = half_screen_height + 20, color = (60,60,60))
            self.text.show(self.screen, 16, f"Deaths : {self.death_count}", pos_x = half_screen_width - 100, pos_y = half_screen_height + 60,color = (255,0,0))
            self.text.show(self.screen, 16, f"Score : {self.score.score}", pos_x = half_screen_width + 100, pos_y = half_screen_height + 60, color = (0,255,0))
            self.text.show(self.screen, 16, f"High Score: {self.score.max_score}", pos_y = half_screen_height + 90, color = (200,255,0))

        pygame.display.update()
        self.handle_menu_events()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.start_game()