'''
Created on 5 Aug 2013

@author: michael
'''
from micaherne.unidexter.engine import Engine

class BitboardEngine(Engine):
    
    def __init__(self):
        Engine.__init__(self)
        
class Board():
    
    rooks = 0
    knights = 0
    bishops = 0
    queens = 0
    kings = 0
    pawns = 0
    
    whitePieces = 0
    blackPieces = 0
    
    castle = 0
    epSquare = 0
    halfmove = 0
    fullmove = 0 
    
    whiteToMove = None
    
    def startPos(self):
        p = lambda x: x << 56 | x
        self.rooks   = p(0b10000001)
        self.knights = p(0b01000010)
        self.bishops = p(0b00100100)
        self.queens  = p(0b00010000)
        self.kings   = p(0b00001000)
        
        self.pawns   = 0xFF << 48 | 0xFF << 8
        self.whitePieces = 0xFFFF
        self.blackPieces = self.whitePieces << 48
        
        self.castle = 0b1111 # KQkq
        self.epSquare = None
        self.halfmove = 0
        self.fullmove = 1
        self.whiteToMove = True
        
    def __str__(self):
        p = { 'R': self.rooks, 'N': self.knights, 'B': self.bishops, 'Q': self.queens, 'K': self.kings, 'P': self.pawns }
        separator = "+-" * 8 + "+\n"
        result = separator
        for s in range(63, -1, -1):
            result += '|'
            thingS = ' '
            for k,v in p.items():
                if self.isSet(v, s):
                    if self.isSet(self.whitePieces, s):
                        thingS = k.upper()
                        continue
                    elif self.isSet(self.blackPieces, s):
                        thingS = k.lower()
                        continue
                    else:
                        raise Exception("No colour set for piece " + str(s))
            result += thingS
            if s % 8 == 0:
                result += "|\n" + separator
        return result
    
    def toFEN(self):
        p = { 'R': self.rooks, 'N': self.knights, 'B': self.bishops, 'Q': self.queens, 'K': self.kings, 'P': self.pawns }
        resultParts = []
        ranks = []
        rankPart = ''
        spaces = 0
        for s in range(63, -1, -1):
            thingS = None
            for k,v in p.items():
                if self.isSet(v, s):
                    if spaces > 0:
                        rankPart += str(spaces)
                        spaces = 0
                    if self.isSet(self.whitePieces, s):
                        thingS = k.upper()
                        continue
                    elif self.isSet(self.blackPieces, s):
                        thingS = k.lower()
                        continue
                    else:
                        raise Exception("No colour set for piece " + str(s))
            
            if thingS != None:
                rankPart += thingS
            else:
                spaces += 1
            if s % 8 == 0:
                if spaces > 0:
                    rankPart += str(spaces)
                    spaces = 0
                ranks.append(rankPart)
                rankPart = ''
        resultParts.append("/".join(ranks))
        
        resultParts.append("w" if self.whiteToMove else "b")
        
        castling = []
        for i in range(4):
            if (self.castle & (1 << (3 - i))) != 0: 
                castling.append("KQkq"[i])
            
        resultParts.append("".join(castling))
        if self.epSquare == None:
            resultParts.append("-")
        else:
            resultParts.append(self.toSquare(self.epSquare))
        
        resultParts.append(str(self.halfmove))
        resultParts.append(str(self.fullmove))
        
        return " ".join(resultParts)
    
    def toSquare(self, index):
        return chr(ord('a') + (index & 0b111)) + str(1 + (index >> 3))
            
    def isSet(self, bitboard, bit):
        return (bitboard >> bit) & 1