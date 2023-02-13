import pygame
import os

####Function
## Game Over
def game_over(game_result):
    global running, running1, LEVEL

    if LEVEL ==2:
        running = False
    else:
        running = False
        running1 = False
    screen.fill(BLACK)
    msg = ending_font.render(game_result, True, YELLOW)
    msg_rect = msg.get_rect(center = (screen_width/2, screen_height/2- 100))
    thank_msg = game_font.render("Thank you for playing DK-Game. Have a great day!", True, YELLOW)
    screen.blit(thank_msg, ((screen_width /6)  , screen_height * 5/8))
    screen.blit(msg, msg_rect)
    pygame.display.update()
    pygame.time.delay(2000)

# screen blit function
def draw(image, x, y):
    screen.blit(image, (x, y))


#Render life text at the top left
def count_life():
    global life

    life_text = game_font.render(f"Lives: {life}", True, BLACK)
    draw(life_text, 150, 10)
#screen set up
def screen_setup(screen_width, screen_height):
    screen_width = screen_width
    screen_height = screen_height
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("DK BUBBLE")
    return screen_width, screen_height, screen
#Render total time left and if out of time, this function leads to gameover function
def timer_calculate():
    global game_result, running, LEVEL
    time_limit = 77
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time: {}".format(int(time_limit - elapsed_time)), True, BLACK)
    if time_limit - elapsed_time > 0:
        draw(timer, 10, 10)
    else:
        if LEVEL == 2:
            LEVEL = 1
        game_result = "Out of time"
        game_over(game_result)



pygame.init()
###############

