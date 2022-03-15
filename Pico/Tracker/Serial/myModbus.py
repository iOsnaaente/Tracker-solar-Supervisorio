# IMPLEMENTAR OS EXCEPTIONS CODE

from Tracker.Serial.myRegisters import Registers
from constants                  import *

import machine
import struct
import time
import math 


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
    # -----------------------------------------------------


from pinout import * 

def serial_main():
    com = myModbusCommunication( 1, 115200, addr = 0x12, tx = machine.Pin(20), rx = machine.Pin(21), debug = True, parity = 'even' ) 
    print( com.myUART )
    
    com.DEBUG = True
    com.FACTOR = 1
    
    com.set_registers( DISCRETES, COILS, INPUTS, HOLDINGS )
    com.INPUTS.set_regs( 0, [12,15,6,7,14,89,1555] ) 
    com.HOLDINGS.set_regs( 0, [ 12,15,6,7,14,89,1555] ) 
        
    print( com.DISCRETES.STACK , com.DISCRETES.REGS )
    print( com.COILS.STACK     , com.COILS.REGS     )
    print( com.INPUTS.STACK    , com.INPUTS.REGS    )
    print( com.HOLDINGS.STACK  , com.HOLDINGS.REGS  )

    while True:
        if com.has_message:      
        #    print( com.DISCRETES.STACK , com.DISCRETES.REGS )
        #    print( com.COILS.STACK     , com.COILS.REGS     )
        #    print( com.INPUTS.STACK    , com.INPUTS.REGS    )
        #    print( com.HOLDINGS.STACK  , com.HOLDINGS.REGS  )
            com.has_message = False
            LED1_BLUE_PIN.value( COILS.get_reg_bool( COIL_LED1_BLUE ) ) 
            LED1_RED_PIN.value ( COILS.get_reg_bool( COIL_LED1_RED  ) ) 
            LED2_BLUE_PIN.value( COILS.get_reg_bool( COIL_LED2_BLUE ) ) 
            LED2_RED_PIN.value ( COILS.get_reg_bool( COIL_LED2_RED  ) )

        time.sleep(0.15)

if __name__ == '__main__':
    serial_main()
        
        
        




