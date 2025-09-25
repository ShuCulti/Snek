import pygame, random, sys

class FOOD:
    def __init__(self):
        self.randomize()

    def draw_food(self):
        food_rect = pygame.Rect(self.pos.x * cell_size,self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen,'red',food_rect)
        pygame.draw.rect(screen,'black',food_rect,2)

    def randomize(self):
        self.pos = pygame.Vector2(random.randint(0,cell_numbersx -1), random.randint(0, cell_numbersy -1))

class SNAKE:
    def __init__(self):
        self.body = [pygame.Vector2(7,10), pygame.Vector2(6,10), pygame.Vector2(5,10)]
        self.direction = pygame.Vector2(1,0)
    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(block.x * cell_size,block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen,'forestgreen',snake_rect)
            pygame.draw.rect(screen,'black',snake_rect,2)

    def move(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, self.body[0] + self.direction)
        self.body = body_copy[:]

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()
        
cell_size = 20
cell_numbersx = 40
cell_numbersy = 30
Width = 800
Height = 600
pygame.init()
screen = pygame.display.set_mode((Width,Height))
running = True

food = FOOD()
snake = SNAKE()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == SCREEN_UPDATE:
            snake.move()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                snake.direction = pygame.Vector2(0,-1)
            if e.key == pygame.K_s:
                snake.direction = pygame.Vector2(0,1)
            if e.key == pygame.K_a:
                snake.direction = pygame.Vector2(-1,0)
            if e.key == pygame.K_d:
                snake.direction = pygame.Vector2(1,0)
    screen.fill('pink')
    food.draw_food()
    snake.draw_snake()
    pygame.display.update()
pygame.quit()
sys.exit()