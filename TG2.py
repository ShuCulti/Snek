import pygame,sys,random,math
from pygame import mixer

class FOOD:
    def __init__(self):
        self.randomize()
        self.pulse_value = 0
        self.pulse_direction = 1

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        stem_rect = pygame.Rect(fruit_rect.x + 8, fruit_rect.y -5, 3, 8)
        leaf_rect = pygame.Rect(fruit_rect.x + 10, fruit_rect.y -3, 6, 3)
        leaf_rect2 = pygame.Rect(fruit_rect.x + 3, fruit_rect.y -4, 6, 3)
        pygame.draw.rect(screen,'red',fruit_rect)
        pygame.draw.rect(screen,'black',fruit_rect,2)
        pygame.draw.rect(screen,'brown',stem_rect)
        pygame.draw.rect(screen,'green',leaf_rect)
        pygame.draw.rect(screen,'black',leaf_rect,1)
        pygame.draw.rect(screen,'green',leaf_rect2)
        pygame.draw.rect(screen,'black',leaf_rect2, 1)

    def randomize(self):
        self.pos = pygame.Vector2(random.randint(0,cell_numberx -1), random.randint(0,cell_numbery - 1))
    
    def draw_pulse(self):
        # Creating da pulse
        self.color = (255,185,45)
        # self.color = (255,200,100)
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
        
        pulse_rect = pygame.Rect((self.pos.x * cell_size, self.pos.y * cell_size), (cell_size, cell_size))
        pygame.draw.rect(screen, pulse_color, pulse_rect)
        pygame.draw.rect(screen, (100, 0, 0), pulse_rect, 1)
        pygame.draw.rect(screen, (0, 0, 0), pulse_rect, 1)

