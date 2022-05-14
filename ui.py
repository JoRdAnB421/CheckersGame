import pygame as pg
from regex import B
from constants import BLACK, WHITE, boardXLoc, boardYLoc, height

class UI:
    def __init__(self):
        self.font = pg.font.Font(None, 56)
        self.blackTaken = self.whiteTaken = 0

    def DrawText(self, win):
        '''
        Draw the counting text
        
        Input >>> win = pygame.win surface to draw on
        '''
        self.textBlack = self.font.render(f"Black: {self.blackTaken} pieces taken", True, BLACK)
        self.blackTextPos = self.textBlack.get_rect(x=10, y = 20)

        self.textWhite = self.font.render(f"White : {self.whiteTaken} pieces taken", True, WHITE)
        self.whiteTextPos = self.textWhite.get_rect(x=10, y = height - 60)

        win.blit(self.textBlack, self.blackTextPos)
        win.blit(self.textWhite, self.whiteTextPos)

    def PiecesTaken(self, color, number):
        '''
        Track the pieces that have been taken for the text counters
        
        Input >>> color = color of player whose turn it is
                  number = number of pieces taken
        '''
        if color == BLACK:
            self.blackTaken += number
        else:
            self.whiteTaken += number

    def WinningText(self, win, color):
        '''
        Draw winning text if someone takes all oppenents pieces
        
        Input >>> win = pygame.win surface to draw on
                  color = colour of losing player
        '''

        winningFont = pg.font.Font(None, 150) # Set large font
        if color == WHITE:
            # If black wins, black text on white background
            winningText = winningFont.render(f"YOU WIN!!!", True, BLACK, WHITE)
        else: 
            # If white wins, black text on black background
            winningText = winningFont.render(f"YOU WIN!!!", True, WHITE, BLACK)
        
        # Set the position to center and draw
        winningTextPos = winningText.get_rect(centerx = height/2, centery = height/2)

        win.blit(winningText, winningTextPos)
            


