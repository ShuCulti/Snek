import pygame
import sys
import random
import math
import time

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Perfect Snake Game")

# Colors
BACKGROUND = (15, 30, 40)
GRID_COLOR = (30, 50, 60)
SNAKE_HEAD_COLOR = (0, 200, 100)
SNAKE_BODY_COLOR = (0, 180, 80)
FOOD_COLOR = (220, 50, 50)
TEXT_COLOR = (220, 220, 220)
UI_BG = (25, 45, 55)
UI_BORDER = (60, 120, 140)

# Game constants
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 60

# Fonts
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_medium = pygame.font.SysFont("arial", 32, bold=True)
font_small = pygame.font.SysFont("arial", 24)

# Game variables
score = 0
high_score = 0
game_speed = 10
game_mode = "classic"  # classic, wall_pass, speed_up

# Load sounds
try:
    eat_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytearray([0])))  # Placeholder
    crash_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytearray([0])))  # Placeholder
except:
    # Create silent sounds if audio loading fails
    eat_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytearray([0])))
    crash_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytearray([0])))

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.color = SNAKE_HEAD_COLOR
        self.body_colors = [SNAKE_BODY_COLOR] * (self.length - 1)
        self.score = 0
        self.grow_to = 3
        self.last_move_time = 0
        self.move_delay = 0.1  # seconds
        self.is_alive = True
        self.special_effect = None
        self.effect_timer = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return  # Cannot turn directly backwards
        self.direction = point
    
    def move(self):
        if not self.is_alive:
            return
            
        current_time = time.time()
        if current_time - self.last_move_time < self.move_delay:
            return
            
        self.last_move_time = current_time
        
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Check for self collision
        if new_position in self.positions[1:] and game_mode != "wall_pass":
            self.is_alive = False
            crash_sound.play()
            return
            
        self.positions.insert(0, new_position)
        
        # Check if snake should grow
        if len(self.positions) > self.grow_to:
            self.positions.pop()
    
    def draw(self, surface):
        # Draw snake body with gradient effect
        for i, p in enumerate(self.positions):
            color = self.color if i == 0 else self.body_colors[i-1] if i-1 < len(self.body_colors) else SNAKE_BODY_COLOR
            
            # Create a gradient effect for the body
            if i > 0:
                color = (max(0, color[0] - i*2), 
                         max(0, color[1] - i*2), 
                         max(0, color[2] - i*2))
            
            rect = pygame.Rect((p[0] * CELL_SIZE, p[1] * CELL_SIZE), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)
            
            # Draw eyes on the head
            if i == 0:
                # Determine eye positions based on direction
                dx, dy = self.direction
                eye_size = CELL_SIZE // 5
                eye_offset = CELL_SIZE // 4
                
                # Left eye
                left_eye_x = p[0] * CELL_SIZE + CELL_SIZE // 2 - eye_offset * dx - eye_offset * abs(dy)
                left_eye_y = p[1] * CELL_SIZE + CELL_SIZE // 2 - eye_offset * dy - eye_offset * abs(dx)
                pygame.draw.circle(surface, (0, 0, 0), (left_eye_x, left_eye_y), eye_size)
                
                # Right eye
                right_eye_x = p[0] * CELL_SIZE + CELL_SIZE // 2 + eye_offset * abs(dy)
                right_eye_y = p[1] * CELL_SIZE + CELL_SIZE // 2 + eye_offset * abs(dx)
                pygame.draw.circle(surface, (0, 0, 0), (right_eye_x, right_eye_y), eye_size)
    
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.turn((1, 0))
                elif event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_w:
                    self.turn((0, -1))
                elif event.key == pygame.K_s:
                    self.turn((0, 1))
                elif event.key == pygame.K_a:
                    self.turn((-1, 0))
                elif event.key == pygame.K_d:
                    self.turn((1, 0))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()
        self.spawn_time = time.time()
        self.pulse_value = 0
        self.pulse_direction = 1
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.spawn_time = time.time()
        
    def draw(self, surface):
        # Create a pulsing effect
        self.pulse_value += 0.1 * self.pulse_direction
        if self.pulse_value >= 1.0:
            self.pulse_value = 1.0
            self.pulse_direction = -1
        elif self.pulse_value <= 0.5:
            self.pulse_value = 0.5
            self.pulse_direction = 1
            
        pulse_color = (
            min(255, int(self.color[0] * self.pulse_value)),
            min(255, int(self.color[1] * self.pulse_value)),
            min(255, int(self.color[2] * self.pulse_value))
        )
        
        rect = pygame.Rect((self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, pulse_color, rect)
        pygame.draw.rect(surface, (100, 0, 0), rect, 1)
        
        # Draw a simple apple shape
        stem_rect = pygame.Rect((self.position[0] * CELL_SIZE + CELL_SIZE//2 - 2, 
                                 self.position[1] * CELL_SIZE - 5), (4, 8))
        pygame.draw.rect(surface, (100, 70, 30), stem_rect)
        
        leaf_rect = pygame.Rect((self.position[0] * CELL_SIZE + CELL_SIZE//2 + 2, 
                                 self.position[1] * CELL_SIZE - 3), (6, 4))
        pygame.draw.ellipse(surface, (0, 150, 0), leaf_rect)

# Create game objects
snake = Snake()
food = Food()

# Draw grid function
def draw_grid(surface):
    for y in range(0, HEIGHT, CELL_SIZE):
        for x in range(0, WIDTH, CELL_SIZE):
            rect = pygame.Rect((x, y), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

# Draw UI function
def draw_ui(surface):
    # Score panel
    score_rect = pygame.Rect(10, 10, 300, 40)
    pygame.draw.rect(surface, UI_BG, score_rect, border_radius=8)
    pygame.draw.rect(surface, UI_BORDER, score_rect, 2, border_radius=8)
    
    score_text = font_small.render(f"Score: {snake.score}", True, TEXT_COLOR)
    surface.blit(score_text, (20, 18))
    
    # High score
    high_score_text = font_small.render(f"High: {high_score}", True, TEXT_COLOR)
    surface.blit(high_score_text, (170, 18))
    
    # Game mode
    mode_text = font_small.render(f"Mode: {game_mode}", True, TEXT_COLOR)
    surface.blit(mode_text, (WIDTH - mode_text.get_width() - 20, 18))
    
    # Game over message
    if not snake.is_alive:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        
        game_over_text = font_large.render("GAME OVER", True, (220, 50, 50))
        surface.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        
        restart_text = font_medium.render("Press R to Restart", True, TEXT_COLOR)
        surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 20))

# Main game loop
clock = pygame.time.Clock()

while True:
    # Handle events
    snake.handle_keys()
    
    # Move snake
    snake.move()
    
    # Check if snake ate food
    if snake.get_head_position() == food.position and snake.is_alive:
        snake.grow_to += 1
        snake.score += 10
        high_score = max(high_score, snake.score)
        eat_sound.play()
        food.randomize_position()
        
        # Make sure food doesn't spawn on snake
        while food.position in snake.positions:
            food.randomize_position()
    
    # Draw everything
    screen.fill(BACKGROUND)
    draw_grid(screen)
    snake.draw(screen)
    food.draw(screen)
    draw_ui(screen)
    
    # Update display
    pygame.display.update()
    clock.tick(FPS)