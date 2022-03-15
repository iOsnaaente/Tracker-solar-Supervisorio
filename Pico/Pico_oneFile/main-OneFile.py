from machine import Pin, soft_reset
from machine import I2C, SoftI2C 
from struct  import pack, unpack
from rp2     import StateMachine 
from time    import sleep_ms
from rp2     import asm_pio 
from rp2     import PIO
from math    import *

import machine 
import struct
import utime
import time
import sys 

# LEFT SIDE 
#----------------
STEP_GIR    = 0 
STEP_ELE    = 1 
STEP_GEN    = 2
DIR_GIR     = 3
DIR_ELE     = 4
DIR_GEN     = 5 
BUTTON_GP   = 6 
BUTTON_GM   = 7
BUTTON_EP   = 8
BUTTON_EM   = 9
LED1_RED    = 10
LED1_BLUE   = 11
LED2_RED    = 12
LED2_BLUE   = 13
ENABLE_MTS  = 14
POWER       = 15
#-----------------

# RIGTH SIDE
#----------------
SDA_DS      = 16 
SCL_DS      = 17
SDA_AS      = 18
SCL_AS      = 19 
UART_TX     = 20 
UART_RX     = 21
LED_BUILTIN = 25
NONE_22     = 22 
NONE_23     = 23 
NONE_24     = 24 
NONE_26     = 26 
NONE_27     = 27 
NONE_28     = 28 


# CONFIGURAÇÕES DE RASTREAMENTO 
LATITUDE            = -29.16530765942215
LONGITUDE           = -54.89831672609559 
TEMPERATURE         =  298.5
PRESSURE            =  101.0

# MODBUS HOLDING REGISTER ADDRESSES
HR_STATE            = 0x00

HR_AZIMUTE          = 0x01
HR_ALTITUDE         = 0x03

HR_PV_MOTOR_GIR     = 0x05
HR_PV_MOTOR_ELE     = 0x07

HR_KP_GIR           = 0x09
HR_KI_GIR           = 0x0B
HR_KD_GIR           = 0x0D
HR_KP_ELE           = 0x0F
HR_KI_ELE           = 0x11
HR_KD_ELE           = 0x13

HR_GIR_STEP         = 0x15
HR_GIR_USTEP        = 0x17
HR_GIR_RATIO        = 0x19
HR_ELE_STEP         = 0x1B
HR_ELE_USTEP        = 0x1D
HR_ELE_RATIO        = 0x1F

HR_YEAR             = 0x21
HR_MONTH            = 0x22
HR_DAY              = 0x23
HR_HOUR             = 0x24
HR_MINUTE           = 0x25
HR_SECOND           = 0x26

HR_POS_MGIR         = 0x27
HR_POS_MELE         = 0x29

HR_LATITUDE         = 0x31 
HR_LONGITUDE        = 0x33
HR_TEMPERATURE      = 0x35  
HR_PRESSURE         = 0x37     
HR_ALTURA           = 0x39

# MODBUS INPUTS REGISTER ADDRESSES
INPUT_SENS_GIR      = 0x00
INPUT_SENS_ELE      = 0x02
INPUT_AZIMUTE       = 0x04
INPUT_ALTITUDE      = 0x06
INPUT_YEAR          = 0x07
INPUT_MONTH         = 0x08
INPUT_DAY           = 0x09
INPUT_HOUR          = 0x0A
INPUT_MINUTE        = 0x0B
INPUT_SECOND        = 0x0C
INPUT_SENS_CONF_GIR = 0x0D
INPUT_SENS_CONF_ELE = 0x0F

# MODBUS COILS REGISTER ADDRESSES
COIL_POWER          = 0X00
COIL_LED1_BLUE      = 0x01
COIL_LED1_RED       = 0x02
COIL_LED2_BLUE      = 0x03
COIL_LED2_RED       = 0x04
COIL_PRINT          = 0x05 
COIL_DATETIME_SYNC  = 0x06
COIL_FORCE_DATETIME = 0x07

# MODBUS DISCRETES REGISTER ADDRESSES
DISCRETE_POWERC_L    = 0x00
DISCRETE_WAITING     = 0x01
DISCRETE_TIME_STATUS = 0x02 
DISCRETE_LEVER1_L    = 0x03
DISCRETE_LEVER1_R    = 0x04
DISCRETE_LEVER2_L    = 0x05
DISCRETE_LEVER2_R    = 0x06

# STATES 
FAIL_STATE     = 0
AUTOMATIC      = 1
MANUAL         = 2
REMOTE         = 3
DEMO           = 4
IDLE           = 5
RESET          = 6
PRE_RETURNING  = 7
RETURNING      = 8
SLEEPING       = 9 


# CONSTANTES MATEMÁTICAS:
MPI    = 3.14159265358979323846e6 
R2D    = 57.2957795130823208768 
R2H    = 3.81971863420548805845 
TWO_PI = 6.28318530717958647693
PI     = 3.14159265358979323846


# DATA E HORA 
ANB = lambda year : True if (year%100 != 0 and year%4 == 0) or (year%100 == 0 and year%400 == 0) else False
DOM = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
UTC = -3 

# FILE CONSTANTS
FILE_PATH   = '/Tracker/Files/mem_pico.txt'
FILE_RW     = 'rw' 
FILE_READ   = 'r'
FILE_WRITE  = 'wo'
FILE_APPEND = 'a'

# MOTORS CONSTANTS 
BACKWARD = False
FORWARD  = True

DISABLE = 1 
ENABLE  = 0

# AS5600 CONSTANTS 
MD_CHECK = 1
MH_CHECK = 2
ML_CHECK = 3 

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

