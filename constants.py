import pygame as pg

WHITE=(255,255,255)
BLACK=(0,0,0)

GREY=(64,64,64)
LIGHTBROWN=(204,102,0)
DARKBROWN=(102,51,0)
BLUE=(0,0,255)

width, height = (600, 600)
tilesize = 55
rows = cols = 8

boardXLoc, boardYLoc = (width-tilesize*rows)/2, (height-tilesize*cols)/2

crown = pg.transform.scale(pg.image.load('crown.png'), (30, 25))
