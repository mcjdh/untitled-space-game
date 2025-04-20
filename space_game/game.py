import pygame
import random
import math
from space_game import entities, ui, audio, collisions, powerups
from space_game import progression


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.screen_width = 480
        self.screen_height = 640
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Space Game")
        self.stars = self.generate_starfield()
        
        self.player = entities.Player(self.screen, self.screen_width, self.screen_height)
        self.bullets = []
        self.enemies = []
        self.explosions = []
        self.score_popups = []
        self.score = 0
        self.progression = progression.load_progression()
        self.enemy_spawn_delay = max(1000, 2000 - (self.progression['level'] - 1) * 100)  # Adjust spawn delay based on level

        self.start_screen = ui.StartScreen(self.screen, self.screen_width, self.screen_height)
        self.gameover_screen = ui.GameOverScreen(self.screen, self.screen_width, self.screen_height)
        self.game_state = "start"
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        self.last_shot_time = 0
        self.shot_delay = 300  # milliseconds

        audio.init_audio()

    def generate_starfield(self):
        stars = []
        NUM_STARS = 50
        for _ in range(NUM_STARS):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 2)
            stars.append((x, y, size))
        return stars

    def draw_background(self):
        WHITE = (255, 255, 255)
        for star in self.stars:
            pygame.draw.circle(self.screen, WHITE, (star[0], star[1]), star[2])

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            current_time = pygame.time.get_ticks()
            self.screen.fill((0, 0, 0))
            
            if self.game_state == "start":
                self.start_screen.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        self.game_state = "playing"
                        self.reset_game()
            elif self.game_state == "playing":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if current_time - self.last_shot_time > self.shot_delay:
                                bullet = self.player.shoot()
                                self.bullets.append(bullet)
                                self.last_shot_time = current_time
                                audio.play_shoot()
                
                keys = pygame.key.get_pressed()
                self.player.update(keys)
                for bullet in self.bullets:
                    bullet.update()
                self.bullets = [b for b in self.bullets if b.rect.y > -b.rect.height]

                if current_time - self.last_enemy_spawn_time > self.enemy_spawn_delay:
                    enemy = entities.Enemy(self.screen, current_time)
                    self.enemies.append(enemy)
                    self.last_enemy_spawn_time = current_time
                for enemy in self.enemies:
                    enemy.update(current_time)
                self.enemies = [e for e in self.enemies if e.rect.y < self.screen_height]

                collisions.handle_collisions(self)

                for explosion in self.explosions:
                    explosion.update()
                self.explosions = [exp for exp in self.explosions if not exp.finished]
                
                for popup in self.score_popups:
                    popup.update()
                self.score_popups = [p for p in self.score_popups if not p.finished]

                self.draw_background()
                self.player.draw()
                for bullet in self.bullets:
                    bullet.draw()
                for enemy in self.enemies:
                    enemy.draw()
                for explosion in self.explosions:
                    explosion.draw()
                for popup in self.score_popups:
                    popup.draw()
                ui.draw_score(self.screen, self.score)
            elif self.game_state == "gameover":
                self.gameover_screen.draw(self.score)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        xp_gain = self.score // 10
                        self.progression = progression.update_progression(self.score, xp_gain, self.progression)
                        self.enemy_spawn_delay = max(1000, 2000 - (self.progression['level'] - 1) * 100)
                        self.game_state = "playing"
                        self.reset_game()

            pygame.display.flip()
        pygame.quit()

    def reset_game(self):
        self.player.reset()
        self.bullets.clear()
        self.enemies.clear()
        self.explosions.clear()
        self.score_popups.clear()
        self.score = 0
        self.enemy_spawn_delay = max(1000, 2000 - (self.progression['level'] - 1) * 100)


if __name__ == "__main__":
    Game().run() 