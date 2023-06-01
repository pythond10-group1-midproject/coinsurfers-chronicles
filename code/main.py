import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI

class Game:
    def __init__(self):
        
        # game attributes
        self.max_level = 2
        self.max_health = 100
        self.cur_health = 100
        self.total_coins = 0
        self.coins = 0
        self.global_coins = 0
        pygame.mixer.init()

        # audio
        self.level_bg_music = pygame.mixer.Sound('audio/level_music.wav')
        self.level_bg_music.set_volume(0.3)
        self.overworld_bg_music = pygame.mixer.Sound('audio/overworld_music.wav')
        self.overworld_bg_music.set_volume(0.3)
        
        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen,self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops = -1)
        
        # ui
        self.ui = UI(screen)
        
    def create_level(self,current_level):
        self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health,self.change_total_coins)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)

    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'    
        self.level_bg_music.stop()
        self.overworld_bg_music.play(loops = -1)
        
    def change_coins(self, amount):
        if amount == 0 :
            self.coins = 0
        else:    
            self.coins += amount

    def change_total_coins(self):
        self.total_coins += self.coins    
    
    def change_health(self, amount):  
        self.cur_health += amount
    
    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.total_coins =0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops = -1)
            
    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
            self.ui.show_coins(self.total_coins)
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()

# screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
    screen.fill('gray')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    game.run()
    
    pygame.display.update()
    clock.tick(60)