import pygame,sys,random,math

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
    
    def draw(self):
        # Create a pulsing effect
        self.color = (255,0,255)
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
        
        rect = pygame.Rect((self.pos[0] * cell_size, self.pos[1] * cell_size), (cell_size, cell_size))
        pygame.draw.rect(screen, pulse_color, rect)
        pygame.draw.rect(screen, (100, 0, 0), rect, 1)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)

class SNAKE:
    def __init__(self):
        self.body = [pygame.Vector2(5,10), pygame.Vector2(6,10), pygame.Vector2(7,10)]
        self.direction = pygame.Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            self.snake_head = self.body[0]
            snake_head_rect = pygame.Rect(self.snake_head.x * cell_size, self.snake_head.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, 'lightblue', snake_rect)
            pygame.draw.rect(screen, 'midnightblue', snake_rect,3)
            pygame.draw.rect(screen,'lightblue',snake_head_rect)
            pygame.draw.rect(screen,'black',snake_head_rect,3)
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
    
    def add_block(self):
        self.new_block = True
    
    def reset(self):
        if self.body[0] == self.body[0:]:
            pygame.quit()
            sys.exit()

class MAIN:

    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.snake = SNAKE()
        self.food = FOOD()
        self.reset()


    def update(self):
        self.snake.move()
        self.collision()
        self.reset()

    def draw_ellem(self):
        self.snake.draw_snake()
        self.food.draw_fruit()
        self.food.draw()

    def collision(self):
        if self.snake.body[0] == self.food.pos:
            self.score += 5
            self.high_score +=5
            self.food.randomize()
            self.snake.add_block()
    
    def reset(self):
        if self.snake.body[0] == self.snake.body[0:]:
            self.game_over()

    def game_over(self):
        overlay = pygame.Surface((Width, Height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        game_over_text = font_large.render("GAME OVER", True, (220, 50, 50))
        screen.blit(game_over_text, (Width//2 - game_over_text.get_width()//2, Height//2 - 50))
        
        restart_text = font_medium.render("Press R to Restart", True, (220, 220, 220))
        screen.blit(restart_text, (Width//2 - restart_text.get_width()//2, Height//2 + 20))
            


class GameUI:
    def draw_grid(screen):
        for x in range(0,Width,cell_size):
            pygame.draw.line(screen,'brown', (x,0), (x,Height))
        for y in range(0,Height,cell_size):
            pygame.draw.line(screen,'brown',(0,y), (Width,y))
    def draw_borders(screen):
        score_border_rect = pygame.Rect(20,10,100,25)
        high_score_border_rect = pygame.Rect(140,10,150,25)
        pygame.draw.rect(screen,'black',score_border_rect,2)
        pygame.draw.rect(screen,'black',high_score_border_rect,2)

    def draw_score_rect(screen):
        score_bg_rect = pygame.Rect(20,10,100,25)
        high_score_bg_rect = pygame.Rect(140,10,150,25)
        pygame.draw.rect(screen,'crimson',score_bg_rect)
        pygame.draw.rect(screen,'crimson',high_score_bg_rect)
    
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




cell_size = 20
cell_numberx = 40
cell_numbery = 30
Width = 800
Height = 600
game_mode = 'classic'

pygame.init()
game = MAIN()
gameUI = GameUI()

Rattle_icon = pygame.image.load('Rattle_icon.png')
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption('Eastern Diamond Back')
pygame.display.set_icon(Rattle_icon)
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 21)
font_large = pygame.font.SysFont("arial", 48, bold=True)
font_medium = pygame.font.SysFont("arial", 32, bold=True)

running = True

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)


while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == SCREEN_UPDATE:
            game.update()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                if game.snake.direction != pygame.Vector2(0,1):
                    game.snake.direction = pygame.Vector2(0,-1)
            if e.key == pygame.K_s:
                if game.snake.direction != pygame.Vector2(0,-1):
                    game.snake.direction = pygame.Vector2(0,1)
            if e.key == pygame.K_a:
                if game.snake.direction != pygame.Vector2(1,0):
                    game.snake.direction = pygame.Vector2(-1,0)
            if e.key == pygame.K_d:
                if game.snake.direction != pygame.Vector2(-1,0):
                    game.snake.direction = pygame.Vector2(1,0)
            if e.key == pygame.K_r:
                    pass

    screen.fill('lightpink')
    game.draw_ellem()
    GameUI.draw_grid(screen)
    GameUI.draw_score_rect(screen)
    score = font.render(f'Score:{game.score}', True, (0,0,0),'crimson')
    high_score = font.render(f'High Score:{game.high_score}', True, (0,0,0),'crimson')
    score_rect = score.get_rect(topleft = (20,10))
    high_score_rect = high_score.get_rect(topleft = (140,10))
    screen.blit(score,score_rect)
    screen.blit(high_score,high_score_rect)
    # GameUI.draw_ui(screen)
    GameUI.draw_borders(screen)
    pygame.display.update()
    clock.tick(60)
pygame.quit()
sys.exit()

