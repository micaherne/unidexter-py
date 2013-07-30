'''
Created on 29 Jul 2013

@author: michael
'''

from micaherne.unidexter.engine import Engine, SimpleEngine

class Perft():
    '''
    classdocs
    '''

    def __init__(self, engine):
        '''
        Constructor
        '''
        self.engine = engine
        
    def perft(self, depth):
        nodes = 0
        if depth == 0:
            return 1
        assert isinstance(self.engine, Engine)
        moves = self.engine.generateMoves()
        for m in moves:
            undoData = self.engine.move(m)
            nodes += self.perft(depth - 1)
            self.engine.undoMove(undoData)
        return nodes
    
if __name__ == '__main__':
    e = SimpleEngine()
    e.startPos()
    p = Perft(e)
    print(p.perft(2))
        