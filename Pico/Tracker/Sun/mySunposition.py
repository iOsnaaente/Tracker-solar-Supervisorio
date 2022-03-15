from math import *

# Constants:
MPI    = 3.14159265358979323846e6  # One Megapi...
R2D    = 57.2957795130823208768    # Radians to degrees conversion factor
R2H    = 3.81971863420548805845    # Radians to hours conversion factor
TWO_PI = 6.28318530717958647693
PI     = 3.14159265358979323846

'''
A função compute faz os calculos necessários para encontrar a posição do sol dados os parametros ::
    >>> Location : list[4] -> Dados de localização ( Latitude : Longitude : Temperatura : Pressão ) [Temperatura e pressão são usados para refração, podem ser passados como nulos]
    >>> Time : list[6] -> Dados de data ( Ano AA / Mês MM / Dia DD - Hora HH : Minuto Mi : Segundo SS -- UTC = 3 para horário de Brasilia )
    >>> useDegrees : bool = True -> Saída dos dados em Graus ao invés de Radianos 
    >>> useNorthEqualsZero : bool = True -> Saída dos dados com o Norte como 0º de Azimute 
    >>> computeRefrEquatorial : bool = False -> Calcular a refração dadas a temperatura e pressão do local ( Se True deve ser passado Temperatura e pressão em Location[2:3])
    >>> computeDistance : bool = False -> Sem utilidade por enquanto 
'''
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
