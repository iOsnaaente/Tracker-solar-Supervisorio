from Tracker.Sun.mySunposition    import *
from pinout          import *
from constants       import * 
import math 

class FAKE_TIME:
    FAKE_TIME     = [ ]
    minutes_diff  = 0.0
    seconds_diff  = 0.0
    new_day       = False 
    SUNRISE       = [ ]
    SUNSET        = [ ]
    
    def __init__(self, LOCALIZATION, TIME ):
        self.TIME = TIME
        self.FAKE_TIME = TIME
        self.LOCALIZATION = LOCALIZATION 
    
    def compute_new_day(self ):
        self.TIME[2] = self.TIME[2]+1
        self.SUNRISE, self.SUNSET = get_twilights( self.LOCALIZATION, self.TIME )
        self.FAKE_TIME = self.SUNRISE

    def compute( self ):
        self.FAKE_TIME[5] += 0
        self.FAKE_TIME[4] += 1
        if self.FAKE_TIME[5] >= 60:
            self.FAKE_TIME[5] %= 60
            self.FAKE_TIME[4] += 1
        if self.FAKE_TIME[4] >= 60:
            self.FAKE_TIME[4] %= 60
            self.FAKE_TIME[3] += 1
            if self.FAKE_TIME[3] >= 24:
                self.FAKE_TIME[3] = 0
                self.FAKE_TIME[2] += 1
                if self.FAKE_TIME[1] == 2: 
                    if ANB(self.FAKE_TIME[0]) :  DOM[1] = 29 
                    else:                        DOM[1] = 28 
                if self.FAKE_TIME[2] > DOM[self.FAKE_TIME[1]]:
                    self.FAKE_TIME[2] = 1 
                    self.FAKE_TIME[1] += 1
                    if self.FAKE_TIME[1] > 12: 
                        self.FAKE_TIME[1] = 1
                        self.FAKE_TIME[0] += 1

        self.FAKE_TIME = [ int(d) for d in self.FAKE_TIME ]
        return self.FAKE_TIME 

