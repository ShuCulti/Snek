import pygame, sys, random, pygame.mixer


class FRUIT:
    def __init__(self):
        self.randomize()
        
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * pixel), int(self.pos.y * pixel), pixel, pixel)
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

        self.snakehead = pygame.image.load('snakehead.png').convert()
        self.snakehead =  pygame.transform.scale(self.snakehead,(45,45))
        self.snakehead_up = pygame.transform.rotate(self.snakehead,-90)
        self.snakehead_down = pygame.transform.rotate(self.snakehead,90)
        self.snakehead_right = pygame.transform.rotate(self.snakehead,0)
        self.snakehead_left = pygame.transform.rotate(self.snakehead,180)

        self.snakebody = pygame.image.load('snakebody.png').convert()
        self.snakebody = pygame.transform.scale(self.snakebody,(45,45))
        self.snakebody_up = pygame.transform.rotate(self.snakebody,-90)
        self.snakebody_down = pygame.transform.rotate(self.snakebody,90)
        self.snakebody_right = pygame.transform.rotate(self.snakebody,0)
        self.snakebody_left = pygame.transform.rotate(self.snakebody,180)

        self.snaketurn = pygame.image.load('snaketurn.png').convert()
        self.snaketurn = pygame.transform.scale(self.snaketurn,(45,45))
        self.snaketurn_up = pygame.transform.rotate(self.snaketurn,-90)
        self.snaketurn_down = pygame.transform.rotate(self.snaketurn,90)
        self.snaketurn_right = pygame.transform.rotate(self.snaketurn,0)
        self.snaketurn_left = pygame.transform.rotate(self.snaketurn,180)

        self.snakeend = pygame.image.load('snakeend.png').convert()
        self.snakeend = pygame.transform.scale(self.snakeend,(45,45))
        self.snakeend_up = pygame.transform.rotate(self.snakeend,-90)
        self.snakeend_down = pygame.transform.rotate(self.snakeend,90)
        self.snakeend_right = pygame.transform.rotate(self.snakeend,0)
        self.snakeend_left = pygame.transform.rotate(self.snakeend,180)
        

    def draw_snake(self):
        self.update_snake()

        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(int(block.x * pixel), int(block.y * pixel), pixel, pixel)
            if index == 0:
                screen.blit(self.snakehead, block_rect)
            elif index == 1:
                screen.blit(self.snakebody, block_rect)
            elif index == len(self.body) - 1:
        # Last segment = Tail
                screen.blit(self.snakeend, block_rect)
            else: screen.blit(self.snakebody, block_rect)


            
    def update_snake(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == pygame.Vector2(-1,0): self.snakehead = self.snakehead_right
        if head_relation == pygame.Vector2(1,0): self.snakehead = self.snakehead_left
        if head_relation == pygame.Vector2(0,-1): self.snakehead = self.snakehead_up
        if head_relation == pygame.Vector2(0,1): self.snakehead = self.snakehead_down

        body_relation = self.body[2] - self.body[1]
        if body_relation == pygame.Vector2(-1,0): self.snakebody = self.snakebody_right
        if body_relation == pygame.Vector2(1,0): self.snakebody = self.snakebody_left
        if body_relation == pygame.Vector2(0,-1): self.snakebody = self.snakebody_down
        if body_relation == pygame.Vector2(0,1): self.snakebody = self.snakebody_up

        end_relation = self.body[-1] - self.body[-2]

        if end_relation == pygame.Vector2(-1,0): self.snakeend = self.snakeend_right
        if end_relation == pygame.Vector2(1,0): self.snakeend = self.snakeend_left
        if end_relation == pygame.Vector2(0,-1): self.snakeend = self.snakeend_up
        if end_relation == pygame.Vector2(0,1): self.snakeend = self.snakeend_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[0:]
            body_copy.insert(0,body_copy[0]+ self.direction)
            self.body = body_copy[0:]
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


snakehead = pygame.image.load('snakehead.png').convert()
snakehead = pygame.transform.scale(snakehead,(45,45))
snakebody = pygame.image.load('snakebody.png').convert()
snakebody = pygame.transform.scale(snakehead,(45,45))
snaketurn = pygame.image.load('snaketurn.png').convert()
snaketurn = pygame.transform.scale(snakehead,(45,45))
snakeend = pygame.image.load('snakeend.png').convert()
snakeend = pygame.transform.scale(snakehead,(45,45))
snakeend2 = pygame.transform.rotate(snakeend,90)

snakehead = pygame.transform.smoothscale(snakehead,(pixel,pixel))
snakebody = pygame.transform.smoothscale(snakebody,(pixel,pixel))
snaketurn = pygame.transform.smoothscale(snaketurn,(pixel,pixel))
snakeend = pygame.transform.smoothscale(snakeend,(pixel,pixel))

background = pygame.image.load('SpaceFond.gif')
background = pygame.transform.scale(background,(855,855))

game = GAME()
game.fruit.draw_fruit()
game.snake.draw_snake()

score = 0
font = pygame.font.SysFont('Arial',24)  
font1 = pygame.font.SysFont('Arial',72)
score_surface = font.render(f'Score:{score}',True, (255,255,255))



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
            if e.key == pygame.K_UP:
                if game.snake.direction.y != 1:
                    game.snake.direction = pygame.Vector2(0,-1)  
            if e.key == pygame.K_LEFT:
                if game.snake.direction.x != 1:
                    game.snake.direction = pygame.Vector2(-1,0)
            if e.key == pygame.K_DOWN:
                if game.snake.direction.y != -1:
                    game.snake.direction = pygame.Vector2(0,1)
            if e.key == pygame.K_RIGHT:
                if game.snake.direction.x != -1:
                    game.snake.direction = pygame.Vector2(1,0)                 


    screen.fill('lightgreen')
    screen.blit(background,(0, 0))
    screen.blit(score_surface,(10,10))
    game.draw_elenents()
    game.fruit.draw_fruit()
    game.snake.draw_snake()
    pygame.display.update()
    pygame.display.flip()

pygame.quit(), sys.exit()

