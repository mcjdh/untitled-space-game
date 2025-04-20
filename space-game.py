import pygame
import sys
import random
import math

pygame.init()

# Constants
BASE_UNIT = 8

# Screen dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Game")

clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Background - generate starfield
NUM_STARS = 50
stars = []
for _ in range(NUM_STARS):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    size = random.randint(1, 2)
    stars.append((x, y, size))

def draw_background():
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), star[2])

# Player properties
PLAYER_WIDTH = 4 * BASE_UNIT   # 32 px
PLAYER_HEIGHT = 4 * BASE_UNIT  # 32 px
player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
player_speed = 5

def draw_player():
    # Draw the player's spaceship as an 8-bit style sprite using a 4x4 pattern
    pattern = [
        "  X ",
        "XXXX",
        " XX ",
        " XX "
    ]
    for row_idx, row in enumerate(pattern):
        for col_idx, ch in enumerate(row):
            if ch == "X":
                rect = pygame.Rect(player_x + col_idx * BASE_UNIT, player_y + row_idx * BASE_UNIT, BASE_UNIT, BASE_UNIT)
                pygame.draw.rect(screen, CYAN, rect)
    # Draw thruster flame for a retro flicker effect
    flame_height = BASE_UNIT * random.choice([1, 2])
    flame_width = BASE_UNIT * 2
    flame_x = player_x + (4 * BASE_UNIT) // 2 - flame_width // 2
    flame_y = player_y + 4 * BASE_UNIT
    pygame.draw.rect(screen, YELLOW, (flame_x, flame_y, flame_width, flame_height))

# Bullet properties
BULLET_WIDTH = 1 * BASE_UNIT  # 8 px
BULLET_HEIGHT = 2 * BASE_UNIT  # 16 px
bullet_speed = -7
bullets = []
last_shot_time = 0
shot_delay = 300  # milliseconds

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)


def update_bullets():
    global bullets
    for bullet in bullets:
        bullet.y += bullet_speed
    bullets = [bullet for bullet in bullets if bullet.y > -BULLET_HEIGHT]

# Enemy properties
ENEMY_WIDTH = 6 * BASE_UNIT   # 48 px
ENEMY_HEIGHT = 4 * BASE_UNIT  # 32 px
enemy_speed = 2
enemies = []
enemy_spawn_delay = 2000  # milliseconds
last_enemy_spawn_time = pygame.time.get_ticks()

# Score
score = 0
font = pygame.font.SysFont("Arial", 20)

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to draw a pixel-art style alien using a pattern
# The alien is defined by a 6x4 character pattern
# Each 'X' will be drawn as a BASE_UNIT sized square

def draw_alien(x, y):
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
                pygame.draw.rect(screen, RED, rect)


def draw_enemies():
    for enemy in enemies:
        draw_alien(enemy['rect'].x, enemy['rect'].y)

# Explosion properties for 8px style explosions
explosions = []
EXPLOSION_DURATION = 300  # milliseconds

def update_enemies():
    global enemies, score, bullets
    current_time = pygame.time.get_ticks()
    for enemy in enemies:
        enemy['rect'].y += enemy_speed
        enemy['rect'].x = enemy['start_x'] + enemy['amplitude'] * math.sin(enemy['frequency'] * (current_time - enemy['spawn_time']))
    enemies[:] = [enemy for enemy in enemies if enemy['rect'].y < SCREEN_HEIGHT]
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy['rect']):
                # Create an explosion at the enemy's center
                explosions.append({
                    'x': enemy['rect'].centerx,
                    'y': enemy['rect'].centery,
                    'start_time': current_time
                })
                score_popups.append({
                    'x': enemy['rect'].centerx,
                    'y': enemy['rect'].centery,
                    'text': '+10',
                    'start_time': current_time
                })
                enemies.remove(enemy)
                if bullet in bullets:
                    bullets.remove(bullet)
                score += 10
                break

def update_explosions():
    global explosions
    current_time = pygame.time.get_ticks()
    explosions[:] = [exp for exp in explosions if current_time - exp['start_time'] <= EXPLOSION_DURATION]

