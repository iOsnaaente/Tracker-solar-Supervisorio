from Tracker.Time.myDS3231 import DS3231
from Tracker.Time.myRTC    import RTC

import machine
import time

class Datetime:
    
    RTC_DATETIME = [2000, 2, 20, 2, 20, 20, 3]
    DS_DATETIME  = [2000, 2, 20, 2, 20, 20, 3]
    
    RTC_AUTO : bool = False
    SYNC : bool = False 
    
    def __init__( self, I2C ):
        self.RTC = RTC( 2000, 2, 20, 2, 20, 20 ) 
        self.DS  = DS3231( I2C )
        

    def set_DS_datetime( self, yr : int, mt : int, dy : int, hr : int, mn : int, sc : int ):  
        try:
            self.DS.set_time( yr, mt, dy, hr, mn, sc )
            return self.SYNC  
        except:
            return self.SYNC 
        
    def set_RTC_datetime( self, yr : int, mt : int, dy : int, hr : int, mn : int, sc : int ):  
        try:
            if yr < 2000:
                yr += 2000 
            self.RTC.set_datetime( yr, mt, dy, hr, mn, sc )
            return self.SYNC 
        except:
            return self.SYNC 
            
    def get_JuliansDay(self, y, m, d):
        if m < 3:
            y = y -1 
            m = m +12 
        A = y // 100 
        B = A // 4 
        C = 2 -A +B
        # Funciona para datas posteriores de 04/10/1582
        D = int( 365.25 * ( y +4716 ) )
        E = int( 30.6001 * ( m +1 ) )
        DJ = D + E + d + 0.5 + C - 1524.5 
        return DJ 
    
    @property 
    def DS_STR(self):
        STR = '' 
        for b in self.DS.now()[:6]:
            STR += str(b) if b >= 10 else '0'+str(b)
        return STR 
    
    @property 
    def RTC_STR(self):
        STR = '' 
        for b in self.RTC.get_datetime():
            STR += str(b) if b >= 10 else '0'+str(b) 
        return STR
        
    @property 
    def SYNC(self):
        ds = int( self.DS_STR )
        rt = int(self.RTC_STR )
        return True if abs( ds - rt ) < 130 else False 
        
    def get_datetime( self ):
        return [ self.now(), self.SYNC ] 
    
    def now(self):
        return self.DS.now()




from pinout import *

def main_Datetime(): 
    isc = machine.I2C( 0, sda = machine.Pin( SDA_DS ), scl = machine.Pin( SCL_DS ), freq = 10000  ) 
    
    date = Datetime( isc )
    
    y,m,d,h,n,s,_ = date.now()
    
    date.set_RTC_datetime( y,m,d,h,n,s ) 
    
    print( date.SYNC, date.DS_STR, date.RTC_STR  )
    
    
if __name__ == '__main__':
    main_Datetime()
    