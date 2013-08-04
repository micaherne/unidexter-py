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
        
        self.engine.fenPos('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1 ')
        self.engine.printPosition()
        self.engine.moveUCI("e5f7")
        self.engine.printPosition();
        
        engine2 = SimpleEngine()
        engine2.fenPos('r3k2r/p1ppqNb1/bn2pnp1/3P4/1p2P3/2N2Q1p/PPPBBPPP/R3K2R b KQkq - 0 1')

        engine2.printPosition()
    
        for i in range(128):
            self.assertEqual(self.engine.board[i], engine2.board[i], "Not the same " + str(i))
            
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
            
    def testGenerateCastlingMoves2(self):
        self.engine.fenPos('4k2r/8/8/8/8/8/8/5K2 b k - 0 1')
        moves = self.engine.generateCastlingMoves(0x74)
        self.assertEqual([False, False, True, False], self.engine.castling, "Black K-side castling should be set")
        self.assertEqual(1, len(moves), "Should be one valid move")
        #self.assertIn([0x74, 0x76], moves, "Should have h5h7")

    def testPerftPos1(self):
        fen = "4k3/8/8/8/8/8/8/4K2R w K - 0 1"
        self.engine.fenPos(fen)
        moves = self.engine.generateSliderMoves(7, self.engine.LINEARMOVES)
        self.assertEqual(9, len(moves), "Generate rook moves")
        moves = self.engine.generateMoves()
        self.assertEqual(15, len(moves), "Generate all moves")
        
    def testPerftPos2(self):
        fen = "7k/RR6/8/8/8/8/rr6/7K w - - 0 1"
        self.engine.fenPos(fen)
        moves = self.engine.generateSliderMoves(96, self.engine.LINEARMOVES)
        self.assertNotIn(0, moves, "a1 shouldn't be in moves")
        moves = self.engine.generateMoves()
        self.assertEqual(19, len(moves), "Correct number of moves")
        
    def testPerftPos3(self):
        fen = "k7/8/8/7p/6P1/8/8/K7 w - - 0 1"
        self.engine.fenPos(fen)
        #self.engine.printPosition()
        moves = self.engine.generateMoves();
        self.assertEqual(5, len(moves), "5 moves generated")
        
    def testMove2(self):
        fen = "4k3/8/8/8/8/8/8/R3K3 w Q - 0 1"
        self.engine.fenPos(fen)
        self.engine.moveUCI("e1c1")
        self.assertEqual(6, self.engine.board[3])
        
    def testMove3(self):
        self.engine.fenPos('4k3/8/8/8/8/8/8/R3K3 w Q - 0 1 ')
        self.engine.moveUCI("e1d1")
        self.assertEqual([False] * 4, self.engine.castling)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEngine']
    unittest.main()