from numpy import piecewise, tile
import pygame as pg
from board import Board
from ui import UI
from constants import WHITE, BLACK, BLUE, tilesize, boardXLoc, boardYLoc

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def Update(self):
        '''
        Update the game pieces and board 
        '''

        self.board.Draw(self.win)
        self.ui.DrawText(self.win)
        self.DrawAvailableMoves(self.availableMoves)
        if self.Winner()!=None:
            # If someone wins than add winner text
            self.ui.WinningText(self.win, self.Winner())

        # Update the pygame surface 
        pg.display.update()

    def _init(self):
        '''
        Private init function to set up the board on a reset as well as init
        '''
        self.selected = None
        self.board = Board()
        self.ui = UI()
        self.turn = WHITE
        self.availableMoves = {}

    def Reset(self):
        '''
        Resets the board state
        '''
        self._init()
    
    def Select(self, row, col):
        '''
        Select a piece to move or position to move to
        
        Input >>> row, col = grid position of wanted piece/place 
        
        Output >>> returns booleen True if selected piece and False if empty tile is selected
        '''
        if self.selected:
            # If piece already selected try and move to choosen point
            result = self._Move(row, col)
            if not result:
                # If invalid move, unselect piece 
                self.selected = None
                self.Select(row, col)

        # If no piece already selected, get location state
        piece = self.board.GetPiece(row, col)
        if piece != 0 and piece.color == self.turn:
            # If location isn't empty grab the piece and find the available moves
            self.selected = piece
            self.availableMoves = self.board.GetAvailableMoves(piece)
            return True
        else:
            # If empty space selected no available moves
            self.availableMoves = []

        return False

    def Winner(self):
        '''
        Check if someone has won
        '''
        return self.board.Winner()

    def _Move(self, row, col):
        '''
        private move function to move piece to new grid location
        
        Input >>> row, col = grid positions to move to
        
        Output >>> booleen False if invalid movement space
        '''
        piece = self.board.GetPiece(row, col)
        if self.selected and piece == 0 and (row, col) in self.availableMoves:
            # If choosen location is available for selected piece move there 
            self.board.Move(self.selected, row, col)
            skipped = self.availableMoves[(row, col)]
            if skipped:
                # If jumped pieces remove them from the board and update the counter
                self.board.Remove(skipped)
                self.ui.PiecesTaken(self.turn, len(skipped))
            self.ChangeTurn() # Switch turn
        else:
            return False
        
        return True

    def DrawAvailableMoves(self, moves):
        '''
        Draws dots for available moves
        
        Input >>> moves = dict of available movement positions
        '''
        for move in moves:
            row, col = move
            pg.draw.circle(self.win, BLUE, (col*tilesize + tilesize//2+boardXLoc, row*tilesize + tilesize//2+boardYLoc), radius=5)

    def ChangeTurn(self):
        '''
        Switches turns from white to black, resetting the available moves every time
        '''
        self.availableMoves = []
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE