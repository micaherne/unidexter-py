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
        
    def testEp(self):
        fen = "position startpos moves e2e4 g8f6 e4e5 d7d5 e5d6"
        
    def testGenerateMoves(self):
        self.engine.startPos()
        #self.engine.moveUCI("d2d4")
        #self.engine.moveUCI("d7d5")
        moves = self.engine.generateMoves()
        for m in moves:
            print(m[0], m[1])
        self.assertEqual(20, len(moves))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEngine']
    unittest.main()