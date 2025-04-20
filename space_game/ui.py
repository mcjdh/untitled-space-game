import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)

class StartScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.SysFont("Arial", 40)
        self.info_font = pygame.font.SysFont("Arial", 20)
        
    def draw(self):
        title_text = self.title_font.render("Space Game", True, WHITE)
        info_text = self.info_font.render("Press any key to start", True, WHITE)
        self.screen.blit(title_text, ((self.screen_width - title_text.get_width()) // 2, self.screen_height // 3))
        self.screen.blit(info_text, ((self.screen_width - info_text.get_width()) // 2, self.screen_height // 2))

class GameOverScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_font = pygame.font.SysFont("Arial", 40)
        self.info_font = pygame.font.SysFont("Arial", 20)
        
    def draw(self, score):
        title_text = self.title_font.render("Game Over", True, RED)
        score_text = self.info_font.render(f"Score: {score}", True, WHITE)
        info_text = self.info_font.render("Press any key to restart", True, WHITE)
        self.screen.blit(title_text, ((self.screen_width - title_text.get_width()) // 2, self.screen_height // 3))
        self.screen.blit(score_text, ((self.screen_width - score_text.get_width()) // 2, self.screen_height // 2))
        self.screen.blit(info_text, ((self.screen_width - info_text.get_width()) // 2, self.screen_height // 2 + 30))


def draw_score(screen, score):
    font = pygame.font.SysFont("Arial", 20)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10)) 