class SNAKE:
    def __init__(self):
        self.gen_start_pos()
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            self.snake_head = self.body[0]
            snake_head_rect = pygame.Rect(self.snake_head.x * cell_size, self.snake_head.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, 'lightblue', snake_rect)
            pygame.draw.rect(screen, 'blue', snake_rect,3)
            pygame.draw.rect(screen,'lightblue',snake_head_rect)
            pygame.draw.rect(screen,'blue',snake_head_rect,3)
            #The Snake Eyes RIGHT, LEFT, UP, DOWN
            if self.direction == pygame.Vector2(1,0):
                pygame.draw.circle(screen,'black',(snake_head_rect.x +15 ,snake_head_rect.y+ 5),5)
                pygame.draw.circle(screen,'black',(snake_head_rect.x +15 ,snake_head_rect.y+ 15),5)
                pygame.draw.circle(screen,'white',(snake_head_rect.x +15 ,snake_head_rect.y+ 5),5,2)
                pygame.draw.circle(screen,'white',(snake_head_rect.x +15 ,snake_head_rect.y+ 15),5,2)
               
            if self.direction == pygame.Vector2(-1,0):
                pygame.draw.circle(screen,'black',(snake_head_rect.x + 5,snake_head_rect.y+ 5),5)
                pygame.draw.circle(screen,'black',(snake_head_rect.x + 5,snake_head_rect.y+ 15),5)              
                pygame.draw.circle(screen,'white',(snake_head_rect.x + 5,snake_head_rect.y+ 5),5,2)
                pygame.draw.circle(screen,'white',(snake_head_rect.x + 5,snake_head_rect.y+ 15),5,2)
            if self.direction == pygame.Vector2(0,-1):
                pygame.draw.circle(screen,'black',(snake_head_rect.x +5 ,snake_head_rect.y + 5),5)
                pygame.draw.circle(screen,'black',(snake_head_rect.x +15 ,snake_head_rect.y+ 5),5)
                pygame.draw.circle(screen,'white',(snake_head_rect.x +5 ,snake_head_rect.y + 5),5,2)
                pygame.draw.circle(screen,'white',(snake_head_rect.x +15 ,snake_head_rect.y+ 5),5,2)
            if self.direction == pygame.Vector2(0,1):
                pygame.draw.circle(screen,'black',(snake_head_rect.x +5 ,snake_head_rect.y+ 15),5)
                pygame.draw.circle(screen,'black',(snake_head_rect.x +15 ,snake_head_rect.y+ 15),5)
                pygame.draw.circle(screen,'white',(snake_head_rect.x +5 ,snake_head_rect.y+ 15),5,2)
                pygame.draw.circle(screen,'white',(snake_head_rect.x +15 ,snake_head_rect.y+ 15),5,2)

    def move(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

        self.can_turn = True

    def add_block(self):
        self.new_block = True
    
    def gen_start_pos(self):
        center = pygame.Vector2(cell_numberx // 2, cell_numbery // 2)  # (20,15) for 800x600, CELL=20
        choices = [
            [center + pygame.Vector2(1,0), center, center - pygame.Vector2(1,0)],   # +x
            [center + pygame.Vector2(-1,0), center, center - pygame.Vector2(-1,0)], # -x
            [center + pygame.Vector2(0,1), center, center - pygame.Vector2(0,1)],   # +y
            [center + pygame.Vector2(0,-1), center, center - pygame.Vector2(0,-1)], # -y
        ]
        self.body = random.choice(choices)
        startdirection = [pygame.Vector2(1,0),pygame.Vector2(-1,0),pygame.Vector2(0,1),pygame.Vector2(0,-1)]
        if self.body == choices[0]:
            self.direction = random.choice([startdirection[0],startdirection[2],startdirection[3]])
        if self.body == choices[1]:
            self.direction = random.choice([startdirection[1], startdirection[2],startdirection[3]])
        if self.body == choices[2]:
            self.direction = random.choice([startdirection[2],startdirection[0], startdirection[1]])
        if self.body == choices[3]:
            self.direction = random.choice([startdirection[3], startdirection[0], startdirection[1]])
    def reset(self):
        self.gen_start_pos()
    
class MAIN:

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.snake = SNAKE()
        self.food = FOOD()
        self.initial_ms, self.min_ms, self.step_ms = 150, 10, 10
        self.current_ms = self.initial_ms
        self.game_active = True

    def update(self):
        if not self.game_active:
            return          # paused on game over
        self.snake.move()
        self.collision()
        self.fail()

    def draw_ellem(self):
        if self.game_active == True:
            self.snake.draw_snake()
            self.food.draw_fruit()
            self.food.draw_pulse()
    
        if not self.game_active:
            self.game_overscreen()
            
    
    def start_screen(self):
        overlay = pygame.Surface((Width, Height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        title_font = pygame.font.SysFont("arial", 72, bold=True)
        title_text = title_font.render("PYTHON", True, "cyan")
        screen.blit(title_text, (Width//2 - title_text.get_width()//2, Height//4 - 50))
        
        start_font = pygame.font.SysFont("arial", 36)
        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0:  
            start_text = start_font.render("Press SPACE to Start", True, "#FFF200")
            screen.blit(start_text, (Width//2 - start_text.get_width()//2, Height//2 + 50))
        
        controls_font = pygame.font.SysFont("arial", 24)
        controls_text = controls_font.render("Controls: W A S D  |  R to Restart", True, (180, 180, 180))
        screen.blit(controls_text, (Width//2 - controls_text.get_width()//2, Height//2 + 100))
        
        if self.high_score > 0:
            score_font = pygame.font.SysFont("arial", 28)
            score_text = score_font.render(f"High Score: {self.high_score}", True, (255, 215, 0))
            screen.blit(score_text, (Width//2 - score_text.get_width()//2, Height//2 + 150))
        
    def collision(self):
        if self.snake.body[0] == self.food.pos:
            self.score += 5
            self.high_score = max(self.high_score, self.score)
            self.food.randomize()
            self.snake.add_block()
            pygame.mixer.Sound.play(crunch)
            self.current_ms = max(min_ms, self.current_ms - step_ms)
            pygame.time.set_timer(SCREEN_UPDATE, self.current_ms)

    
    def fail(self):
        head = self.snake.body[0]
        x, y = int(head.x), int(head.y)
        out_of_bounds = (x < 0 or x >= cell_numberx or y < 0 or y >= cell_numbery)
        hit_self = any(block == head for block in self.snake.body[1:])
        if out_of_bounds or hit_self:
            self.game_over()
            pygame.mixer.Sound.play(fail_sound)

    def game_over(self):
        self.high_score = max(self.high_score, self.score)
        self.current_ms = self.initial_ms
        self.game_active = False

    def game_overscreen(self):
        overlay = pygame.Surface((Width, Height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        game_over_text = font_large.render("GAME OVER", True, (220, 50, 50))
        screen.blit(game_over_text, (Width//2 - game_over_text.get_width()//2, Height//2 - 50))
        gameoverscore_text = font_medium.render(f"Score:{self.score}", True, "#5CF4FF")
        screen.blit(gameoverscore_text, (Width//2 - gameoverscore_text.get_width()//2, Height//2 + 10))
        restart_text = font_medium.render("Press R to Restart", True, (220, 220, 220))
        screen.blit(restart_text, (Width//2 - restart_text.get_width()//2, Height//2 + 50))

    def restart(self):
        self.score = 0
        self.snake.reset()
        self.food.randomize()
        self.game_active = True

class GameUI:
    def draw_grid(screen):
        for x in range(0,Width,cell_size):
            pygame.draw.line(screen,(31,36,41), (x,0), (x,Height))
        for y in range(0,Height,cell_size):
            pygame.draw.line(screen,(31,36,41),(0,y), (Width,y))
    def draw_borders(screen):
        score_border_rect = pygame.Rect(20,10,100,25)
        high_score_border_rect = pygame.Rect(140,10,150,25)
        pygame.draw.rect(screen,'#2B3A55',score_border_rect,2)
        pygame.draw.rect(screen,'#2B3A55',high_score_border_rect,2)

    def draw_score_rect(screen):
        score_bg_rect = pygame.Rect(20,10,100,25)
        high_score_bg_rect = pygame.Rect(140,10,150,25)
        pygame.draw.rect(screen,(28,32,38),score_bg_rect)
        pygame.draw.rect(screen,(28,32,38),high_score_bg_rect)
    
    # def draw_ui(screen):
    # # Score panel
    #     score_rect = pygame.Rect(10, 10, 300, 40)
    #     pygame.draw.rect(screen,  (25, 45, 55), score_rect, border_radius=8)
    #     pygame.draw.rect(screen, (60, 120, 140), score_rect, 2, border_radius=8)
        
    #     score_text = font.render(f"Score: {game.score}", True, (220, 220, 220))
    #     screen.blit(score_text, (20, 18))
        
    #     # High score
    #     high_score_text = font.render(f"High: {game.high_score}", True, (220, 220, 220))
    #     screen.blit(high_score_text, (170, 18))
        
    #     # Game mode
    #     mode_text = font.render(f"Mode: {game_mode}", True, (220, 220, 220))
    #     screen.blit(mode_text, (Width - mode_text.get_width() - 20, 18))



pygame.init()
pygame.mixer.init()
cell_size = 20
cell_numberx = 40
cell_numbery = 30
Width = 800
Height = 600
game_mode = ["easy","classic","normal","hard","insane"]

crunch = pygame.mixer.Sound("sfx_crunch.wav")
crunch.set_volume(0.20)
fail_sound = pygame.mixer.Sound("gameover.wav")
fail_sound.set_volume(0.25)
pygame.mixer.music.load("elevator_music.wav")
pygame.mixer.music.set_volume(0.15)   
pygame.mixer.music.play(-1, fade_ms=500) 

# Create screen FIRST
Rattle_icon = pygame.image.load('/Users/David/Documents/Alletruc/RattleGame/Rattle_icon.png')
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption('Eastern Diamond Back')
pygame.display.set_icon(Rattle_icon)

# THEN create game objects with screen
game = MAIN()  # Pass screen to MAIN
gameUI = GameUI()

clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 21, bold= True)
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_medium = pygame.font.SysFont("arial", 32, bold=True)

running = True
SCREEN_UPDATE = pygame.USEREVENT + 1
initial_ms, min_ms, step_ms = 150, 50, 10
pygame.time.set_timer(SCREEN_UPDATE, initial_ms)

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == SCREEN_UPDATE:
            game.update()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r and not game.game_active:
                game.restart()
                pygame.time.set_timer(SCREEN_UPDATE, game.initial_ms)
        if e.type == pygame.KEYDOWN and game.game_active:  
            if e.key == pygame.K_w:
                if game.snake.direction.y != 1 and game.snake.direction != pygame.Vector2(0,1):
                    game.snake.direction = pygame.Vector2(0, -1)
            if e.key == pygame.K_s:
                if game.snake.direction.y != -1 and game.snake.direction != pygame.Vector2(0,-1):
                    game.snake.direction = pygame.Vector2(0, 1)
            if e.key == pygame.K_a:
                if game.snake.direction.x != 1 and game.snake.direction != pygame.Vector2(1,0):
                    game.snake.direction = pygame.Vector2(-1, 0)
            if e.key == pygame.K_d:
                if game.snake.direction.x != -1 and game.snake.direction != pygame.Vector2(-1,0):
                    game.snake.direction = pygame.Vector2(1, 0)
    
    screen.fill((18,20,23))
    GameUI.draw_grid(screen)
    GameUI.draw_score_rect(screen)
    GameUI.draw_borders(screen)
    score = font.render(f'Score:{game.score}', True, "#5CF4FF",(28,32,38))
    high_score = font.render(f'High Score:{game.high_score}', True, "#5CF4FF",(28,32,38))
    score_rect = score.get_rect(topleft = (22,10))
    high_score_rect = high_score.get_rect(topleft = (142,10))
    screen.blit(score,score_rect)
    screen.blit(high_score,high_score_rect)
    GameUI.draw_borders(screen)
    game.draw_ellem()
    # GameUI.draw_ui(screen)
    pygame.display.update()
    clock.tick(60)
pygame.quit()
sys.exit()

