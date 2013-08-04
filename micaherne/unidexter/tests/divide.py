'''
Created on 31 Jul 2013

@author: michael
'''

from micaherne.unidexter.tests.perft import Perft
from micaherne.unidexter.engine import Engine, SimpleEngine

if __name__ == '__main__':
    e = SimpleEngine()
    p = Perft(e)
    #e.fenPos('r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 0 1')
    #e.moveUCI("e8g8")
    #e.fenPos('r4rk1/8/8/8/8/8/8/R3K2R w KQ - 0 1')
    #e.fenPos('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1 ')
    e.fenPos('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1')
    e.fenPos('r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1 ')
    
    e.fenPos('r3k2r/p1ppqNb1/1n2pnp1/1b1P4/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1')
    
    p.divide(2)
    