import math
import os
import pygame


#claw class
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image #temp
        self.rect = image.get_rect(center=position)
        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

        #claw direction
        self.direction = LEFT 
        self.angle_speed = 2.5 #claw rotation speed
        self.angle = 10 #claw max angle set. (10, 180-10)

    #move angle based on keyboard
    def update(self, to_x):
        if self.direction == LEFT: 
            self.angle += self.angle_speed 
        elif self.direction == RIGHT:
            self.angle -= self.angle_speed

        #determine claw direction {right or left}
        if self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT)
        elif self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)
        
        #move claw to x pos
        self.offset.x += to_x
        self.rotate() #roate images

    def set_direction(self, direction):
        self.direction = direction

    def rotate(self):
        #image rotation
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1) 
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center= self.position+offset_rotated)
        # pygame.draw.rect(screen, RED, self.rect, 1) # can draw rectangle line of claw image changes

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        # pygame.draw.circle(screen, RED, self.position, 3) 
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5)

    def set_init_state(self):
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT

#doll Class
class doll(pygame.sprite.Sprite):
    def __init__(self, image, position, price, speed):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center = position)
        self.price = price
        self.speed = speed
    
    #redirect claw position to a center of doll
    def set_position(self, position, angle):
        r = self.rect.size[0] // 2 
        rad_angle = math.radians(angle) # 180 is 3.14
        to_x = r * math.cos(rad_angle) #bottom of triangle
        to_y = r * math.sin(rad_angle) #height of triangle
        self.rect.center = (position[0] + to_x, position[1] + to_y)

####Functions
#set up doll in the game
def setup_doll():
    #cat
    doll_group.add(doll(doll_images[0], (300, 325), doll_PS[0][0], doll_PS[0][1]))
    doll_group.add(doll(doll_images[0], (1125, 520), doll_PS[0][0], doll_PS[0][1])) 
    doll_group.add(doll(doll_images[0], (800, 350), doll_PS[0][0], doll_PS[0][1]))
    doll_group.add(doll(doll_images[0], (950, 280), doll_PS[0][0], doll_PS[0][1]))
    doll_group.add(doll(doll_images[0], (475, 500), doll_PS[0][0], doll_PS[0][1]))
    #princess
    doll_group.add(doll(doll_images[1], (150, 225),doll_PS[1][0], doll_PS[1][1]))
    doll_group.add(doll(doll_images[1], (620, 480), doll_PS[1][0], doll_PS[1][1]))
    doll_group.add(doll(doll_images[1], (1150, 400), doll_PS[1][0], doll_PS[1][1]))
    #elephant
    doll_group.add(doll(doll_images[2], (320, 500), doll_PS[2][0], doll_PS[2][1]))
    doll_group.add(doll(doll_images[2], (1100, 250), doll_PS[2][0], doll_PS[2][1]))
    doll_group.add(doll(doll_images[2], (940, 450), doll_PS[2][0], doll_PS[2][1]))
    doll_group.add(doll(doll_images[2], (150, 375), doll_PS[2][0], doll_PS[2][1]))
    #goat
    doll_group.add(doll(doll_images[3], (450, 350), doll_PS[3][0], doll_PS[3][1]))
    doll_group.add(doll(doll_images[3], (1065, 435), doll_PS[3][0], doll_PS[3][1]))
    doll_group.add(doll(doll_images[3], (150, 565), doll_PS[3][0], doll_PS[3][1]))

#if doll came all the way back, we add it to the score
def score_update(score):
    global curr_score
    curr_score += score

#render score board in the game
def score():
    txt_curr_score = game_font.render(f"Current Score : {curr_score:,}", True, BLACK)
    screen.blit(txt_curr_score, (50, 20))
    txt_goal_score = game_font.render(f"Goal Score: {goal_score:,}", True, BLACK)
    screen.blit(txt_goal_score, (50, 50))

