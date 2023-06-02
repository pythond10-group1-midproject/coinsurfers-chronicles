import pygame, sys
from settings import screen_width

class MainMenu:
    def __init__(self, surface, create_overworld):
        self.display_surface = surface
        self.background = pygame.image.load('graphics/logo.png').convert_alpha()
        self.button_one_rect = pygame.Rect(screen_width/2 - 340, 528, 170, 142)
        self.button_one = pygame.image.load('graphics/sett_but.png').convert_alpha()
        self.button_two_rect = pygame.Rect(screen_width/2 - 85, 528, 170, 142)
        self.button_two = pygame.image.load('graphics/play_but.png').convert_alpha()
        self.button_three_rect = pygame.Rect(screen_width/2 + 170, 528, 170, 142)
        self.button_three = pygame.image.load('graphics/quit_but.png').convert_alpha()
        self.create_overworld = create_overworld
        
    def create_button(self, image, pos):
        new_image = pygame.transform.scale(image, (170, 142))
        return self.display_surface.blit(new_image,pos)
    
    def is_pressed(self):
        mouse_presses = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_rect = pygame.Rect(mouse_pos[0],mouse_pos[1],20,20)
        print(mouse_pos, mouse_presses)
        if self.button_two_rect.colliderect(mouse_pos_rect) and mouse_presses[0]:
            self.create_overworld(0, 4)
        if self.button_three_rect.colliderect(mouse_pos_rect) and mouse_presses[0]:
            sys.exit()
            
    def run(self):
        self.display_surface.blit(self.background, (0, 0))
        self.create_button(self.button_one, (screen_width/2 - 340, 528))
        self.create_button(self.button_two, (screen_width/2 - 85, 528))
        self.create_button(self.button_three, (screen_width/2 + 170, 528))
        self.is_pressed()
        