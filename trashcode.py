import pygame
import os
import game_module

pygame.font.init()
# pygame.mixer.init()

# list of variables
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("One Hit Hero!")

WHITE = (255,255,255)
BLACK = (0,0,0)
FPS = 60
VEL = 3
SAMURAI_WIDTH, SAMURAI_HEIGHT = 80, 60
MAIN_FONT = pygame.font.SysFont('comicsans', 24)
idle_player = pygame.image.load(os.path.join('assets/bonfiresprite.png')).convert_alpha()
player_idle = game_module.SpriteSheet(idle_player)

# images and image rendering
FIRST_SAMURAI = pygame.image.load(os.path.join('assets', 'samurai.png'))
SAMURAI = pygame.transform.scale(FIRST_SAMURAI, (SAMURAI_WIDTH, SAMURAI_HEIGHT)) # this resizes the image of samurai

BACKGROUND = pygame.image.load(os.path.join('assets', 'background.png'))

animation_list = []
animation_steps = 8


for x in range(animation_steps):
    animation_list.append(player_idle.get_image(x, 200, 300, .15, BLACK))

# drawing the screen
def draw_window(player, frame):
    WIN.blit(BACKGROUND, (0,0))
    WIN.blit(animation_list[frame], (player.x, player.y))
    TEAM_ONE = MAIN_FONT.render("This is the work of Team 1", 1, WHITE)
    WIN.blit(TEAM_ONE, (WIDTH//2 - TEAM_ONE.get_width()//2, HEIGHT - 30))
    # WIN.blit(sprite_sheet_iamge, (player.x, player.y))
    pygame.display.update()
    
# define player movement
def player_movement(keys_pressed, player, SAMURAI): 
    if keys_pressed[pygame.K_a] and player.x - VEL > 0: # Left direction
        # SAMURAI = pygame.transform.flip(flip_x=True)
        player.x -= VEL
        
    if keys_pressed[pygame.K_d] and player.x + VEL + player.width < WIDTH: # Right direction
        player.x += VEL

# main loop
def main():
    player = pygame.Rect(280, 515, SAMURAI_WIDTH, SAMURAI_HEIGHT) # render player box
    clock = pygame.time.Clock()
    frame = 0
    animation_cooldown = 100
    last_update = pygame.time.get_ticks()
    run = True
    while run:
        clock.tick(FPS) # handles FPS of the while loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(animation_list):
                frame = 0
        keys_pressed = pygame.key.get_pressed() # handles keys pressed
        player_movement(keys_pressed, player, SAMURAI) # handles player movement
        draw_window(player, frame) # draws window
        
    pygame.quit()
    
if __name__ == "__main__":
    main()
