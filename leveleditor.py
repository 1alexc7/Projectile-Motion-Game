import pygame
import button
import csv

pygame.init()

FPS = 240
clock = pygame.time.Clock()

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
#screen margins
SIDE_MARGIN = 300
LOWER_MARGIN = 100

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

#define game variables
ROWS = 15
COLUMNS = 40
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 7
current_tile = 0
level = 0
font = pygame.font.SysFont('Futura', 30)

#define colours
HOTPINK = (255, 105, 180)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLUMNS
    world_data.append(r)

#function for outputting text on screen
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x,y))


#load images
background = pygame.image.load('leveleditorbackgroundnew1.png').convert_alpha()
#img1 = pygame.image.load('1.png').convert_alpha()
#img2 = pygame.image.load('2.png').convert_alpha()
#img3 = pygame.image.load('3.png').convert_alpha()
#img4 = pygame.image.load('4.png').convert_alpha()
#img5 = pygame.image.load('5.png').convert_alpha()
#img6 = pygame.image.load('6.png').convert_alpha()
#img7 = pygame.image.load('7.png').convert_alpha()

#store tiles in a list
img_list = []
for i in range(33):
    img = pygame.image.load(f'{i+1}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('save.png').convert_alpha()
load_img = pygame.image.load('load.png').convert_alpha()

#function to draw background'
def draw_bg():
    screen.fill(HOTPINK)
    screen.blit(background, (0, 0))

#function to draw grids
def draw_grid():
#vertical lines                           #start pos of line    #end pos of line    #x pos of line stays the same
    for v in range(COLUMNS + 1):
        pygame.draw.line(screen, WHITE, (v * TILE_SIZE, 0), (v * TILE_SIZE, SCREEN_HEIGHT))
#horizontal lines
    for h in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, h * TILE_SIZE), (SCREEN_WIDTH, h * TILE_SIZE))

#function to draw world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE, y * TILE_SIZE))


save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 80, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 80, load_img, 1)

#creating buttons and making a list for it
button_list = []
button_column = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + 35 + (50 * button_column), 50 * button_row + 50, img_list[i], 0.75)
    button_list.append(tile_button)
    button_column += 1
    if button_column == 5:  
        button_row += 1
        button_column = 0

run = True
while run == True:
    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press up or down to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    clock.tick(FPS)

    #save and load data
    if save_button.draw(screen):
        #save level data
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)
        
    if load_button.draw(screen):
        #load level data
    
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)


    #draw tile panel and tiles
    pygame.draw.rect(screen, HOTPINK, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    #choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    
    pygame.draw.rect(screen, BLACK, button_list[current_tile].rect, 3)

 
    
    #adding new tiles on screen
    #to do this get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0]) // TILE_SIZE
    y = (pos[1]) // TILE_SIZE
 

    #check that co-ords are in the image background
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1
    
    

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        #checking for keyboard presses
        if event.type == pygame.KEYDOWN:
           
            if event.key == pygame.K_UP:
                level += 1

            if event.key == pygame.K_DOWN:
                level -= 1


    pygame.display.update()
pygame.quit()
    

