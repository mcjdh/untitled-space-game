import pygame, random, math

BASE_UNIT = 8

class Player:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 4 * BASE_UNIT   # 32 px
        self.height = 4 * BASE_UNIT  # 32 px
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - self.height - 10
        self.speed = 5
        self.pattern = [
            "  X ",
            "XXXX",
            " XX ",
            " XX "
        ]

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < self.screen_width - self.width:
            self.x += self.speed

    def draw(self):
        CYAN = (0, 255, 255)
        YELLOW = (255, 255, 0)
        for row_idx, row in enumerate(self.pattern):
            for col_idx, ch in enumerate(row):
                if ch == "X":
                    rect = pygame.Rect(self.x + col_idx * BASE_UNIT, self.y + row_idx * BASE_UNIT, BASE_UNIT, BASE_UNIT)
                    pygame.draw.rect(self.screen, CYAN, rect)
        # Draw thruster flame
        flame_height = BASE_UNIT * random.choice([1, 2])
        flame_width = BASE_UNIT * 2
        flame_x = self.x + (4 * BASE_UNIT) // 2 - flame_width // 2
        flame_y = self.y + 4 * BASE_UNIT
        pygame.draw.rect(self.screen, YELLOW, (flame_x, flame_y, flame_width, flame_height))

    def shoot(self):
        bullet_x = self.x + self.width // 2 - BASE_UNIT // 2
        bullet_y = self.y
        return Bullet(self.screen, bullet_x, bullet_y)

    def reset(self):
        self.x = self.screen_width // 2 - self.width // 2
        self.y = self.screen_height - self.height - 10
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bullet:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.speed = -7  # bullet speed
        self.rect = pygame.Rect(x, y, BASE_UNIT, 2 * BASE_UNIT)  # 8x16 px

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        YELLOW = (255, 255, 0)
        pygame.draw.rect(self.screen, YELLOW, self.rect)

class Enemy:
    def __init__(self, screen, current_time):
        self.screen = screen
        self.rect = pygame.Rect(self.random_x(), -4 * BASE_UNIT, 6 * BASE_UNIT, 4 * BASE_UNIT)  # 48x32 px
        self.speed = 2
        self.start_x = self.rect.x
        self.amplitude = random.randint(20, 50)
        self.frequency = random.uniform(0.005, 0.02)
        self.spawn_time = current_time

    def random_x(self):
        screen_width = self.screen.get_width()
        return random.randint(0, screen_width - 6 * BASE_UNIT)

    def update(self, current_time):
        self.rect.y += self.speed
        self.rect.x = self.start_x + self.amplitude * math.sin(self.frequency * (current_time - self.spawn_time))

    def draw(self):
        self.draw_alien(self.rect.x, self.rect.y)
        
    def draw_alien(self, x, y):
        RED = (255, 0, 0)
        pattern = [
            "  XX  ",
            " X  X ",
            "XXXXXX",
            "X XX X"
        ]
        for row_idx, row in enumerate(pattern):
            for col_idx, ch in enumerate(row):
                if ch == "X":
                    rect = pygame.Rect(x + col_idx * BASE_UNIT, y + row_idx * BASE_UNIT, BASE_UNIT, BASE_UNIT)
                    pygame.draw.rect(self.screen, RED, rect)

class Explosion:
    def __init__(self, screen, x, y, start_time):
        self.screen = screen
        self.x = x
        self.y = y
        self.start_time = start_time
        self.duration = 300  # milliseconds
        self.finished = False

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.finished = True

    def draw(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        YELLOW = (255, 255, 0)
        RED = (255, 0, 0)
        if elapsed < self.duration / 2:
            pattern = [
                "   ",
                " X ",
                "   "
            ]
            color = YELLOW
        else:
            pattern = [
                "XXX",
                "XXX",
                "XXX"
            ]
            color = RED
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])
        top_left_x = self.x - (pattern_width * BASE_UNIT) // 2
        top_left_y = self.y - (pattern_height * BASE_UNIT) // 2
        for row_idx, row in enumerate(pattern):
            for col_idx, ch in enumerate(row):
                if ch == "X":
                    rect = pygame.Rect(top_left_x + col_idx * BASE_UNIT, top_left_y + row_idx * BASE_UNIT, BASE_UNIT, BASE_UNIT)
                    pygame.draw.rect(self.screen, color, rect)

class ScorePopup:
    def __init__(self, screen, x, y, text, start_time):
        self.screen = screen
        self.x = x
        self.y = y
        self.text = text
        self.start_time = start_time
        self.duration = 800  # milliseconds
        self.finished = False
        self.font = pygame.font.SysFont("Arial", 20)

    def update(self):
        current_time = pygame.time.get_ticks()
        self.y -= 0.5  # move upward slowly
        if current_time - self.start_time > self.duration:
            self.finished = True

    def draw(self):
        YELLOW = (255, 255, 0)
        text_surface = self.font.render(self.text, True, YELLOW)
        self.screen.blit(text_surface, (self.x, self.y)) 