import pygame as pg
import asyncio

from constants import *
from game import Game

pg.init()

win = pg.display.set_mode((width, height))
pg.display.set_caption("Checkers")

def GetPosMouse(pos):
    x, y = pos
    row = int((y - boardYLoc) // tilesize)
    col = int((x - boardXLoc) // tilesize)
    return row, col

game = Game(win)
clock = pg.time.Clock()

async def main():
    running = True

    while running:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = GetPosMouse(pos)
                if (min(row, col) >= 0) and (max(row, col) < 8):
                    game.Select(row, col)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    game.Reset()

        # Draw everything
        game.Update()

        await asyncio.sleep(0)

    pg.quit()

# 🔑 THIS is the correct pygbag entry point
asyncio.ensure_future(main())
