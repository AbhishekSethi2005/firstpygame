import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 700
HEIGHT = 800
PLAY_AREA = 600

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flag Capture Game")

# Circle properties
circle_radius = 20
circle_x = WIDTH // 2
circle_y = HEIGHT // 2
circle_speed = 5

# Flag properties
flag_colors = [BLUE, GREEN, YELLOW, PURPLE, ORANGE, WHITE]
flags = []
score = 0
font = pygame.font.SysFont(None, 36)

# Create flags at random positions
for i in range(6):
    flag_x = random.randint(50, WIDTH - 50)
    flag_y = random.randint(50, HEIGHT - 50)
    flags.append({
        'x': flag_x,
        'y': flag_y,
        'color': flag_colors[i],
        'captured': False
    })

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                running = False
    
    if not game_over:
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Move the circle based on arrow key presses
        if keys[pygame.K_LEFT] and circle_x - circle_speed > circle_radius:
            circle_x -= circle_speed
        if keys[pygame.K_RIGHT] and circle_x + circle_speed < WIDTH - circle_radius:
            circle_x += circle_speed
        if keys[pygame.K_UP] and circle_y - circle_speed > circle_radius:
            circle_y -= circle_speed
        if keys[pygame.K_DOWN] and circle_y + circle_speed < HEIGHT - circle_radius:
            circle_y += circle_speed
        
        # Check for flag captures
        for flag in flags:
            if not flag['captured']:
                # Calculate distance between circle and flag
                distance = ((circle_x - flag['x'])**2 + (circle_y - flag['y'])**2)**0.5
                if distance < circle_radius + 20:  # Flag capture radius
                    flag['captured'] = True
                    score += 50
        
        # Check if all flags are captured
        if all(flag['captured'] for flag in flags):
            game_over = True
    
    # Fill the screen with black
    screen.fill(BLACK)
    
    # Draw the flags
    for flag in flags:
        if not flag['captured']:
            # Draw flag pole
            pygame.draw.rect(screen, BROWN, (flag['x'], flag['y'] - 30, 5, 40))
            # Draw triangular flag
            pygame.draw.polygon(screen, flag['color'], [
                (flag['x'] + 5, flag['y'] - 30),
                (flag['x'] + 25, flag['y'] - 20),
                (flag['x'] + 5, flag['y'] - 10)
            ])
    
    # Draw the circle
    pygame.draw.circle(screen, RED, (circle_x, circle_y), circle_radius)
    
    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Display game over message
    if game_over:
        game_over_text = font.render("All flags captured! Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2))
        restart_text = font.render("Press ENTER to exit", True, WHITE)
        screen.blit(restart_text, (WIDTH//2 - 100, HEIGHT//2 + 40))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()