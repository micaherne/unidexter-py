'''
Created on 25 Jul 2013

@author: michael
'''
import sys
import time

from micaherne.unidexter.engine import Engine

class UciController:
    
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
        
        self.debug = 0
        
        self.engine = None

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
                try:
                    return self.commands[keyword](data)
                except KeyError:
                    print("Invalid command")
    
        # TODO: We should silently ignore commands we don't understand (UCI spec)
        print("No valid command found")
    
    '''
    Given a list of keywords, parse the values into a dictionary
    '''
    def parseKeywords(self, keywords, data):
        result = {}
        for k in keywords:
            result[k] = []
        
        currentKeyword = None
        
        while len(data) > 0:
            word = data.pop(0)
            if word in keywords:
                currentKeyword = word
                continue
            
            if currentKeyword != None:
                result[currentKeyword].push(word)
            else:
                raise
            
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
            debug = 1
            self.doInfo("string debugging switched on")
            
        if data[0] == 'off':
            debug = 0
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
        print("position not implemented")
    
    def doGo(self, data):
        print("go not implemented")
    
    def doStop(self, data):
        print("stop not implemented")
    
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
    controller.engine = Engine()
    controller.run()