#Level setting var
LEVEL = 1
running1 = True
while running1:
    #screen setup
    screen_width, screen_height, screen = screen_setup(1024, 680)
    #FPS
    clock = pygame.time.Clock()

    ###############
    ####Image
    #image directory set up
    current_path = os.path.dirname(__file__)
    image_path = os.path.join(current_path, "images")
    character_path = os.path.join(image_path, "characters")
    background_path = os.path.join(image_path, "backgrounds")
    bubble_path = os.path.join(image_path, "bubbles")

    #backgroud image
    background = pygame.image.load(os.path.join(background_path, "background.png"))

    #stage image
    stage_width,stage_height = 48, 48
    stages = [pygame.image.load(os.path.join(background_path, "stage_horizontal_b.png")),
            pygame.image.load(os.path.join(background_path, "stage_horizontal_t.png")),
            pygame.image.load(os.path.join(background_path, "stage_vertical_l.png")),
            pygame.image.load(os.path.join(background_path, "stage_vertical_r.png"))]
    stage_position = ((0, screen_height - stage_height),(0, 0),(0, 0),(screen_width - stage_width, 0))
    #character images
    char_t = pygame.image.load(os.path.join(character_path, "char_t.png"))
    char_b = pygame.image.load(os.path.join(character_path, "char_b.png"))
    char_l = pygame.image.load(os.path.join(character_path, "char_l.png"))
    char_r = pygame.image.load(os.path.join(character_path, "char_r.png"))  
    char = char_b
    char_size = char.get_rect().size
    char_width = char_size[0]
    char_height = char_size[1]
    char_pos_x = (screen_width) / 2 + (char_width /2)
    char_pos_y = screen_height - stage_height - char_height
    char_speed = 5
    char_to_x = 0
    char_to_y = 0



    #bubble images
    bubble_list = [
        pygame.image.load(os.path.join(bubble_path, "bubble1.png")),
        pygame.image.load(os.path.join(bubble_path, "bubble2.png")),
        pygame.image.load(os.path.join(bubble_path, "bubble3.png")),
        pygame.image.load(os.path.join(bubble_path, "bubble4.png"))]

    #bubbles maximum jump distance limit and initial speed after crack


    #weapon image
    weapon = pygame.image.load(os.path.join(character_path, "weapon.png"))
    weapon_size = weapon.get_rect().size
    weapon_width = weapon_size[0]
    weapon_height = weapon_size[1]
    weapon_speed = 7
    weapon_pos_x = 0
    weapon_pos_y = 0


    ###############
    ####Current bubble and weapon in the game
    #current bubble in the game
    bubbles = []
    #initial bubble based on a current level
    if LEVEL == 1:
        bubbles.append({
            "pos_x" : 50,
            "pos_y" : 50,
            "img_idx" : 0,
            "to_x" : 3,
            "to_y" : -6
        })
    if LEVEL == 2:
                bubbles.append({
            "pos_x" : 50,
            "pos_y" : 50,
            "img_idx" : 0,
            "to_x" : 3,
            "to_y" : -6
        })
                bubbles.append({
            "pos_x" : 774,
            "pos_y" : 50,
            "img_idx" : 0,
            "to_x" : 3,
            "to_y" : -6
        })
    #current weapons of 4 directions in the game
    current_weapons = [[] for x in range(4)]

    # keeping delete idx if a bubble collide with a weapon
    weapon_to_remove = [-1, -1, -1, -1]
    bubble_to_remove = -1

    ###############
    ####Game font and color var
    #game font
    game_font = pygame.font.Font(None, 40)
    ending_font = pygame.font.SysFont("Times New Roman", 120 )
    
    #color 

    PURPLE = "#A020F0"
    BLACK = "#000000"
    YELLOW = "#FFFF00"
    RED = "#FF0000"
    BLUE = "#0000FF"
    WHITE = "#FFFFFF"

    #if ball hits character, char turns on its superpower. Invulnerable status for 2 seconds
    super_power = False
    # How much lives left till game over
    life = 7
    ###############
    ####game running

    #initiating game
    running = True
    start_ticks = pygame.time.get_ticks()
    while running:
        #FPS
        dt = clock.tick(60)

        # all event keys
        for event in pygame.event.get():
            #if user close the program
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if char_pos_y == screen_height - stage_height - char_height or char_pos_y == stage_height:
                        char_to_x -= char_speed
                elif event.key == pygame.K_RIGHT:
                    if char_pos_y == screen_height - stage_height - char_height or char_pos_y == stage_height:
                        char_to_x += char_speed
                elif event.key == pygame.K_UP:
                    if char_pos_x == stage_width or char_pos_x == screen_width - stage_width - char_width:
                        char_to_y -= char_speed
                elif event.key == pygame.K_DOWN:
                    if char_pos_x == stage_width or char_pos_x == screen_width - stage_width - char_width:
                        char_to_y += char_speed
                elif event.key == pygame.K_SPACE:
                    #weapon moves
                            #depends on characters current position. Top, bottom, left, right side of the stage in the game
                            # Number of weapons are limited to 5 on every direction
                            if char == char_t:
                                weapon_pos_x = char_pos_x + (char_width /2 ) - (weapon_width /2)
                                weapon_pos_y = char_pos_y
                                if len(current_weapons[0]) < 5:
                                    current_weapons[0].append([weapon_pos_x, weapon_pos_y])  

                            elif char == char_b:
                                weapon_pos_x = char_pos_x + (char_width /2 ) - (weapon_width /2)
                                weapon_pos_y = char_pos_y 
                                if len(current_weapons[1]) < 5:
                                    current_weapons[1].append([weapon_pos_x, weapon_pos_y])  
                            elif char == char_l:
                                weapon_pos_x = char_pos_x + (char_width /2 ) - (weapon_width /2)
                                weapon_pos_y = char_pos_y 
                                if len(current_weapons[2]) < 5:
                                    current_weapons[2].append([weapon_pos_x, weapon_pos_y])  
                            elif char == char_r:
                                weapon_pos_x = char_pos_x + (char_width /2 ) - (weapon_width /2)
                                weapon_pos_y = char_pos_y 
                                if len(current_weapons[3]) < 5:
                                    current_weapons[3].append([weapon_pos_x, weapon_pos_y])  
            #if user stop pressing keyboard key, charater stops
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    char_to_x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    char_to_y = 0  
        # change position based on keyboard key
        char_pos_x += char_to_x
        char_pos_y += char_to_y
        
        #char
        #limit character's x axis move
        if char_pos_x <= stage_width:
            char_pos_x = stage_width
            # char = rot_center(char, 90)
        elif char_pos_x > screen_width - stage_width - char_width:
            char_pos_x = screen_width - stage_width - char_width
        #limit character's y axis move
        if char_pos_y <= stage_height:
            char_pos_y = stage_height
        elif char_pos_y > screen_height - stage_height - char_height:
            char_pos_y = screen_height - stage_height- char_height
        #if bubbles are out of range after collide with weapons.. I couldn't fix all bugs yet..
        if stage_width <=char_pos_x <= screen_width - stage_width - char_width and char_pos_y <= stage_height:
            char = char_t
        elif char_pos_y >= screen_height - stage_height - char_height and stage_width <=char_pos_x <= screen_width - stage_width - char_width:
            char = char_b
        elif char_pos_x  <= stage_width and stage_height <= char_pos_y <= screen_height - stage_height : 
            char = char_l
        elif char_pos_x  >= stage_width - stage_width - char_width and stage_height <= char_pos_y <= screen_height - stage_height: 
            char = char_r 
        #weapon's move based on the time user press the space
        current_weapons[0] = [[w[0], w[1] + weapon_speed] for w in current_weapons[0]]
        current_weapons[0] = [[w[0], w[1]] for w in current_weapons[0] if w[1] < screen_height - stage_height]
        current_weapons[1] = [[w[0], w[1] - weapon_speed] for w in current_weapons[1]]
        current_weapons[1] = [[w[0], w[1]] for w in current_weapons[1] if w[1] > stage_height]
        current_weapons[2] = [[w[0] + weapon_speed, w[1]] for w in current_weapons[2]]
        current_weapons[2] = [[w[0], w[1]] for w in current_weapons[2] if w[0] < screen_width - stage_width]
        current_weapons[3] = [[w[0] - weapon_speed, w[1]] for w in current_weapons[3]]
        current_weapons[3] = [[w[0], w[1]] for w in current_weapons[3] if w[0] > stage_width]


        #bubble move
        for bubble_val in bubbles:
            bubble_pos_x = bubble_val["pos_x"]
            bubble_pos_y = bubble_val["pos_y"]
            bubble_image_idx = bubble_val["img_idx"]

            bubble_size = bubble_list[bubble_image_idx].get_rect().size
            bubble_width = bubble_size[0]
            bubble_height = bubble_size[1]

            if bubble_pos_x <= stage_width or bubble_pos_x >= screen_width - bubble_width - stage_width:
                bubble_val["to_x"] = bubble_val["to_x"] * -1        
            if bubble_pos_y >= screen_height - stage_height - bubble_height or bubble_pos_y <= stage_height:
                bubble_val["to_y"] = bubble_val["to_y"] * -1

            if bubble_pos_x < stage_width and bubble_pos_y > screen_height - screen_height - bubble_height:
                bubble_pos_x =stage_width +20
                bubble_pos_y =screen_height - screen_height - bubble_height - 150
            elif bubble_pos_x <stage_width and bubble_pos_y < screen_height:
                bubble_pos_x =stage_width +1
                bubble_pos_y =screen_height + 1
            elif bubble_pos_x > screen_width - stage_width - bubble_width and bubble_pos_y < screen_height:
                bubble_pos_x = screen_width - stage_width - bubble_width -1
                bubble_pos_y =screen_height + 1
            elif bubble_pos_x > screen_width - stage_width - bubble_width and bubble_pos_y >= screen_height - screen_height - bubble_height:
                bubble_pos_x = screen_width - stage_width - bubble_width -1
                bubble_pos_y =screen_height - screen_height - bubble_height - 150

            bubble_val["pos_x"] += bubble_val["to_x"]
            bubble_val["pos_y"] += bubble_val["to_y"]

    ###############
    ####collision

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

            #if character collide with bubble..game over.
            
            if char_rect.colliderect(bubble_rect):
                if not super_power:
                    life -= 1
                    if life > 0:
                        super_power = True
                        super_power_start = pygame.time.get_ticks()

                    elif life <= 0:
                        if LEVEL == 2:
                            LEVEL = 1
                        game_result = "Game Over"
                        game_over(game_result)
                
            # when bubble collide with weapons
            for current_weapon_idx, current_weapon in enumerate(current_weapons):
                for weapon_idx, weapon_val in enumerate(current_weapon):
                    weapon_pos_x = weapon_val[0]
                    weapon_pos_y = weapon_val[1]

                    weapon_rect = weapon.get_rect()
                    weapon_rect.left = weapon_pos_x
                    weapon_rect.top = weapon_pos_y
                    #put collided buble and weapon idxes to delete var 
                    if weapon_rect.colliderect(bubble_rect):
                        weapon_to_remove[current_weapon_idx] = weapon_idx
                        bubble_to_remove = bubble_idx
                        #after collision, if bubble index is smaller than 1, the bubble divided  into 2 smaller bubbles
                        if bubble_image_idx < 1:
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
                                "to_y" : -6
                                
                            }
                        )
                            bubbles.append(
                                {
                                "pos_x" : bubble_pos_x + (bubble_width / 2) - (small_bubble_width /2),
                                "pos_y" : bubble_pos_y + (bubble_height /2) - (small_bubble_height/2),
                                "img_idx" : bubble_image_idx + 1,
                                "to_x" : 3,
                                "to_y" : -6

                                })

                        #after collision, if bubble index is bigger than 1 and smaller than 3 , the bubble divided  into 4 smaller bubbles
                        elif bubble_image_idx < 3:
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
                                "to_y" : -6
                                
                            }
                        )
                            bubbles.append(
                                {
                                "pos_x" : bubble_pos_x + (bubble_width / 2) - (small_bubble_width /2),
                                "pos_y" : bubble_pos_y + (bubble_height /2) - (small_bubble_height/2),
                                "img_idx" : bubble_image_idx + 1,
                                "to_x" : 3,
                                "to_y" : -6

                                })
                            bubbles.append(
                                {
                                "pos_x" : bubble_pos_x + (bubble_width / 2) - (small_bubble_width /2),
                                "pos_y" : bubble_pos_y + (bubble_height /2) - (small_bubble_height/2),
                                "img_idx" : bubble_image_idx + 1,
                                "to_x" : -3,
                                "to_y" : 6

                                })
                            bubbles.append(
                                {
                                "pos_x" : bubble_pos_x + (bubble_width / 2) - (small_bubble_width /2),
                                "pos_y" : bubble_pos_y + (bubble_height /2) - (small_bubble_height/2),
                                "img_idx" : bubble_image_idx + 1,
                                "to_x" : 3,
                                "to_y" : 6
                                })
                        break #if there is a collision, divided the buble and get out of nested weapon for loop
                else:
                    continue
                break #if there is a collision, divided the buble and get out of main weapon for loop
            else:
                continue
            break #if there is a collision, divided the buble and get out of bubble for loop

    # del bubble and weapon that are collided 
        if bubble_to_remove > -1:
            del bubbles[bubble_to_remove]
            bubble_to_remove = -1
        for idx, i in enumerate(weapon_to_remove):
            if i > -1:
                del current_weapons[idx][i]
                weapon_to_remove[idx] = -1

    # super power time. The character can not be hurt
        if super_power:
            super_power_time = 2
            sp_elapsed_time = (pygame.time.get_ticks() - super_power_start) / 1000
            if super_power_time - sp_elapsed_time <= 0: 
                super_power = False

    # if there is no bubble left in the game:
        if len(bubbles) <= 0:
            game_result = "Round Clear"
            pygame.time.delay(1000)
            LEVEL += 1
            break
    ###############
    ####draw
        #draw background and stage first
        draw(background, 0,0)
        for stage_idx, stage in enumerate(stages):
            stage = stages[stage_idx]
            draw(stage, stage_position[stage_idx][0], stage_position[stage_idx][1])

    #draw reload msg.
        #if there are more than 5 weapons in the game on each direction, print "RELOADING"
        for current_weapon in current_weapons:
            if len(current_weapon) >= 5:
                reload_msg = game_font.render("RELOADING", True, PURPLE)
                reload_get_rect = reload_msg.get_rect(topleft = ((char_pos_x + char_width), (char_pos_y - char_height/2)))
                screen.blit(reload_msg, reload_get_rect)

    #draw weapon
        for current_weapon in current_weapons:
            for weapon_pos_x, weapon_pos_y in current_weapon:
                draw(weapon, weapon_pos_x, weapon_pos_y)

    #draw bubbles
        for bubble in bubbles:
            bubble_pos_x = bubble["pos_x"]
            bubble_pos_y = bubble["pos_y"]
            bubble_image_idx = bubble["img_idx"]
            draw(bubble_list[bubble_image_idx], bubble_pos_x, bubble_pos_y)

    #draw character
        draw(char, char_pos_x, char_pos_y)
        count_life()

    #draw timer and set time limit
        timer_calculate()
        pygame.display.update() 

    #if running is false, print game over msg
    game_over(game_result)
pygame.quit()


