'''
Created on 25 Jul 2013

@author: michael
'''
from threading import Thread
from threading import Event
import time

class Engine():
    '''
    classdocs
    '''

    stop_event = None
    count = 0

    def __init__(self):
        '''
        Constructor
        '''
        self.analysisThread = None
        
    def go(self):
        self.stop_event = Event()
        self.analysisThread = Thread(target=self.startAnalysis, args=[self.stop_event], group=None)
        self.analysisThread.start()
        
    def stop(self):
        self.stop_event.set()
        
        print("Counted ", self.count, " hundredths of a second");
        
    def startAnalysis(self, stop_event):
        while (not stop_event.is_set()):
            self.count += 1
            time.sleep(0.01);
        
    
        