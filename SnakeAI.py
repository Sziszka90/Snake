import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import neat
import time
import random
pygame.font.init()

WIN_WIDTH = 1200
WIN_HEIGHT = 900

BACKGROUND_IMG = pygame.transform.scale(pygame.image.load("background.png"), (1200, 900))

SNAKE_PART_IMG = pygame.transform.scale(pygame.image.load("snake_part.png"), (40, 40))
snakePartMask = pygame.mask.from_surface(SNAKE_PART_IMG)
snakePartRect = SNAKE_PART_IMG.get_rect()
centerSnakePartsX = WIN_WIDTH - snakePartRect.center[0]
centerSnakePartsY = WIN_HEIGHT - snakePartRect.center[0]

SNAKE_HEAD_IMG = pygame.transform.scale(pygame.image.load("snake_head.png"), (40, 40))
snakeHeadMask = pygame.mask.from_surface(SNAKE_HEAD_IMG)
snakeHeadRect = SNAKE_HEAD_IMG.get_rect()
centerHeadX = WIN_WIDTH - snakeHeadRect.center[0]
centerHeadY = WIN_HEIGHT - snakeHeadRect.center[1]

APPLE_IMG = pygame.transform.scale(pygame.image.load("apple.png"), (40, 40))
appleMask = pygame.mask.from_surface(APPLE_IMG)
appleRect = APPLE_IMG.get_rect()
centerAppleX = WIN_WIDTH - appleRect.center[0]
centerAppleY = WIN_HEIGHT - appleRect.center[1]

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Snake:
    def __init__(self):
        self.x_head = 0
        self.y_head = 0
        self.x_speed = 0
        self.y_speed = 0
        self.x_parts = []
        self.y_parts = []
        self.currentMove = 'DOWN' 
        self.snakeHead = pygame.transform.rotate(SNAKE_HEAD_IMG,0) 

    def move(self, action):
        self.action = action

        if(self.action == 'LEFT' and self.currentMove!='RIGHT'): # move left
            if ( self.currentMove == 'UP' ):
                self.snakeHead = pygame.transform.rotate(self.snakeHead, 90) 
            elif ( self.currentMove == 'DOWN' ):
                self.snakeHead = pygame.transform.rotate(self.snakeHead, -90) 

            self.x_speed = -30
            self.y_speed = 0
            self.currentMove = 'LEFT'

        elif(self.action == 'RIGHT'  and self.currentMove!='LEFT'): # move right           
            if ( self.currentMove == 'UP' ):
                self.snakeHead = pygame.transform.rotate(self.snakeHead, -90) 
            elif ( self.currentMove == 'DOWN' ):
                self.snakeHead = pygame.transform.rotate(self.snakeHead, 90) 

            self.x_speed = 30
            self.y_speed = 0
            self.currentMove = 'RIGHT'

        elif(self.action == 'UP' and self.currentMove!='DOWN'): # move up          
            if ( self.currentMove =='RIGHT' ):
                self.snakeHead = pygame.transform.rotate(self.snakeHead, 90) 
            elif ( self.currentMove == 'LEFT' ):
                self.snakeHead = pygame.transform.rotate(self.snakeHead, -90) 

            self.x_speed = 0
            self.y_speed = -30
            self.currentMove = 'UP'

        elif(self.action == 'DOWN' and self.currentMove!='UP'): # move down
            if ( self.currentMove == 'RIGHT' ):
                self.snakeHead = pygame.transform.rotate(self.snakeHead, -90) 
            elif ( self.currentMove == 'LEFT' ):
                self.snakeHead = pygame.transform.rotate(self.snakeHead, 90) 

            self.x_speed = 0
            self.y_speed = 30
            self.currentMove = 'DOWN'

    def draw(self,win):
        if len(self.x_parts) > 0 and len(self.y_parts) > 0:
            for i in range(len(self.x_parts)-1,-1,-1):
                if ( i == 0 ):
                    self.x_parts[i] = self.x_head
                else:
                    self.x_parts[i] = self.x_parts[i-1]

            for i in range(len(self.y_parts)-1,-1,-1):
                if ( i == 0 ):
                        self.y_parts[i] = self.y_head
                else:
                    self.y_parts[i] = self.y_parts[i-1]
                
            for i in range(len(self.x_parts)):
                win.blit(SNAKE_PART_IMG, (self.x_parts[i], self.y_parts[i]))

        self.x_head += self.x_speed
        self.y_head += self.y_speed
            
        win.blit(self.snakeHead, (self.x_head, self.y_head))
       

    def catch(self, applePosX, applePosY):
        result = appleMask.overlap(snakeHeadMask, (applePosX-self.x_head, applePosY-self.y_head))
        if(result):
            self.x_parts.append(self.x_head+50)
            self.y_parts.append(self.y_head+50)
        return result

    def collosion(self):
        if self.x_head < 0 or self.x_head > 1200 or self.y_head < 0 or self.y_head > 900:
            return False
        for i in range(len(self.x_parts)-1):
            if(snakePartMask.overlap(snakeHeadMask,(self.x_head-self.x_parts[i+1],self.y_head-self.y_parts[i+1]))):
                return False
        return True

class Apple:
    def create(self, snakeHeadPosX, snakeHeadPosY):
        self.applePosX = random.randrange(1, 1170)
        self.applePosY = random.randrange(1, 870)

        while(appleMask.overlap(snakePartMask, (self.applePosX-snakeHeadPosX, self.applePosX-snakeHeadPosX))):
            self.applePosX = random.randrange(1, 1170)
            self.applePosY = random.randrange(1, 870)

    def draw(self,win):
        win.blit(APPLE_IMG, (self.applePosX, self.applePosY))


def draw_window(win, apple, snake):
    win.blit(BACKGROUND_IMG,(0,0))
    snake.draw(win)
    apple.draw(win)
    pygame.display.update()
    
def main():
    run = True
    snake = Snake()
    apple = Apple()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    apple.create(snake.x_head,snake.y_head)
    action = ''

    while run:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        if pygame.key.get_pressed()[pygame.K_RIGHT] == True:
            action = 'RIGHT'
        if pygame.key.get_pressed()[pygame.K_LEFT] == True:
            action = 'LEFT'
        if pygame.key.get_pressed()[pygame.K_UP] == True:
            action = 'UP'
        if pygame.key.get_pressed()[pygame.K_DOWN] == True:
            action = 'DOWN'

        snake.move(action)

        if(snake.catch(apple.applePosX,apple.applePosY)):
            apple.create(snake.x_head, snake.y_head)

        draw_window(win,apple,snake)

        run = snake.collosion()


main()
                
   