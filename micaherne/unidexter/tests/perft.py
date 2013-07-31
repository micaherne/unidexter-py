
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
            #print(self.engine.toUCINotation(m))
        return nodes
    
    def divide(self, depth):
        moves = self.engine.generateMoves()
        nodeCount = 0
        for m in moves:
            undoData = self.engine.move(m)
            if(depth < 2):
                m2 = 1
            else:
                m2 = self.perft(depth - 1)
            nodeCount += m2
            print(self.engine.toUCINotation(m), m2)
            self.engine.undoMove(undoData)
            
        print("Moves: ", len(moves))
        print("Nodes: ", nodeCount)
    
if __name__ == '__main__':
    results = [0]*2
    file = open('perftsuite.epd', 'r')
    e = SimpleEngine()
    p = Perft(e)
    depth = 3
    for line in file:
        parts = line.split(';')
        fen = parts[0]
        e.fenPos(fen)
        print(fen)
        e.printPosition()
        nodes = p.perft(depth)
        depthParts = parts[depth].split()
        correctNodes = int(depthParts[1])
        print(nodes, parts[depth])
        if correctNodes == nodes:
            print("Correct!")
            results[0] += 1
        else:
            print("Incorrect!")
            results[1] += 1
    print(results[0], " correct, ", results[1], " incorrect")
            
        