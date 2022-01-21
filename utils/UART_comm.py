from serial import Serial, SerialException
from typing import Union
import sys 
import glob

from serial.serialutil import PARITY_ODD 
   

class UART_COM( Serial ):
    
    seriais_available = [] 
    BUFFER_MAX = 30
    BUFFER_IN  = []
    BUFFER_OUT = [] 

    COUNTER_OUT = 0 
    COUNTER_IN  = 0 

    def __init__ ( self, COM : str, baudrate : int = 9600, timeout : int = 1, *args, **kwargs ):
        try: 
            super().__init__( COM, baudrate = baudrate, timeout = timeout, parity = PARITY_ODD)
            self.seriais_available.append( COM )  
            self.BAUDS     = baudrate
            self.TIMEOFF   = timeout
            self.COMPORT   = COM
            self.connected = True 
        except:
            self.connected = False 
            print( "Serial comport cant be opened" ) 
        
    def _write(self, data  : bytes ):
        return super().write(data)
    
    def _read(self, size : int = 1 ):
        return super().read( size = size )

    def write( self, msg : Union[str, bytes] ): 
        if self.connected: 
            if type( msg ) == str: 
                self.BUFFER_OUT.append( msg.encode() )
                self._write( self.BUFFER_OUT[-1] )
            elif type( msg ) == bytes:
                self.BUFFER_OUT.append( msg )
                self._write( self.BUFFER_OUT[-1] )
            else: 
                return -1 
            if len(self.BUFFER_OUT) > self.BUFFER_MAX:
                self.BUFFER_OUT.pop( 0 )
            self.COUNTER_OUT += 1 
            return True
        else: 
            return -1 

    def read( self, n_bytes : int = 0 ):
        if self.connected:
            if n_bytes == 0:
                n_bytes = self.in_waiting() 
            self.BUFFER_IN.append( self._read( n_bytes ) ) 
            if len(self.BUFFER_IN) > self.BUFFER_MAX: 
                self.BUFFER_IN.pop(0)
            self.COUNTER_IN += 1 
            return self.BUFFER_IN[-1]
        else:
            return [] 
    
    def in_waiting(self):
        try: 
            if self.connected: 
                return super().in_waiting 
            else: 
                return -1 
        except: 
            print("Erro no In_Waiting")
            return -1 

    def isOpen(self):
        return super().isOpen()

    def close(self):
        try:
            super().close() 
            self.connected   = False 
            self.BUFFER_IN   = []
            self.BUFFER_OUT  = [] 
            self.COUNTER_IN  = 0
            self.COUNTER_OUT = 0
            return  True
        except:
            return -1 

    def connect(self):
        if not self.connected: 
            try: 
                super().__init__( self.COMPORT, baudrate = self.BAUDS, timeout = self.TIMEOFF )
                self.connected = True
                return True
            except:
                self.connected = False
                return -1 

    def get_serial_ports( self, lenght : int = 25 ):
        if self.connected:
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