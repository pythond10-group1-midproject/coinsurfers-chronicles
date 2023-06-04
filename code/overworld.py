import pygame
from game_data import levels
from support import import_folder
from decorations import Sky,Clouds,Stars
from settings import *

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed,path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'available':
            self.status = "available"
        else:
            self.status = 'locked'
        self.rect = self.image.get_rect(center = pos)

        self.detection_zone = pygame.Rect(self.rect.centerx - (icon_speed/2),self.rect.centery - (icon_speed/2),icon_speed*2,icon_speed*2)

    def animate(self):
        self.frame_index += 0.15 # edit if you want a slower coin animation
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]  

    def update(self):
        if self.status == "available":
            self.animate() 
        else:
            tint_surface = self.image.copy()
            tint_surface.fill('black',None,pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surface,(0,0))       

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self, start_level, max_level, surface,create_level,buy_health,create_mainmenu):

        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_mainmenu = create_mainmenu
        self.create_level = create_level

        # movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        # buy health button
        self.health_button_image = pygame.image.load('graphics/overworld/plus_life.png').convert_alpha()
        self.health_button = pygame.transform.scale(self.health_button_image,(self.health_button_image.get_width()*0.5,self.health_button_image.get_height()*0.5))
        self.buy_health = buy_health
        self.did_buy =False
        self.delay = 500
        self.click_time = 0
        
        # go back button
        self.go_back_button_image = pygame.image.load('graphics/go_back_but.png').convert_alpha()
        self.go_back_rect = pygame.Rect(30, screen_height-55, 55, 55)

        # sprites
        self.setup_nodes()
        self.setup_icon()

        # sky
        self.sky= Sky(8,'overworld')
        self.clouds = Clouds(350,screen_width,25)
        self.stars = Stars(350,screen_width,100)
        
        # time 
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for index ,node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available' , self.speed,node_data['node_graphics'])
            else:
                node_sprite = Node(node_data['node_pos'], 'locked' , self.speed,node_data['node_graphics'])
            self.nodes.add(node_sprite)

    def draw_paths(self):
        points = [node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level] # list comprehention
        if len(points) != 1:
            pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving and self.allow_input:
            if keys[pygame.K_d] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_a] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        elif target == 'previous':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)

    def input_timer(self):
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True
 
    def show_buy_button(self):
        self.display_surface.blit(self.health_button,(screen_width - 100, 40))

    def buy_on_click(self):
        if not self.did_buy:
                self.buy_health(10,25)
                self.click_time = pygame.time.get_ticks()
                self.did_buy = True

    def create_button(self, image, pos):
        new_image = pygame.transform.scale(image, (85, 72))
        self.display_surface.blit(new_image,pos)
    
    def is_pressed(self):
        if self.allow_input:
            mouse_presses = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos_rect = pygame.Rect(mouse_pos[0],mouse_pos[1],20,20)
            if self.go_back_rect.colliderect(mouse_pos_rect) and mouse_presses[0]:
                self.create_mainmenu(self.display_surface)
    
    def buy_timer(self):
        cur_time = pygame.time.get_ticks()
        if self.did_buy:
            if cur_time - self.click_time >= self.delay:
                self.did_buy = False
                 
    def on_click(self):
        mouse_presses = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_rect = pygame.Rect(mouse_pos[0],mouse_pos[1],20,20)
        health_but = pygame.Rect(screen_width-100,40,42,32)
        if health_but.colliderect(mouse_pos_rect) and mouse_presses[0]:
            self.buy_on_click()

    def run(self):
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.nodes.update()
        self.sky.draw(self.display_surface)
        self.stars.draw(self.display_surface,0)
        self.clouds.draw(self.display_surface,0)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        self.show_buy_button()
        self.buy_timer()
        self.on_click()
        self.create_button(self.go_back_button_image, (0, screen_height-85))
        self.is_pressed()

            