def draw_explosions():
    current_time = pygame.time.get_ticks()
    for exp in explosions:
        elapsed = current_time - exp['start_time']
        if elapsed < EXPLOSION_DURATION / 2:
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
        top_left_x = exp['x'] - (pattern_width * BASE_UNIT) // 2
        top_left_y = exp['y'] - (pattern_height * BASE_UNIT) // 2

        for row_idx, row in enumerate(pattern):
            for col_idx, ch in enumerate(row):
                if ch == "X":
                    rect = pygame.Rect(top_left_x + col_idx * BASE_UNIT, top_left_y + row_idx * BASE_UNIT, BASE_UNIT, BASE_UNIT)
                    pygame.draw.rect(screen, color, rect)

# Score popup properties for 8px style popups
score_popups = []
POPUP_DURATION = 800  # milliseconds

def update_score_popups():
    global score_popups
    current_time = pygame.time.get_ticks()
    for popup in score_popups:
        popup['y'] -= 0.5  # move upward slowly
    score_popups[:] = [popup for popup in score_popups if current_time - popup['start_time'] <= POPUP_DURATION]

def draw_score_popups():
    current_time = pygame.time.get_ticks()
    for popup in score_popups:
        text_surface = font.render(popup['text'], True, YELLOW)
        screen.blit(text_surface, (popup['x'], popup['y']))

# Insert new screen functions
def draw_start_screen():
    title_font = pygame.font.SysFont("Arial", 40)
    info_font = pygame.font.SysFont("Arial", 20)
    title_text = title_font.render("Space Game", True, WHITE)
    info_text = info_font.render("Press any key to start", True, WHITE)
    screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, SCREEN_HEIGHT // 3))
    screen.blit(info_text, ((SCREEN_WIDTH - info_text.get_width()) // 2, SCREEN_HEIGHT // 2))


def draw_gameover_screen():
    title_font = pygame.font.SysFont("Arial", 40)
    info_font = pygame.font.SysFont("Arial", 20)
    title_text = title_font.render("Game Over", True, RED)
    score_text = info_font.render(f"Score: {score}", True, WHITE)
    info_text = info_font.render("Press any key to restart", True, WHITE)
    screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, ((SCREEN_WIDTH - score_text.get_width()) // 2, SCREEN_HEIGHT // 2))
    screen.blit(info_text, ((SCREEN_WIDTH - info_text.get_width()) // 2, SCREEN_HEIGHT // 2 + 30))

def main():
    global player_x, last_enemy_spawn_time, bullets, score, last_shot_time
    running = True
    game_state = "start"
    
    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        current_time = pygame.time.get_ticks()
        
        if game_state == "start":
            draw_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    game_state = "playing"
                    player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
                    bullets = []
                    enemies.clear()
                    score = 0
                    last_shot_time = 0
                    last_enemy_spawn_time = current_time
            pygame.display.flip()
            continue
        
        elif game_state == "playing":
            draw_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
                player_x -= player_speed
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
                player_x += player_speed
            if keys[pygame.K_SPACE]:
                if current_time - last_shot_time > shot_delay:
                    new_bullet = pygame.Rect(player_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2, player_y, BULLET_WIDTH, BULLET_HEIGHT)
                    bullets.append(new_bullet)
                    last_shot_time = current_time
                    
            if current_time - last_enemy_spawn_time > enemy_spawn_delay:
                enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
                enemy = {
                    'rect': pygame.Rect(enemy_x, 0, ENEMY_WIDTH, ENEMY_HEIGHT),
                    'spawn_time': current_time,
                    'start_x': enemy_x,
                    'amplitude': random.randint(20, 50),
                    'frequency': random.uniform(0.002, 0.005)
                }
                enemies.append(enemy)
                last_enemy_spawn_time = current_time
                
            update_bullets()
            update_enemies()
            update_explosions()
            update_score_popups()
            
            # Check collision between player and enemies
            player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
            for enemy in enemies:
                if player_rect.colliderect(enemy['rect']):
                    game_state = "gameover"
                    break
            
            draw_player()
            draw_bullets()
            draw_enemies()
            draw_explosions()
            draw_score_popups()
            draw_score()
        
        elif game_state == "gameover":
            draw_gameover_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    game_state = "playing"
                    player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
                    bullets = []
                    enemies.clear()
                    score = 0
                    last_shot_time = 0
                    last_enemy_spawn_time = current_time
            
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main() 