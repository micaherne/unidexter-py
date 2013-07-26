'''
Created on 25 Jul 2013

@author: michael
'''
from micaherne.unidexter.engine import SimpleEngine
import sys
import time


class UciController:
    """ Analysis engine controller which speaks UCI """
    
    def __init__(self):
    
        self.commands = {'uci': self.doUCI,
                    'debug' : self.doDebug,
                    'isready' : self.doIsReady,
                    'setoption' : self.doSetOption,
                    'register' : self.doRegister,
                    'ucinewgame' : self.doUciNewGame,
                    'position' : self.doPosition,
                    'go' : self.doGo,
                    'stop' : self.doStop,
                    'ponderhit' : self.doPonderHit,
                    'quit' : self.doQuit
                    }
        
        self.debug = 1 # TODO: Change back to zero
        
        self.engine = None
        
    def setEngine(self, engine):
        self.engine = engine

    def run(self):
        while 1:
            try:
                time.sleep(0.005)
                line = sys.stdin.readline()
            except KeyboardInterrupt:
                break
        
            if not line:
                break
        
            self.doCommand(line)
            
    def doCommand(self, line):
        data = line.split()
    
        while len(data) > 0:
            keyword = data.pop(0)
            if keyword in self.commands:
                return self.commands[keyword](data)
    
        # TODO: We should silently ignore commands we don't understand (UCI spec)
        print("No valid command found")
    
    
    def parseKeywords(self, keywords, data):
        """ Given a list of keywords, parse the values into a dictionary """
        
        result = {}
        for k in keywords:
            result[k] = []
        
        currentKeyword = None
        
        while len(data) > 0:
            word = data.pop(0)
            if word in keywords:
                currentKeyword = word
            else:
                if currentKeyword != None:
                    result[currentKeyword].append(word)
                else:
                    raise Exception("Keyword not found")

        return result
    
    def output(self, line):
        print(line)
        
    # Output commands
    def doUCI(self, data):
        self.doId("name unidexter");
        self.doId("author Michael Aherne");
            
        #TODO: send options here
            
        self.doUciOk()
        
    def doDebug(self, data):
        if data[0] == 'on':
            self.debug = 1
            self.doInfo("string debugging switched on")
            
        if data[0] == 'off':
            self.debug = 0
            self.doInfo("string debugging switched off")
    
    # Input commands
    
    def doIsReady(self, data):
        self.doReadyOk()
    
    def doSetOption(self, data):
        print("setoption not implemented")
    
    def doRegister(self, data):
        print("register not implemented")
    
    def doUciNewGame(self, data):
        print("ucinewgame not implemented")
    
    def doPosition(self, data):
        keyword = data[0]
        if keyword == 'startpos':
            self.engine.startPos()
            subKeywords = {'moves' : data[2:]}
        elif keyword == 'fen':
            subKeywords = self.parseKeywords(['fen', 'moves'], data)
            self.engine.fenPos(" ".join(subKeywords['fen']))
        else:
            raise Exception("Invalid position type")

        for move in subKeywords['moves']:
            self.engine.moveUCI(move)

        if self.debug:
            self.engine.printPosition()
    
    def doGo(self, data):
        self.engine.go()
    
    def doStop(self, data):
        self.engine.stop()
    
    def doPonderHit(self, data):
        print("ponderhit not implemented")
    
    def doQuit(self, data):
        print("quit not implemented")
    
    # Output commands
    
    def doId(self, data):
        self.output("id " + data)
        
    def doUciOk(self):
        self.output("uciok")
        
    def doReadyOk(self):
        self.output("readyok")
    
    def doBestMove(self, move, ponder=None):
        result = ['bestmove', move];
        if ponder != None:
            result += ['ponder', ponder]
        self.output(" ".join(result))
        
    def doCopyProtection(self):
        pass
    
    def doRegistration(self):
        pass
    
    def doInfo(self, data):
        self.output("info " + data)
        
    def doOption(self, data):
        pass
    
    

# Just for testing
if __name__ == '__main__':
    controller = UciController()
    engine = SimpleEngine()
    controller.setEngine(engine)
    controller.run()