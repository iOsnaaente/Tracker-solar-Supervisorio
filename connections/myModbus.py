from serial            import Serial, SerialException
from minimalmodbus     import Instrument, MODE_RTU
from typing            import Union

import glob
import sys 

class MyModbus:
    seriais_available = [] 
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
    PICO_FAIL_STATE     = 0x00
    PICO_AUTOMATIC      = 0x01
    PICO_MANUAL         = 0x02
    PICO_REMOTE         = 0x03
    PICO_DEMO           = 0x04
    PICO_IDLE           = 0x05
    PICO_RESET          = 0x06
    PICO_PRE_RETURNING  = 0x07
    PICO_RETURNING      = 0x08
    PICO_SLEEPING       = 0x09 


    # PRIVATE FUNCTIONS 
    def _read_coils(self, addr : int, num : int = 1 ) -> Union[ int, list ]: 
        read  = [] 
        try: 
            if   num > 1  : read = self.COM.read_bits ( addr, num, functioncode = 1 )  
            elif num == 1 : read = self.COM.read_bit  ( addr,      functioncode = 1 ) 
            return read 
        except: 
            print( 'Read_coils error: ADDR ', addr, ' NUM_REGS: ', num )
            return [] 
    def _read_discretes(self, addr : int, num : int = 1 ) -> Union[ int, list ]: 
        read  = [] 
        try: 
            if   num > 1  : read = self.COM.read_bits( addr, num,  functioncode = 2 ) 
            elif num == 1 : read = self.COM.read_bit ( num,        functioncode = 2 )
            return read 
        except: 
            print( 'Read_discretes error: ADDR ', addr, ' NUM_REGS: ', num )
            return []    
    def _read_holdings( self, addr : int, num : int = 1 ) -> Union[ int, list ]: 
        read  = [] 
        try: 
            if   num > 1  : read = self.COM.read_register  ( addr, num,  functioncode = 3 ) 
            elif num == 1 : read = self.COM.read_registers ( num,        functioncode = 3 )
            return read  
        except: 
            print( '_read_holdings error: ADDR ', addr, ' NUM_REGS: ', num )
            return False
    def _read_input_float( self, addr : int ) -> float: 
        try: 
            return self.COM.read_float( addr, functioncode = 4 )
        except:
            print( '_return_inputs_float error.')
            return -1
    def _read_inputs(self, addr : int, num : int ) -> Union[ int, list ]: 
        read  = [] 
        try: 
            if   num == 1 : read = self.COM.read_register  ( addr,      functioncode = 4 ) 
            elif num >  1 : read = self.COM.read_registers ( addr, num, functioncode = 4 )
            return read  
        except: 
            print( '_read_inputs error: ADDR ', addr, ' NUM_REGS: ', num )
            return -1
    def _write_coils( self, addr : int , regs : Union[ bool, list ] ) -> bool: 
        self.COM.write_bit ( addr, regs,   functioncode = 5 )
        try: 
            if   type(regs) == bool: self.COM.write_bit ( addr, regs,   functioncode = 5 )
            elif type(regs) == list: self.COM.write_bits( addr, regs ) #functioncode = 15
            else:                    return False
            return True
        except:
            print( 'write_coils error: ADDR: ', addr, ' REGS: ', regs )
            return False 
    def _write_holdings( self, addr : int, regs : Union[ int, float, list] ) -> bool:
        try: 
            print( type(regs), regs )
            if   type(regs) == int:   self.COM.write_register ( registeraddress = addr, value = regs )
            elif type(regs) == float: self.COM.write_float    ( registeraddress = addr, value = regs )
            elif type(regs) == list:  self.COM.write_registers( registeraddress = addr, value = regs )
            else:                     return False 
            return True 
        except:
            print( 'write_holdings error: ADDR: ', addr, ' REGS: ', regs )
            return False  

    # CONSTRUTOR 
    def __init__ ( self, COM : str = 'None', baudrate : int = 115200, SLAVE : int = 0x12, timeout : int = 0.125, *args, **kwargs ):
        if COM == 'None': 
            self.COM = 'None' 
        else:         
            self.COM = Instrument( port = COM, baudrate = baudrate,timeout = timeout,slaveaddress = SLAVE,  mode = MODE_RTU, close_port_after_each_call = False, debug = False )
            self.seriais_available.append( COM )  
        self.BAUDS     = baudrate
        self.SLAVE     = SLAVE
        self.TIMEOUT   = timeout
        self.COMPORT   = COM
    
    @property
    def monitor(self) -> list:
        return self.COM.MONITOR_DEBUG 
    @property
    def is_open(self):
        if type( self.COM ) == str: 
            return False 
        else:                       
            return self.COM.serial.is_open 

    # CONNECTION FUNCTIONS 
    def close(self):
        try:
            self.COM.serial.close()
            self.BUFFER_IN   = []
            self.BUFFER_OUT  = []
            return  True
        except:
            return -1 
    def connect(self):
        if not self.is_open: 
            try: 
                self.COM = Instrument( 
                    port = self.COMPORT, 
                    baudrate = self.BAUDS,
                    timeout = self.TIMEOUT,
                    slaveaddress = self.SLAVE,  
                    mode = MODE_RTU, 
                    close_port_after_each_call = False, 
                    debug = False)
                print( self.COM )
                return True
            except:
                print( 'Não conectou o instrumento')
                return -1 
    def get_serial_ports( self, lenght : int = 25 ):
        if self.is_open:
            portList = [ self.COMPORT ]
        else: 
            portList = [] 

        if sys.platform.startswith('win'):  
            ports = ['COM%s' % (i + 1) for i in range( lenght )]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        else:
            print("Sistema Operacional não suportado")
        for port in ports:
            try:
                s = Serial( port )
                s.close()
                portList.append(port)
            except (OSError, SerialException):
                pass
        self.seriais_available = portList
        return portList
  
    # PUBLIC FUNCTIONS 
    def read_coils(self, addr : int, num : int = 1 ) -> Union[ int, list ]: 
        return self._read_coils( addr, num )
    def read_discretes(self, addr : int, num : int = 1 ) -> Union[ int, list ]: 
        return self._read_discretes( addr, num )
    def read_holdings( self, addr : int, num : int = 1 ) -> Union[ int, list ]: 
        return self._read_holdings( addr, num )
    def read_inputs(self, addr : int, num : int ) -> Union[ int, list ]: 
        return self._read_inputs( addr, num )
    def write_coils( self, addr : int , regs : Union[ bool, list ] ) -> bool: 
        return self._write_coils( addr, regs )
    def write_holdings( self, addr : int, regs : Union[ int, float, list] ) -> bool:
        return self._write_holdings( addr, regs )
    def read_input_float(self, addr : int) -> float:
        return self._read_input_float( addr )
    
  
