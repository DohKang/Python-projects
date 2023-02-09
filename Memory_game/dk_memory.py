import pygame
from random import *

#set up a start screen

def setup(level):
    global time_limit
    #Counting down time before we hide numbers
    time_limit = 5 - (level // 3)
    time_limit = max(time_limit, 2) 
    #how many number shows up this round
    numbers = 5 + (level // 2)
    #Let's draw a grid
    draw_grid(numbers)

def draw_grid(numbers):
    #how many rows
    rows = 5
    #how many columns
    cols = 9

    #each grid size
    grid_size = 130
    #give padding to left
    left_margin = 55
    #give padding to top
    top_margin = 20

    #set up grid
    grid = [[0 for col in range(cols)] for row in range(rows) ]

    number = 1
    #picking random square to put numbers in
    #we are looping till i hits the highest number 
    while number <= numbers:
        row_idx = randrange(0, rows)
        col_idx = randrange(0, cols)
        #if randomly selected square is 0, we put number in
        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number
            number += 1

            #get a center position of each grid that contains number

            button_x_pos = left_margin + (col_idx * grid_size) + (grid_size / 2)
            button_y_pos = top_margin + (row_idx * grid_size) + (grid_size / 2)

            #set button size 110, 110
            button = pygame.Rect(0, 0, 110 , 110)
            #get each button center point 
            button.center = (button_x_pos, button_y_pos)
            #add button into a list
            buttons_list.append(button)

def start_screen():
    #draw a big rectangle to click 
    pygame.draw.rect(screen, PURPLE, start_button)

    #add text inside of that rectangle

    text = start_font.render(f"Click me to start level  {level}", True, WHITE)
    text_rect = text.get_rect(center = (screen_width / 2 , screen_height / 2))
    
    #draw the text
    screen.blit(text, text_rect)

def game_screen():
    global hidden, time_limit
    #if number steal appears
    if not hidden:
        #check how much time passed
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        ramaining_time(time_limit - int(elapsed_time)) # show how much time left to user
        #if time passes more than limit we set
        if time_limit - int(elapsed_time) <= 0:
            #hide numbers
            hidden = True
    #use list to draw each square from grid to screen
    for idx, rect in enumerate(buttons_list, start=1):
        if hidden:
            pygame.draw.circle(screen, WHITE, rect.center, 60, 5)
        #show numbers in order
        else:
            pygame.draw.circle(screen, WHITE, rect.center, 60, 5)
            text = game_font.render(str(idx), True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

#check whether user clicked start rectangle or not
def check_pos(mouse_pos):
    global start, level, hidden, start_ticks
    #check user clicks click me button or not
    if start:
        #check user is clicking number correctly
        for button in buttons_list:
            if button.collidepoint(mouse_pos):
                #if user hit first index in the list
                if button == buttons_list[0]:
                    if not hidden:
                        hidden = True
                    #delete first index in the list
                    del buttons_list[0]
                else:
                    #if user clicked number not in order
                    game_over()
        if len(buttons_list) == 0:
            start = False
            level += 1
            hidden = False
            setup(level)

    elif start_button.collidepoint(mouse_pos):
        start = True
        #when we start the game. Ticking starts, too.
        start_ticks = pygame.time.get_ticks()

#game over
def game_over():
    global running
    #stop looping
    running = False
    #fill screen with black
    screen.fill(BLACK)
    #show text.
    text = start_font.render(f"Thank you for playing DK's Memory Game, Your reached Lv {level} ", True, PURPLE)
    text_rect = text.get_rect(center = (screen_width /2 , screen_height / 2))
    screen.blit(text, text_rect)

#show remaining time before words hidden
def ramaining_time(time):
    text_timer = timer_font.render(f"Time : {time}", True, WHITE)
    screen.blit(text_timer, (10, 10))



#basic set up
pygame.init()
#title of the game
pygame.display.set_caption("DK's Memory Game")
#screen size
screen_width, screen_height = 1280, 720
#set up screen
screen = pygame.display.set_mode((screen_width, screen_height))


#Color
WHITE = "#FFFFFF"
BLUE = "#1B80AB"
PURPLE = "#6A0DAD"
BLACK = "#000000"
YELLOW = "#DCF630"
GRAY = "#808080"
#font
start_font = pygame.font.SysFont("Gothic", 35, True, True)
game_font = pygame.font.SysFont("Gothic", 120, True, True)
timer_font = pygame.font.SysFont("TIMES ROMAN", 30, True, True)
#start button
start_button = pygame.Rect(screen_width / 3 - 70, screen_height / 3, 550, 250)

#Is started?
start = False

#game variables
level = 1
time_limit = None
buttons_list = []
hidden = False
start_ticks = None

setup(level)
#while playing
running = True
while running:
    mouse_pos = None
    #if user cliked close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
    
    screen.fill(BLACK)
    
    # if start is True, show game screen
    if start:
        game_screen()
    # if start is False, show start screen
    else:
        start_screen()
    # get mouse position and check whether person hit click start box or not
    if mouse_pos:
        check_pos(mouse_pos)
    
    #always update display
    pygame.display.update()

#before quit the game, give some delay to read letters
pygame.time.delay(4000) 

#quit the game
pygame.quit()
