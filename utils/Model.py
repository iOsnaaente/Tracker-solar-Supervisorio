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
        if type( latitude  ) == float: latitude  = str( latitude  )
        if type( longitude ) == float: longitude = str( longitude )
        
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
        if type( latitude  ) == float: latitude  = str( latitude  )
        if type( longitude ) == float: longitude = str( longitude )

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
    
    def set_latitude(self, latitude):
        if type( latitude  ) == float: latitude  = str( latitude  )
        self.latitude         = latitude 
        self.me.lat           = self.latitude 
        self.update()

    def set_longitude(self, longitude ): 
        if type( longitude ) == float: longitude = str( longitude )
        self.longitude        = longitude
        self.me.lon           = self.longitude
        self.update() 

    def set_altitude(self, altitude):
        self.altitude     = altitude
        self.me.elevation = self.altitude
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
        # OBRIGADO USAR DATA NO ESTILO DATETIME.DATETIME
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
        try:
            self.rising  = self.me.previous_rising( self.sun ).datetime()
            self.transit = self.me.next_transit( self.sun ).datetime()   
            self.sunset  = self.me.next_setting( self.sun ).datetime()    
        except:
            print( 'Fora dos limites aceitáveis de calculo para sunrising/sunrise devido ao circulo polar ') 

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

    def get_pos_from_date(self, date):
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
            time = today + diff * i 
            dots.append( [ azi, alt, time ] )
        
        # Retorna a data ao self.me.date 
        self.me.date = self.date 
        self.update() 

        return dots
