from math import ceil
import struct

# INTERFACE
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
    
  


# ---------------------------------------- #
# To call the main function 
def mainRegisters():
    
    #a = Registers( 10, bool ) # 10 REGS = 5 floats 
    #a.set_regs_bool( 0, [ True, False, True, True, True, False] ) 
    #print( a.get_regs_bool(2, 8) )
    #print( a.STACK )
    
    a = Registers( 12, int ) # 10 REGS = 5 floats 
    a.set_regs_float( 2, [12.054, 168.6, 1435.14, 135.5] )
    #a.set_reg_float( 3, 16.783 ) 
    
    print( a.STACK )
    print( a.get_regs_float( 6, 2 ) ) 

    print ( a.__str__() )
    
if __name__ == '__main__' :
    mainRegisters()
# ---------------------------------------- #

