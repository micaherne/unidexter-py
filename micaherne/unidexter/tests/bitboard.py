'''
Created on 5 Aug 2013

@author: michael
'''
import unittest
from micaherne.unidexter.bitboard import Board


class Test(unittest.TestCase):


    def setUp(self):
        self.bb = Board()

    def tearDown(self):
        pass


    def testStartPos(self):
        self.bb.startPos()
        self.assertEqual(1, self.bb.rooks >> 63)
        self.assertTrue(self.bb.isSet(self.bb.knights, 62))
        self.assertFalse(self.bb.isSet(self.bb.bishops, 62))
        
    def testStr(self):
        self.bb.startPos()
        
    def testToStr(self):
        self.bb.startPos()
        self.assertEqual('e5', self.bb.toSquare(36))
        
    def testToFEN(self):
        self.bb.startPos()
        self.assertEqual("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", self.bb.toFEN())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testStartPos']
    unittest.main()