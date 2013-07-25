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
    fenRepresentation = {v:k for k, v in representation.items()} # flip keys and values
    
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
                if c.upper() in self.fenRepresentation:
                    self.board[file + 16*rank] = self.fenRepresentation[c.upper()] * (1 if c.istitle() else -1)
                elif c.isdigit():
                    c = int(c)
                    for s in range(c):
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
            file = ord(epString[0]) - ord('a')
            rank = int(epString[1]) - 1
            self.epSquare = file + 16*rank
            
        # half move
        if len(fenParts) > 4:
            self.halfMove = int(fenParts[4])
            
        # full move
        if len(fenParts) > 5:
            self.fullMove = int(fenParts[5])
            
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
        
    def startAnalysis(self, stop_event):
        while (not stop_event.is_set()):
            self.count += 1
            time.sleep(0.01);
        
        print("Analysis stopped")
    
        