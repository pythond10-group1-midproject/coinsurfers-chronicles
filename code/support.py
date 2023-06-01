from os import walk
import pygame
from csv import reader
from settings import tile_size
import datetime

hour_of_day = datetime.datetime.now().time().hour

def import_folder(path):
    animation_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            animation_list.append(image_surf)
    return animation_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map
    
def import_cut_graphic(path):
    surface = pygame.image.load(path).convert_alpha()
    x, y = surface.get_width(), surface.get_height()
    factor = tile_size // y
    pygame.transform.scale(surface, (x* factor, y* factor))
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)
    
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size),flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)
            
    return cut_tiles