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
GRAY = (128, 128, 128)
DARK_GREEN = (0, 100, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flag Capture Game")

# Circle properties
circle_radius = 20
circle_x = WIDTH // 2
circle_y = HEIGHT // 2
circle_speed = 5

# Playground dimensions
playground_x = 50
playground_y = 100
playground_width = WIDTH - 100
playground_height = HEIGHT - 200

# Font
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

# Game variables
score = 0
level = 0
game_state = "menu"  # menu, playing, level_complete, game_over

# Flag properties
flag_colors = [BLUE, GREEN, YELLOW, PURPLE, ORANGE, WHITE, RED, GRAY]
flags = []
bombs = []
captured_flags_count = 0

def generate_random_position():
    return (random.randint(playground_x + 30, playground_x + playground_width - 30), 
            random.randint(playground_y + 30, playground_y + playground_height - 30))

def setup_level(level_num):
    global flags, bombs, score, circle_x, circle_y, game_state, captured_flags_count
    
    # Reset player position
    circle_x = WIDTH // 2
    circle_y = HEIGHT // 2
    
    # Reset score when starting from menu
    if game_state == "menu":
        score = 0
    
    flags = []
    bombs = []
    captured_flags_count = 0
    
    if level_num == 1:
        # Level 1: 6 flags, all visible from start
        for i in range(6):
            flag_x, flag_y = generate_random_position()
            flags.append({
                'x': flag_x,
                'y': flag_y,
                'color': flag_colors[i % len(flag_colors)],
                'captured': False,
                'visible': True
            })
    
    elif level_num == 2:
        # Level 2: 16 flags, only 7 visible initially
        for i in range(16):
            flag_x, flag_y = generate_random_position()
            flags.append({
                'x': flag_x,
                'y': flag_y,
                'color': flag_colors[i % len(flag_colors)],
                'captured': False,
                'visible': i < 7  # Only first 7 are visible initially
            })
    
    elif level_num == 3:
        # Level 3: 30 flags with bombs
        for i in range(30):
            flag_x, flag_y = generate_random_position()
            flags.append({
                'x': flag_x,
                'y': flag_y,
                'color': flag_colors[i % len(flag_colors)],
                'captured': False,
                'visible': i < 7  # Only first 7 are visible initially
            })
    
    game_state = "playing"

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key == pygame.K_1:
                    level = 1
                    score = 0  # Reset score when starting new game
                    setup_level(level)
                elif event.key == pygame.K_2:
                    level = 2
                    score = 0  # Reset score when starting new game
                    setup_level(level)
                elif event.key == pygame.K_3:
                    level = 3
                    score = 0  # Reset score when starting new game
                    setup_level(level)
            
            elif game_state == "level_complete":
                if event.key == pygame.K_RETURN:
                    if level < 3:
                        level += 1
                        setup_level(level)
                    else:
                        game_state = "menu"
            
            elif game_state == "game_over":
                if event.key == pygame.K_RETURN:
                    game_state = "menu"
    
    # Fill the screen with black
    screen.fill(BLACK)
    
    if game_state == "menu":
        # Draw menu
        title_text = font.render("FLAG CAPTURE GAME", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - 150, HEIGHT//3))
        
        level1_text = font.render("Press 1 for EASY", True, GREEN)
        screen.blit(level1_text, (WIDTH//2 - 100, HEIGHT//3 + 60))
        
        level2_text = font.render("Press 2 for MEDIUM", True, YELLOW)
        screen.blit(level2_text, (WIDTH//2 - 100, HEIGHT//3 + 100))
        
        level3_text = font.render("Press 3 for HARD", True, RED)
        screen.blit(level3_text, (WIDTH//2 - 100, HEIGHT//3 + 140))
    
    elif game_state == "playing":
        # Draw playground
        pygame.draw.rect(screen, DARK_GREEN, (playground_x, playground_y, playground_width, playground_height))
        pygame.draw.rect(screen, WHITE, (playground_x, playground_y, playground_width, playground_height), 2)
        
        # Game logic
        # Get pressed keys
        keys = pygame.key.get_pressed()
        
        # Move the circle based on arrow key presses
        if keys[pygame.K_LEFT] and circle_x - circle_speed > playground_x + circle_radius:
            circle_x -= circle_speed
        if keys[pygame.K_RIGHT] and circle_x + circle_speed < playground_x + playground_width - circle_radius:
            circle_x += circle_speed
        if keys[pygame.K_UP] and circle_y - circle_speed > playground_y + circle_radius:
            circle_y -= circle_speed
        if keys[pygame.K_DOWN] and circle_y + circle_speed < playground_y + playground_height - circle_radius:
            circle_y += circle_speed
        
        # Check for flag captures
        visible_flags = 0
        
        for i, flag in enumerate(flags):
            if flag['visible']:
                visible_flags += 1
                
                # Calculate distance between circle and flag
                distance = ((circle_x - flag['x'])**2 + (circle_y - flag['y'])**2)**0.5
                
                if not flag['captured'] and distance < circle_radius + 20:
                    flag['captured'] = True
                    score += 50
                    captured_flags_count += 1
                    
                    # Make next flag visible in levels 2 and 3
                    if level in [2, 3]:
                        next_invisible = next((j for j, f in enumerate(flags) if not f['visible']), None)
                        if next_invisible is not None:
                            flags[next_invisible]['visible'] = True
        
        # Add bombs in level 3
        if level == 3 and random.random() < 0.01 and len(bombs) < 3:  # 1% chance each frame to add a bomb
            bomb_x, bomb_y = generate_random_position()
            bombs.append({
                'x': bomb_x,
                'y': bomb_y,
                'timer': 60,  # 1 second at 60 FPS
                'exploded': False,
                'radius': 0
            })
        
        # Update bombs
        for bomb in bombs[:]:  # Create a copy of the list to safely remove items
            if not bomb['exploded']:
                bomb['timer'] -= 1
                if bomb['timer'] <= 0:
                    bomb['exploded'] = True
            else:
                # Explosion animation
                bomb['radius'] += 2
                if bomb['radius'] > 100:  # Max explosion radius
                    bombs.remove(bomb)
                    continue
                
                # Check if player is caught in explosion
                distance = ((circle_x - bomb['x'])**2 + (circle_y - bomb['y'])**2)**0.5
                if distance < circle_radius + bomb['radius']:
                    game_state = "game_over"
        
        # Check if all flags are captured
        if captured_flags_count == len(flags):
            if level < 3:
                game_state = "level_complete"
            else:
                game_state = "game_over"
                
        # Draw the flags
        for flag in flags:
            if flag['visible'] and not flag['captured']:
                # Draw flag pole
                pygame.draw.rect(screen, BROWN, (flag['x'], flag['y'] - 30, 5, 40))
                # Draw triangular flag
                pygame.draw.polygon(screen, flag['color'], [
                    (flag['x'] + 5, flag['y'] - 30),
                    (flag['x'] + 25, flag['y'] - 20),
                    (flag['x'] + 5, flag['y'] - 10)
                ])
        
        # Draw bombs
        for bomb in bombs:
            if not bomb['exploded']:
                pygame.draw.circle(screen, BLACK, (bomb['x'], bomb['y']), 15)
                pygame.draw.circle(screen, RED, (bomb['x'], bomb['y']), 12)
                # Draw timer
                timer_text = small_font.render(str(bomb['timer'] // 6), True, WHITE)
                screen.blit(timer_text, (bomb['x'] - 5, bomb['y'] - 8))
            else:
                # Draw explosion
                pygame.draw.circle(screen, ORANGE, (bomb['x'], bomb['y']), bomb['radius'])
                pygame.draw.circle(screen, YELLOW, (bomb['x'], bomb['y']), bomb['radius'] - 10)
        
        # Draw the circle (player)
        pygame.draw.circle(screen, RED, (circle_x, circle_y), circle_radius)
        
        # Display level and score
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (10, 10))
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 50))
        
        # Display flags captured/total
        total_flags = len(flags)  # Total flags for the level
        flags_text = font.render(f"Flags: {captured_flags_count}/{total_flags}", True, WHITE)
        screen.blit(flags_text, (10, 90))
    
    elif game_state == "level_complete":
        complete_text = font.render(f"Level {level} Complete!", True, GREEN)
        screen.blit(complete_text, (WIDTH//2 - 120, HEIGHT//2 - 50))
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - 60, HEIGHT//2))
        
        next_text = font.render("Press ENTER for next level", True, WHITE)
        screen.blit(next_text, (WIDTH//2 - 150, HEIGHT//2 + 50))
    
    elif game_state == "game_over":
        if level == 3 and captured_flags_count == len(flags):
            # Player won the game
            over_text = font.render("Congratulations! You Won!", True, GREEN)
        else:
            # Player died from bomb
            over_text = font.render("Game Over!", True, RED)
        
        screen.blit(over_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
        
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - 80, HEIGHT//2))
        
        menu_text = font.render("Press ENTER for menu", True, WHITE)
        screen.blit(menu_text, (WIDTH//2 - 120, HEIGHT//2 + 50))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()