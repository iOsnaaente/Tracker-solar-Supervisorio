import machine, utime

class RTC(object):
    def __init__(self, year : int, month : int, day : int, hour : int, minutes : int, seconds : int ) -> None:
        self.set_datetime( year, month, day, hour, minutes, seconds ) 

    def set_datetime(self, year : int, month : int, day : int, hour : int, minutes : int, seconds : int ):
        t  = utime.localtime( utime.mktime ( [ year, month, day, hour, minutes, seconds, 0, 0 ] ) )
        o  = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334 ]
        f  = int( not t[1] > 2)
        a  = t[0] - 1700 - f
        d  = ((5 + (a + f) * 365) + (a // 4 - a // 100 + (a + 100) // 400) + (o[t[1] - 1] + (t[2] - 1))) % 7 
        machine.mem32[0x4005c004] = (t[0] << 12) | (t[1] << 8) | t[2]
        machine.mem32[0x4005c008] = d << 24 |(t[3] << 16) | (t[4] << 8) | t[5]
        machine.mem32[0x4005c00c] = machine.mem32[0x4005c00c] | 0x10
        
    def get_datetime(self) :
        date = list(utime.localtime()[:-2])
        date[0] -= 2000
        return date
    
    @property
    def year ( self ) :
        return self.get_date()[0]
    @property
    def month ( self ) :
        return self.get_date()[1]
    @property
    def day ( self ) :
        return self.get_date()[2]

    @property
    def hours ( self ) :
        return self.get_hour()[0]
    @property
    def minutes ( self ) :
        return self.get_hour()[1]
    @property
    def seconds ( self ) :
        return self.get_hour()[2]
    
    def get_date( self ):
        return self.get_datetime()[:3]

    def get_hour( self ):
        return self.get_datetime()[3:6]
    
    def get_day_of_week(self):
        return self.get_datetime()[7]
    
    

def main_RTC(): 
    from Tracker.Time.myDS3231 import DS3231
    from pinout                import SDA_DS, SCL_DS
    import time 
    
    isc = machine.I2C( 0, sda = machine.Pin( SDA_DS ), scl = machine.Pin( SCL_DS ), freq = 10000  ) 
    DS  = DS3231  ( isc )

    y, m, d, h, n, s, _ = DS.now()
    rtc = RTC( y +2000 , m, d, h, n, s )

    while True:
        print( '\n\n\n\n')
        print("Datetime pico:\t", rtc.get_datetime() )
        print("Datetime DS:\t", DS.now() )
        print( rtc.hours, rtc.minutes, rtc.seconds ) 
        
        time.sleep(1)
    

if __name__ == '__main__':
    main_RTC() 
    
    
    
    
    
    
    
    
    
    