import pygame
import os

#Game over section
def game_over(game_result):
    msg = game_font.render(game_result, True, (255, 255, 0))
    msg_rect = msg.get_rect(center = (screen_width/2, screen_height/2))
    screen.blit(msg, msg_rect)
    pygame.display.update()
    pygame.time.delay(2000)

pygame.init()

#screen set up
screen_width = 1024
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("DK BUBBLE")

#game running
#FPS
clock = pygame.time.Clock()

#image set up

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")
character_path = os.path.join(image_path, "characters")
background_path = os.path.join(image_path, "backgrounds")
bubble_path = os.path.join(image_path, "bubbles")
#backgroud
background = pygame.image.load(os.path.join(background_path, "background.png"))

#stage 
stage = pygame.image.load(os.path.join(background_path, "stage_horizontal_b.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]
stage_pos_y = screen_height - stage_height

#character

char =pygame.image.load(os.path.join(character_path, "char_b.png"))
char_size = char.get_rect().size
char_width = char_size[0]
char_height = char_size[1]
char_pos_x = (screen_width) / 2 + (char_width /2)
char_pos_y = screen_height - stage_height - char_height

char_speed = 5
char_to_x = 0
char_to_y = 0
#bubble
bubble_list = [
    pygame.image.load(os.path.join(bubble_path, "bubble1.png")),
    pygame.image.load(os.path.join(bubble_path, "bubble2.png")),
    pygame.image.load(os.path.join(bubble_path, "bubble3.png")),
    pygame.image.load(os.path.join(bubble_path, "bubble4.png"))]
bubble_y_limit = [-21, - 18, - 15, -12]

bubbles = []
bubbles.append({
    "pos_x" : 50,
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x" : 3,
    "to_y" : -6,
    "y_limit" : bubble_y_limit[0]
})


#weapon
weapon = pygame.image.load(os.path.join(character_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]
weapon_speed = 7
#store all weapons in the game
current_weapon = []
#weapon's current location
weapon_pos_x = 0
weapon_pos_y = 0


# delete from list weapon and bubble
weapon_to_remove = -1
bubble_to_remove = -1


#game font
game_font = pygame.font.Font(None, 40)
game_result = "Game Over"

#timer
time_limit = 50
start_ticks = pygame.time.get_ticks()
weapon_msg_render = None
#color 
PURPLE = "#A020F0"
BLACK = "#000000"

running = True
while running:
    #draw background and stage first
    screen.blit(background, (0,0))
    screen.blit(stage, (0, stage_pos_y))
    #FPS
    dt = clock.tick(60)
    #all keyboard event keys
    for event in pygame.event.get():
        #if user close the program
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        #keyboard:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                char_to_x -= char_speed
            elif event.key == pygame.K_RIGHT:
                char_to_x += char_speed
            elif event.key == pygame.K_UP:
                char_to_y -= char_speed
            elif event.key == pygame.K_DOWN:
                char_to_y += char_speed
            elif event.key == pygame.K_SPACE:
                if len(current_weapon) < 5:
                    weapon_pos_x = char_pos_x + (char_width /2 ) - (weapon_width /2)
                    weapon_pos_y = char_pos_y 
                    current_weapon.append([weapon_pos_x, weapon_pos_y])                       


        #If user lift the keyboard key, the character stops    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                char_to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                char_to_y = 0
    #character moves based on keyboard key
    char_pos_x += char_to_x
    char_pos_y += char_to_y

    #character and screen boundary 
    if char_pos_x <= 0:
        char_pos_x = 0
    elif char_pos_x > screen_width - char_width:
        char_pos_x = screen_width - char_width
    #weapon's movement
    current_weapon = [[w[0], w[1] - weapon_speed] for w in current_weapon]
    current_weapon = [[w[0], w[1]] for w in current_weapon if w[1] > 0]
    #bubble's movement
    for bubble_val in bubbles:
        bubble_pos_x = bubble_val["pos_x"]
        bubble_pos_y = bubble_val["pos_y"]
        bubble_image_idx = bubble_val["img_idx"]

        bubble_size = bubble_list[bubble_image_idx].get_rect().size
        bubble_width = bubble_size[0]
        bubble_height = bubble_size[1]

        if bubble_pos_x <= 0 or bubble_pos_x > screen_width - bubble_width:
            bubble_val["to_x"] = bubble_val["to_x"] * -1
        
        if bubble_pos_y >= screen_height - stage_height - bubble_height:
            bubble_val["to_y"] = bubble_val["y_limit"]
        else:
            bubble_val["to_y"] += 0.5

        bubble_val["pos_x"] += bubble_val["to_x"]
        bubble_val["pos_y"] += bubble_val["to_y"]
#collision
    char_rect = char.get_rect()
    char_rect.left = char_pos_x
    char_rect.top = char_pos_y

    for bubble_idx, bubble_val in enumerate(bubbles):
        bubble_pos_x = bubble_val["pos_x"]
        bubble_pos_y = bubble_val["pos_y"]
        bubble_image_idx = bubble_val["img_idx"]
        bubble_rect = bubble_list[bubble_image_idx].get_rect()
        bubble_rect.left = bubble_pos_x
        bubble_rect.top = bubble_pos_y
        #if character colides with bubble. stop the game
        if char_rect.colliderect(bubble_rect):
            running = False
            break
        
        for weapon_idx, weapon_val in enumerate(current_weapon):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y
            #if bubble collides with weapon
            #Mark that bubble and weapon index
            if weapon_rect.colliderect(bubble_rect):
                weapon_to_remove = weapon_idx
                bubble_to_remove = bubble_idx

                #after bubble collides with weapon,if bubble idx is smaller than 3 , seperate into 2 smaller bubbles
                if bubble_image_idx < 3:
                    bubble_width = bubble_rect.size[0]
                    bubble_height = bubble_rect.size[1]

                    small_bubble_rect = bubble_list[bubble_image_idx+1].get_rect()
                    small_bubble_width = small_bubble_rect[0]
                    small_bubble_height = small_bubble_rect[1]

                    bubbles.append(
                    {
                        "pos_x" : bubble_pos_x + (bubble_width / 2) - (small_bubble_width /2),
                        "pos_y" : bubble_pos_y + (bubble_height /2) - (small_bubble_height/2),
                        "img_idx" : bubble_image_idx + 1,
                        "to_x" : -3,
                        "to_y" : -6,
                        "y_limit": bubble_y_limit[bubble_image_idx+1]
                    }
                )
                    bubbles.append(
                        {
                        "pos_x" : bubble_pos_x + (bubble_width / 2) - (small_bubble_width /2),
                        "pos_y" : bubble_pos_y + (bubble_height /2) - (small_bubble_height/2),
                        "img_idx" : bubble_image_idx + 1,
                        "to_x" : 3,
                        "to_y" : -6,
                        "y_limit": bubble_y_limit[bubble_image_idx+1]
                        })

                break
        else:
            continue
        break

    #delete the collided bubble and weapon
    if bubble_to_remove > -1:
        del bubbles[bubble_to_remove]
        bubble_to_remove = -1
    if weapon_to_remove > -1:
        del current_weapon[weapon_to_remove]
        weapon_to_remove = -1
    #timer
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time: {}".format(int(time_limit - elapsed_time)), True, BLACK)

    #if there is no bubble in the game, user win
    if len(bubbles) == 0:
        game_result = "Mission clear"
        running = False
    #if out of time, user lose
    if time_limit - elapsed_time <= 0:
        game_result = "Out of time"
        running = False    

    #if there is more than 5 weapons in the game, print "RELOADING"
    if len(current_weapon) >= 5:
        reload_msg = game_font.render("RELOADING", True, BLACK)
        reload_get_rect = reload_msg.get_rect(topleft = ((char_pos_x + char_width), (char_pos_y - char_height/2)))
        screen.blit(reload_msg, reload_get_rect)

    #draw weapons
    for weapon_pos_x, weapon_pos_y in current_weapon:
        screen.blit(weapon, (weapon_pos_x, weapon_pos_y))
    #draw bubbles
    for bubble in bubbles:
        bubble_pos_x = bubble["pos_x"]
        bubble_pos_y = bubble["pos_y"]
        bubble_image_idx = bubble["img_idx"]
        screen.blit(bubble_list[bubble_image_idx], (bubble_pos_x, bubble_pos_y))
    #draw character and timer
    screen.blit(char, (char_pos_x, char_pos_y))
    screen.blit(timer, (10, 10))

    
    pygame.display.update() 
game_over(game_result)
pygame.quit()
