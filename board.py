from constants import GREY, WHITE, BLACK, LIGHTBROWN, DARKBROWN, rows, cols, tilesize, boardXLoc, boardYLoc
import pygame as pg
import itertools
import numpy as np
from pieces import Piece
from ui import UI

class Board:
    '''
    Board class
    Initialises and draws the board to the screen
    '''
    def __init__(self):
        self.board = []
        self.blackLeft = self.whiteLeft = 12
        self.blacKings = self.whiteKings = 0
        self.CreateBoard()
    
    def DrawTiles(self, win):
        '''
        Draws the back ground board

        Input >>> win = pygame window to draw on 
        '''
        win.fill(GREY)
        for row in range(rows):
            for col in range(rows):
                if (col+row)%2:
                    # The grid is offset by boardYloc and boardXloc to give a border
                    pg.draw.rect(win, LIGHTBROWN, (row*tilesize+boardYLoc, col*tilesize+boardXLoc, tilesize, tilesize))
                else:
                    pg.draw.rect(win, DARKBROWN, (row*tilesize+boardYLoc, col*tilesize+boardXLoc, tilesize, tilesize))

    def Move(self, piece, row, col):
        '''
        Moves a piece to a specified tile, if it is an allowed move
        
        Input >>> piece = selected piece
                  row, col = row and column to move to
        '''
        # This swaps the places in the 2D list so a 0 is where the piece used to be
        self.board[piece.row][piece.col], self.board[row][col] =  self.board[row][col], self.board[piece.row][piece.col]
        piece.Move(row, col)

        # Checks if the piece is on the final row, if so it becomes a king
        if row == rows-1 or row == 0:
            piece.King()

            if piece.color == WHITE:
                self.whiteKings+=1
            else:
                self.blacKings+=1
    
    def GetPiece(self, row, col):
        '''
        selects a row and column
        
        Input >>> row, col = row and columns choosen

        Output >>> self.board[row][col] = the state of that board position (0 for empty and piece for occupied)
        '''
        return(self.board[row][col])
    
    def CreateBoard(self):
        '''
        Creates a 2D list storing the intial board state
        0 for empty space and black and white pieces on the occupied spaces
        '''

        for row in range(rows):
            self.board.append([])
            for col in range(rows):
                # Here we skip every other spot to give the checkers positioning
                if col%2 == ((row+1)%2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def Draw(self, win):
        '''
        Draws the tiled board and the pieces where there isn't a 0 in the board state
        
        Input >>> win = pygame.window to draw on
        '''
        self.DrawTiles(win)
        for row in range(rows):
            for col in range(rows):
                piece = self.board[row][col]
                if piece != 0:
                    piece.Draw(win)
    
    def Remove(self, pieces):
        '''
        Sets board state of taken piece to 0 so it is not drawn
        
        Input >>> pieces = list of taken pieces
        '''
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.whiteLeft -= 1
                else:
                    self.blackLeft -= 1

    def Winner(self):
        if self.whiteLeft <= 0:
            return BLACK
        elif self.blackLeft <= 0:
            return WHITE
        else:
            return None

    def GetAvailableMoves(self, piece):
        '''
        Finds the available moves based on the selected piece.
        The available moves are stored in a dictionary
        
        Input >>> piece = selected piece
        
        Output >>> moves = dictionary of available moves
        '''
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # Check the piece color and if it is a king to get the correct moves
        if piece.color == WHITE or piece.king:
            moves.update(self._MoveLeft(row - 1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._MoveRight(row - 1, max(row-3, -1), -1, piece.color, right))
        
        if piece.color == BLACK or piece.king:
            moves.update(self._MoveLeft(row + 1, min(row+3, rows), 1, piece.color, left))
            moves.update(self._MoveRight(row + 1, min(row+3, rows), 1, piece.color, right))

        return moves
    
    def _MoveLeft(self, start, stop, step, color, left, skipped=[]):
        '''
        Finds the possible moves going to the left (up or down)
        
        Input >>> start = row to start looking for available spaces
                  stop = row to stop looking for availble spaces 
                  step = size of step (number of cols, rows stepping)
                  color = piece.color what team the piece is from to determine the move direction
                  left = column to the left of the current column
                  skipped = list to store skipped over pieces
        
        Output >>> moves = dictionary of available moves
                '''
        # Dictionary for moves and list for last piece we jumped
        moves = {}
        last = []
        
        # Look at rows up to three away (multi jump)
        for r in range(start, stop, step):
            if left < 0:
                # If at edge of board no moves 
                break
            
            current = self.board[r][left] # position in question 
            if current == 0:
                # If space is empty look ahead and check what spaces are available to move to 
                # This function is called recursively to check for multijumps
                if skipped and not last:
                    # if space 1 in front is free but we have skipped it is not available 
                    break

                elif skipped:
                    # if there is a space behind an enemy piece add it as available
                    moves[(r, left)] = last + skipped
                else:
                    # if we haven't moved yet free places in front are available
                    moves[(r, left)] = last 

                if last:
                    # If there was a piece we can check how close to the edge of the board we are
                    # And call this function again to search
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, rows)

                    # Search spaces ahead again
                    moves.update(self._MoveLeft(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._MoveRight(r+step, row, step, color, left+1, skipped=last))
                break

            elif current.color == color:
                # Can't jump over same color
                break
            
            else:
                # if there was a piece in front keep the position to check for skips
                last = [current]
            left -= 1

        return moves

    def _MoveRight(self, start, stop, step, color, right, skipped=[]):
        '''
        Finds the possible moves going to the right (up or down)
        
        Input >>> start = row to start looking for available spaces
                  stop = row to stop looking for availble spaces 
                  step = size of step (number of cols, rows stepping)
                  color = piece.color what team the piece is from to determine the move direction
                  right = column to the right of the current column
                  skipped = list to store skipped over pieces
        
        Output >>> moves = dictionary of available moves
        '''
        # Dictionary for moves and list for last piece we jumped
        moves = {}
        last = []
        
        # Look at rows up to three away (multi jump)
        for r in range(start, stop, step):
            if right >= cols:
                # If at edge of board no moves 
                break
            
            current = self.board[r][right] # position in question
            if current == 0:
                # If space is empty look ahead and check what spaces are available to move to 
                # This function is called recursively to check for multijumps
                if skipped and not last:
                    # if space 1 in front is free but we have skipped it is not available 
                    break
                elif skipped:
                    # if there is a space behind an enemy piece add it as available
                    moves[(r, right)] = last + skipped
                else:
                    # if we haven't moved yet free places in front are available
                    moves[(r, right)] = last

                if last:
                    # If there was a piece we can check how close to the edge of the board we are
                    # And call this function again to search
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, rows)

                    # Search spaces ahead again
                    moves.update(self._MoveLeft(r+step, row, step, color, right-1, skipped=last))
                    moves.update(self._MoveRight(r+step, row, step, color, right+1, skipped=last))
                break

            elif current.color == color:
                # Can't jump over same color
                break
            
            else:
                # if there was a piece in front keep the position to check for skips
                last = [current]
            right += 1
        
        return moves