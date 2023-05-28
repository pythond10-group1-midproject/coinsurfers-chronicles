import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = position)
        
        # player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        
        # player status
        self.status = 'idle'
        self.facing_right = True
        
    def import_character_assets(self):
        character_path = 'graphics/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def animate(self):
        animation = self.animations[self.status]
        
        # looping over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        self.image = animation[int(self.frame_index)]
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
            
        if keys[pygame.K_SPACE]:
            self.jump()
          
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1: # this number should be greater than gravity for the purpose of status handling and collision detection
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
                
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y = self.jump_speed
        
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        