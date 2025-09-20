import pygame, sys, random, pygame.mixer

class FRUIT:
    def __init__(self):
        self.randomize()
        
    def draw_fruit(self):
        fruit_rect = pygame.Rect((self.pos.x * pixel),(self.pos.y * pixel), pixel, pixel)
        screen.blit(pommedor,fruit_rect)
        #create fruit with random x and y
        #and blit it
    def randomize(self):
        self.pos = pygame.Vector2(random.randint(0,pixel_number - 1), random.randint(0,pixel_number - 1))
    

class SNAKE:
    def __init__(self):
        self.body = [pygame.Vector2(5,10),pygame.Vector2(4,10),pygame.Vector2(3,10)]
        self.direction = pygame.Vector2(1,0)
        self.new_direction = self.direction
        self.new_block = False
    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(int(block.x * pixel), int(block.y * pixel), pixel, pixel)
            screen.blit(snakehead,snake_rect)
            
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0]+ self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0]+ self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

        
class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    def update(self):
        self.snake.move_snake()
        self.collision()
        self.fail()
    
    def draw_elenents(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()
    
    def collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
        
    def boundaries(self):
        if self.snake.body == pixel_number:
            pass

    def fail(self):
        if not 0<= self.snake.body[0].x <= pixel_number -1:
            self.game_over()
        if not 0<= self.snake.body[0].y <= pixel_number -1:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit() 
        sys.exit()

pygame.init()


pixel = 45
pixel_number = 19
screen = pygame.display.set_mode((pixel_number * pixel, pixel_number * pixel))
pygame.display.set_caption('Rattle.py')
clock = pygame.time.Clock()
pommedor = pygame.image.load('golden_apple.png').convert_alpha()
pommedor = pygame.transform.scale(pommedor, (45, 45))


snakehead = pygame.image.load('/Users/David/Documents/Alletruc/Rattle_Game/snakehead.png').convert()
snakehead = pygame.transform.scale(pommedor,(45,45))
snakebody = pygame.image.load('/Users/David/Documents/Alletruc/Rattle_Game/snakebody.png').convert()
snaketurn = pygame.image.load('/Users/David/Documents/Alletruc/Rattle_Game/snaketurn.png').convert()
snakeend = pygame.image.load('/Users/David/Documents/Alletruc/Rattle_Game/snakeend.png').convert()
snakeend2 = pygame.transform.rotate(snakeend,90)

game = GAME()
game.fruit.draw_fruit()
game.snake.draw_snake()


screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update,150)
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == screen_update:
            game.update()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                if game.snake.direction.y != 1:
                    game.snake.direction = pygame.Vector2(0,-1) 
            if e.key == pygame.K_a:
                if game.snake.direction.x != 1:
                    game.snake.direction = pygame.Vector2(-1,0)
            if e.key == pygame.K_s:
                if game.snake.direction.y != -1:
                    game.snake.direction = pygame.Vector2(0,1)
            if e.key == pygame.K_d:
                if game.snake.direction.x != -1:
                    game.snake.direction = pygame.Vector2(1,0)


    screen.fill('lightgreen')
    game.draw_elenents()
    game.fruit.draw_fruit()
    game.snake.draw_snake()

    pygame.display.update()
    pygame.display.flip()

pygame.quit(), sys.exit()