class Registers:
    
    ''' STACK é a fila de registradores. Utiliza uma lista para ordenação dos registradores'''
    STACK = []
    
    ''' REGS é responsável por guardar o tamanho da lista STACK''' 
    REGS  = 0
    
    ''' PARA AJUDAR NA HORA DE DEBUGAR'''
    DEBUG = False


    # Construtor 
    def __init__(self, reg_len : int, reg_type : str = int ):
        if reg_type == bool : self.STACK = bytearray( ceil(reg_len/8) )
        else :                self.STACK = bytearray( reg_len*2 )
        self.TYPE = reg_type 
        self.LEN  = len(self.STACK)
        self.REGS = reg_len

        if self.DEBUG: print( 'Criados {} registradores - EMPTY STACK: {} LEN: {}'. format( self.REGS, self.STACK, self.LEN ) )

    def __str__(self) -> str:
        return 'Registrador bytearray - TYPE: {} LEN: {} REGS: {} STACK: {}'.format( self.TYPE, self.LEN, self.REGS, self.STACK) 

    # Setar um único registrador 
    def set_reg( self, addr, reg ):
        if 0 > addr > self.LEN:
            if self.DEBUG: print('SET_REG ADDR ERROR: 0 > ADDR > LEN( STACK ) ')
            return False
        else:
            try: 
                REG = struct.pack( '>H', reg )
                for n, b in enumerate(REG):
                    self.STACK[ addr*2 + n ] = b
                return True 
            except:
                print( 'SET_REG STRUCT ERROR: Try to write {} of type {}.'.format(reg, type(reg)) ) 
                return False 

    def set_reg_bool( self, addr, reg ): 
        if 0 > addr > self.REGS:
            if self.DEBUG: print('SET_REG_BOOL ADDR ERROR: 0 > ADDR > REGS ')
            return False
        else:
            ADDR = addr // 8
            REG = self.get_reg( ADDR )
            REG = (REG & ( 0xff ^ (1<<addr) )) + ( 1<<addr%8 if reg == True else 0 )
            self.STACK[ADDR] = REG
            if self.DEBUG: print( 'STACK[{}] = {} \nSetado o bit {} da stack com o valor {}'.format( ADDR, self.STACK[ADDR], addr, reg ) )
            return True 

    def set_reg_float( self, addr, reg ): 
        if 0 > addr > self.REGS:
            if self.DEBUG: print('SET_REG_FLOAT ADDR ERROR: ADDR > LEN( STACK ) ')
            return False
        else:
            try:
                self.STACK[ addr*2 : addr*2 + 4] = struct.pack( '>f', reg )
                return True 
            except struct.error as e:
                print( 'SET_REG_FLOAT STRUCT ERROR: ', e ) 
                return False 


    # Setar multiplos registradores 
    def set_regs(self, addr : int, regs : list ) -> bool: 
        for index, reg in enumerate(regs):
            status = self.set_reg( addr + index, reg )
            if status == False:
                if self.DEBUG: print('SET REGS ERROR.')
                return False
        if self.DEBUG: print('SET REGS SUCCESS - STACK: {}'.format(self.STACK))
        return True

    def set_regs_float( self, addr : int, regs : list ) -> bool: 
        for index, reg in enumerate(regs):
            status = self.set_reg_float( addr + index*2, reg )
            if status == False:
                if self.DEBUG: print('SET REGS FLOAT ERROR.')
                return False
        if self.DEBUG: print('SET REGS FLOAT SUCCESS - STACK: {}'.format(self.STACK))
        return True

    def set_regs_bool( self, addr : int, regs : list ) -> bool: 
        for index, reg in enumerate(regs):
            status = self.set_reg_bool( addr + index, reg )
            if status == False:
                if self.DEBUG: print('SET REGS BOOL error.')
                return False
        if self.DEBUG: print('Set_regs_bool Success - STACK: {}'.format(self.STACK))
        return True


    # Pegar um unico registrador 
    def get_reg(self, addr : int ) : 
        if self.TYPE == bool:
            if self.REGS >= addr >= 0 : 
                return struct.unpack( '>B', self.STACK[addr:addr+1] )[0]
        else:
            if self.REGS >= addr >= 0 : 
                return struct.unpack( '>H', self.STACK[addr*2:addr*2+2] )[0]

    def get_reg_bool (self, addr ): 
        if self.REGS >= addr >= 0 : 
            REG = self.STACK[ ceil(addr//8)]
            return True if (REG & 1<<addr%8) else False

    def get_reg_float( self, addr : int ):
        if self.REGS-1 >= addr and addr >= 0 : 
            return struct.unpack( '>f', self.STACK[addr*2:addr*2+4] )[0]

    # Pegar multiplos registradores 
    def get_regs(self, addr : int, num : int ) -> list :
        if addr + num <= self.REGS and addr >= 0 and num > 0:
            return [ self.get_reg( addr + ind ) for ind in range( num ) ]
        else:
            return [] 
    
    def get_regs_bool( self, addr : int, num : int ) -> list: 
        if addr + num <= self.REGS and addr >= 0 and num > 0:
            return [ self.get_reg_bool( addr + ind ) for ind in range( num ) ] 
        else: 
            return []

    def get_regs_float( self, addr : int, num : int ) -> list: 
        if addr + num <= self.REGS and addr >= 0 and num > 0:
            return [ self.get_reg_float(addr+ind*2) for ind in range(num) ] 
        else: 
            return [] 

    # Verificar o offset dos registradores 
    def check_offset(self, addr : int, num_regs : int ):
        if num_regs == 0:                             return True
        elif num_regs < 0 or addr < 0:                return False
        elif (addr + num_regs*2 ) > len(self.STACK):  return False
        else:                                         return True 

class Fake_time:
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
    
class DS3231: 
    # Days of week - DoW  // Temperatura 
    DoW  = [ "Domingo", "Segunda-feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira" , "Sexta-Feira", "Sábado" ]
    temp = 0.0
    
    raw_datetime = b'' 

    wrong_datetime = False
    
    '''
    Construtor da classe DS3231 ::
        >>> NUM : int -> (0 ou 1) depende qual dos dois I2C iremos usar ( Olhar o pinout do Rasp )
        >>> SDA : Pin -> Pino Serial DAta (SDA)  
        >>> SCL : Pin -> Pino Serial CLock ( SCL )
        >>> addrs : bytes(2) -> Endereços do DS3231 e AT24C32 ( Utilizar somente se forem alterados os valores em hardware)
        >>> pages : int -> Número de páginas do EEPROM ( O AT24C32 possui por padrão 128 páginas ) 
        >>> len_pages : int -> Número de bytes por página da EEPROM ( O AT24C32 possui por padrão 32 bytes por página )
    '''
    def __init__(self, i2c, addrs : bytes(2) = [0x68, 0x57], pages : int = 128, len_pages : int = 32 ):
        self.DS_I2C    = i2c
        self.ADDR_DS   = addrs[0]
        self.ADDR_EE   = addrs[1]
        self.len_pages = len_pages
        self.num_pages = pages
        self.time_not_sync = True 
        
        
    ''' Função de baixo nível para escrita no DS. Aceita tanto I2C quanto SoftI2C.
    É necessário que o dados estejam em um buffer de bytes do tipo::
        >>> buff = b'cafe'
        >>> type( buff ) -> <class 'bytes'>
    >>> Caso a função retorne -1 é porque algum erro aconteceu e a escrita
    não pode ser concluida
    >>> Se algum erro for detectado, não irá interromper o fluxo 
    '''
    def _write( self, addr_dev : int, addr_mem : int, buffer : bytes ) -> None:
        try: 
            if type( self.DS_I2C ) == I2C:        self.DS_I2C.writeto_mem( addr_dev, addr_mem, buffer)
            elif type( self.DS_I2C ) == SoftI2C:  self.DS_I2C.writeto( addr_dev, buffer, addr_mem )
        except:
            return -1 
            
    ''' Função de baixo nível para leitura no DS. Aceita tanto I2C quanto SoftI2C.
    os dados de saída terão uma estrutura de buffer de bytes do tipo::
        >>> buff = _read( addr_mem, num_bytes : N ) -> b'cafe' 
        >>> type( buff ) -> <class 'bytes'>
        >>> len( buff ) -> N
    >>> Caso a função retorne -1 é porque algum erro aconteceu e a escrita
    não pode ser concluida
    >>> Se algum erro for detectado, não irá interromper o fluxo 
    '''      
    def _read( self, addr_dev : int, addr_mem : int, num_bytes : int = 2 ) -> list:
        try:
            if type( self.DS_I2C ) == I2C:        return self.DS_I2C.readfrom_mem( addr_dev, addr_mem, num_bytes )
            elif type( self.DS_I2C ) == SoftI2C:  return self.DS_I2C.readfrom( addr_dev, num_bytes, addr_mem )
        except:
            print( "DS3231 - Error -> _read line 31" )
            return -1 
              
            
    '''Seta os parametros de data e hora::
            >>> y  : byte -> Year 
            >>> m  : byte -> Month  
            >>> d  : byte -> Day
            >>> hh : byte -> Hour 
            >>> mm : byte -> Minute 
            >>> ss : byte -> Second
        >>> Retorna 1 caso a data tenha sido trocada
        >>> Retorna -1 em caso de erro 
    '''
    def set_time(self, y : bytes, m : bytes, d : bytes, hh : bytes, mm : bytes, ss : bytes ): 
        dow = self.get_DoW( y, m, d )
        buff = pack( 'bbbbbb', self.dec2bcd(ss), self.dec2bcd(mm), self.dec2bcd(hh), self.dec2bcd(dow), self.dec2bcd(d), self.dec2bcd(m), self.dec2bcd(y) )
        status = self._write(  self.ADDR_DS, 0x00, buff )
        if status == -1:
            print('Erro na escrita de datetime no DS3231')
            return -1
        else: 
            return 1 
        
    ''' Recebe os parametros de data e hora do momento da chamada::
            >>> Retorna um array de bytes com datetime de 7 bytes 
            >>> Caso retorne -1, a data não pode ser lida do DS3231 
    '''
    def now( self ) -> list:
        time = self._read( self.ADDR_DS, 0x00, 7 )
        if time == -1 :
            print( 'Erro na leitura do DS3231' )
            return -1
        else: 
            time = [ self.bcd2dec( time[i] ) for i in range(len(time)-1,-1,-1) if i != 3 ]
            time.append( 3 )
            self.raw_datetime = time
            return time
    
    def get_raw_datetime(self):
        if type(self.raw_datetime) == list:
            to_send = b''
            for i in self.raw_datetime:
                to_send += chr(i)
            self.raw_datetime = to_send 
        return self.raw_datetime
    
    
    ''' Executa a leitura de temperatura do sensor interno do DS3231. O sensor
        de temperuta esta localizado no endereço 0x11 e possui precisão de 0.5º
            >>> Retorna um valor positivo caso a leitura tenha sido bem sucedida
            >>> Retorna -1 caso não tenha executado a leitura da temperatura. 
    '''
    def get_temperature( self ) -> float:
        temp = self._read( self.ADDR_DS, 0x11, 2)
        if temp == -1 :
            print( 'Leitura de temperatura indisponível' )
            return -1 
        else: 
            self.temp = temp[0] + ((temp[1] and 0xC0)>>6)/4
            return self.temp 
        
    ''' Retorna a hora, mais o parâmetro de wrong_datetime::
            >>> Se self.wrong_datetime == True::
                >>> Precisa-se solicitar uma correção de datetime para o supervisório
            >>> Se self.wrong_datetime == False::
                >>> A hora esta sincronizada com a hora do supervisório
    '''
    def get_datetime(self):
        return self.now()


    ''' Retorna o dia da semana de 0 a 6 sendo::
        >>> 0 = Segunda-feira
        >>> .....
        >>> 6 = Domingo
    '''
    def get_DoW(self, year : int, month : int, day : int) -> int :
        year  = year if year < 99 else year & 0x63 
        y_key = ((year//4 + year%7) % 7)-1 
        m_key = [ 1, 4, 4, 0, 2, 5, 0, 3, 6, 1, 4, 6 ] 
        DoW   = ( day + m_key[month-1] + y_key )
        DoW   = DoW if DoW < 7 else DoW // 7 
        return DoW if DoW >= 0 else 7 

    ''' Retorna o dia da semana por extenso.
        >>> 'Segunda-feira', 'Terça-feira' .... 'Domingo' 
    '''
    def get_day_of_week(self ) -> bytes:
        return self.DoW[ self.get_DoW ]
    
    ''' Conversão dos bytes em formato Decimal apartir do formato BCD '''
    def bcd2dec(self, bcd : bytes ) -> bytes: 
        return (bcd>>4)*10 + ( bcd & 0b1111 )  

    ''' Conversão dos bytes em formato BCD apartir do formato Decimal '''
    def dec2bcd(self, dec : bytes ) -> bytes:
        return ((dec//10)<<4) + (dec % 10)
    

    def scan( self, dec : bool = True ) -> list:
        if dec :
            return self.DS_I2C.scan()
        else:
            return [ hex(add) for add in self.DS_I2C.scan() ] 
        
    def get_parameters(self) -> list:
        return self.DS


    '''
    Read é o método que irá ler um byte da EEPROM AT24C32 do DS3231 ::
        >>> addr : int -> Endereço de leitura da EEPROM 
        >>> nbytes : int ->  Quantidade de bytes para serem lidos 
    nbytes é número de bytes que queremos ler apartir do endereço passa como parâmetro.
    >>> Retorna a leitura do endereço passado como parametro
    >>> Caso retorne -1, não foi possível executar a leitura dos parametros 
    '''
    def read_eeprom( self, addr : int, nbytes : int ) -> bytearray:
        # Implementar ainda
        # Escrever Dummy no endereço de leitura
        # ler os n bytes apartir do endereço
        pass 

    ''' 
    Write é o método de escrita na EEPROM AT24C32 do DS3231 ::
        >>> addr : int -> Endereço de escrita de 1 byte 
        >>> buff : bytearray -> dados a serem escritos na EEPROM
    O Buff começa a ser escrito a partir do primeiro endereço passado como parâmetro 
    na variável addr e vai sendo escrito na medida que é necessário.
    '''
    def write_eeprom( self, addr : int, buff : bytearray) -> None:
        if len(buff) == 1:
            self._write( self.ADDR_EE, addr, buff )
            
        # Verificando a necessidade de se dar um offset nos valores do buffer 
        block = addr//self.len_pages
        block = self._read( self.ADDR_EE, block, self.len_pages )
        offset = addr % self.len_pages
        buff = block[ : offset ] + buff if len(buff) >  self.len_pages else block[ : offset] + buff + block[offset+len(buff):]
        
        # verificando a necessidade de se separar a escrita em vários blocos 
        if len(buff) > self.len_pages: buff = [ buff[(init)*self.len_pages : (init+1)*self.len_pages] for init in range( len(buff)//self.len_pages +1) ]
        else:                          buff = [ buff ]
        
        # Escreve cada bloco em suas respectivas páginas 
        for bloco, buffer  in enumerate(buff):
            self._write( self.ADDR_EE, (addr//self.len_pages + 1)*self.len_pages*bloco, buffer)
            sleep_ms(1)

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

class AS5600: 
  ##  FIGURE 21 - DATASHEET available in https://ams.com/documents/20143/36005/AS5600_DS000365_5-00.pdf
  ## Configuration registers 
  ZMCO      = 0x0 
  ZPOS      = 0x1
  MPOS      = 0x3
  MANG      = 0x5
  CONF      = 0x7
  ## Output Registers
  RAWANGLE  = 0x0C
  ANGLE     = 0x0E
  ## Status Registers
  STATUS    = 0x0B
  AGC       = 0x1A
  MAGNITUDE = 0x1B 
  ## Burn Commands 
  BURN      = 0xff

  # Magnetic sensor stuffs 
  Status     = 0       # Status register (MD, ML, MH)
  ADDRESS    = 0x36    # By default 

  startAngle = 0  # starting angle
  totalAngle = 0  # total absolute angular displacement
  
  ## Constructor 
  def __init__( self, I2C : machine.I2C , addr : int = 0x36, startAngle : float = 0.0  ): 
    self.ADDRESS    = addr 
    self.AS5600     = I2C 
    self.startAngle = startAngle
    self.LAST_ANGLE = startAngle
    self.ERRORS     = 0 
    
      
  ## To write in the I2C we need a buffer struct like b'a21@\x02' 
  def _write( self, addr_mem : int, buffer : bytes ) -> None:
    try:
        if type( self.AS5600 ) == machine.I2C: 
          self.AS5600.writeto_mem( self.ADDRESS, addr_mem, buffer )
        elif type( self.AS5600 ) == machine.SoftI2C:
          self.AS5600.writeto( self.ADDRESS, buffer, addr_mem )
        return True 
    except:
        self.ERRORS += 1 
        #print( "AS5600 - ERROR -> _write line 49 ")
        return False 
    
  ## to read, we start at addr_mem and we read num_bytes from addr_mem 
  def _read( self, addr_mem : int, num_bytes : int = 2 ) -> list:
    try:
        if type( self.AS5600 ) == machine.I2C: 
          return self.AS5600.readfrom_mem( self.ADDRESS, addr_mem, num_bytes )
        elif type( self.AS5600 ) == machine.SoftI2C:
          return self.AS5600.readfrom( self.ADDRESS, num_bytes, addr_mem )
    except:
        self.ERRORS += 1 
        #print( "AS5600 - ERROR -> _read line 60 ")
        pass 

  ## read the unscaled angle and unmodified angle
  def rawAngle( self ) -> bytes:
    try:
        raw_angle = self._read( self.ANGLE, 2 )
        HIGH_BYTE = raw_angle[0]    #  RAW ANGLE(11:8) on 0x0C address 
        LOW_BYTE  = raw_angle[1]    #  RAW ANGLE(7:0) on 0X0D address 
        RAW_ANGLE = ( (HIGH_BYTE << 8) | LOW_BYTE ) 
        return RAW_ANGLE 
    except: 
        self.ERRORS += 1
        if self.ERRORS > 10:
            self.set_config()
        return -1  

  def gain(self):
    self.GAIN = self._read( self.AGC , 1 )
    return self.GAIN

  ## Read the scaled angle 
  def degAngle( self ) -> bytes : 
    # To calculate the real angle : 
    # We have to divide the 360º by the 12bits (0x0fff) plus the value from the sensor
    # rawAngle * 360/4096 = rawAngle * 0.087890625
    RAW_ANGLE = self.rawAngle()
    if RAW_ANGLE == -1: return False
    else:               DEG_ANGLE = RAW_ANGLE * ( 360.0 / 0x0fff )
    self.LAST_ANGLE = (DEG_ANGLE - self.startAngle) if (DEG_ANGLE - self.startAngle) >= 0 else (DEG_ANGLE - self.startAngle)+360
    
    # If the angle is negative, we have to normalize it to be between [0, 360)º
    return self.LAST_ANGLE
    

  ## Verify the status of the magnetic range 
  ### The status be in the 0x0B address in the 5:3 bits
  #  
  ## MH [3] AGC minimum gain overflow, magnet too strong  
  ## ML [4] AGC maximum gain overflow, magnet too weak
  ## MD [5] Magnet was detected
  #
  ## To operate properly, the MD have to be set and the MH and ML have to be 0 
  def checkStatus( self ): 
    status = self._read( self.STATUS, 1 )
    self.MH = status[0] >> 3 and 1
    self.ML = status[0] >> 4 and 1
    self.MD = status[0] >> 5 and 1

    ## Return 0 if OK, else -1 to low magnetic level or 1 to high magnetic level 
    if self.MD:
      return MD_CHECK
    else: 
      if self.MH:
        return MH_CHECK
      if self.ML:
        return  ML_CHECK

  def print_diagnosis(self):
        print( self._read( 0, 11 ) )

  def get_config( self ):
    try:
        config = [ struct.unpack('B', val)[0] for val in self._read( 0, 11 )]
        return config
    except:
        return False

  def set_config( self ):
    for i in range( 9 ):
        status = self._write( i, chr(0) )
        if status == False:
            self.ERRORS += 1
            return False
    return True 

  # Número de erros registrados 
  def get_error_count(self):
      return self.ERRORS
    
  def reset_errros_count(self):
      self.ERRORS = 0

class myModbusCommunication:
    CRC16_TABLE = (
    0x0000,0xC0C1,0xC181,0x0140,0xC301,0x03C0,0x0280,0xC241,0xC601,
    0x06C0,0x0780,0xC741,0x0500,0xC5C1,0xC481,0x0440,0xCC01,0x0CC0,
    0x0D80,0xCD41,0x0F00,0xCFC1,0xCE81,0x0E40,0x0A00,0xCAC1,0xCB81,
    0x0B40,0xC901,0x09C0,0x0880,0xC841,0xD801,0x18C0,0x1980,0xD941,
    0x1B00,0xDBC1,0xDA81,0x1A40,0x1E00,0xDEC1,0xDF81,0x1F40,0xDD01,
    0x1DC0,0x1C80,0xDC41,0x1400,0xD4C1,0xD581,0x1540,0xD701,0x17C0,
    0x1680,0xD641,0xD201,0x12C0,0x1380,0xD341,0x1100,0xD1C1,0xD081,
    0x1040,0xF001,0x30C0,0x3180,0xF141,0x3300,0xF3C1,0xF281,0x3240,
    0x3600,0xF6C1,0xF781,0x3740,0xF501,0x35C0,0x3480,0xF441,0x3C00,
    0xFCC1,0xFD81,0x3D40,0xFF01,0x3FC0,0x3E80,0xFE41,0xFA01,0x3AC0,
    0x3B80,0xFB41,0x3900,0xF9C1,0xF881,0x3840,0x2800,0xE8C1,0xE981,
    0x2940,0xEB01,0x2BC0,0x2A80,0xEA41,0xEE01,0x2EC0,0x2F80,0xEF41,
    0x2D00,0xEDC1,0xEC81,0x2C40,0xE401,0x24C0,0x2580,0xE541,0x2700,
    0xE7C1,0xE681,0x2640,0x2200,0xE2C1,0xE381,0x2340,0xE101,0x21C0,
    0x2080,0xE041,0xA001,0x60C0,0x6180,0xA141,0x6300,0xA3C1,0xA281,
    0x6240,0x6600,0xA6C1,0xA781,0x6740,0xA501,0x65C0,0x6480,0xA441,
    0x6C00,0xACC1,0xAD81,0x6D40,0xAF01,0x6FC0,0x6E80,0xAE41,0xAA01,
    0x6AC0,0x6B80,0xAB41,0x6900,0xA9C1,0xA881,0x6840,0x7800,0xB8C1,
    0xB981,0x7940,0xBB01,0x7BC0,0x7A80,0xBA41,0xBE01,0x7EC0,0x7F80,
    0xBF41,0x7D00,0xBDC1,0xBC81,0x7C40,0xB401,0x74C0,0x7580,0xB541,
    0x7700,0xB7C1,0xB681,0x7640,0x7200,0xB2C1,0xB381,0x7340,0xB101,
    0x71C0,0x7080,0xB041,0x5000,0x90C1,0x9181,0x5140,0x9301,0x53C0,
    0x5280,0x9241,0x9601,0x56C0,0x5780,0x9741,0x5500,0x95C1,0x9481,
    0x5440,0x9C01,0x5CC0,0x5D80,0x9D41,0x5F00,0x9FC1,0x9E81,0x5E40,
    0x5A00,0x9AC1,0x9B81,0x5B40,0x9901,0x59C0,0x5880,0x9841,0x8801,
    0x48C0,0x4980,0x8941,0x4B00,0x8BC1,0x8A81,0x4A40,0x4E00,0x8EC1,
    0x8F81,0x4F40,0x8D01,0x4DC0,0x4C80,0x8C41,0x4400,0x84C1,0x8581,
    0x4540,0x8701,0x47C0,0x4680,0x8641,0x8201,0x42C0,0x4380,0x8341,
    0x4100,0x81C1,0x8081,0x4040
    )

    ## STATE MACHINE  
    #-------------
    #ADU
    SLAVE       = 10
    #-------------
    # PDU
    FC          = 11
    #----------------
    ADDR_REG_H  = 21
    ADDR_REG_L  = 22
    QNT_REG_H   = 31
    QNT_REG_L   = 32
    N_REGISTERS = 41
    REGISTERS   = 42 
    #----------------
    CHK         = 56 
    #-------------

    # ETAPA EXTRA 
    RESOLVE     = 57 
    #-------------


    ## FUNCTIONS CODE 
    ADDR_BROADCAST = 0 
    # DISCRETES
    READ_DISCRETE_INPUT       = 2
    #------------------------------
    # COILS 
    READ_COIL_REGISTER        = 1
    WRITE_COIL_REGISTER       = 5
    WRITE_COIL_REGISTERS      = 15
    #------------------------------
    # ANALOGS
    READ_INPUT_REGISTER       = 4
    #------------------------------
    # HOLDINGS
    READ_HOLDING_REGISTER     = 3
    WRITE_HOLDING_REGISTER    = 6
    WRITE_HOLDING_REGISTERS   = 16
    #------------------------------
    # EXCEPTIONS CODE 
    ILLEGAL_FUNCTION          = -1 
    ILLEGAL_ADDR              = -2
    ILLEGAL_DATA              = -3
    #------------------------------


    # Save the FC used
    ADDR_SLAVE     = 0
    FUNCTION_CODE  = 0
    ADDR_REG       = 0
    QNT_REG        = 0 
    DATA_REG       = 0 
    #-----------------

    
    # PARAM. DE FUNC.
    FUNCTIONS_CODE_AVAILABLE = [ 1, 2, 3, 4, 5, 6, 15, 16 ]
    HOLDING_REGS_MAX         = 10 
    INPUT_REGS_MAX           = 10 
    DISCRETE_REGS_MAX        = 10
    COIL_REGS_MAX            = 10 
    #----------------------------
    

    # VARIÁVEIS AUXILIARES 
    HIGH_REG = True
    LOW_REG  = False 
    #---------------------


    # VARIÁVEIS DE PROCESSO 
    STATE      = 0.0
    ADDR_SLAVE = 0
    NUM_BYTES  = 0
    DATA_BYTES = b''
    DEBUG      = False  
    MSG_GOT    = b''
    CHK_GET    = 0 
    #-----------------------

    DISCRETES : Registers = []  
    COILS     : Registers = []  
    INPUTS    : Registers = [] 
    HOLDINGS  : Registers = []  
    #-----------------------


    # Fator de escala para os registradores HOLDING e INPUT 
    # Garantem uma precisão de até 0.01 para o uso de floats 
    FACTOR = 100 
    #-----------------------
    

    # CONSTRUTOR 
    def __init__( self, uart_num : int, baudrate : int, addr : int, tx : int, rx : int, parity : str = 'even', debug : bool = False ):
        '''
        QUADRO RS485 MODBUS COM PARIDADE
        | START_BIT | 8 DATA_BITS | EVEN_PARITY | STOP_BIT |
        
        QUADRO RS485 MODBUS SEM PARIDADE
        | START_BIT | 8 DATA_BITS |   STOP_BIT  | STOP_BIT |
        
        '''
        if type( parity ) == str :
            if parity == 'even' : self.parity = 0
            elif parity == 'odd': self.parity = 1
            else                : self.parity = None
        elif type( parity ) == int:
            if parity > 1 or parity < 0:
                self.parity = None
        else:
            self.parity = 0
    
        if self.parity is None: self.stop_bits = 2
        else:                   self.stop_bits = 1
        self.data_bits = 8

        self.myUART = machine.UART( uart_num, baudrate, parity = self.parity, stop = self.stop_bits, bits = self.data_bits, rx = rx, tx = tx )
        time.sleep_ms(100)
        
        self.TX_PIN = rx
        self.TX_PIN.irq( handler = self.read, trigger = machine.Pin.IRQ_FALLING ) 
        
        self.STATE      = self.SLAVE
        self.ADDR_SLAVE = addr
        
        self.time_SL = 0
        
        self.has_message = False
        self.debug       = debug  
    #----------------------------------



    # DEFINE QUEM SERÃO OS REGISTRADORES USADOS NO myModbus
    def set_registers( self, DISCRETES, COILS, INPUTS, HOLDINGS ):
        self.DISCRETES = DISCRETES 
        self.HOLDINGS = HOLDINGS     
        self.INPUTS = INPUTS 
        self.COILS = COILS
    #----------------------------------
    

    # SETAR OS REGISTRADORES AUXILIARES 
    def _set_high_reg(self):
        self.HIGH_REG = True
        self.LOW_REG  = False

    def _set_low_reg(self):
        self.HIGH_REG = False
        self.LOW_REG = True 
    #----------------------------------
    

    # USA O IRQ DE RECEBIMENTO DE MENSAGEM MODBUS 
    def read(self, irq_obj ):
        while self.myUART.any():

            # Executa a leitura de 1 byte e salva em um 
            # Buffer de bytes da mensagem chamado self.MSG_GOT
            # A variável read é tratada como um valor 8bits  
            read = self.myUART.read(1)
            self.MSG_GOT += read
            read = struct.unpack( 'B', read )[0]
            #-------------------------------------------------------
            

            # IDENTIFICA O SLAVE        
            if self.STATE == self.SLAVE:
                if read == self.ADDR_SLAVE or read == self.ADDR_BROADCAST:
                    if self.DEBUG: print( '\nSLAVE {} FOUND'.format( self.ADDR_SLAVE) )
                    self.STATE = self.FC
                    self.time_SL = time.ticks_us() 
                else:
                    self.STATE = self.SLAVE
                    self.MSG_GOT = b''
                    self.DATA_BYTES = b'' 
            #-------------------------------------------------------
                    
            
            # IDENTIFICA AS FUNÇÕES DISPONÍVEIS 
            elif self.STATE == self.FC:

                # DISCRETES
                if read == self.READ_DISCRETE_INPUT:
                    if self.DEBUG:  print( 'FC = 2: READ_DISCRETE_INPUT' )
                    self.FUNCTION_CODE = self.READ_DISCRETE_INPUT
                    self.STATE         = self.ADDR_REG_H
                #-------------------------------------------------------
                
                
                # COILS 
                elif read == self.READ_COIL_REGISTER:
                    if self.DEBUG:  print( 'FC = 1 : READ_COIL_REGISTER' )
                    self.FUNCTION_CODE = self.READ_COIL_REGISTER
                    self.STATE         = self.ADDR_REG_H 
                    self._set_high_reg()
                
                elif read == self.WRITE_COIL_REGISTER:
                    if self.DEBUG:  print( 'FC = 5 : WRITE_COIL_REGISTER' )
                    self.FUNCTION_CODE = self.WRITE_COIL_REGISTER
                    self.STATE         = self.ADDR_REG_H 
                
                elif read == self.WRITE_COIL_REGISTERS:
                    if self.DEBUG:  print( 'FC = 15 : WRITE_COIL_REGISTERS' )
                    self.FUNCTION_CODE = self.WRITE_COIL_REGISTERS
                    self.STATE         = self.ADDR_REG_H 
                #-------------------------------------------------------
 
 
                # ANALOGS
                elif read == self.READ_INPUT_REGISTER:
                    if self.DEBUG:  print( 'FC = 4 : READ_INPUT_REGISTER' )
                    self.FUNCTION_CODE = self.READ_INPUT_REGISTER
                    self.STATE         = self.ADDR_REG_H 
                #-------------------------------------------------------
                
                
                # HOLDINGS
                elif read == self.READ_HOLDING_REGISTER:
                    if self.DEBUG:  print( 'FC = 3 : READ_HOLDING_REGISTER' )
                    self.FUNCTION_CODE = self.READ_HOLDING_REGISTER
                    self.STATE         = self.ADDR_REG_H 
                
                elif read == self.WRITE_HOLDING_REGISTER:
                    if self.DEBUG:  print( 'FC = 6 : WRITE_HOLDING_REGISTER' )
                    self.FUNCTION_CODE = self.WRITE_HOLDING_REGISTER
                    self.STATE         = self.ADDR_REG_H 
                
                elif read == self.WRITE_HOLDING_REGISTERS:
                    if self.DEBUG:  print( 'FC = 16 : WRITE_HOLDING_REGISTERS' )
                    self.FUNCTION_CODE = self.WRITE_HOLDING_REGISTERS  
                    self.STATE         = self.ADDR_REG_H 
                #-------------------------------------------------------
                
                
                # EXCEPTION 
                else:
                    if self.DEBUG:  print( 'FUNCTION CODE {} NOT FOUND - EXCEPTION CODE'.format(read) )
                    self.FUNCTION_CODE = self.ILLEGAL_FUNCTION 
                    self.STATE = self.SLAVE
                #-------------------------------------------------------
                    
                    
            # VERIFICA O ADDR DE OFFSET 
            elif self.STATE == self.ADDR_REG_H:
                self.ADDR_REG = read << 8
                self.STATE = self.ADDR_REG_L
            
            elif self.STATE == self.ADDR_REG_L:
                self.ADDR_REG += read
                if self.DEBUG: print('ADDR_REG: ', self.ADDR_REG )
                self.STATE = self.QNT_REG_H
            #-------------------------------------------------------
            
            
            # VERIFICA A QUANTIDADE DE REGISTRADORES PARA LER 
            elif self.STATE == self.QNT_REG_H:
                self.QNT_REG = read << 8
                self.STATE = self.QNT_REG_L
            elif self.STATE == self.QNT_REG_L:
                self.QNT_REG += read
                if self.DEBUG: print('QNT_REG: ', self.QNT_REG )
        
                # VERIFICAR PARA ONDE DEVE IR DE ACORDO COM O CÓDIGO DE FUNÇÃO - SOMENTE OS PRESET_MULTIPLE MERECEM ATENÇÃO ESPECIAL 
                self._set_high_reg() 
                if self.FUNCTION_CODE == self.WRITE_COIL_REGISTERS:
                    self.STATE = self.N_REGISTERS
                    if self.DEBUG: print('FC15 Force Multiple Coils' )
                elif self.FUNCTION_CODE == self.WRITE_HOLDING_REGISTERS:
                    self.STATE = self.N_REGISTERS
                    if self.DEBUG: print('FC16 Force Multiple Holding Registers' )
                else:
                    self.STATE = self.CHK
            #-------------------------------------------------------
            
            
            # FUNCTION CODE - PRESET_MULTIPLE_REGISTERS 
            elif self.STATE == self.N_REGISTERS:
                self.NUM_BYTES = read   
                self.STATE     = self.REGISTERS
                if self.DEBUG: print('NUM_BYTES: ', self.NUM_BYTES )
            
            elif self.STATE == self.REGISTERS: 
                if self.NUM_BYTES > 0: 
                    self.DATA_BYTES += chr(read)
                    self.NUM_BYTES -= 1 
                if self.NUM_BYTES == 0: 
                    if self.DEBUG: print('DATA_BYTES: ', self.DATA_BYTES )
                    self.STATE = self.CHK 
            #-------------------------------------------------------
            
            
            # VERIFICA O CHK PARA EXECUTAR AS OPERAÇÕES 
            elif self.STATE == self.CHK:
                if self.HIGH_REG:
                    self.CHK_GET = read << 8 
                    self._set_low_reg() 
                elif self.LOW_REG: 
                    self.CHK_GET += read
            
                    # DECIDE SE FAZ ALGO OU NÃO 
                    # self.check_crc16 faz o calculo dos CRCs e retorna
                    # True se o CRC combinar ou False caso não
                    if self.check_crc16:
                        self.STATE = self.RESOLVE 
                    else:
                        if self.DEBUG: print('Erro no CRC - Encerrando frame sem resposta' ) 
                        self.STATE = self.SLAVE
                        self.DATA_BYTES = b''
                        self.MSG_GOT = b''
            #-------------------------------------------------------
                
            
            # RECEBIDO A MENSAGEM, DEVE-SE ESCREVER OU LER OS REGISTRADORES
            # E RESPONDER A MENSAGEM DE CONFIRMAÇÃO 
            if self.STATE == self.RESOLVE:
                try: 
                    ADDR_REG  = self.ADDR_REG 
                    QNT_REG   = self.QNT_REG 
                    

                    # READ_COIL_REGISTER
                    #     >>> QUERY 
                    #     >>> 11 01 0013 0025 0E84
                    #     >>> RESPONSE 
                    #     >>> 11 01 05 CD6BB20E1B 45E6
                    if  self.FUNCTION_CODE == self.READ_COIL_REGISTER:     
                       
                        # Vefica se não houve estouro de registradores 
                        if (ADDR_REG + QNT_REG) > self.COILS.REGS:
                            self.response( self.ILLEGAL_ADDR, None )
                        
                        else: 
                            # Contabiliza o número de bytes necessários para escrita 
                            NUM_BYTES = math.ceil( QNT_REG / 8 )
                            # Lê os registradores 
                            DATA_REG = 0
                            for reg in self.COILS.get_regs_bool( ADDR_REG, QNT_REG ):
                                DATA_REG = ( DATA_REG << 1) | reg 
                            
                            DATA_REG = struct.pack( 'B'*NUM_BYTES, DATA_REG )
                            
                            # Monta o Frame de dados  
                            DATA = struct.pack( 'B', NUM_BYTES) + DATA_REG


                    # READ_DISCRETE_INPUT 
                    #   >>> QUERY 
                    #   >>> 11 02 00C4 0016 BAA9
                    #   >>> RESPONSE 
                    #   >>> 11 02 03 ACDB35 2018
                    elif self.FUNCTION_CODE == self.READ_DISCRETE_INPUT:     

                        # vefica se não houve estouro de registradores 
                        if (ADDR_REG + QNT_REG) > self.DISCRETES.REGS:
                            self.response( self.ILLEGAL_ADDR, None )
                        
                        else:
                            # Contabiliza o número de bytes necessários para escrita 
                            NUM_BYTES = math.ceil( QNT_REG / 8 )
                            # Lê os registradores 
                            DATA_REG = 0
                            for reg in self.DISCRETES.get_regs_bool( ADDR_REG, QNT_REG ):
                                DATA_REG = ( DATA_REG << 1) | reg 
                            
                            DATA_REG = struct.pack( 'B'*NUM_BYTES, DATA_REG )
                            
                            # Monta o Frame de dados  
                            DATA = struct.pack( 'B', NUM_BYTES) + DATA_REG


                    # READ_HOLDING_REGISTER
                    #   >>> QUERY 
                    #   >>> 11 03 006B 0003 7687   
                    #   >>> RESPONSE
                    #   >>> 11 03 06 AE41 5652 4340 49AD
                    elif self.FUNCTION_CODE == self.READ_HOLDING_REGISTER:
                        # Vefica se não houve estouro de registradores 
                        if (ADDR_REG + QNT_REG) > self.HOLDINGS.REGS:
                            self.response( self.ILLEGAL_ADDR, None )
                        else:
                            # Lê os registradores 
                            DATA_REG = b''
                            for byte in self.HOLDINGS.get_regs( ADDR_REG, QNT_REG ):
                                DATA_REG += struct.pack( '>H', byte )
                            # Monta o frame de dados 
                            DATA = struct.pack('B', QNT_REG*2 ) + DATA_REG


                    # READ_INPUT_REGISTER 
                    #   >>> QUERY 
                    #   >>> 11 04 0008 0001 B298
                    #   >>> RESPONSE 
                    #   >>> 11 04 02 000A F8F4
                    elif self.FUNCTION_CODE == self.READ_INPUT_REGISTER:     
                        # Vefica se não houve estouro de registradores 
                        if (ADDR_REG + QNT_REG) > self.INPUTS.REGS:
                            self.response( self.ILLEGAL_ADDR, None )
                        else:
                            # Lê os registradores 
                            DATA_REG = b''
                            for byte in self.INPUTS.get_regs( ADDR_REG, QNT_REG ):
                                DATA_REG += struct.pack( '>H', byte )
                            # Monta o frame de dados 
                            DATA = struct.pack('B', QNT_REG*2 ) + DATA_REG
                    # --------------------------------------------------------------------


                    # WRITE_COIL_REGISTER 
                    #   >>> QUERY 
                    #   >>> 11 05 00AC FF00 4E8B
                    #   >>> RESPONSE  
                    #   >>> 11 05 00AC FF00 4E8B
                    #   >>> AN ECHO OF QUERY BUFFER
                    elif self.FUNCTION_CODE == self.WRITE_COIL_REGISTER:
                        if ADDR_REG > self.COILS.REGS:
                            self.response( self.ILLEGAL_ADDR, None )
                        else: 
                            DATA_BYTES = True if struct.unpack('>H', self.MSG_GOT[4:-2] )[0] == 0xff00 else False 
                            status = self.COILS.set_reg_bool( ADDR_REG, DATA_BYTES )
                            if status == True:
                                self.has_message = True
                            DATA = self.MSG_GOT[2:-2]
                            if self.DEBUG: print( 'MSG_GOT: {} ADDR: {} BOOLEAN: {}\nSTACK: {}\nSTACK_MAX: {}'.format( self.MSG_GOT[4:-2], ADDR_REG, DATA_BYTES, self.COILS.STACK, len(self.COILS.STACK) ) )  
                        
                    # WRITE_HOLDING_REGISTER 
                    #   >>> QUERY 
                    #   >>> 11 06 0001 0003 9A9B
                    #   >>> RESPONSE  
                    #   >>> 11 06 0001 0003 9A9B
                    #   >>> AN ECHO OF QUERY BUFFER 
                    elif self.FUNCTION_CODE == self.WRITE_HOLDING_REGISTER:
                        if ADDR_REG > self.HOLDING.REGS:
                            self.response( self.ILLEGAL_ADDR, None )
                        else:                            
                            DATA_BYTES = struct.unpack('>H', self.MSG_GOT[4:-2] )[0]
                            
                            status = self.HOLDINGS.set_reg( ADDR_REG, DATA_BYTES )  
                            if status == True:
                                self.has_message = True                            
                            if self.DEBUG: print( "MSG_GOT: {} LEN: {} DATA_BYTE: {}\nHOLDINGS: {}".format( self.MSG_GOT[4:-2], len(self.MSG_GOT[4:-2]), DATA_BYTES, self.HOLDINGS.STACK) ) 
                            DATA = self.MSG_GOT[2:-2]

                    # WRITE_COIL_REGISTERS 
                    #   >>> QUERY 
                    #   >>> 11 0F 0013 000A 02 CD01 BF0B
                    #   >>> RESPONSE  
                    #   >>> 11 0F 0013 000A 2699
                    #   >>> AN SEMI ECHO OF QUERY BUFFER
                    elif self.FUNCTION_CODE == self.WRITE_COIL_REGISTERS:
                        if (ADDR_REG + QNT_REG) > self.COILS.REGS:
                            self.response( self.ILLEGAL_ADDR, None )
                        else:
                            NUM_BYTES = self.MSG_GOT[6]
                            ARRAY = [] 
                            for i in range( NUM_BYTES ):  
                                INT = self.MSG_GOT[7+i] << 8*i
                                for n in range(8):
                                    ARRAY.append( True if (INT >> n) & 1 else False )
                                    
                            status = self.COILS.set_regs_bool( ADDR_REG, ARRAY )
                            if status == True :
                                self.has_message = True
                                
                            if self.DEBUG: print( 'COILS STACK: ', self.COILS.STACK ) 
                            DATA = self.MSG_GOT[2:6]


                    # WRITE_HOLDING_REGISTERS 
                    #   >>> QUERY 
                    #   >>> 11 10 0001 0002 04 000A 0102 C6F0
                    #   >>> RESPONSE  
                    #   >>> 11 10 0001 0002 1298 
                    #   >>> AN SEMI ECHO OF QUERY BUFFER
                    elif self.FUNCTION_CODE == self.WRITE_HOLDING_REGISTERS: 
                        if ADDR_REG > self.HOLDINGS.REGS:
                            self.response( self.ILLEGAL_ADDR, None )
                        else:
                            NUM_BYTES = self.MSG_GOT[6]
                            ARRAY = struct.unpack( '>'+'H'*QNT_REG, self.DATA_BYTES )  
                            status = self.HOLDINGS.set_regs( ADDR_REG, ARRAY )  
                            if status == True:
                                self.has_message = True                            
                            if self.DEBUG: print( "MSG_GOT: {} LEN: {} DATA_BYTE: {}\nHOLDINGS: {}".format( self.MSG_GOT[4:-2], len(self.MSG_GOT[4:-2]), self.DATA_BYTES, self.HOLDINGS.STACK) ) 
                            DATA = self.MSG_GOT[2:6]
                                          

                    # PARTE COMUM DESDE QUE MANTENHA A ESTRUTURA 
                    self.response( self.FUNCTION_CODE, DATA )
                
                except:
                   self.response( self.ILLEGAL_ADDR, None ) 
                                         
                self.STATE = self.SLAVE
                self.MSG_GOT = b''
                self.DATA_BYTES = b'' 

            # -----------------------------------------------
    # -----------------------------------------------------------------------------------------


    # ENIVAR RESPOSTA VIA tx
    def response(self, FC, DATA ):
        if FC == self.ILLEGAL_ADDR:
            FRAME  = struct.pack( 'B', self.ADDR_SLAVE  ) 
            FRAME += struct.pack( 'B', FC + 0b1000_0000 )
            FRAME += struct.pack( 'B', 2                )      
            FRAME += self.get_crc16( FRAME )
            if self.DEBUG: print( 'ILLEGAL ADDR: {} Len: {}\nFrom: {}'.format(FRAME, type(FRAME), len(FRAME), self.MSG_GOT ) )
            self.myUART.write( FRAME )
        
        else: 
            FRAME  = struct.pack( 'B', self.ADDR_SLAVE ) 
            FRAME += struct.pack( 'B', FC )
            FRAME += DATA
            FRAME += self.get_crc16( FRAME )
            if self.DEBUG: print( 'MSG_RECV: {} type: {} Len: {}\nMSG_SEND: {} type: {} Len: {}\nTime spend: {}ms'.format( self.MSG_GOT, type(self.MSG_GOT ), len(self.MSG_GOT), FRAME, type(FRAME), len(FRAME), (time.ticks_us() - self.time_SL)/1000 ) )
            self.myUART.write( FRAME )
            
        


    ''' CHECA SE UM CRC16 É COMPATÍVEL COM UMA MENSAGEM::
            INPUT::
                >>> None => pega os valores dos atributos da classe  
            RETURN::
                >>> True : boolean => Retorna verdadeiro se o crc corresponder
                >>> False : boolean => Retorna falso se o crc não corresponder      
    '''
    @property
    def check_crc16( self ):
        crc = 0xFFFF
        for char in self.MSG_GOT[:-2]:
            crc = (crc >> 8) ^ self.CRC16_TABLE[((crc) ^ char) & 0xFF]
        
        got = struct.unpack( '<H', self.MSG_GOT[-2:] )[0]
        if self.DEBUG : print( '\nCRC_CALC: HEX: {} DEC: {}\nCRC_RECV: HEX: {} DEC: {}\n{}'.format( struct.pack('H',crc), crc, struct.pack('H',got), got, 'CRC PASS\n' if crc == got else 'CRC FAIL\n'  ))
        
        if  crc == got:
            return True 
        return False
    # -----------------------------------------------------

    ''' GERADOR DE CRC16 USANDO O MÉTODO XOR::
            INPUT::
                >>> data : bytes => Mensagem para gerar o CRC 
            RETURN::
                >>> CRC16 : bytes => Retorna 2 bytes de CRC     
    '''
    def get_crc16(self, data ):
        crc = 0xFFFF
        for char in data:
            crc = (crc >> 8) ^ self.CRC16_TABLE[((crc) ^ char) & 0xFF]

        crc = struct.pack('<H', crc) 
        if self.DEBUG: print( 'CRC_SEND: HEX: {} DEC: {}'.format( crc, struct.unpack('H',crc)[0] ) )
        return crc 
    # -----------------------------------------------------------------------------

    # PARA ENVIAR ALGUM DADO DEFINIDO 
    def serial_write( self, DATA ): 
        try: 
            if   type(DATA) == bytes: self.myUART.write(DATA)
            elif type(DATA) == str  : self.myUART.write( DATA.encode() )
            elif type(DATA) == float: self.myUART.write( struct.pack( 'f', DATA ) ) 
            elif type(DATA) == int  : self.myUART.write( struct.pack( 'i', DATA ) ) 
            else:
                if self.DEBUG: print( 'Formato inválido dos dados ')
                return False
            return True  
        except:
            return False

    # PARA ENVIAR UMA MENSAGEM COM CABEÇALHO 
    def serial_write_msg( self, **kwargs ):
        try: 
            for key, value in kwargs.items():
                if type(value) == str: value = value.encode() 
                key = key.encode()
                msg = key + value
                self.myUART.write( msg )
            return True 
        except:
            return False 
    
    # PARA ENVIAR UMA MENSAGEM ESTRUTURADA COM CABEÇALHO 
    def serial_write_data( self, **kwargs ):
        try: 
            for key, value in kwargs.items():
                value = struct.pack( 'f', value )  
                key = key.encode()
                msg = key + value
                self.write( msg )
            return True 
        except:
            return False 
    
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
          
class Lever_control: 
    LEVER_A = 0
    LEVER_B = 0
    LED_A   = 0 
    LED_B   = 0
    
    '''
    Função construtor::
        def __init__( self, lever_pins_A : list, lever_pins_B : list, LED : list = [0,0]  )::
            >>> lever_pins_A : list => Lista de pinos dos levers -x e +x 
            >>> lever_pins_B : list => Lista de pinos dos levers -y e +y 
            >>> LED : list => Lista de pinos dos leds de cada um dos levers::
                >>> LED: ON  +p 
                >>> LED: OFF -p 
    '''
    def __init__ ( self, lever_pins_A : list, lever_pins_B : list, LED : list = [0,0] ):
        self.LEVER_A = [ Pin( lever_pins_A[0], Pin.IN, Pin.PULL_UP), Pin( lever_pins_A[1], Pin.IN, Pin.PULL_UP) ]
        self.LEVER_B = [ Pin( lever_pins_B[0], Pin.IN, Pin.PULL_UP), Pin( lever_pins_B[1], Pin.IN, Pin.PULL_UP) ]
        if LED != [0,0]:
            self.LED_A = Pin( LED[0], Pin.OUT ) 
            self.LED_B = Pin( LED[1], Pin.OUT )  
    
    '''
    Verifica o estado de cada lever, retornando uma lista de 4 valores com cada estado de cada lever. 
    Pode retornar o log dos estados caso a flag log seja setada em True::
        def check_levers( self, log = False )::
            >>> log : bool => Flag de log.
                >>> True => Retorna uma lista e uma string com os estados de cada lever para print
                >>> False => Retorna somente a lista dos estados de cada lever 
            >>> Return => Estado de cada lever em uma array de 4 elementos booleanos::
                >>> -x 
                >>> +x 
                >>> -y
                >>> +y 
            Caso a flag Log seja setada, retorna também::
                >>> flag : str => String com o valor dos levers por extenso, exemplo::
                    -> GIRO P : ELE N 
                        >>> Giro positivo e Elevação Negativa ( +x e -y )
    '''
    def check(self, factor : float = 1, log : bool = False ):
        levers_state = [ False, True, False, True ] 
        if log: flag = '-> '

        if not self.LEVER_A[0].value():
            levers_state[0] = True
            levers_state[1] = False
            self.LED_A.toggle()
            if log: flag +=  " GIRO P :"
        elif not self.LEVER_A[1].value():
            levers_state[1] = True
            levers_state[0] = False
            self.LED_A.toggle()
            if log: flag += " GIRO N :"
        else:
            levers_state[1] = False
            levers_state[0] = False
            
        if not self.LEVER_B[0].value():
            levers_state[2] = True
            levers_state[3] = False
            self.LED_B.toggle()
            if log: flag +=  " ELE P :"
        elif not self.LEVER_B[1].value():
            levers_state[3] = True
            levers_state[2] = False
            self.LED_B.toggle()
            if log: flag += " ELE N :"
        else:
            levers_state[2] = False
            levers_state[3] = False
        
        if log:     return levers_state, flag 
        else:       return levers_state 
        

# MODBUS REGISTER ARRAYS 
INPUTS    = rg.Registers( 0x0F, int )
# | 0x00 |  0x01 | 0x02 | 0x03 |   0x04 |   0x05 |     0x06 |          0x08 |     0x09 |          0x0B | 
# | YEAR | MONTH |  DAY | HOUR | MINUTE | SECOND | SENS_GIR | SENS_CONF_GIR | SENS_ELE | SENS_CONF_ELE |

HOLDINGS  = rg.Registers( 0x3F, int )
#         0x00 |   0x02 |   0x03 |   0x04 |    0x05 |         0x07 |   0x09 |   0x0A |   0x0B |     0x0C |  0x0E |
# PV_MOTOR_GIR | KP_GIR | KI_GIR | KD_GIR | AZIMUTE | PV_MOTOR_ELE | KP_ELE | KI_ELE | KD_ELE | ALTITUDE | STATE |           

DISCRETES = rg.Registers( 0x08, bool )
# |    0x00 |    0x01 |   0x02  |    0x03 |
# | LEVER1L | LEVER1R | LEVER2L | LEVER2R | 

COILS     = rg.Registers( 0x08, bool ) 
# |     0x00 |     0x01 |     0x02 |    0x03 |    0x04 | 
# | LED1BLUE | LED1RED  | LED2BLUE | LED2RED | POWERCL | 

HOLDINGS.set_regs_float( HR_LATITUDE, [ -29.16530765942215, -54.89831672609559 ,  298.5,  101.0 ] )

# LOCALIZATION LIST - GET_SUN_POSITION
LOCALIZATION = HOLDINGS.get_regs_float( HR_LATITUDE, 4 )

LED1_RED_PIN  = machine.Pin( LED1_RED , machine.Pin.OUT)
LED2_RED_PIN  = machine.Pin( LED2_RED , machine.Pin.OUT)
LED1_BLUE_PIN = machine.Pin( LED1_BLUE, machine.Pin.OUT)
LED2_BLUE_PIN = machine.Pin( LED2_BLUE, machine.Pin.OUT)


def compute(Location : list, Time : list, useDegrees : bool = True, useNorthEqualsZero : bool = True, computeRefrEquatorial : bool = False, computeDistance : bool = False):
    # descompactação da lista Time 
    Tyear   = Time[0] + 2000 
    Tmonth  = Time[1]
    Tday    = Time[2]
    Thour   = Time[3] + Time[6]
    Tminute = Time[4]
    Tsecond = Time[5]

    # descompactação da lista Location
    Llatitude    = Location[0]
    Llongitude   = Location[1]
    Ltemperature = Location[2]
    Lpressure    = Location[3]   
    LsinLat      = sin( Llatitude ) 
    LcosLat      = sqrt( 1.0 - LsinLat**2 ) 

    if( useDegrees ): 
        Llongitude /= R2D
        Llatitude  /= R2D
    
    LsinLat = sin(  Llatitude)
    LcosLat = sqrt( 1.0 - LsinLat**2 )

    PjulianDay = computeJulianDay( Tyear, Tmonth, Tday,  Thour, Tminute, Tsecond)
    
    PUT   = Thour + float( Tminute/60.0 ) + float( Tsecond/3600.0 )
    PtJD  = PjulianDay
    PtJC  = PtJD / 36525.0
    PtJC2 = PtJC**2

    l0 = fmod(4.895063168 + 628.331966786 * PtJC  +  5.291838e-6  * PtJC2, TWO_PI)
    m  = fmod(6.240060141 + 628.301955152 * PtJC  -  2.682571e-6  * PtJC2, TWO_PI)

    c = fmod((3.34161088e-2 - 8.40725e-5*PtJC - 2.443e-7*PtJC2)*sin(m) + (3.489437e-4 - 1.76278e-6*PtJC)*sin(2*m), TWO_PI)   # Sun's equation of the centre
    odot = l0 + c

    omg  = fmod(2.1824390725 - 33.7570464271 * PtJC  + 3.622256e-5 * PtJC2, TWO_PI)
    dpsi = -8.338601e-5*sin(omg)
    dist = 1.0000010178

    if( computeDistance ):
        ecc = 0.016708634 - 0.000042037   * PtJC  -  0.0000001267 * PtJC2
        nu = m + c
        dist = dist*( 1.0 - ecc*ecc) / (1.0 + ecc*cos(nu) )
    
    aber = -9.93087e-5/dist

    eps0 = 0.409092804222 - (2.26965525e-4*PtJC + 2.86e-9*PtJC2)
    deps = 4.4615e-5*cos(omg)

    Plongitude    = fmod(odot + aber + dpsi, TWO_PI)
    Pdistance     = dist
    Pobliquity    = eps0 + deps
    PcosObliquity = cos(Pobliquity)
    PnutationLon  = dpsi

    #convertEclipticToEquatorial(Plongitude, PcosObliquity,  &PrightAscension, &Pdeclination)
    sinLon = sin(  Plongitude           )
    sinObl = sqrt( 1.0-PcosObliquity**2 )

    PrightAscension = atan2( PcosObliquity*sinLon, cos(Plongitude) )
    Pdeclination    = asin( sinObl * sinLon )

    #void convertEquatorialToHorizontal(struct STLocation location, struct STPosition *position) {   
    gmst  = 1.75336856 + fmod(0.017202791805*PtJD, TWO_PI) + 6.77e-6*PtJC2 + PUT/R2H
    Pagst = fmod(gmst + PnutationLon * PcosObliquity, TWO_PI)

    sinAlt=0.0

    #void eq2horiz(double sinLat, double cosLat, double longitude,  double rightAscension, double declination, double agst,   double *azimuth, double *sinAlt) {
    ha     = Pagst + Llongitude - PrightAscension
    sinHa  = sin(ha)
    cosHa  = cos(ha)
    sinDec = sin(Pdeclination)
    cosDec = sqrt(1.0 - sinDec * sinDec)
    tanDec = sinDec/cosDec
    PazimuthRefract = atan2( sinHa,  cosHa  * LsinLat - tanDec * LcosLat )
    sinAlt = LsinLat * sinDec + LcosLat * cosDec * cosHa

    alt    = asin( sinAlt )
    cosAlt = sqrt(1.0 - sinAlt * sinAlt)

    alt -= 4.2635e-5 * cosAlt
    Paltitude = alt

    dalt  = 2.967e-4 / tan(alt + 3.1376e-3/(alt + 8.92e-2))
    dalt *= Lpressure/101.0 * 283.0/Ltemperature
    alt  += dalt

    PaltitudeRefract = alt
    
    if(computeRefrEquatorial):
        cosAz  = cos(PazimuthRefract)
        sinAz  = sin(PazimuthRefract)
        sinAlt = sin(PaltitudeRefract)
        cosAlt = sqrt(1.0 - sinAlt * sinAlt)
        tanAlt = sinAlt/cosAlt
        LhourAngleRefract   = atan2( sinAz ,  cosAz  * LsinLat + tanAlt * LcosLat )
        LdeclinationRefract = asin(  LsinLat * sinAlt  -  LcosLat * cosAlt * cosAz  )

    if(useNorthEqualsZero):
        PazimuthRefract = PazimuthRefract + PI;                       
        if(PazimuthRefract > TWO_PI): 
            PazimuthRefract -= TWO_PI       
        if(computeRefrEquatorial):
            PhourAngleRefract = PhourAngleRefract + PI;                 
            if(PhourAngleRefract > TWO_PI):
                PhourAngleRefract -= TWO_PI

    if(useDegrees):
        Plongitude      *= R2D
        PrightAscension *= R2D
        Pdeclination    *= R2D

        Paltitude        *= R2D
        PazimuthRefract  *= R2D
        PaltitudeRefract *= R2D

        if(computeRefrEquatorial):
            PhourAngleRefract  *= R2D
    
    return [ PazimuthRefract, PaltitudeRefract ]

def computeJulianDay( year, month, day, hour, minute, second ):
    if(month <= 2):
        year -= 1 
        month += 12
    tmp1 = int( floor(year/100.0) )
    tmp2 = 2 - tmp1 + int( floor(tmp1/4.0) )
    dDay = day + hour/24.0 + minute/1440.0 + second/86400.0
    JD   = floor(365.250*(year-2000)) - 50.5 + floor(30.60010*(month+1)) + dDay + tmp2
    return JD 

def get_sunrising( Location : list, Time : list) -> float :
    Time[3:-1] = 0, 0, 0 
    rising = []
    while True: 
        azi_alt  = compute( Location, Time, useNorthEqualsZero= False  )
        if azi_alt[1] > 0 :
            return Time
        Time[4] += 1
        if Time[4] >= 60: 
            Time[4] = 0
            Time[3] += 1 
            if Time[3] >= 24:
                break

def get_twilights( Location : list, Time : list) -> list :
    Time[3:-1] = 0, 0, 0  
    rising = [] 
    sunset = []
    while True: 
        azi_alt  = compute( Location, Time, useNorthEqualsZero= False  )
        if azi_alt[1] > 0 :
            sunset = [ t for t in Time ] 
            if rising == []:
                rising = [ t for t in Time ]
                
        Time[4] += 1
        if Time[4] >= 60: 
            Time[4] = 0
            Time[3] += 1 
            if Time[3] >= 24:
                break
    return [ rising, sunset ]

# FILE CONFIGURATIONS 
def file_write( file_path, data, where = 0, OP = 'w'  ):
    with open( file_path, OP ) as file:
        file.seek(where, 0)
        file.write( data )

def file_readlines( file_path, OP = 'r'  ):
    with open( file_path, OP ) as file: 
        lines = file.readlines()
    return lines

def file_size( file_path, OP = 'r'  ) :
    with open( file_path, OP ) as file:
        return file.tell() 

def reboot_statement():
    file = open( '/Tracker/Files/mem_pico.txt', 'r' )
    file.seek(0)
    r = file.read(1)
    file.close()
    file = open( '/Tracker/Files/mem_pico.txt', 'w' )
    file.seek(0)
    if r == '1':
        file.write( '0' )
        return True
    else:
        file.write( '1' )
        return False 


# Inicio da criação do objeto motores. Responsável pelo controle 
# de posição dos motores e controle automático quando os sensores
# falharem, por isso, as configurações de STEP, uSTEP e Ratio devem
# ser configuradas de acordo para evitar problemas de FAIL STATE 
Motors = stp.Motors( STEP_GIR, DIR_GIR, STEP_ELE, DIR_ELE, ENABLE_MTS, POWER      )
Motors.configure   ( Motors.GIR, pos = 0.0, step = 1.8, micro_step = 8, ratio = 1 )
Motors.configure   ( Motors.ELE, pos = 0.0, step = 1.8, micro_step = 8, ratio = 1 )
Motors.set_torque  ( False )

HOLDINGS.set_regs_float( HR_GIR_STEP, [ 1.8, 8, 1 ] ) 
HOLDINGS.set_regs_float( HR_ELE_STEP, [ 1.8, 8, 1 ] )

# Inicializando o protocolo de comunicação Modbus
Modbus = mmb.myModbusCommunication( 1, 115200, 0x12, tx  = machine.Pin(UART_TX) , rx  = machine.Pin(UART_RX), parity = 'even' )
print( 'Utilizando modo de comunicação Modbus:  ')
print( Modbus.myUART ,'\nSLAVE ADDRESS: ', Modbus.ADDR_SLAVE, "\nFunction code available: ", Modbus.FUNCTIONS_CODE_AVAILABLE )

# CADASTRA OS REGISTRADORES
Modbus.set_registers( DISCRETES, COILS, INPUTS, HOLDINGS )
print( 'Registradores cadastrados\n' )
print( 'Holdings  - Type: {} Len: {} {}'.format( Modbus.HOLDINGS.TYPE , Modbus.HOLDINGS.REGS , Modbus.HOLDINGS.STACK  )  )
print( 'Inputs    - Type: {} Len: {} {}'.format( Modbus.INPUTS.TYPE   , Modbus.INPUTS.REGS   , Modbus.INPUTS.STACK    )  )
print( 'Coils     - Type: {} Len: {} {}'.format( Modbus.COILS.TYPE    , Modbus.COILS.REGS    , Modbus.COILS.STACK     )  )
print( 'Discretes - Type: {} Len: {} {}'.format( Modbus.DISCRETES.TYPE, Modbus.DISCRETES.REGS, Modbus.DISCRETES.STACK )  , end = '\n\n' )
     

# Criação dos barramentos i2c usados para os sensores AS5600 e DS3231 
isc0   = machine.I2C ( 0, freq = 100000, sda = machine.Pin( SDA_DS  ), scl = machine.Pin( SCL_DS  ) ) 
isc1   = machine.I2C ( 1, freq = 100000, sda = machine.Pin( SDA_AS  ), scl = machine.Pin( SCL_AS  ) )
print( "Barramento I2C0: ", isc0, "Endereços no barramento: ", isc0.scan() )
print( 'Barramento I2C1: {} Endereços no barramento: {}\n'.format(isc1, isc1.scan()) ) 

# Criação do objeto TIME que esta atrelado ao relógio RTC
# Responsável pela administração do tempo e temporizadores 
# de alarmes para Wake-up 
try:
    Time = dt.Datetime( isc0  )
    INPUTS.set_regs      ( INPUT_YEAR        , Time.DS.get_datetime()[:-1]      )
    HOLDINGS.set_regs    ( HR_YEAR           , Time.RTC.get_datetime()          )
    COILS.set_reg_bool   ( COIL_DATETIME_SYNC, Time.SYNC                        )
    
    TIME     , TIME_STATUS = Time.get_datetime( )
    fake_time              = FAKE_TIME        ( LOCALIZATION, INPUTS.get_regs( INPUT_YEAR, 6 ) )
    AZIMUTE  , ALTITUDE    = sun.compute      ( LOCALIZATION,  TIME )
    
    print( "DS3231 e Relógio RTC inicializados.\nHora registrada no DS3231 ( [yy/mm/dd - hh:mn:ss] {} - Sync: {}\n".format( INPUTS.get_regs( INPUT_YEAR, 6), COILS.get_reg_bool(COIL_DATETIME_SYNC) ) )
    
# Se o DS3231 não estiver de acordo, não tem como o Tracker
# entrar em operação e será obrigado a resetar 
except:
    print( "Relógio não inicializou, erro crítico.") 
    print( "Entrando em modo de reinicialização!\n") 
    machine.soft_reset() 
    
# INICIA OS LEVERS PARA CONTROLE MANUAL 
levers = ml.Lever_control( [BUTTON_GP, BUTTON_GM], [BUTTON_EP, BUTTON_EM], [LED1_RED, LED1_BLUE] )
print( "Levers inicializados (Modo Manual)\n")

# Tenta instanciar os sensores de posição AS5600 
# Caso os sensores estejam vivos, seta-se as configurações de 
# incialização ( escrita de 0 nos endereços [0:11] )
# Caso os sensores não estejam funcionando, deve-se colocar 
# o Tracker em modo FAIL-STATE 
ASGIR  = sn.AS5600 ( isc0, startAngle =   0 )
ASELE  = sn.AS5600 ( isc1, startAngle = 331 )

if (ASGIR.set_config ( ) == True) and ( ASELE.set_config() == True ) :
    SENS_GIR = ASGIR.degAngle()
    INPUTS.set_reg_float(  INPUT_SENS_GIR , SENS_GIR if SENS_GIR != False else 0.0  )
    INPUTS.set_reg_float  ( INPUT_SENS_CONF_GIR, ASGIR.get_config() )
    
    SENS_ELE = ASELE.degAngle()
    INPUTS.set_reg_float  ( INPUT_SENS_ELE , SENS_ELE if SENS_ELE != False else 0.0 )
    INPUTS.set_reg_float  ( INPUT_SENS_CONF_ELE, ASELE.get_config() )
    
    # Setar posição dos motores de passo para FAIL STATE
    Motors.GIR.position = SENS_GIR if SENS_GIR != False else 0.0  
    Motors.ELE.position = SENS_ELE if SENS_ELE != False else 0.0
    
    HOLDINGS.set_reg_float( HR_POS_MGIR, Motors.GIR.position ) 
    HOLDINGS.set_reg_float( HR_POS_MELE, Motors.ELE.position )
    
    HOLDINGS.set_reg      ( HR_STATE, AUTOMATIC )
    
    print( "Sensores AS5600 de Giro e Elevação inicializados e configurados. Prontos para uso.")

else:
    HOLDINGS.set_reg( HR_STATE, FAIL_STATE )
    print( 'Erro na inicialização do AS5600 de Giro. Verificar barramento I2C!')
    
# Cada motor possui um PID para correção da posição
# Instanciamento dos PIDs de cada motor
PID_GIR = mp.PID( PV = 100, Kp = 0.55, Kd = 0.25, Ki = 0.15 )
PID_ELE = mp.PID( PV = 100, Kp = 0.55, Kd = 0.25, Ki = 0.15 )

# Atualizaão do angulo para calculo de correção. Há diferenças 
# entre a atualização e computação dos angulos de correção
PID_GIR.att( INPUTS.get_reg_float( INPUT_SENS_GIR ) )
PID_ELE.att( INPUTS.get_reg_float( INPUT_SENS_ELE ) )

HOLDINGS.set_regs_float( HR_KP_GIR, [ PID_GIR.Kp, PID_GIR.Ki, PID_GIR.Kd] ) 
HOLDINGS.set_regs_float( HR_KP_ELE, [ PID_ELE.Kp, PID_ELE.Ki, PID_ELE.Kd] )

print( "PID do motor de GIR configurado: Kd Ki Kp: {} {} {} - PV_gir: {}  ".format( PID_GIR.Kd, PID_GIR.Ki, PID_GIR.Kp, PID_GIR.PV ) )
print( "PID do motor de ELE configurado: Kd Ki Kp: {} {} {} - PV_ele: {}\n".format( PID_ELE.Kd, PID_ELE.Ki, PID_ELE.Kp, PID_ELE.PV ) )

# AO CONTRARIO, TODA VEZ QUE FOR PRECISO USAR OS VALORES
# DE REGISTRADORES, DEVE-SE PEGAR ESSES VALORES  
def update_configurations():
    # HOLDINGS
    # Set the RTC datetime 
    y,m,d,h,n,s = HOLDINGS.get_regs( HR_YEAR, 6 ) 
    Time.set_RTC_datetime( y,m,d,h,n,s)
    
    if HOLDINGS.get_reg( HR_STATE ) == AUTOMATIC and COILS.get_reg_bool( COIL_FORCE_DATETIME) == True:
        Time.set_DS_datetime( y,m,d,h,n,s )
        COILS.set_reg_bool( COIL_DATETIME_SYNC, Time.SYNC )
        COILS.set_reg_bool( COIL_FORCE_DATETIME, False ) 
        
    # Set the motors configuration
    posGIR, posELE    = HOLDINGS.get_regs_float( HR_POS_MGIR, 2 )
    
    sGIR, usGIR, rGIR = HOLDINGS.get_regs_float( HR_GIR_STEP, 3 )
    Motors.configure( Motors.GIR, posGIR, sGIR, usGIR, rGIR )
    
    sELE, usELE, rELE = HOLDINGS.get_regs_float( HR_ELE_STEP, 3 )
    Motors.configure( Motors.ELE, posELE, sELE, usELE, rELE )
    
    # set the PID configs 
    PID_GIR.Kp = HOLDINGS.get_reg_float( HR_KP_GIR )
    PID_GIR.Kd = HOLDINGS.get_reg_float( HR_KD_GIR )
    PID_GIR.Ki = HOLDINGS.get_reg_float( HR_KI_GIR )
    PID_ELE.Kp = HOLDINGS.get_reg_float( HR_KP_ELE )
    PID_ELE.Kd = HOLDINGS.get_reg_float( HR_KD_ELE )
    PID_ELE.Ki = HOLDINGS.get_reg_float( HR_KI_ELE )
    
    #COILS
    LED1_BLUE_PIN.value( COILS.get_reg_bool( COIL_LED1_BLUE ) ) 
    LED1_RED_PIN.value ( COILS.get_reg_bool( COIL_LED1_RED  ) ) 
    LED2_BLUE_PIN.value( COILS.get_reg_bool( COIL_LED2_BLUE ) ) 
    LED2_RED_PIN.value ( COILS.get_reg_bool( COIL_LED2_RED  ) )
    Motors.set_torque  ( COILS.get_reg_bool( COIL_POWER     ) )

'''# --------------------------------------- INICIO DO LOOP ---------------------------------------------------------------------------#'''
last_print = time.ticks_ms()

POS_ELE = 0.0 
POS_GIR = 0.0 

LAST_STATE = 0

while True:
    time_spend_by_loop = time.ticks_ms()
    
    # Timmer via software para não usar interrupção de Timmer via hardware e conflitar com interrupção das mensagens Modbus 
    if (time.ticks_ms() - last_print > 2500) and (COILS.get_reg_bool( COIL_PRINT) == True ):
        LED1_RED_PIN(1)
        MSG  = 'STATE:\t\t{}\n'.format( HOLDINGS.get_reg( HR_STATE ) ) 
        MSG += 'Datetime:\t{}\n'.format( Time.get_datetime())
        MSG += "Giro:\n"
        MSG += "Kd Ki Kp:\t{}\t\t{}\t\t{}\n"   .format( PID_GIR.Kd, PID_GIR.Ki, PID_GIR.Kp )
        MSG += "Sens:\t\t{}\tReg. read:\t{}\n" .format( ASGIR.degAngle(), INPUTS.get_reg_float( INPUT_SENS_GIR ) ) 
        MSG += "PV(GIR):\t{}  \nError:\t\t{}\nPID:\t\t{}\n".format( PID_GIR.PV, PID_GIR.error_real, PID_GIR.compute( INPUTS.get_reg_float( INPUT_SENS_GIR ) ) )
        MSG += "\nElevação:\n"
        MSG += "Kd Ki Kp:\t{}\t\t{}\t\t{}\n"   .format( PID_ELE.Kd, PID_ELE.Ki, PID_ELE.Kp )
        MSG += "Sens:\t\t{}\tReg. read:\t{} \n".format( ASELE.degAngle(), INPUTS.get_reg_float(INPUT_SENS_ELE)  )
        MSG += "PV(ELE):\t{}  \nError:\t\t{}\nPID:\t\t{}\n".format( PID_ELE.PV, PID_ELE.error_real, PID_ELE.compute( INPUTS.get_reg_float( INPUT_SENS_ELE ) ) )
        MSG += "\nAZIMUTE: \t{}  \tReg. read:\t{}\n".format( AZIMUTE , INPUTS.get_reg_float( INPUT_AZIMUTE  ) )
        MSG += "ALTITUDE:\t{}  \tReg. read:\t{}\n".format( ALTITUDE, INPUTS.get_reg_float( INPUT_ALTITUDE ) )
        
        MSG += "FAIL STATE:\tGIR:{}\t\tELE:{}\n".format( HOLDINGS.get_reg_float( HR_POS_MGIR ), HOLDINGS.get_reg_float( HR_POS_MGIR ) ) 
        
        MSG += '\nHoldings  - Type: {} Len: {} {}\n'.format( HOLDINGS.TYPE , HOLDINGS.REGS , HOLDINGS.STACK  )   
        MSG += 'Inputs    - Type: {} Len: {} {}\n'.format( INPUTS.TYPE   , INPUTS.REGS   , INPUTS.STACK    )  
        MSG += 'Coils     - Type: {} Len: {} {}\n'.format( COILS.TYPE    , COILS.REGS    , COILS.STACK     )  
        MSG += 'Discretes - Type: {} Len: {} {}\n\n'.format( DISCRETES.TYPE, DISCRETES.REGS, DISCRETES.STACK )  
        sys.stdout.write( MSG )
        last_print = time.ticks_ms() 
        LED1_RED_PIN(0)
    
    # SETAR OS REGISTRADORES DE INPUTS
    SENS_GIR = ASGIR.degAngle()
    SENS_ELE = ASELE.degAngle()
    
    if SENS_ELE == False or SENS_GIR == False: 
        HOLDINGS.set_reg      ( HR_STATE        , FAIL_STATE )
        continue 
    else: 
        HOLDINGS.set_reg_float( HR_POS_MGIR, SENS_GIR )
        HOLDINGS.set_reg_float( HR_POS_MELE, SENS_ELE )
        INPUTS.set_reg_float  ( INPUT_SENS_GIR , SENS_GIR )
        INPUTS.set_reg_float  ( INPUT_SENS_ELE , SENS_ELE )

    # SETAR A DATA E HORA
    TIME, TIME_STATUS = Time.get_datetime()
    INPUTS.set_regs        ( INPUT_YEAR          , TIME[:-1]   )
    DISCRETES.set_reg_bool ( DISCRETE_TIME_STATUS, TIME_STATUS )
    
    # SETA O AZIMUTE E ALTITUDE DE INPUT COM O VALOR CALCULADO
    AZIMUTE, ALTITUDE = sun.compute( LOCALIZATION,  TIME )
    INPUTS.set_reg_float ( INPUT_AZIMUTE       , AZIMUTE     )
    INPUTS.set_reg_float ( INPUT_ALTITUDE      , ALTITUDE    )
    
    # Confere se foi recebido alguma mensagem para atualização das variáveis  
    if Modbus.has_message == True:
        update_configurations(  )
        Modbus.has_message = False 

    # Entra nos estados de operação
    STATE = HOLDINGS.get_reg( HR_STATE )
    if STATE == AUTOMATIC:
        # SETA O PV DO PID COM O AZIMUTE E ZENITE  
        PID_GIR.set_PV( INPUTS.get_reg_float ( INPUT_AZIMUTE  ) ) 
        PID_ELE.set_PV( INPUTS.get_reg_float ( INPUT_ALTITUDE ) )
        
        # SETA O PV DOS MOTORES PARA FUTUROS FAIL STATES 
        HOLDINGS.set_reg_float ( HR_PV_MOTOR_GIR, PID_GIR.PV ) 
        HOLDINGS.set_reg_float ( HR_PV_MOTOR_ELE, PID_ELE.PV )
    
        # Se a altitude for menor que 0 então o sol já se pôs e o tracker deve retornar
        # para a posição inicial ( do novo dia ) e aguardar até o sol nascer.
        if ALTITUDE < 0 :
            HOLDINGS.set_reg( HR_STATE, PRE_RETURNING )
            LAST_STATE = AUTOMATIC 
            continue 
        
        # COMPUTA O MOVIMENTO NECESSÁRIO PARA CORREÇÃO DOS MOTORES 
        POS_GIR = PID_GIR.compute( INPUTS.get_reg_float( INPUT_SENS_GIR ) ) 
        POS_ELE = PID_ELE.compute( INPUTS.get_reg_float( INPUT_SENS_ELE ) )
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == FAIL_STATE: 
        if ASGIR.degAngle(): 
            INPUTS.set_reg_float(  INPUT_SENS_GIR , SENS_GIR if SENS_GIR != False else INPUTS.get_reg_float(INPUT_SENS_GIR) )
            HOLDINGS.set_reg( HR_STATE, AUTOMATIC )
            continue
        else: 
            HOLDINGS.set_reg( HR_STATE, FAIL_STATE )
        if ASELE.degAngle():
            INPUTS.set_reg_float(  INPUT_SENS_ELE , SENS_ELE if SENS_ELE != False else INPUTS.get_reg_float(INPUT_SENS_ELE) )
            HOLDINGS.set_reg( HR_STATE, AUTOMATIC )
            continue
        else: 
            HOLDINGS.set_reg( HR_STATE, FAIL_STATE )
        
        # SETA O PV DO PID COM O AZIMUTE E ZENITE  
        PID_GIR.set_PV( HOLDINGS.get_reg_float ( INPUT_AZIMUTE  ) ) 
        PID_ELE.set_PV( HOLDINGS.get_reg_float ( INPUT_ALTITUDE ) )
        
        # Se a altitude for menor que 0 então o sol já se pôs e o tracker deve retornar
        # para a posição inicial ( do novo dia ) e aguardar até o sol nascer.
        if ALTITUDE < 0 :
            HOLDINGS.set_reg( HR_STATE, PRE_RETURNING )
            LAST_STATE = AUTOMATIC 
            continue 
        
        # COMPUTA O MOVIMENTO NECESSÁRIO PARA CORREÇÃO DOS MOTORES 
        POS_GIR = PID_GIR.compute( INPUTS.get_reg_float( HR_POS_MGIR ) ) 
        POS_ELE = PID_ELE.compute( INPUTS.get_reg_float( HR_POS_MELE ) )
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    elif STATE == PRE_RETURNING:
        NEW_AZIMUTE    = sun.get_sunrising( LOCALIZATION, TIME        ) 
        NEW_AZIMUTE, _ = sun.compute       ( LOCALIZATION, NEW_AZIMUTE )
        HOLDINGS.set_reg_float             ( HR_AZIMUTE  , NEW_AZIMUTE )
        HOLDINGS.set_reg                   ( HR_STATE    , RETURNING   )

    elif STATE == RETURNING:
        # Verifica a distancia do PV_NEW_DAY
        DIFF = abs( INPUTS.get_reg_float( INPUT_SENS_GIR ) - HOLDINGS.get_reg_float( HR_AZIMUTE ) )
        if DIFF > 5: 
            POS_ELE = 0.0
            POS_GIR = 2.5
            
        else: 
            PID_GIR.set_PV( HOLDINGS.get_reg_float ( HR_AZIMUTE  ) ) 
            PID_ELE.set_PV( 1 ) 
            # COMPUTA O MOVIMENTO NECESSÁRIO PARA CORREÇÃO DOS MOTORES 
            POS_GIR = PID_GIR.compute( INPUTS.get_reg_float( INPUT_SENS_GIR ) ) 
            POS_ELE = PID_ELE.compute( INPUTS.get_reg_float( INPUT_SENS_ELE ) )

            if ( abs(POS_GIR) < 0.5 ) and ( abs(POS_ELE) < 0.5 ):
                if LAST_STATE == AUTOMATIC:
                    HOLDINGS.set_reg( HR_STATE, SLEEPING )
                elif LAST_STATE == DEMO:
                    HOLDINGS.set_reg( HR_STATE, DEMO ) 
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == MANUAL:
        # PEGA O ESTADO DOS LEVERS 
        status = levers.check( )
        if   status[0] == True:            POS_ELE =  1
        elif status[1] == True:            POS_ELE = -1
        else:                              POS_ELE =  0
        if   status[2] == True:            POS_GIR =  1
        elif status[3] == True:            POS_GIR = -1
        else:                              POS_GIR =  0

        Motors.move( POS_ELE, POS_GIR )
        HOLDINGS.set_reg_float( HR_PV_MOTOR_GIR, Motors.get_gir_position() ) 
        HOLDINGS.set_reg_float( HR_PV_MOTOR_ELE, Motors.get_ele_position() )    
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == REMOTE:
        # PEGA O AZIMUTE E ZENITE DOS HOLDINGS AO INVÉS DOS INPUTS 
        PID_GIR.set_PV( HOLDINGS.get_reg_float( HR_AZIMUTE  )   )
        PID_ELE.set_PV( HOLDINGS.get_reg_float( HR_ALTITUDE )   )
        POS_GIR = PID_GIR.compute( INPUTS.get_reg_float( INPUT_SENS_GIR ) ) 
        POS_ELE = PID_ELE.compute( INPUTS.get_reg_float( INPUT_SENS_ELE ) )
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == IDLE:
        continue
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == SLEEPING:
        if ALTITUDE > 0:
            COILS.set_reg_bool( COIL_POWER, True      ) 
            HOLDINGS.set_reg  ( HR_STATE  , AUTOMATIC )
            Modbus.has_message = True 
        else:
            if COILS.get_reg_bool( COIL_POWER ) == True: 
                COILS.set_reg_bool( COIL_POWER, False )
                Modbus.has_message = True 
        continue
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == RESET:
        machine.soft_reset()    
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == DEMO:
        TIME = fake_time.compute()
        AZIMUTE, ALTITUDE = sun.compute( LOCALIZATION,  TIME )
        time.sleep(0.5) 
        
        if LAST_STATE != DEMO or ALTITUDE < 0: 
            LAST_STATE = DEMO
            fake_time.compute_new_day()
            HOLDINGS.set_reg( HR_STATE, PRE_RETURNING )
            continue 
        
        COILS.set_reg_bool( COIL_POWER, False )
        COILS.set_reg_bool( COIL_PRINT, False )
        
        HOLDINGS.set_reg_float( HR_AZIMUTE , AZIMUTE  )
        HOLDINGS.set_reg_float( HR_ALTITUDE, ALTITUDE )

        PID_GIR.set_PV( HOLDINGS.get_reg_float( HR_AZIMUTE  ) ) 
        PID_ELE.set_PV( HOLDINGS.get_reg_float( HR_ALTITUDE ) )
        
        POS_GIR = PID_GIR.compute( INPUTS.get_reg_float( INPUT_AZIMUTE  ) )
        POS_ELE = PID_ELE.compute( INPUTS.get_reg_float( INPUT_ALTITUDE ) )
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
      
    # MOVE OS MOTORES 
    Motors.move( POS_ELE*0.05, POS_GIR*0.05 )

    # SALVA A NOVA POSIÇÃO DOS MOTORES
    HOLDINGS.set_reg_float( HR_POS_MGIR, Motors.GIR.position ) 
    HOLDINGS.set_reg_float( HR_POS_MELE, Motors.ELE.position )

    # Tempo de looping do Pico
    dt = (time.ticks_ms() - time_spend_by_loop )
    if dt <= 25:
        time.sleep_ms( 25 - dt )