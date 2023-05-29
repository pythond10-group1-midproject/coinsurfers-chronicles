import pygame
from support import import_csv_layout, import_cut_graphic
from game_data import *
from settings import tile_size
from tiles import Tile, StaticTile, Crate, AnimatedTile

class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        
        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        
        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        
        # crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')
        
        # coins
        coins_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coins_layout, 'coins')
        
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'grass':
                        grass_tile_list = import_cut_graphic('graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        
                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)
                        
                    if type == 'coins':
                        sprite = AnimatedTile(tile_size, x, y,'graphics/coins/gold')

                    sprite_group.add(sprite)
                    
        return sprite_group
    
    def run(self):
        # draw the terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        # draw the grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
        
        # draw the crates
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)
        
        # draw the coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)