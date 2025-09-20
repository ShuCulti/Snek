import pygame, sys, random, math, time

pygame.init()
pygame.mixer.init()

Width, Height = 800, 600
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption('Rattle')

font_large = pygame.font.SysFont('Arial,', 48, bold= False)
font_medium = pygame.font.SysFont('Arial',32, bold = False)
font_small = pygame.font.SysFont('Arial', 24)

score = 0
high_score = 0
game_mode = "classic"

cell_size = 20
grid_width = Width // cell_size
grid_height = Height // cell_size
grid_color = (30,50,60)
fps = pygame.time.Clock()

class Food:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.rect.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        leaf_rect = pygame.Rect(fruit_rect.x+10,fruit_rect.y-3, 6, 3)
        stem_rect = pygame.Rect(fruit_rect.x+8,fruit_rect.y-6, 3, 6)
        pygame.draw.rect(screen,'red',fruit_rect)
        pygame.draw.rect(screen,'black',fruit_rect,2)
        pygame.draw.rect(screen,'brown',stem_rect)
        pygame.draw.rect(screen,'green',leaf_rect)
    def randomize(self):
        self.pos = pygame.Vector2(random.randint(0,grid_width -1),random.randint(0,grid_height -1))

class Snake:
    def __init__(self):
        self.body = [pygame.Vector2(5,10),pygame.Vector2(6,10),pygame.Vector2(7,10)]
        self.snake_head= self.body[0]
        self.direction = pygame.Vector2(1,0)
    

    def draw_snake(self):
        for block in self.body:
            fruit_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            self.snake_head = self.body[0]
            snake_head_rect = pygame.Rect(self.snake_head.x * cell_size, self.snake_head.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, 'lightblue', fruit_rect)
            pygame.draw.rect(screen, 'midnightblue', fruit_rect,2)
            pygame.draw.rect(screen,'lightblue',snake_head_rect)
            pygame.draw.rect(screen,'black',snake_head_rect,2)
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
        body_copy = self.body[:-1]
        body_copy.insert(0,self.body[0] + self.direction)    
        self.body = body_copy[:]
    
class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
    def update(self):
        self.snake.move()
        self.collision()
    
    def draw_ellem(self):
        self.food.draw_fruit()
        self.snake.draw_snake()
    def collision(self):
        if self.snake.body[0] == self.food.pos:
            self.food.randomize()

class GameUI:
    def draw_grid(screen):
        for x in range(0,Width,cell_size):
            pygame.draw.line(screen,(grid_color),(x,0),(x,Height))
        for y in range(0,Height,cell_size):
            pygame.draw.line(screen,(grid_color),(0,y),(Width,y))



game = MAIN()
gameUI = GameUI()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)



running = True
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
    screen.fill((140,180,200))
    game.draw_ellem()
    GameUI.draw_grid(screen)
    pygame.display.update()
    fps.tick(60)
pygame.quit
sys.exit



