import pygame
import csv
import math
import time

pygame.init()

FPS = 240
clock = pygame.time.Clock()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#define game variables
ROWS = 15
COLUMNS = 40
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 7
current_tile = 0
level = 0
font = pygame.font.SysFont('Futura', 30)
xb = 0
yb = 0
time = 0
power = 0
angle = 0
launch = False
start = [100, 400]
g =[1, 9.8, 1.6, 8.9]
stroke = 0
win = 0

#define colours
HOTPINK = (255, 105, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Projectile Motion Game')

#loading images

#store backgrounds in a list

background = pygame.image.load(f'Images/leveleditorbackgroundnew{level}.png').convert_alpha()


img_list = [] #tile images
for i in range(33):
    img = pygame.image.load(f'Images/{i+1}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('Images/save.png').convert_alpha() #load and save button images
load_img = pygame.image.load('Images/load.png').convert_alpha()

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLUMNS
    world_data.append(r)

#functions from level editor
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x,y))

def draw_bg():
    screen.blit(background, ((0), 0))

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE, y * TILE_SIZE))
                

class ball(object):
    def __init__(self, xb, yb, radius, color): #xb is x position of ball
        self.xb = xb
        self.yb = yb
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (self.xb, self.yb), self.radius)
        pygame.draw.circle(screen, self.color, (self.xb, self.yb), self.radius - 1)

    @staticmethod
    def ball_path(startx, starty, power, angle, time):
        velx = math.cos(angle) * power
        vely = math.sin(angle) * power
        
        distx = velx * time
        disty = (vely * time) + (-(g[level] / 2) * (time)**2)

        newx = startx + distx
        newy = starty - disty

        return(newx, newy)

def draw_ball():
    golf_ball.draw(screen)

def draw_line():
    pygame.draw.line(screen, BLACK, line[0], line[1])

def find_angle(pos):
    try:
        angle = math.atan((golf_ball.yb - pos[1]) / (golf_ball.xb - pos[0]))
    except:
        angle = math.pi / 2
    
    if pos[1] < golf_ball.yb and pos[0] > golf_ball.xb:
        angle = abs(angle)
    elif pos[1] < golf_ball.yb and pos[0] < golf_ball.xb:
        angle = math.pi - angle
    elif pos[1] > golf_ball.yb and pos[0] < golf_ball.xb:
        angle = math.pi + abs(angle)
    elif pos[1] > golf_ball.yb and pos[0] > golf_ball.xb:
        angle = (math.pi * 2) - angle

    return angle


golf_ball = ball(start[0], start[1], 5, WHITE)
line = [(golf_ball.xb, golf_ball.yb), (golf_ball.xb, golf_ball.yb)]



