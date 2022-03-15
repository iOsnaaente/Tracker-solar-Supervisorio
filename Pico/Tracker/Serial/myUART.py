import machine
import struct 
import time

class UART_SUP:

    # SERIAL CONFIGURAÇÕES 
    BYTE_INIT = [b'I',b'N',b'I',b'T']  
    count     = 0
    
    data_bits = 8
    stop_bits = 1
    timeout   = 0
    parity    = 1

    def __init__( self, uart_num : int, baudrate : int, tx : int, rx : int, **kwargs ):
        
        if kwargs.keys():
            if 'parity' in kwargs.keys():
                self.parity = kwargs['parity']
                if type( self.parity ) == str :
                    if self.parity == 'even' : self.parity = 0
                    elif self.parity == 'odd': self.parity = 1
                    else                     : self.parity = None
                elif type( self.parity ) == int:
                    if self.parity > 1 or self.parity < 0:
                        self.parity = None
            else:
                self.parity = None 
                    
            if 'stop_bits' in kwargs.keys():
                self.stop_bits = kwargs['stop_bits']
                if type( self.stop_bits ) is not int:
                    self.stop_bits = 1
            else:
                self.stop_bits = 1 
                    
            if 'data_bits' in kwargs.keys():
                self.data_bits = kwargs['data_bits']
                if type( self.data_bits ) is not int:
                    self.data_bits = 8
            else:
                self.data_bits = 8 
            
            if 'timeout' in kwargs.keys():
                self.timeout =  kwargs['timeout']
                if type( self.timeout ) is not int:
                    self.timeout = 0
            else:
                self.timeout = 0.05

        self.myUART = machine.UART( uart_num, baudrate, parity=self.parity, stop=self.stop_bits, bits=self.data_bits, rx=rx, tx=tx)

    
    # Função de leitura 
    def read(self, nbytes : int = 1 ) -> bytes:
        if self.myUART.any():
            return self.myUART.read( nbytes )
        else:
            return False
    
    # Função de escrita
    def write( self, msg ) -> int:
        if type( msg ) == str:
            msg = msg.encode()
        elif type(msg) == bytes:
            return self.myUART.write( msg ) 
        else:
            return False 
    
    # VERIFICA SE RECEBEU ALGO DA SERIAL 
    def recv_from(self) -> str :
        while self.myUART.any():
            cmd = self.myUART.read(1)
            if cmd == self.BYTE_INIT[self.count]: self.count += 1
            else:                                 self.count  = 0
            if self.count == 4:
                self.count = 0
                return self.myUART.read(1)
        return False

    # Responde com uma mensagem identificada e um valor agregado 
    def response( self, **kwargs ):
        try: 
            for key, value in kwargs.items():
                value = struct.pack( 'f', value )  
                key = key.encode()
                msg = key + value
                self.write( msg )
            return True 
        except:
            return False 
    
    
    def response_msg( self, **kwargs ):
        try: 
            for key, value in kwargs.items():
                if type(value) == bytes:
                    pass
                elif type(value) == str:
                    value = value.encode() 
                key = key.encode()
                msg = key + value
                self.write( msg )
            return True 
        except:
            return False 
  