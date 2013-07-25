'''
Created on 25 Jul 2013

@author: michael
'''
from threading import Thread
from threading import Event
import time

class Engine():
    '''
    The base engine class. This provides the analysis threading mechanism and should
    be overridden to implement an actual analysis engine.
    '''

    stop_event = None

    def __init__(self):
        '''
        Constructor
        '''
        self.analysisThread = None
        
    def go(self):
        self.stop_event = Event()
        self.analysisThread = Thread(target=self.startAnalysis, args=[self.stop_event], group=None)
        self.analysisThread.start()
        
    def stop(self):
        self.stop_event.set()
                
    def startPos(self):
        print("Not implemented")
        
    def fenPos(self, fen):
        print("Not implemented")
        
    def printPosition(self):
        print("Not implemented")
        
    def moveUCI(self, moveNotation):
        """ Make the move given by the UCI string representation of the move (e.g. "e2e4") """
        print("Not implemented")
        
    def startAnalysis(self, stop_event):
        print("Not implemented")

        
class SimpleEngine(Engine):
    
    count = 0
    board = [0]*128
    whiteToMove = None
    castling = [True, True, True, True] # K, Q, k, q
    epSquare = None
    halfMove = 0
    fullMove = 0
        
    
    # Uses piece values from Robert Hyatt's article
    PAWN = 1
    KNIGHT = 2
    KING=3
    BISHOP=5
    ROOK=6
    QUEEN=7
    
    # Not used, just for reference!
    WHITE = 1
    BLACK = -1
    
    representation = { 0: " ", 1: "P", 2: "N", 3: "K", 5: "B", 6: "R", 7: "Q"}
    notationRepresentation = {v:k for k, v in representation.items()} # flip keys and values
    
    def startPos(self):
        pieces = [self.ROOK, self.KNIGHT, self.BISHOP, self.QUEEN, self.KING, self.BISHOP, self.KNIGHT, self.ROOK]
        
        self.board = [0] * 128
        for i in range(8):
            self.board[i] = pieces[i]
            self.board[i+16] = self.PAWN
            self.board[i+16*6] = -self.PAWN
            self.board[i+16*7] = -pieces[i]
            
        self.whiteToMove = True
        self.castling = [True, True, True, True]
        self.epSquare = None
        self.halfMove = 0
        self.fullMove = 0
         
    def fenPos(self, fen):
        fenParts = fen.split(" ")
        boardParts = fenParts[0].split("/")
        
        if len(boardParts) != 8:
            raise Exception("FEN must have 8 parts for board")
        
        self.board = [0] * 128
        for i in range(8):
            rank = 7 - i
            part = boardParts[i]
            file = 0
            for c in list(part):
                if c.upper() in self.notationRepresentation:
                    self.board[file + 16*rank] = self.notationRepresentation[c.upper()] * (1 if c.istitle() else -1)
                elif c.isdigit():
                    c = int(c)
                    for _ in range(c):
                        self.board[file + 16*rank] = 0
                        file += 1
                else:
                    raise Exception("Invalid character in FEN:", c)
                
                file += 1
                
        if (fenParts[1] == 'w'):
            self.whiteToMove = True
        elif (fenParts[1] == 'b'):
            self.whiteToMove = False
        else:
            raise Exception("Invalid to-move value")
        
        castling = ['K', 'Q', 'k', 'q']
        for i in range(4):
            if castling[i] in fenParts[2]:
                self.castling[i] = True
            else:
                self.castling[i] = False
                
        # e.p. square
        epString = fenParts[3]
        if epString != '-':
            self.epSquare = self._notationToSquare(fenParts[3])
            
        # half move
        if len(fenParts) > 4:
            self.halfMove = int(fenParts[4])
            
        # full move
        if len(fenParts) > 5:
            self.fullMove = int(fenParts[5])
            
    def _notationToSquare(self, notation):
        """ Convert a two character algebraic square notation (e.g. "d4") to a board offset """

        file = ord(notation[0]) - ord('a')
        rank = int(notation[1]) - 1
        return file + 16*rank
            
    def printPosition(self):
        
        separator = "+-" * 8 + "+"
        for rank in range(7, -1, -1):
            print(separator)
            row = []
            for file in range(8):
                piece = self.board[file + rank * 16]
                r = self.representation[abs(piece)]
                if piece < 0:
                    r = r.lower()
                row.append(r)
            print("|" + "|".join(row) + "|")
        print(separator)
        
    def moveUCI(self, moveNotation):
        frm = moveNotation[:2]
        t = moveNotation[2:4]
        move = [self._notationToSquare(frm), self._notationToSquare(t), None]
        if len(t) > 4:
            move[2] = self.notationRepresentation[t[4].upper()]
        self.move(move)
        
    def move(self, move):
        if move[0] == 7: self.castling[0] = False
        if move[0] == 0: self.castling[1] = False
        if move[0] == 119: self.castling[2] = False
        if move[0] == 112: self.castling[3] = False
        
        if self.board[move[0]] == self.KING: 
            self.castling[0:1] = [False, False]
        
        if self.board[move[0]] == -self.KING: 
            self.castling[2:3] = [False, False]
        
        if abs(self.board[move[0]]) == self.PAWN or self.board[move[1]] != 0:
            self.halfMove = 0
            
        if abs(self.board[move[0]]) == self.PAWN and (abs(move[1] - move[0]) == 32):
            self.epSquare = (move[1] - move[0])/2 + move[0]
        else:
            self.epSquare = None
            
        # e.p. capture
        if abs(self.board[move[0]]) == self.PAWN and self.epSquare == move[1] and abs(move[1] - move[0]) % 16 != 0:
            epTakenPawn = (move[0] & 0x80) & (move[1] & 0x08) # move-from rank, move-to file
            self.board[epTakenPawn] = 0

        if move[2] == None:
            self.board[move[1]] = self.board[move[0]]
        else:
            self.board[move[1]] = move[2] # pawn promotion
            
        self.board[move[0]] = 0
    
        
        
    def startAnalysis(self, stop_event):
        while (not stop_event.is_set()):
            self.count += 1
            time.sleep(0.01);
        
        print("Analysis stopped")
    
        