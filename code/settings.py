import pygame

level_map = [
'                       ',
'                       ',
'                       ',
' XX   XX          XX   ',
' XX P                  ',
' XXXX         XX    XX ',
' XX    X      XX    XX ',
'       X   XXXXX   XXX ',
' XXXXXXX   XXXXX  XXXX ']

tile_size = 64
screen_width = 1200
screen_height = len(level_map) * tile_size # Here it is great to have tile size multiplied by the number of rows in level_map for better display
