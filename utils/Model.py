import datetime 
import ephem 

# CLASSE DE POSIÇÃO DO SOL USANDO EPHEM  
class SunPosition:
    # SEGUNDOS DO DIA E DIAS JULIANOS TOTAIS 
    total_seconds = 0
    dia_juliano   = 0 

    # DEFINIÇÃO DE DATA E HORA 
    year   = 0
    month  = 0
    day    = 0
    hour   = 0
    minute = 0
    second = 0

    # DEFINIÃO DOS PARAMETROS DE LAT/LONG
    latitude = 0        #-29.165307659422155
    longitude = 0       #-54.89831672609559

    # ALTURA - AZIMUTE - SOL 
    alt = 0 
    azi = 0 

    # ALTURA - AZIMUTE - LUA
    m_alt = 0
    m_azi = 0 

    # NASCER DO SOL - TRANSIÇÃO - POR DO SOL 
    rising  = 0  
    transit = 0  
    sunset  = 0 

    elevation_transit = 0.0 
    azimute_sunrise   = 0.0 
    azimute_sunset    = 0.0 

    winter_solstice = 0 
    summer_solstice = 0 
    equinox         = 0 


    def __init__(self, latitude, longitude, altitude, utc_local = -3 ):
        # DEFINIÇÃO DOS PARAMETROS 
        self.latitude  = latitude 
        self.longitude = longitude
        self.altitude  = altitude

        # CRIAÇÃO DO OBSERVADOR 
        self.me = ephem.Observer()

        # CRIAÇÃO DO ASTRO OBSERVADO
        self.sun = ephem.Sun()
        self.moon = ephem.Moon()

        # DEFINIÇÃO DO OBSERVADOR 
        self.me.lat       = self.latitude 
        self.me.lon       = self.longitude
        self.me.elevation = self.altitude

        # HORÁRIO LOCAL 
        self.utc_local = utc_local 

        # ATUALIZAÇÃO DA DATA E COMPUTAÇÃO DOS VALORES 
        self.date = 0
        self.update_date()

    # Para setar novos parametros 
    def set_parameters(self, latitude, longitude, altitude ):
        # DEFINIÇÃO DOS NOVOS PARAMETROS 
        self.latitude  = latitude 
        self.longitude = longitude
        self.altitude  = altitude

        # ATUALIZAÇÃO DO OBSERVADOR 
        self.me.lat       = self.latitude 
        self.me.lon       = self.longitude
        self.me.elevation = self.altitude

        # ATUALIZAÇÃO DOS CALCULOS
        self.update()
    
    def update_coordenates(self):
        self.me.lat       = self.latitude
        self.me.lon       = self.longitude
        self.me.elevation = self.altitude
        self.update()
    
    # Calculo das horas de sol do dia 
    def get_sunlight_hours(self):
        return (self.sunset - self.rising)

    # Setar a data manualmente
    def set_date(self, data):
        # OBRIGADO USAR DARA NO ESTILO DATETIME.DATETIME
        if type(data) is datetime.datetime:
            self.date = data
            self.update_date(True)

    # Atualiza a data 
    def update_date(self, manual = False):
        if not manual:
            # Pega a hora local
            self.date   = datetime.datetime.utcnow()
        self.year   = self.date.year   
        self.month  = self.date.month  
        self.day    = self.date.day    
        self.hour   = self.date.hour + self.utc_local 
        self.minute = self.date.minute 
        self.second = self.date.second 
        self.total_seconds = self.second + self.minute*60 + self.hour*3600
        self.dia_juliano   = self.DJ()

        # ATUALIZAÇÃO DOS DADOS PASSADOS 
        self.update()

    # calculo do Dia Juliano segundo - ghiorzi.org/diasjuli.html
    def DJ( self ):
        y = self.year
        m = self.month
        d = self.day 
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

    def update(self):
        # ATUALIZAÇÃO DO OBSERVADOR 
        self.me.lat = self.latitude 
        self.me.lon = self.longitude 
        self.me.date = self.date 
        
        # COMPUTAÇÃO DOS DADOS
        self.sun.compute( self.me )
        self.moon.compute( self.me )

        # Calculando a altitude e azimute - do sol 
        self.alt = float( self.sun.alt )  
        self.azi = float( self.sun.az  ) 

        # Calculando a altitude e azimute - da Lua 
        self.m_alt = float( self.sun.alt )  
        self.m_azi = float( self.sun.az  )  
        
        # Calculando o nascer e por do sol
        self.rising  = self.me.previous_rising( self.sun ).datetime()
        self.transit = self.me.next_transit( self.sun ).datetime()   
        self.sunset  = self.me.next_setting( self.sun ).datetime()    
        
        self.me.date = self.rising 
        self.sun.compute( self.me )
        self.azimute_sunrise = float( self.sun.az )
        
        self.me.date = self.transit 
        self.sun.compute( self.me )
        self.elevation_transit = float( self.sun.alt )
        
        self.me.date = self.sunset 
        self.sun.compute( self.me )
        self.azimute_sunset = float( self.sun.az )

        self.winter_solstice = ephem.next_solstice( str(self.date.year)  )
        self.summer_solstice = ephem.next_solstice( self.winter_solstice )

    def get_azi_from_date(self, date):
        self.me.date = date 
        self.sun.compute( self.me )

        # Calculo do azimute e altitude 
        alt = self.sun.alt.norm   # Altitude above horizon  # -13:04:48.9
        azi = self.sun.az.norm    # Azimuth east of north   #  226:41:12.8
        
        # Retorna a data ao self.me.date 
        self.me.date = self.date 
        self.update() 
        
        return [ alt, azi ]

    def trajetory(self, resolution = 24, all_day = False ):
        # Hora do dia atual 
        self.update()
        
        if all_day: 
            # Total de segundos em um dia 
            delta_day_time = 24*3600 - 1
            diff = datetime.timedelta ( seconds = delta_day_time // resolution )
            today = datetime.datetime( self.date.year, self.date.month, self.date.day, 0, 0, 0)
        else:
            # Total de segundos do nascer do sol ao por do sol 
            delta_day_time = self.sunset - self.rising 
            diff = datetime.timedelta ( seconds = delta_day_time.seconds // resolution ) 
            today = datetime.datetime( self.date.year, self.date.month, self.date.day, self.rising.hour , self.rising.minute, self.rising.second)
 
        # Lista de pontos
        dots = []        
        for i in range( resolution ):
            # Atualização da data para configuração dos pontos 
            self.me.date = today + diff * i 
            self.sun.compute( self.me )

            # Calculo do azimute e altitude 
            alt = self.sun.alt.norm   # Altitude above horizon  # -13:04:48.9
            azi = self.sun.az.norm    # Azimuth east of north   #  226:41:12.8

            dots.append( [ azi, alt ] )
        
        # Retorna a data ao self.me.date 
        self.me.date = self.date 
        self.update() 

        return dots





##########################################################################################################################################

from struct import pack 
import serial

class Motors : 

    CARACTER = b'~'
    
    message_byte = ''

    pulse_per_degree = 0 
    pulses_per_turn  = 0

    def __init__(self, comport = 0 , micro_step = 1, step = 1 ):
        
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
        
        HORARIO     = True 
        ANTIHORARIO = False

        # Motor de giro 
        diff_gir = self.pos_gir - ang_gir
        if diff_gir < 0 : 
            sentido_gir = HORARIO
            total_gir = abs(diff_gir) 
        else:
            sentido_gir = ANTIHORARIO
            total_gir = self.pos_gir + 360 - ang_gir  

        # Motor de elevação 
        diff_ele = self.pos_ele - ang_ele
        if diff_ele < 0 :
            sentido_ele = HORARIO
            total_ele = abs(diff_ele) 
        else:
            sentido_ele = ANTIHORARIO
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
    
