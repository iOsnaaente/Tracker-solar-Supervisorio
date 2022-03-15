from machine import Pin 

'''
class Lever_control: Conrola as alavancas de movimentação::
    2 eixos de movimento -> -x e +x : -y e +y:: 
        >>> Lever_A -> Controla o eixo -x e +x
        >>> Lever_B -> Controla o eixo -y e +y
        >>> LED_A   -> Controla os leds de movimento de X
        >>> LED_B   -> Controla os leds de movimento de Y 
'''

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
        