run = True
while run == True:
    
    clock.tick(FPS)

    background = pygame.image.load(f'Images/leveleditorbackgroundnew{level}.png').convert_alpha()
    draw_bg()
    draw_world()
    draw_ball()
    draw_line()
    draw_text(f'Level: {level}', font, BLACK, 10, 30)
    

    #scale
    pygame.draw.line(screen, WHITE, (680, 520), (720, 520))
    pygame.draw.line(screen, WHITE, (680, 510), (680, 530))
    pygame.draw.line(screen, WHITE, (720, 510), (720, 530))
    draw_text('40m', font, WHITE, 680, 530)
    
    #get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0]) // TILE_SIZE
    y = (pos[1]) // TILE_SIZE
    
    line = [(golf_ball.xb, golf_ball.yb), pos]
    
    #to display angle and velocity on screen for player
    check_angle = find_angle(pos)
    check_power = math.sqrt((line[1][1] - line[0][1])**2 + (line[1][0] - line[0][0])**2) / 8

    
    draw_text(f'Velocity = {round(check_power, 2)} m/s', font, WHITE, 10, SCREEN_HEIGHT - 85)
    draw_text(f'Angle = {round(check_angle * 180 / math.pi, 2)} degrees', font, WHITE, 10, SCREEN_HEIGHT - 60)
    draw_text(f'Gravity = {g[level]} m/s/s', font, WHITE, 10, SCREEN_HEIGHT - 35)
    draw_text(f'Stroke: {stroke}', font, BLACK, 700, 30)

    #stopping mechanic for ball
    if launch:
        if golf_ball.yb < 600  and 0 <= golf_ball.xb <= 800:
            time += 0.05
            pos_ball = ball.ball_path(xb, yb, power, angle, time)
            golf_ball.xb = pos_ball[0]
            golf_ball.yb = pos_ball[1]
            if 0 < golf_ball.xb < 160 and golf_ball.yb > 400:
                launch = False
                golf_ball.yb = 400
            if 160 < golf_ball.xb < 240 and golf_ball.yb > 500:
                launch = False
                pygame.time.delay(1000)
                golf_ball.xb = start[0]
                golf_ball.yb = start[1]
            if 240 < golf_ball.xb < 280 and golf_ball.yb > 520:
                launch = False
                golf_ball.yb = 520
            if 280 < golf_ball.xb < 320 and golf_ball.yb > 520:
                if level == 2:
                    launch = False
                    win += 1
                    golf_ball.yb = 520
                else:
                    launch = False
                    golf_ball.yb = 520
            if 320 < golf_ball.xb < 360 and 400 < golf_ball.yb < 520:
                launch = False
                golf_ball.xb = 330
                golf_ball.yb -= 30
            if 360 < golf_ball.xb < 400 and golf_ball.yb > 380 - 0.5 * (golf_ball.xb - 360):
                launch = False
                golf_ball.yb = 380 - 0.5 * (golf_ball.xb -360)
            if 400 < golf_ball.xb < 440 and golf_ball.yb > 360:
                launch = False
                golf_ball.yb = 360
            if 440 < golf_ball.xb < 480 and golf_ball.yb > 360:
                if level == 3:
                    launch = False
                    win += 1
                    golf_ball.yb = 360
                else:
                    launch = False
                    golf_ball.yb = 360
            if 480 < golf_ball.xb < 520 and golf_ball.yb > 360:
                launch = False
                golf_ball.yb = 360
            if 520 < golf_ball.xb < 560 and golf_ball.yb > 400:
                launch = False
                golf_ball.yb = 400
            if 560 < golf_ball.xb < 600 and golf_ball.yb > 440:
                launch = False
                golf_ball.yb = 440
            if 600 < golf_ball.xb < 760 and golf_ball.yb > 480:
                launch = False
                golf_ball.yb = 480
            if 760 < golf_ball.xb < 800 and golf_ball.yb > 400:
                if level == 1:
                    launch = False
                    win += 1
                    golf_ball.yb = 400
                else:
                    launch = False
                    golf_ball.yb = 400
      
        else:
            launch = False
            pygame.time.delay(1000)
            golf_ball.xb = start[0]
            golf_ball.yb = start[1]

    
    #display text when target is hit
    if win == 1:
        draw_text(f'You won in {stroke} strokes! ', font, BLACK, SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2 - 75)
   
   

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                #level += 1
                if level < 3: #prevent crashing
                    golf_ball.xb = start[0]
                    golf_ball.yb = start[1]
                    stroke = 0
                    win = 0
                    level += 1
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)

            if event.key == pygame.K_DOWN:
                #level -= 1
                golf_ball.xb = start[0]
                golf_ball.yb = start[1]
                stroke = 0
                win = 0
                if level > 0: #prevent crashing
                    level -= 1 
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)  
           
            if event.key == pygame.K_SPACE:
                if launch == False:
                    launch = True
                    xb = golf_ball.xb
                    yb = golf_ball.yb
                    time = 0
                    power = math.sqrt((line[1][1] - line[0][1])**2 + (line[1][0] - line[0][0])**2) / 8
                    angle = find_angle(pos)
                    check_power = power
                    check_angle = angle
                    stroke += 1
                    win = 0
                    
    
    #testing
    #print(pos) 
    #print(line)
    #print(check_power)
    
   
    pygame.display.update()
pygame.quit()
