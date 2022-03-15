from machine import Pin
from time    import sleep_ms
from rp2     import StateMachine 
from rp2     import asm_pio 
from rp2     import PIO

BACKWARD = False
FORWARD  = True

DISABLE = 1 
ENABLE  = 0

@asm_pio( set_init = PIO.OUT_LOW )
def move():
    label('init')
    pull( )
    mov( x, osr )
    label( 'step_m1' )
    set(pins, 1)             
    set(pins, 0)            
    jmp( x_dec, 'step_m1')  
    jmp( 'init' )

class Motor: 
    direction = FORWARD
    torque    = ENABLE
    position  = 0.0 
    ratio     = 1.0 
    step      = 1.8
    u_step    = 16 
    nano_step = 0.0
    name      = '' 

    # Para ter 30rpm durante 1 segundo
    rpm       = 0 
    pps       = 800  

    def __init__(self, STEP_PIN : int, DIRECTION_PIN : int, ENABLE_PIN : int, TORQUE : bool = False, FREQ : int = 2000, NUM_SM : int = 1 ) -> None:
        self.STEP_PIN       = Pin( STEP_PIN     , Pin.OUT ) 
        self.DIRECTION_PIN  = Pin( DIRECTION_PIN, Pin.OUT )
        self.ENABLE_PIN     = Pin( ENABLE_PIN   , Pin.OUT )

        self.direction      = FORWARD
        self.torque         = ENABLE if TORQUE else DISABLE 
        self.ENABLE_PIN.value( self.torque )

        self.NUM_SM = NUM_SM
        self.FREQ = FREQ 

        self.step   = 1.8
        self.u_step = 8 
        self.ratio  = 1

        self.sm = StateMachine( self.NUM_SM , move, freq = self.FREQ, set_base= self.STEP_PIN )
        
    def activate( self ):
        self.sm.active(1)

    def deactivate(self):
        self.sm.active(0) 
    
    def get_position(self):
        return self.position 

    def configure(self, step : float = 1.8, u_step : int = 8, ratio : float = 1) -> None: 
        self.step   = step
        self.u_step = u_step 
        self.ratio  = ratio 

    def set_torque( self, torque : bool = ENABLE ) -> None:
        self.torque = ENABLE if torque else DISABLE 
        self.ENABLE_PIN.value( self.torque )
    
    def set_name(self, name):
        self.name = name 

    def set_velocity( self, rpm : int = 1 ) -> None:
        self.pps = int( ( rpm * 360 * ( self.u_step // self.step ) )/( 60 * self.step ))
        self.rpm = rpm 
    
    def set_direction( self, direction : bool ) -> None:
        self.direction = FORWARD if direction else BACKWARD
        self.DIRECTION_PIN.value( 1 if self.direction == FORWARD else 0 ) 
    
    #def _pulse(self, time_spend : int = 2 ) -> None :
    #    self.STEP_PIN.high()
    #    sleep_ms ( time_spend//2 )
    #    self.STEP_PIN.low()
    #    sleep_ms ( time_spend//2 )
    
    def move( self, n_pulses : int, time_stemp : int = 10 ) -> None:  
        if self.torque != DISABLE:
            self.sm.put( n_pulses )
            if self.direction: self.position += self.step / (self.u_step * self.ratio)  
            else:              self.position -= self.step / (self.u_step * self.ratio)
            if   self.position > 360.0: self.position -= 360.0
            elif self.position < 0:     self.position = 360 - self.position 

    def get_num_pulses(self, angle : int) -> int:
        n_pulso = ((angle*self.u_step)/self.step)*self.ratio
        self.nano_step += n_pulso % 1
        n_pulso = int( n_pulso // 1 )
        
        if self.nano_step > 1.0 :
            self.nano_step -= 1  
            n_pulso += 1
        
        return n_pulso

class Motors:
    GIR_POS = 0
    ELE_POS = 0
    POWER   = 0  

    def __init__(self, gir_stp : [Pin, int], gir_dir : Pin, ele_stp : Pin, ele_dir : Pin, enb_motors : Pin, pin_power : Pin ):
        self.GIR = Motor ( gir_stp, gir_dir, enb_motors, NUM_SM = 0 )
        self.GIR.set_name("Gir/Azimute")
        self.ELE = Motor ( ele_stp, ele_dir, enb_motors, NUM_SM = 1 )
        self.ELE.set_name("Ele/Altitude" )
        self.POWER = Pin( pin_power, Pin.OUT ) 
    
    
    def configure(self, MOTOR : Motor, pos : float, step : float, micro_step : int, ratio : float ) -> None:
        MOTOR.u_step = micro_step 
        MOTOR.ratio  = ratio
        MOTOR.step   = step 
        MOTOR.pos    = pos
        MOTOR.activate()


    def set_torque(self, state : bool ) -> None :  
        self.GIR.torque = ENABLE if state else DISABLE
        self.GIR.ENABLE_PIN.value( self.GIR.torque )
        self.ELE.torque = ENABLE if state else DISABLE
        self.ELE.ENABLE_PIN.value( self.GIR.torque )
        self.POWER.value( state )


    def get_positions(self):
        return [ self.GIR.position, self.ELE.position ]
    
    def get_gir_position(self):
        return self.get_positions()[0]
    
    def get_ele_position(self):
        return self.get_positions()[1]


    def move(self, g_ang : int, e_ang : int, time_stemp : int = 2 ) -> None :
        if   g_ang < 0:   self.GIR.set_direction( BACKWARD   )
        elif g_ang > 0:   self.GIR.set_direction( FORWARD    )

        if   e_ang < 0:   self.ELE.set_direction( BACKWARD   ) 
        elif e_ang > 0:   self.ELE.set_direction( FORWARD    )
        
        g_ang = self.GIR.get_num_pulses( abs(g_ang) )
        e_ang = self.ELE.get_num_pulses( abs(e_ang) )
        if g_ang > 0: 
            self.GIR.move( g_ang )
        if e_ang > 0:
            self.ELE.move( e_ang )

        self.GIR_POS, self.ELE_POS = self.get_positions()

