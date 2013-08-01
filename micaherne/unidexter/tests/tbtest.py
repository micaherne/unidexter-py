'''
Created on 1 Aug 2013

@author: michael
'''
import unittest
import tb
from micaherne.unidexter.tests.tb import Piece


class Test(unittest.TestCase):
    
    def testSetInit(self):
        e = tb.Engine()
        self.assertFalse(e.set.epmarker == None)

    def testPlacePiece(self):
        e = tb.Engine()
        self.assertIsNot(e.r, e.f)
        self.assertIsNot(e.r[0], e.f[5])
        self.assertIsNot(e.r[0], e.r[7])
        rook = e.set.getUnusedPiece(6, 0)
        e.placePiece(rook, 0, 7)
        self.assertEqual(Piece.ROOK, rook.pieceType)
        self.assertEqual(Piece.BLACK, rook.colour)
        self.assertIs(e.f[0], rook.f)
        self.assertIs(e.r[7], rook.r)
        self.assertIsNot(e.r[0], e.r[7])
        self.assertIs(e.d1[0], rook.d1)
        self.assertIs(e.d1[0][0], rook)
        self.assertIsNot(e.d1, e.d2)
        self.assertIs(e.d2[7], rook.d2)
        self.assertIs(e.d2[7][0], rook)
        
        queen = e.set.getUnusedPiece(7, 1)
        e.placePiece(queen, 3, 4)
        self.assertEqual(Piece.QUEEN, queen.pieceType)
        self.assertEqual(Piece.WHITE, queen.colour)
        
        self.assertIs(e.f[3], queen.f)
        self.assertIs(e.r[4], queen.r)
        self.assertIs(e.d1[6], queen.d1)
        self.assertIs(e.d2[7], queen.d2)
        self.assertIs(e.d1[6][3], queen)
        self.assertIs(e.d2[7][3], queen)
        
        
    def testFromFEN(self):
        e = tb.Engine()
        e.fromFEN('r3k2r/p1ppqpb1/bn2pnp1/3PN3/Pp2P3/2N2Q1p/1PPBBPPP/R3K2R b KQkq a3 0 1')
        
        self.assertEqual(e.f[0][2].pieceType, Piece.EPMARKER)
        
        self.assertEqual(0, e.halfmove)
        self.assertEqual(1, e.fullmove)
        
    def testStartPos(self):
        e = tb.Engine()
        e.startPos()
        # rookA8 = e.f[0][7]
        rookA8 = e.r[7][0]
        self.assertEqual(Piece.ROOK, rookA8.pieceType, "Rook at rookA8")
        self.assertEqual(Piece.BLACK, rookA8.colour, "Black rook at rookA8")
        self.assertIs(e.f[0], rookA8.f, "rookA8 rook on file 0")
        self.assertIs(e.r[7], rookA8.r)
        
        self.assertTrue(e.wtm)
        
        self.assertTrue(e.castling[0])
        self.assertTrue(e.castling[1])
        self.assertTrue(e.castling[2])
        self.assertTrue(e.castling[3])
        
        
    def testPositionToString(self):
        e = tb.Engine()
        e.startPos()
        
    def testGeneratePseudoLegalMoves(self):
        e = tb.Engine()
        e.startPos()
        #m = e.generatePseudoLegalMoves()
        #print(m)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()