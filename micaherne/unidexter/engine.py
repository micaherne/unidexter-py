'''
Created on 25 Jul 2013

@author: michael
'''
from threading import Thread
from threading import Event
import time
import math

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
        
    def go(self, params):
        self.stop_event = Event()
        self.analysisThread = Thread(target=self.startAnalysis, args=[params, self.stop_event], group=None)
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
        
    def startAnalysis(self, params, stop_event):
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
    
    # Move lists. These give offsets for the different types of piece
    KNIGHTMOVES = [-33, -31, -18, -14, 14, 18, 31, 33]
    DIAGONALMOVES = [-17, -15, 15, 17]
    LINEARMOVES = [-16, -1, 1, 16]
    
    
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
        
        # e.p. capture
        if abs(self.board[move[0]]) == self.PAWN and self.epSquare == move[1] and abs(move[1] - move[0]) % 16 != 0:
            epTakenPawn = ((move[0] & 0xF0) + (move[1] & 0x0F)) # move-from rank, move-to file
            self.board[epTakenPawn] = 0

        # set e.p. square
        if abs(self.board[move[0]]) == self.PAWN and (abs(move[1] - move[0]) == 32):
            self.epSquare = (move[1] - move[0])/2 + move[0]
        else:
            self.epSquare = None
            
        
        if move[2] == None:
            self.board[move[1]] = self.board[move[0]]
        else:
            self.board[move[1]] = move[2] # pawn promotion
            
        self.board[move[0]] = 0
        
        self.whiteToMove = not self.whiteToMove
    
        
        
    def startAnalysis(self, params, stop_event):
        print(params)
        while (not stop_event.is_set()):
            self.count += 1
            time.sleep(0.01);
        
        print("Analysis stopped")
        
    # Move generation
    def generateMoves(self):
        result = []
        moverPieceLocations = []
        
        moverSign = self.WHITE if self.whiteToMove else self.BLACK
            
        for rank in range(8):
            for file in range(8):
                square = (rank << 4) + file
                if self.board[square] == 0:
                    continue
                if math.copysign(1, self.board[square]) == moverSign:
                    moverPieceLocations.append(square)
                    if abs(self.board[square]) == self.KING:
                        moverKing = square
        
        for moverSquare in moverPieceLocations:
            piece = self.board[moverSquare]
            assert piece != 0
            
            validSquares = []
            candidateMoves = []
            
            if abs(piece) != 1:
                piece = abs(piece)
            
            # Piece moves
            if piece == 2:
                if self.whiteToMove:
                    validSquares = [moverSquare + x for x in self.KNIGHTMOVES if moverSquare + x >= 0 
                                    and moverSquare + x & 0x88 == 0 and self.board[moverSquare + x] <= 0]
                else:
                    validSquares = [moverSquare + x for x in self.KNIGHTMOVES if moverSquare + x >= 0 
                                    and moverSquare + x & 0x88 == 0 and self.board[moverSquare + x] >= 0]
            
            elif piece == 3:
                if self.whiteToMove:
                    validSquares = [moverSquare + x for x in self.DIAGONALMOVES if moverSquare + x >= 0
                                    and moverSquare + x & 0x88 == 0 and self.board[moverSquare + x] <= 0]
                else:
                    validSquares = [moverSquare + x for x in self.DIAGONALMOVES if moverSquare + x >= 0 
                                    and moverSquare + x & 0x88 == 0 and self.board[moverSquare + x] >= 0]
                 
            elif (abs(piece) & 4) != 0: # slider (abs needed so we don't pick up black pawns)
                
                if (piece & 1) != 0: # it can move diagonally
                    currentSquares = [moverSquare + x for x in self.DIAGONALMOVES]
                    safetyCount = 0; # should always terminate, but we want to be safe
                    while currentSquares != [None]*4:
                        for ts in range(4):
                            if currentSquares[ts] == None:
                                continue
                            if currentSquares[ts] & 0x88 != 0:
                                currentSquares[ts] = None
                                continue
                            if self.whiteToMove:
                                if self.board[currentSquares[ts]] > 0:
                                    currentSquares[ts] = None
                                    continue
                            else:
                                if self.board[currentSquares[ts]] < 0:
                                    currentSquares[ts] = None
                                    continue
                            currentSquares[ts] += self.DIAGONALMOVES[ts]

                        validSquares += [x for x in currentSquares if x != None]
                    
                        safetyCount += 1
                        assert safetyCount < 8
                
                # TODO: Simplify? It's effectively same algorithm as diagonal sliders
                if (piece & 2) != 0: # it can move linearly
                    currentSquares = [moverSquare + x for x in self.LINEARMOVES]
                    safetyCount = 0; # should always terminate, but we want to be safe
                    while currentSquares != [None]*4:
                        for ts in range(4):
                            if currentSquares[ts] == None:
                                continue
                            if currentSquares[ts] & 0x88 != 0:
                                currentSquares[ts] = None
                                continue
                            if self.whiteToMove:
                                if self.board[currentSquares[ts]] > 0:
                                    currentSquares[ts] = None
                                    continue
                            else:
                                if self.board[currentSquares[ts]] < 0:
                                    currentSquares[ts] = None
                                    continue
                            currentSquares[ts] += self.LINEARMOVES[ts]

                        validSquares += [x for x in currentSquares if x != None]
                        
                        safetyCount += 1
                        assert safetyCount < 8
            
            # Pawn moves
            if abs(piece) == 1:
                if self.whiteToMove:
                    oneSquare = moverSquare + 16 
                    if oneSquare >= 0 and oneSquare & 0x88 == 0 and self.board[oneSquare] == 0:
                        # Add queening directly to candidate moves
                        if (oneSquare & 0xF0) == 0x70: # queened
                            for newPiece in [2, 5, 6, 7]:
                                candidateMoves.append([moverSquare, oneSquare, newPiece]);
                        else:
                            validSquares.append(oneSquare)
                        if (moverSquare & 0xF0) == 0x10: # it's on the 2nd rank
                            twoSquares = moverSquare + 32 
                            if twoSquares >= 0 and twoSquares & 0x88 == 0 and self.board[twoSquares] == 0:
                                validSquares.append(twoSquares)
                else:
                    oneSquare = moverSquare - 16 
                    if oneSquare >= 0 and oneSquare & 0x88 == 0 and self.board[oneSquare] == 0:
                        # Add queening directly to result
                        if (oneSquare & 0xF0) == 0x00: # queened
                            for newPiece in [-2, -5, -6, -7]:
                                candidateMoves.append([moverSquare, oneSquare, newPiece]);
                        else:
                            validSquares.append(oneSquare)
                        if (moverSquare & 0xF0) == 0x60: # it's on the 2nd rank
                            twoSquares = moverSquare - 32 
                            if twoSquares >= 0 and twoSquares & 0x88 == 0 and self.board[twoSquares] == 0:
                                validSquares.append(twoSquares)
                
                # e.p. capture
                if self.epSquare != None:
                    if self.whiteToMove and self.epSquare - moverSquare in [15, 17]:
                        validSquares.append(self.epSquare)
                    if not self.whiteToMove and moverSquare - self.epSquare in [15, 17]:
                        validSquares.append(self.epSquare)
                        
            # Castling
            # "castle-through" squares corresponding to self.castling. First value is king destination
            # TODO: Make sure we're not in check first
            castlingSquares = [[0x06, 0x05], [0x02, 0x01, 0x03], [0x76, 0x75], [0x72, 0x71, 0x73]]
            for i in range(4):
                if self.castling[i] == True:
                    canCastle = True
                    for s in castlingSquares[i]:
                        if self.board[s] != 0:
                            canCastle = False
                            break
                    if canCastle:
                        # TODO: validate moves don't castle through or into check
                        candidateMoves.append([moverKing, castlingSquares[i][0], None])
                    
            
            # Add move items to result from validSquares [moverSquare, validSquares[i]
            for v in validSquares:
                candidateMoves.append([moverSquare, v, None, self.board[moverSquare]])
                
            # test that candidate moves don't result in check (or leave us in check)
            for m in candidateMoves:
                # pretend to make the move
                undo = {m[0]: self.board[m[0]], m[1] : self.board[m[1]]}
                if abs(self.board[m[0]]) == self.PAWN:
                    if (m[0] & 0x0F) != (m[1] & 0x0F): # e.p. capture
                        captured = (m[0] & 0xF0) + (m[1] & 0x0F)
                        undo[captured] = self.board[captured]
                        self.board[captured] = 0
                # TODO: Need to check moving through check here
                self.board[m[1]] = self.board[m[0]]
                self.board[m[0]] = 0
                if not self.isCheck(moverKing):
                    result.append(m)
                for k in undo:
                    self.board[k] = undo[k]
                
        return result
    
    def isCheck(self, kingSquare):
        """ Determine whether the given king is in check.
        """
        king = self.board[kingSquare]
        if (abs(king) != self.KING):
            raise Exception("Not a valid king square")
        
        kingSign = math.copysign(1, king)
                    
        for m in self.KNIGHTMOVES:
            testSquare = kingSquare + m
            if (testSquare & 0x88) == 0 and self.board[testSquare] == -1 * kingSign * self.KNIGHT:
                return True
            
        for m in self.DIAGONALMOVES:
            first = self.firstPiece(kingSquare, m)
            if first != None and first > 2:
                if math.copysign(1, first) != kingSign and (abs(first) & 1) != 0:
                    return True
                
        for m in self.LINEARMOVES:
            first = self.firstPiece(kingSquare, m)
            if first != None and first > 2:
                if math.copysign(1, first) != kingSign and (abs(first) & 2) != 0:
                    return True
        
        # Pawn attacks
        for m in [int(kingSign*x) for x in [15, 17]]:
            if self.board[kingSquare + m] == (-1 * kingSign):
                return True
            
        return False
            
     
    def firstPiece(self, square, direction):
        ''' Find the first piece along a ray in the given direction '''
        currentSquare = square + direction
        while (currentSquare) & 0x88 == 0:
            if (self.board[currentSquare] != 0):
                return self.board[currentSquare]
            currentSquare += direction

        return None