#redner game over text in the game
def game_over(game_result):
    global running
    screen.fill(BLACK)
    msg = ending_font.render(game_result, True, YELLOW)
    msg_rect = msg.get_rect(center = (screen_width/2, screen_height/2 - 50))
    thank_msg = game_font.render("Thank you for playing DK-Game. Have a great day!", True, YELLOW)
    screen.blit(thank_msg, ((screen_width /4)  , screen_height * 2/3 - 100))
    screen.blit(msg, msg_rect)
    pygame.display.update()
    pygame.time.delay(2000)

#calculate elapsed time and time limits. and if out of time- > go to game over function
def timer_calculate():
    global running, game_result
    time_limit = 50
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time: {}".format(int(time_limit - elapsed_time)), True, BLACK)
    screen.blit(timer, (1100, 25))
    if time_limit - elapsed_time <= 0:
        running = False
        if curr_score >= goal_score:
            game_result = "Mission Complete"
        else:
            game_result = "Out of time"
        game_over(game_result)

####PYGAME INIT
pygame.init()
#screen setup
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")
#FPS
clock = pygame.time.Clock()

####Images
#image path
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")
####Images
#background
background = pygame.image.load(os.path.join(image_path, "background.png"))

#doll images
doll_images = [
    pygame.image.load(os.path.join(image_path, "cat.png")).convert_alpha(),
    pygame.image.load(os.path.join(image_path, "princess.png")).convert_alpha(),
    pygame.image.load(os.path.join(image_path, "elephant.png")).convert_alpha(),
    pygame.image.load(os.path.join(image_path, "goat.png")).convert_alpha()]
#claw image
claw_image = pygame.image.load(os.path.join(image_path, "claw.png")).convert_alpha()

#each doll's value, weight = how fast it comes back
doll_PS = ((100, 7),(300,5),(10,3),(550,9))

#set claw x +- 40 from the center point dot
default_offset_x_claw = 40 
LEFT = -1 #clas is heading left
STOP = 0  # when mouse is clicked it stops its move and stretch out.
RIGHT = 1 #claw is heading right
caught_doll = None # if claw catches. put it in this var
to_x = 0 #claw stretch speed
move_speed = 12 # claw shooting speed
return_speed = 60 # if claw is launched and didn't capture anything... quickly rewind

#instantiate claw object and group up doll_group
claw = Claw(claw_image, (screen_width / 2, 40 )) 
#make list to Group up dolls
doll_group = pygame.sprite.Group()
#set up dolls
setup_doll() 

#Game color, font, score, timer, game result vars
#COLOR
RED = "#FF0000"
BLACK = "#000000"
YELLOW = "#FFFF00"
#game font
game_font = pygame.font.SysFont("cambriamath", 30)
ending_font = pygame.font.SysFont("Gothic", 60) 
#score board variables
goal_score = 300 
curr_score = 0 
#timer variables
start_ticks = pygame.time.get_ticks() 

#game running
running = True
while running:
    clock.tick(30) #FPS
    #All event keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                claw.set_direction(STOP) #claw rotation stop
                to_x = move_speed 
    
    #if claw hits screen boundary
    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x -= return_speed

    #after claw is back and pass its original place, reimage claw to its original orientation
    if claw.offset.x < default_offset_x_claw:
        to_x = 0
        claw.set_init_state() # return to initial states

        #if claw caught and brough doll back
        if caught_doll:
            score_update(caught_doll.price) #update the scoreboard
            doll_group.remove(caught_doll) #delete that doll image
            caught_doll = None

    #if doll already collide with any doll, bring it back with back speed minus doll speed
    if not caught_doll:
        for doll in doll_group:
            if pygame.sprite.collide_mask(claw, doll): #when it actually hits the image
                #image to bring
                caught_doll = doll 
                #claw speed with doll
                to_x = -doll.speed 
                break

    #put doll image to a center of claw image 
    if caught_doll:
        caught_doll.set_position(claw.rect.center, claw.angle)

    #draw background
    screen.blit(background, (0, 0))
    #draw all doll in the group
    doll_group.draw(screen) 
    #draw claw and let it move
    claw.update(to_x)
    claw.draw(screen)
    #draw score board and timer, if timer hits 0, game over
    score()
    timer_calculate()
    pygame.display.update()
pygame.quit()