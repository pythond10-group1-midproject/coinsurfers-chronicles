"""
Importing important libraries
"""
import pygame, sys
import game_module as gm

"""
Setting up an environment to initialize pygame
"""
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Jump King Team 1')
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height),0,32)
 
#setting font settings
font = pygame.font.SysFont(None, 30)
 
"""
A function that can be used to write text on our screen and buttons
"""
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
# A variable to check for the status later
click = False
background = pygame.image.load('assets/background2.png')
play_button_img = pygame.image.load('assets/play_button.png').convert_alpha()
play_button = pygame.transform.scale(play_button_img, (110, 54))
options_button_img = pygame.image.load('assets/options_button.png').convert_alpha()
options_button = pygame.transform.scale(options_button_img, (110, 54))
# Main container function that holds the buttons and game functions
quit_button_img = pygame.image.load('assets/quit_button.png').convert_alpha()
quit_button = pygame.transform.scale(quit_button_img, (110, 54))
FIRST_SAMURAI = pygame.image.load('assets/staticsprite.png').convert_alpha()
SAMURAI = pygame.transform.scale(FIRST_SAMURAI, (FIRST_SAMURAI.get_width()*4, FIRST_SAMURAI.get_height()*4))
SAMURAI_ANIMATION = gm.SpriteSheet(SAMURAI)
SAMURAI_animation_list = []
SAMURAI_animation_steps = 6
BLACK = (0, 0, 0)

for x in range(SAMURAI_animation_steps):
    SAMURAI_animation_list.append(SAMURAI_ANIMATION.get_image(x, 128, 128, 1, BLACK))
    
def main_menu():
    
    frame = 0
    animation_cooldown = 300
    last_update = pygame.time.get_ticks()
    
    while True:
        
        draw_text('Main Menu', font, (255,255,255), screen, 550, 40)
        mx, my = pygame.mouse.get_pos()

        #creating buttons
        screen.blit(background, (0, 0))
        screen.blit(SAMURAI_animation_list[frame], (180, 420))
        # screen.blit(SAMURAI, (100, 360))
        button_1 = pygame.Rect(555, 100, 110, 54)
        button_2 = pygame.Rect(555, 180, 110, 54)
        button_3 = pygame.Rect(555, 260, 110, 54)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()

        screen.blit(play_button, (550, 100))
        screen.blit(options_button, (550, 180))
        screen.blit(quit_button, (550, 260))
        
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(SAMURAI_animation_list):
                frame = 0

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)
 
"""
This function is called when the "PLAY" button is clicked.
"""
## game variables
BACKGROUND = pygame.image.load('assets/background.png')
bonfire_sprite = pygame.image.load('assets/bonfiresprite.png').convert_alpha()
bonfire = gm.SpriteSheet(bonfire_sprite)
player_width, player_height = 32, 32
VEL = 3

player_sprite = pygame.image.load('assets/staticsprite.png').convert_alpha()
player_animation = pygame.transform.scale(player_sprite, (player_sprite.get_width()*4, player_sprite.get_height()*4))
SAMURAI_ANIMATION = gm.SpriteSheet(SAMURAI)
SAMURAI_animation_list = []
SAMURAI_animation_steps = 6
BLACK = (0, 0, 0)

for x in range(SAMURAI_animation_steps):
    SAMURAI_animation_list.append(SAMURAI_ANIMATION.get_image(x, 128, 128, 1, BLACK))
    
def player_movement(keys_pressed, player, SAMURAI): 
    if keys_pressed[pygame.K_a] and player.x - VEL > 0: # Left direction
        # SAMURAI = pygame.transform.flip(flip_x=True)
        player.x -= VEL
        
    if keys_pressed[pygame.K_d] and player.x + VEL + player.width < screen_width: # Right direction
        player.x += VEL

def game():
    running = True
    frame = 0
    animation_cooldown = 300
    last_update = pygame.time.get_ticks()
    while running:
        screen.blit(BACKGROUND, (0,0))
        player = pygame.Rect(280, 515, player_width, player_height)
        screen.blit(bonfire_sprite, (0, 0))
        # screen.blit(player_animation_list[frame], (player.x, player.y))
        draw_text('Welcome', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        keys_pressed = pygame.key.get_pressed()
        player_movement(keys_pressed, player, SAMURAI)    
        
        pygame.display.update()
        mainClock.tick(60)

"""
This function is called when the "OPTIONS" button is clicked.
"""
def options():
    running = True
    while running:
        screen.fill((0,0,0))
 
        draw_text('OPTIONS SCREEN', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
       
        pygame.display.update()
        mainClock.tick(60)
 
main_menu()