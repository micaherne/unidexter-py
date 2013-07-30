'''
Created on 25 Jul 2013

@author: michael
'''
import unittest
from micaherne.unidexter.engine import SimpleEngine


class Test(unittest.TestCase):


    def setUp(self):
        self.engine = SimpleEngine()


    def tearDown(self):
        pass


    def testFEN(self):
        initFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e5 0 1"
        self.engine.fenPos(initFEN)
        self.assertEqual(6, self.engine.board[0], "White rook on a1")
        self.assertEqual(68, self.engine.epSquare, "e.p. square is e5")
        
        fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        self.engine.fenPos(fen)
        self.assertEqual(3, self.engine.board[4], "King on e1")
        self.assertEqual(6, self.engine.board[7], "White rook on h1")
        
    def testEp(self):
        fen = "position startpos moves e2e4 g8f6 e4e5 d7d5 e5d6"
        
    def testGenerateMoves(self):
        self.engine.startPos()
        #self.engine.moveUCI("d2d4")
        #self.engine.moveUCI("d7d5")
        moves = self.engine.generateMoves()
        self.assertEqual(20, len(moves))
        
    def testGenerateCastlingMoves(self):
        fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        self.engine.fenPos(fen)
        moves = self.engine.generateCastlingMoves(4)
        self.assertEqual(2, len(moves), "Both white castling moves found")

        
    def testMove(self):
        self.engine.startPos()
        undoData = self.engine.moveUCI("h2h4")
        self.assertEqual(39, self.engine.epSquare, "e.p. square set")
        undoData = self.engine.moveUCI("h7h5")
        self.assertEqual(87, self.engine.epSquare, "e.p. square set")
        self.engine.undoMove(undoData)
        self.assertEqual(39, self.engine.epSquare, "e.p. square set")

    def testUndo(self):
        self.engine.startPos()
        undoData = self.engine.move([20, 52, None])
        self.engine.undoMove(undoData)
        self.assertTrue(self.engine.whiteToMove, "White to move")
        self.assertEquals(1, self.engine.board[20])
        
    def testGenerateSliderMoves(self):
        self.engine.startPos()
        self.engine.moveUCI("e2e4")
        self.engine.moveUCI("e7e5")
        kingBishopMoves = self.engine.generateSliderMoves(5, self.engine.DIAGONALMOVES)
        self.assertEqual(5, len(kingBishopMoves), "5 king bishop moves after symmetrical e-pawn opening")
        self.engine.moveUCI("a2a3")
        kingBishopMoves = self.engine.generateSliderMoves(117, self.engine.DIAGONALMOVES)
        self.assertEqual(5, len(kingBishopMoves), "5 king bishop moves after symmetrical e-pawn opening + a3")
        
        fen = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
        self.engine.fenPos(fen)
        moves = self.engine.generateSliderMoves(0, self.engine.LINEARMOVES)
        for m in moves:
            self.assertNotEqual(4, m, "Can't move to king square")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEngine']
    unittest.main()