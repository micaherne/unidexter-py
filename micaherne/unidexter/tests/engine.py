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
        
    def testTemp(self):
        a = "e2e4"
        b = a[2:4]
        self.assertEqual("e4", b, "Can't slice string properly")
        c = a[:2]
        self.assertEqual("e2", c, "Can't slice first bit properly")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testEngine']
    unittest.main()