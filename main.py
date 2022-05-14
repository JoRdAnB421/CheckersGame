'''
Main script
'''
from constants import *
import pygame as pg
from board import Board
from game import Game


pg.init()

FPS = 60

win = pg.display.set_mode((width, height))

pg.display.set_caption('Checkers')

def GetPosMouse(pos):
    '''
    Finds mouse coordinates in terms of grid position

    Input >>> pos = mouse coordinates

    Output >>> row, col = grid position
    '''
    x, y = pos
    row = int((y-boardYLoc) // tilesize)
    col = int((x-boardXLoc) // tilesize)
    return row, col

def Main():
    '''
    main function to run
    '''
    running = True
    finish = False
    clock = pg.time.Clock()
    game = Game(win) # Draw to surface

    while running:
        clock.tick(FPS)

        if game.Winner() != None:
            # If someone wins, freeze screen with winning text, r resets game
            finish=True
            while finish:
                clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        print('Quitting')
                        running, finish = (False, False)
                    if event.type == pg.KEYDOWN: 
                        if event.key == pg.K_r:
                            game.Reset()
                            print('Reset')
                            finish=False

        for event in pg.event.get(pump=True):
            if event.type == pg.QUIT:
                print('Quitting')
                running=False

            if event.type == pg.MOUSEBUTTONDOWN:
                # If mouse clicks find coordinates and select piece as required
                pos = pg.mouse.get_pos()
                row, col = GetPosMouse(pos)
                if (row&col>=0)&(row&col<8):
                   game.Select(row, col)
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    game.Reset()
                    print('Reset')
                    
        game.Update()

    pg.quit()

Main()
