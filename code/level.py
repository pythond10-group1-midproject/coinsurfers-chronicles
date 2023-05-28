import pygame
from tiles import Tile
from settings import tile_size, screen_width
from player import Player

class Level:
    def __init__(self, level_data, surface): # arguments are level data you get 
        # from settings level_map i.e and surface is the home screen
        # this is the level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0 # this is what is bond with the character position to move the map
        
    def setup_level(self, layout): # rendering the map in white blocks
        self.tiles = pygame.sprite.Group() # this is for multiple objects
        self.player = pygame.sprite.GroupSingle() # this is a single player
        
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = tile_size * col_index
                y = tile_size * row_index
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def scroll_x(self): # this method is to scroll the world based on player movement of x
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        
        if player_x < screen_width / 4 and direction_x < 0: # based on screen width since screen width is a number if player is going left
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0: # based on screen width since screen width is a number if player is going right
            self.world_shift = -8 
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
    
    def horizontal_movement_collision(self): # to block player movement collisions on the x axis
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        for sprite in self.tiles.sprites(): 
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        for sprite in self.tiles.sprites(): 
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0 # here to handle the issue of gravity
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0 # here to handle the issue of continuously jumping
            
    
    def run(self): # this is to update the world with the x of player and then display the world
        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        
        # level player position from settings file P
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        