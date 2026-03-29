import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()

# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 90))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def move_up(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.y < SCREEN_HEIGHT - self.rect.height:
            self.rect.y += self.speed

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.base_speed = 5
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def update(self, speed_multiplier=1.0):
        self.rect.x += self.dx * self.base_speed * speed_multiplier
        self.rect.y += self.dy * self.base_speed * speed_multiplier

        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dy *= -1

# Create sprites
left_paddle = Paddle(20, SCREEN_HEIGHT // 2 - 45)
right_paddle = Paddle(SCREEN_WIDTH - 35, SCREEN_HEIGHT // 2 - 45)
ball = Ball()

# Game state
mode = "menu"  # menu, playing, game_over
left_score = 0
right_score = 0
WIN_MATCH = 2

# UI helpers
font = pygame.font.SysFont(None, 48)
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 40, 240, 80)

def draw_text(text, x, y, color=WHITE):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (x, y))

def reset_positions():
    left_paddle.rect.y = SCREEN_HEIGHT // 2 - 45
    right_paddle.rect.y = SCREEN_HEIGHT // 2 - 45
    ball.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball.dx = random.choice([-1, 1])
    ball.dy = random.choice([-1, 1])

reset_positions()

running = True
game_start_ticks = None
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if mode == "menu" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos):
                mode = "playing"
                left_score = 0
                right_score = 0
                reset_positions()
                game_start_ticks = pygame.time.get_ticks()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if mode in ("playing", "game_over"):
                mode = "menu"
                left_score = 0
                right_score = 0
                reset_positions()
                game_start_ticks = None

    screen.fill(BLACK)

    if mode == "menu":
        draw_text("Pong Best of 3", SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 - 120)
        pygame.draw.rect(screen, WHITE, button_rect, border_radius=10)
        draw_text("Start", button_rect.x + 70, button_rect.y + 20, BLACK)
        draw_text("Click to Start", SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 80)

    elif mode == "playing":
        # Handle paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move_up()
        if keys[pygame.K_s]:
            left_paddle.move_down()
        if keys[pygame.K_UP]:
            right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            right_paddle.move_down()

        # Time & speed scaling
        elapsed_time_ms = pygame.time.get_ticks() - (game_start_ticks or pygame.time.get_ticks())
        elapsed_sec = elapsed_time_ms // 1000
        if elapsed_sec >= 120:
            speed_multiplier = 3.0
        elif elapsed_sec >= 60:
            speed_multiplier = 2.0 + (elapsed_sec - 60) / 60.0
        else:
            speed_multiplier = 1.0 + (elapsed_sec / 60.0)

        # Update ball with scaling
        ball.update(speed_multiplier)

        # Check paddle collisions
        if pygame.sprite.spritecollide(ball, pygame.sprite.Group(left_paddle), False):
            ball.dx = 1
        if pygame.sprite.spritecollide(ball, pygame.sprite.Group(right_paddle), False):
            ball.dx = -1

        # Apply speed scaling to paddles
        left_paddle.speed = 5 * speed_multiplier
        right_paddle.speed = 5 * speed_multiplier

        # Score check
        if ball.rect.left < 0:
            right_score += 1
            reset_positions()
            game_start_ticks = pygame.time.get_ticks()
        elif ball.rect.right > SCREEN_WIDTH:
            left_score += 1
            reset_positions()
            game_start_ticks = pygame.time.get_ticks()

        # Best of 3 logic (first to 2 points wins)
        if left_score >= WIN_MATCH or right_score >= WIN_MATCH:
            mode = "game_over"

        # Draw game objects
        screen.blit(left_paddle.image, left_paddle.rect)
        screen.blit(right_paddle.image, right_paddle.rect)
        screen.blit(ball.image, ball.rect)

        draw_text(f"Score: {left_score} - {right_score}", 10, 10)
        draw_text(f"Time: {elapsed_sec}s", SCREEN_WIDTH - 200, 10)
        draw_text(f"Speed: {speed_multiplier:.2f}x", SCREEN_WIDTH - 200, 50)
        draw_text("Press R to return to menu after game over", 180, SCREEN_HEIGHT - 40)

    elif mode == "game_over":
        winner = "Left" if left_score > right_score else "Right"
        draw_text(f"{winner} player wins!", SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 - 40)
        draw_text("Press R to return to Menu", SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 2 + 20)

    pygame.display.flip()

pygame.quit()