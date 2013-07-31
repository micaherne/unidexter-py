
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
            print(self.engine.toUCINotation(m))
        return nodes
    
if __name__ == '__main__':
    file = open('perftsuite.epd', 'r')
    e = SimpleEngine()
    p = Perft(e)
    depth = 1
    for line in file:
        parts = line.split(';')
        fen = parts[0]
        e.fenPos(fen)
        e.printPosition()
        nodes = p.perft(depth)
        print(nodes, parts[depth])
        