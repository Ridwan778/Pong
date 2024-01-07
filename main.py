import pygame
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("PONG")
winner = 0;

#define backgorund colors
screen_bg = (0,0,0)
#define scoreboard
sb_size = 35
computer_score = 0
player_score = 0
font = pygame.font.SysFont('arial',15)

live_ball = False

def draw_board():
    screen.fill(screen_bg)
    pygame.draw.line(screen, (255,255,255), (0,sb_size), (WINDOW_WIDTH,sb_size))

def draw_text(text, font, color, x, y):
    #convert to image as pygame doesn't let me print directly
    img = font.render(text, True, color)
    screen.blit(img,(x,y))#putting image onto a screen
#define scoreboard
sb_size = 35

# create paddles
class paddle():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = Rect(self.x,self.y, 20, 100)
        self.speed = 6

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top >= sb_size:
            self.rect.move_ip(0,-1*self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.move_ip(0,1*self.speed)

    def ai(self):
        #moving down
        if self.rect.centery < ball.rect.top and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.move_ip(0,self.speed)
        #moving up
        elif self.rect.centery > ball.rect.bottom and self.rect.top > sb_size:
            self.rect.move_ip(0,-1*self.speed)

    def draw(self):
        pygame.draw.rect(screen,(255,255,255),self.rect)

class gameBall():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = Rect(self.x,self.y, 2*self.ball_rad, 2*self.ball_rad)
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0 #1 player scored, -1 computer scored

    def draw(self):
        pygame.draw.circle(screen, (255,255,255), ((self.rect.x + self.ball_rad), (self.rect.y + self.ball_rad)), self.ball_rad)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        #collision detection
        if self.rect.top < sb_size:
            self.speed_y *= -1
        if self.rect.bottom > WINDOW_HEIGHT:
            self.speed_y *= -1

        if self.rect.colliderect(player_paddle) or self.rect.colliderect(computer_paddle):
            self.speed_x *= -1


        if self.rect.left < 0:
            self.winner = 1
        if self.rect.right > WINDOW_WIDTH:
            self.winner = -1

        return self.winner

    def reset(self,x,y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = Rect(self.x, self.y, 2 * self.ball_rad, 2 * self.ball_rad)
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0  # 1 player scored, -1 computer scored


player_paddle = paddle(WINDOW_WIDTH- 40, WINDOW_HEIGHT//2)
computer_paddle = paddle(20, WINDOW_HEIGHT//2)

ball = gameBall(WINDOW_WIDTH - 60, WINDOW_HEIGHT // 2 + 50)

run = True

while run:
    clock.tick(60)
    draw_board()
    draw_text('Computer: ' + str(computer_score), font, (255,255,255),20,15)
    draw_text('Player: ' + str(player_score), font, (255, 255, 255), (WINDOW_WIDTH//2+20), 15)

    #paddles
    player_paddle.draw()
    computer_paddle.draw()
    if live_ball == True:
        winner = ball.move()
        if winner ==0:
            player_paddle.move()
            computer_paddle.ai()
            ball.draw()
        else:
            live_ball = False
            if winner == 1:
                player_score += 1
            elif winner == -1:
                computer_score += 1

    #print(winner)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(WINDOW_WIDTH - 60, WINDOW_HEIGHT//2 +50)

    pygame.display.update()

pygame.quit()