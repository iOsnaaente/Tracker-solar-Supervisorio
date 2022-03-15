from time import ticks_ms

class PID:
    actual_measure = 0
    last_measure   = 0
    
    error_rounded = 0
    error_real    = 0
    
    PV = 0.00
    Kp = 0.75
    Ki = 0.55
    Kd = 0.10
    
    dto = 0
    dti = 0
    dt  = 0 

    def __init__( self, PV : float, Kp : float, Kd : float, Ki : float ):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.PV = PV 
    
    @property 
    def pid( self ):
        return (self.Kp*self.error_rounded) + (self.Ki*((self.actual_measure-self.last_measure)*self.dt/2)) + (self.Kp*self.Kd*(self.error_rounded/self.dt)*self.actual_measure)
    
    def att(self, measure : float ):
        self.last_measure = self.actual_measure
        self.actual_measure = measure
        self.dto = ticks_ms()
    
    def set_PV(self, PV):
        self.PV = PV
    
    def get_params( self ):
        return [ self.Kd, self.Ki, self.Kp, self.PV ] 
        
    def compute(self, measure, tol : float = 0.25 ):
        
        self.error_real    = abs( self.PV - measure )
        self.error_rounded = 0 if round( self.error_real, 1 ) < tol else self.error_real 
        self.last_measure   = self.actual_measure
        self.actual_measure = measure
        
        self.dti = ticks_ms()
        self.dt  = self.dti - self.dto 
        self.dto = self.dti
        
        if self.PV < measure:
            op1 = 360 - measure + self.PV
            op2 = measure - self.PV
        else: 
            op1 = self.PV - measure  
            op2 = measure + 360 - self.PV
        
        pid = self.pid if abs(self.pid) < 100 else 100 
        return pid if op1 < op2 else -pid
        

if __name__ == '__main__':
    
    import Tracker.Sensor.myAS5600 as sn
    import time 
    isc0  = machine.I2C ( 0, freq = 100000, sda = machine.Pin( 16  ), scl = machine.Pin( 17  ) ) 
    
    SENS  = sn.AS5600 ( isc0, startAngle = 100 )
    
    myPID = PID( PV = 100, Kp = 0.55, Kd = 0.25, Ki = 0.15 )
    
    ang = SENS.degAngle()
    myPID.att( ang )
    time.sleep( 0.1 )
    
    myPID.set_PV( 100 )
        
    for _ in range( 60 ):
        ang = SENS.degAngle()
        pos = myPID.compute( ang )
        print( ang, myPID.PV, myPID.error_real, pos*0.05 )
        time.sleep( 0.5 ) 
    
    
    
    
    
    
    
    
