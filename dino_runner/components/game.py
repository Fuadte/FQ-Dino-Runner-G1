import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import Obstacle_manager
from dino_runner.components.score import Score
from dino_runner.components.text import Text

from dino_runner.utils.constants import BG, DINO_START, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


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
        self.obstacle_manager = Obstacle_manager()
        self.score = Score()
        self.text = Text()
        self.death_count = 0

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
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self.player, self.on_death)
        self.score.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
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
        self.playing = False
        self.death_count += 1

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_width = SCREEN_WIDTH // 2
        half_screen_height = SCREEN_HEIGHT // 2
        if not self.death_count:
            self.text.show(self.screen, 32, "Welcome, press any key to start!", (half_screen_width, half_screen_height))
        else:
            self.text.show(self.screen, 32, "GAME OVER", (half_screen_width, half_screen_height))
            self.text.show(self.screen, 24, "press to start again", (half_screen_width, half_screen_height + 30))
            self.text.show(self.screen, 24, "Muertes: " + str(self.death_count), (half_screen_width - 70, half_screen_height + 60))
            self.text.show(self.screen, 24, "Score: " + str(self.score.score), (half_screen_width + 70, half_screen_height + 60))

        self.screen.blit(DINO_START, (half_screen_width - 40, half_screen_height - 140))
        pygame.display.update()
        self.handle_menu_events()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False
            elif event.type == pygame.KEYDOWN:
                self.start_game()