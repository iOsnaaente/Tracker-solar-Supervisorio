
from struct import pack 
import serial

class Motors : 

    CARACTER = b'~'
    
    HORARIO     = False 
    ANTIHORARIO = True

    message_byte = ''

    pulse_per_degree = 0 
    pulses_per_turn  = 0

    def __init__(self, comport = 0 , micro_step = 1, step = 1 ):
        
        self.port = 0
        if not comport:
            self.comport  = 0
            self.port     = 0  
            self.baudrate = 0
            self.timeout  = 0     
        
        else: 
            self.comport  = comport 
            self.port     = comport.port 
            self.baudrate = comport.baudrate 
            self.timeout  = comport.timeout

        self.pos_gir = 0
        self.pos_ele = 0

        self.ang_gir = 0
        self.ang_ele = 0 

        self.rest_gir = 0 
        self.rest_ele = 0 

        self.dir_gir = 0 
        self.dir_ele = 0

        self.vel_gir = 0 
        self.vel_ele = 0 

        self.micro_step = micro_step
        self.step       = step


    def __str__(self) -> None:
        return "GIR = motor de giro\nELE = motor de elevação"


    def connect(self, comport : serial.Serial, baudrate : int, timeout : int) -> None:
        self.port     = port 
        self.baudrate = baudrate 
        self.timeout  = timeout 
        try:
            self.comport  = serial.Serial( self.port, self.baudrate, self.timeout )
        except serial.SerialException as err :
            print( "Erro ao conectar : %s " %err )


    def isOpen(self):
        return self.comport.isOpen() 


    def set_parameters(self, micro : int, step : float ) -> None :
        self.micro_step = micro 
        self.step       = step 

        self.pulse_per_degree = self.micro_step / self.step 
        self.pulses_per_turn  = self.pulse_per_degree*360  


    def move(self, dir1 : bool, ang1 : int, vel1 : int, dir2 : bool, ang2 : int, vel2 : int  ) -> None :
        self.ang_gir = ang1 
        self.ang_ele = ang2 
        self.dir_gir = dir1
        self.dir_ele = dir2
        self.vel_gir = vel1
        self.vel_ele = vel2

        self.compute_position( dir1, ang1, dir2, ang2 ) 

        self.send() 

    
    def move_to(self, ang_gir = -1, ang_ele = -1 ):
        
        diff_anti_gir = self.pos_gir + ( 360 - ang_gir ) if ang_gir is not -1 else 0 
        diff_norm_gir = self.pos_gir - ang_gir 
        diff_gir = abs(diff_anti_gir) if abs(diff_anti_gir) < abs(diff_norm_gir) else abs(diff_norm_gir)
        
        diff_anti_ele = self.pos_ele + ( 360 - ang_ele ) if ang_ele is not -1 else 0  
        diff_norm_ele = self.pos_ele - ang_ele 
        diff_ele = abs(diff_anti_ele) if abs(diff_anti_ele) < abs(diff_norm_ele) else abs(diff_norm_ele)



        # Motor de giro 
        diff_gir = self.pos_gir - ang_gir
        if diff_gir < 0 : 
            sentido_gir = self.ANTIHORARIO
            total_gir = abs(diff_gir) 
        else:
            sentido_gir = self.HORARIO
            total_gir = self.pos_gir + 360 - ang_gir  

        # Motor de elevação 
        diff_ele = self.pos_ele - ang_ele
        if diff_ele < 0 :
            sentido_ele = self.ANTIHORARIO
            total_ele = abs(diff_ele) 
        else:
            sentido_ele = self.HORARIO
            total_ele = self.pos_ele + 360 - ang_ele  
        
        self.move( sentido_gir, total_gir, self.vel_gir, sentido_ele, total_ele, self.vel_ele )


    def compute_position(self, dir_gir : bool, pos_gir : int, dir_ele : bool, pos_ele : int ) -> None : 
        ang_fin_ele = pos_ele*self.pulse_per_degree
        self.rest_ele = ang_fin_ele - int(ang_fin_ele) 
        if (self.rest_ele > 1):
            ang_fin_ele   += 1 
            self.rest_ele -= 1
        
        ang_fin_gir = pos_ele*self.pulse_per_degree
        self.rest_ele = ang_fin_gir - int(ang_fin_gir) 
        if (self.rest_ele > 1):
            ang_fin_gir   += 1 
            self.rest_ele -= 1
        
        ang_fin_ele = int(ang_fin_ele)
        ang_fin_gir = int(ang_fin_gir)
        
        self.pos_gir = self.pos_gir + ( ang_fin_gir if dir_gir is True else -ang_fin_gir) 
        self.pos_ele = self.pos_ele + ( ang_fin_ele if dir_ele is True else -ang_fin_ele) 

        # Normalizar entre 0 e 360º
        if self.pos_gir >= 360:
            self.pos_gir = self.pos_gir % 360
        elif self.pos_gir < 0:
            self.pos_gir = 360 - abs(self.pos_gir)
        
        if self.pos_ele > 360:
            self.pos_ele = self.pos_ele % 360
        elif self.pos_ele < 0:
            self.pos_ele = 360 - abs(self.pos_ele)
        


    def send( self ) -> None:
        if self.isOpen():
            message_byte = pack('BBBBBBc', self.dir_gir, self.ang_gir, self.vel_gir, self.dir_ele, self.ang_ele, self.vel_ele, self.CARACTER ) 
            try: 
                self.comport.write( message_byte )
                self.message_byte = message_byte

            except serial.SerialException as err :
                print("Impossível enviar %s erro : %s" %(message_byte, err)) 
        else:
            print('Comport não esta aberta')
    

if __name__ == '__main__': 

    com = serial.Serial('COM11', 9600, timeout= 1) 

    mot = Motors( com, 16, 1.8)

    while True: 
        ang1 = int( input('m1: ' ) )
        ang2 = int( input('m2: ' ) )

        mot.move(False, ang1, 100, False, ang2, 100)