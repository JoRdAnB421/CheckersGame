from numpy import False_
from constants import BLACK, WHITE, GREY, tilesize, boardXLoc, boardYLoc, crown
import pygame as pg

class Piece:
    padding = 10
    border = 2
    
    def __init__(self, row, col, color):
        
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        
        self.x = 0
        self.y = 0
        self.CalcPos()

    def CalcPos(self):
        '''
        Calculates the position of the piece in terms of the surface
        '''
        self.x = boardXLoc + tilesize * self.col + tilesize // 2
        self.y = boardYLoc + tilesize * self.row + tilesize // 2

    def King(self):
        '''
        Sets if a piece is a king
        '''
        self.king = True

    def Draw(self, win):
        '''
        Draws the piece and crown (if king is true)

        Input >>> win = pygame.win surface to draw on
        '''
        radius = tilesize//2 - self.padding
        pg.draw.circle(win, GREY, (self.x, self.y), radius + self.border)
        pg.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            # If piece becomes king, add a crown image to it
            win.blit(crown.convert_alpha(), (self.x-crown.get_width()//2, self.y-crown.get_height()//2))

    def Move(self, row, col):
        '''
        Moves piece to choosen grid position
        
        Input >>> row, col = destination grid positions 
        '''
        self.row = row
        self.col = col
        self.CalcPos()

    def __repr__(self):
        '''
        Sets the representation of the instance to the piece color
        '''
        return str(self.color)