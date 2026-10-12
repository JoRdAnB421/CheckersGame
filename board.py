from constants import GREY, WHITE, BLACK, LIGHTBROWN, DARKBROWN, rows, cols, tilesize, boardXLoc, boardYLoc
import pygame as pg
import itertools
from pieces import Piece
from ui import UI

class Board:
    '''
    Board class
    Initialises and draws the board to the screen
    '''
    def __init__(self):
        self.board = []
        self.canTake = False
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
    
    def GetAllPieces(self, color):
        '''
        Gets the position of every piece for a given color useful in order to find all the available moves 
        (including the restriction to have to capture when possible)
        
        Input  >>> color = the players turn
        
        Output >>> pieces = list of every piece for this player
        '''
        pieces = []
        for j, row in enumerate(self.board):
            for i, col in enumerate(row):
                piece = self.GetPiece(i,j)
                if piece!=0 and piece.color==color:
                    pieces.append(piece)
        return pieces

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

    def GetAllMoves(self, color):
        '''
        Computes all the available moves of a given player
        '''
        pieces = self.GetAllPieces(color)
        moves={}
        for piece in pieces:
            moves[piece] = self.GetAvailableMoves(piece)
        
        return moves

    def GetAvailableMoves(self, piece):
        '''
        Finds the available moves based on the selected piece.
        The available moves are stored in a dictionary
        
        Input >>> piece = selected piece
        
        Output >>> moves = dictionary of available moves
        '''
        moves = {}
        directions = self._Directions(piece)

        # Single diagonal steps onto empty squares
        for dRow, dCol in directions:
            r, c = piece.row + dRow, piece.col + dCol
            if self._OnBoard(r, c) and self.board[r][c] == 0:
                moves[(r, c)] = []

        # Capture moves (including multi jumps)
        takes = self._FindJumps(piece, piece.row, piece.col, directions, [])

        if (self.canTake)&(len(takes)==0):
            return {}
        
        if len(takes)>0:
            # Some capture moves so limit to these
            self.canTake = True 
            moves = takes
        return moves

    def _Directions(self, piece):
        '''
        Finds the diagonal directions a piece is allowed to move in
        
        Input >>> piece = selected piece
        
        Output >>> directions = list of (row step, col step)
        '''
        directions = []
        if piece.color == WHITE or piece.king:
            directions += [(-1, -1), (-1, 1)]
        if piece.color == BLACK or piece.king:
            directions += [(1, -1), (1, 1)]
        return directions

    def _OnBoard(self, row, col):
        '''
        Checks if a grid position is on the board
        '''
        return 0 <= row < rows and 0 <= col < cols

    def _FindJumps(self, piece, row, col, directions, skipped):
        '''
        Finds the capture moves from a position, calling itself again from each landing square to find multi jumps.
        Kings search in all four directions at every step so they can change direction mid-chain
        
        Input >>> piece = piece that is moving
                  row, col = position to jump from
                  directions = directions the piece is allowed to move in
                  skipped = list of pieces already taken this turn
        
        Output >>> jumps = dictionary of landing squares and the pieces taken to get there
        '''
        jumps = {}
        for dRow, dCol in directions:
            landRow, landCol = row + 2*dRow, col + 2*dCol
            if not self._OnBoard(landRow, landCol) or self.board[landRow][landCol] != 0:
                # Need an empty square to land on
                continue

            middle = self.board[row + dRow][col + dCol]
            if middle == 0 or middle.color == piece.color or middle in skipped:
                # Can only jump an enemy piece, and only once per turn
                continue

            taken = skipped + [middle]
            found = {(landRow, landCol): taken}
            found.update(self._FindJumps(piece, landRow, landCol, directions, taken))

            for square, chain in found.items():
                # If two routes reach the same square keep the one that takes more pieces
                if len(chain) > len(jumps.get(square, [])):
                    jumps[square] = chain
        return jumps
