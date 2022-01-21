# Bibliotecas oficiais
from dearpygui.simple import *
from dearpygui.core   import * 

from collections import defaultdict 
from threading   import Thread
from threading   import Lock 

import datetime
import serial 
import ephem

import math
import sys


# Bibliotecas pessoais 
from utils.Async_function_BB import Async_function
from utils.serial_reader     import serialPorts 
from utils.Model             import SunPosition
from utils.Model             import Motors
    

# Definições de exibição 
X, Y = get_main_window_size()
set_main_window_pos( 100,0 )
set_main_window_size( X, Y )
set_main_window_title('Supervisorio Tracker - Teste')

# Definição das cores e alfa 
color = {
    "black"   : lambda alfa : [   0,   0,   0, alfa ],
    "red"     : lambda alfa : [ 255,   0,   0, alfa ],
    "yellow"  : lambda alfa : [ 255, 255,   0, alfa ],
    "green"   : lambda alfa : [   0, 255,   0, alfa ],
    "ciano"   : lambda alfa : [   0, 255, 255, alfa ],
    "blue"    : lambda alfa : [   0,   0, 255, alfa ],
    "magenta" : lambda alfa : [ 255,   0, 255, alfa ],
    "white"   : lambda alfa : [ 255, 255, 255, alfa ],
    'gray'    : lambda alfa : [ 155, 155, 155, alfa ],
    'orange'  : lambda alfa : [ 255,  69,   0, alfa ],
}


# FUNÇÕES 
map_val = lambda value, in_min, in_max, out_min, out_max : ((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min ) 

cos = lambda x : math.cos( x )
sin = lambda x : math.sin( x )
tg  = lambda x : math.tan( x )


# MACRO 
LATITUDE  = '-29.16530765942215'
LONGITUDE = '-54.89831672609559'
ALTITUDE  = 425
UTC_HOUR  = -3

# GLOBAIS
sun_angle_elevation   = 1 
sun_angle_azimute     = 2 

motor_angle_base      = 3
motor_angle_elevation = 4 

resolucaoM1           = 0 
passosM1              = 0 
uPassosM1             = 0 

resolucaoM2           = 0 
passosM2              = 0 
uPassosM2             = 0

window_opened = ''

num_wind = 1 

# DESCOMENTAR PARA FUNCIONAR AS COMPORTS 
#port_list = serialPorts(15)
port_list = [] 

color_maps2plot = ["Default", "Dark", "Pastel", "Paired", "Viridis", "Plasma", "Hot", "Cool", "Pink", "Jet"]

# Configurações padrão 
w, h = 350, 225 
center = [w//2, h//2]
r = 75 
 
serial_log = []

sun_data = SunPosition( LATITUDE, LONGITUDE, ALTITUDE )
sun_data.update_date()

# Janelas 
windows = {
    'Inicio'              : ['Header##IN'          ,'Lateral##IN'           , 'Main##IN'      ],
    'Visualização geral'  : ['Solar_pos##VG'       , 'Atuação##VG'          , 'AtuaçãoBase##VG', 'AtuaçãoElevação##VG', 'log##VG' ],
    'Posição do sol'      : ["Visualização##PS"    , "Altura##PS"           , "Azimute##PS"    , "log##PS"           ],
    "Atuadores"           : ["Controle##AT"        , 'Visualização##AT'     , 'Retorno##AT'    ,'Retorno M2##AT'     ], 
    "Atuação da base"     : ['Visualização##MG'    , 'Infos_inferiores##MG' , 'log##MG'       ], 
    "Atuação da elevação" : ['Visualização##ME'    , 'Infos_inferiores##ME' , 'log##ME'       ],
    'Configurações'       : ['Configurações##CONF'],
    }

window_size = [ 0, 0 ]

# CALLBACKS 
def mouse_update(sender, data): 
    pos = get_mouse_pos( local = True )
    print( pos, get_active_window() )

def render_update(sender, data):
    global sun_angle_azimute, sun_angle_elevation, motor_angle_base, motor_angle_elevation 
    global window_size 

    sunlight = sun_data.get_sunlight_hours()
    now      = datetime.datetime.utcnow() 

    sun_angle_azimute   = math.radians(sun_data.azi)
    sun_angle_elevation = math.radians(sun_data.alt) 

    motor_angle_base      = motor_angle_base + (sun_angle_azimute - motor_angle_base) * get_delta_time() if abs(sun_angle_azimute - motor_angle_base) > 0.005 else motor_angle_base
    motor_angle_elevation = motor_angle_elevation + ( sun_angle_elevation - motor_angle_elevation) * get_delta_time() if abs(sun_angle_elevation - motor_angle_elevation) > 0.005 else motor_angle_elevation
    
    modify_draw_command('MotorElevação', 'Sun'  , p1 = [ (w//2)+r*math.cos( sun_angle_elevation ), h//2+r*math.sin( sun_angle_elevation )] )
    modify_draw_command('MotorBase',     'Sun'  , p1 = [ (w//2)+r*math.cos( sun_angle_azimute )  , h//2+r*math.sin( sun_angle_azimute )  ] )
 
    modify_draw_command('MotorElevação', 'Motor', p1 = [ (w//2)+r*math.cos( motor_angle_elevation ),  h//2+r*math.sin( motor_angle_elevation ) ] )
    modify_draw_command('MotorBase',     'Motor', p1 = [ (w//2)+r*math.cos( motor_angle_base )     ,  h//2+r*math.sin( motor_angle_base      ) ] )

    window_size = get_main_window_size() 

    if window_opened == 'Inicio'                 :
        
        configure_item( 'Header##IN', width = window_size[0]-35                , height = (window_size[1]//10)*3           )
        configure_item( "headerImage", width = get_item_width('Header##IN')-16 , height = get_item_height('Header##IN')-16 )
    
        modify_draw_command('headerImage', 'headerImageTorre', pmin= (-30,-30), pmax= ( window_size[0], round( window_size[1]*3/10)*2 ))
        modify_draw_command('headerImage', 'headerLogo'      , pmin= (10,10)  , pmax= (350,200) )
        
        v_spacing =  get_item_height('Lateral##IN') // 7
        
        configure_item('Lateral##IN'             , width = (window_size[0]//3)   , height = (window_size[1]//10)*6 , x_pos = 10, y_pos = (window_size[1]//10)*3 +30  )
        configure_item( "Visualização geral##IN" , width = window_size[0]//3 - 15, height = v_spacing ) 
        configure_item( "Posição do sol##IN"     , width = window_size[0]//3 - 15, height = v_spacing ) 
        configure_item( "Atuadores##IN"          , width = window_size[0]//3 - 15, height = v_spacing ) 
        configure_item( "Atuação da base##IN"    , width = window_size[0]//3 - 15, height = v_spacing ) 
        configure_item( "Atuação da elevação##IN", width = window_size[0]//3 - 15, height = v_spacing ) 
        configure_item( "Configurações##IN"      , width = window_size[0]//3 - 15, height = v_spacing ) 
        
        configure_item('Main##IN' , width = (window_size[0]//3)*2 -37 , height = (window_size[1]//10)*6 , x_pos = window_size[0]//3 + 15, y_pos = (window_size[1]//10)*3 + 30 )
    
    elif window_opened == 'Visualização geral'   :

        configure_item('Solar_pos##VG', width = round(window_size[0]*2/3)          , height = round(window_size[1]*5/10)          )
        configure_item('Solar_pos##VG', x_pos = 10, y_pos = 25 )
        
        configure_item('Solar'        , width = get_item_width('Solar_pos##VG')-20 , height = get_item_height('Solar_pos##VG')-70 )
        configure_item('progressive'  , width = get_item_width('Solar_pos##VG')    , height = 30                                  ) 
        
        clear_drawing('Solar')
        draw_sun_trajetory('Solar',  get_item_width('Solar_pos##VG')-20,  get_item_height('Solar_pos##VG')-75 )

        configure_item( 'Atuação##VG'        , width = (window_size[0]//3)*2               , height = round(window_size[1]*4/10)-20      )
        configure_item( 'AtuaçãoBase##VG'    , width = get_item_width('Atuação##VG')//2-10 , height = get_item_height('Atuação##VG')-50  )
        configure_item( 'AtuaçãoElevação##VG', width = get_item_width('Atuação##VG')//2-10 , height = get_item_height('Atuação##VG')-50  )
        
        configure_item( 'Atuação##VG'        , x_pos = 10                                     , y_pos = round( window_size[1]*5/10)+30    )
        configure_item( 'AtuaçãoBase##VG'    , x_pos = 15                                     , y_pos = round( window_size[1]*5/10)+75    )
        configure_item( 'AtuaçãoElevação##VG', x_pos = 20 + get_item_width('AtuaçãoBase##VG') , y_pos = round( window_size[1]*5/10)+75    )
        
        configure_item( 'log##VG'            , width = round( window_size[0]/3   ) - 40       , height = round( window_size[1]*9/10) -15  )
        configure_item( 'log##VG'            , x_pos = round( window_size[0]*2/3 ) + 15       , y_pos  = 25                               )
        
        # Definição da Latitude/Longitude 
        sun_data.latitude  = str( get_value('Latitude')  )
        sun_data.longitude = str( get_value('Longitude') )
        sun_data.update_coordenates()

        # Horário automático 
        if ( get_value('Hora manual') is False ):
            # Definição do dia local e hora local
            sun_data.update_date()
            set_value('Dia automatico', [ sun_data.year, sun_data.month, sun_data.day ] ) 
            set_value('Hora automatica', [ sun_data.hour, sun_data.minute, sun_data.second ] )
            set_value('Total segundos', sun_data.total_seconds )
            # Total de segundos no dia convertido entre 0 e 1
            total_seconds_converted = map_val(sun_data.total_seconds, 0, 24*3600, 0, 1)
            set_value('progressive', total_seconds_converted)
            # Dias Julianos 
            set_value( "Dia Juliano", sun_data.dia_juliano)

        else:
            # Pegando a data e hora passadas pelo usuário
            year, month, day     = get_value('Dia arbitrario')
            hour, minute, second = get_value('Hora arbitraria') 
            # Montar a data setada pelo usuário
            data = datetime.datetime( int(year), int(month), int(day), int(hour), int(minute), int(second) )
            sun_data.set_date( data )
            # Total de segundos no dia
            set_value('Total segundos##', sun_data.total_seconds)
            # Total de segundos no dia convertidos entre 0 e 1
            total_seconds_converted = map_val(sun_data.total_seconds, 0, 24*3600, 0, 1)
            set_value('progressive', total_seconds_converted)
            # Calculo do dia Juliano 
            set_value( "Dia Juliano##", sun_data.dia_juliano)

        # Setar o Azimute, Altitude e Elevação
        set_value('Azimute', math.degrees( sun_data.azi) )
        set_value('Altitude', math.degrees( sun_data.alt) )
        set_value('Elevação (m)', sun_data.altitude)

        # Seta as horas do sol calculando as horas minutos e segundos de segundos totais 
        diff_sunlight = (sun_data.sunset - sun_data.rising).seconds
        set_value('Horas de sol', [diff_sunlight//3600, (diff_sunlight//60)%60 , diff_sunlight%60 ] )

        # Setar as informações de Nascer do sol, Culminante (ponto mais alto) e Por do sol
        set_value('Nascer do sol', [ sun_data.rising.hour+sun_data.utc_local , sun_data.rising.minute , sun_data.rising.second  ] )
        set_value('Culminante'   , [ sun_data.transit.hour+sun_data.utc_local, sun_data.transit.minute, sun_data.transit.second ] )
        set_value('Por do sol'   , [ sun_data.sunset.hour+sun_data.utc_local , sun_data.sunset.minute , sun_data.sunset.second  ] )    

    elif window_opened == 'Posição do sol'       : 
        
        # Definição da Latitude/Longitude 
        sun_data.latitude  = str( get_value('Latitude (º)##PS' ) )
        sun_data.longitude = str( get_value('Longitude (º)##PS') )
        sun_data.altitude  = get_value('Altura (m)##PS')
        sun_data.update_coordenates()


        
        set_value ( 'Data atual##PS'     , value = [ now.year, now.month, now.day ] )
        set_value ( 'Data de calculo##PS', value = [ sun_data.year, sun_data.month, sun_data.day ] )
        
        set_value ( 'Nascer do sol##PS', value = [ sun_data.rising.hour + sun_data.utc_local, sun_data.rising.minute , sun_data.rising. second] )        
        set_value ( 'Transição##PS'  , value = [ sun_data.transit.hour+ sun_data.utc_local, sun_data.transit.minute, sun_data.transit. second] )        
        set_value ( 'Por do sol##PS'    , value = [ sun_data.sunset.hour + sun_data.utc_local, sun_data.sunset.minute , sun_data.sunset. second] ) 

        set_value ( 'Horas de luz##PS'  , value = [sunlight.seconds//3600, (sunlight.seconds//60)%60, sunlight.seconds%60] ) 

        set_value ( 'Altitude (º)##PS'  , value = math.degrees( sun_data.alt) ) 
        set_value ( 'Azimute (º)##PS'   , value = math.degrees( sun_data.azi) )

        #set_value ( 'Sombra (m)##PS'    , value = get_value('Altura Obj (m)##PS')/tg( sun_data.alt -math.pi/2 ) )  # Tg(teta)/altura = Projeção da sombra
       
        set_value ( 'Altura (m)##PS'    , value = sun_data.altitude )
        set_value ( 'Latitude (º)##PS'  , value = float( sun_data.latitude  ) )
        set_value ( 'Longitude (º)##PS' , value = float( sun_data.longitude ) )

        set_value ( 'UTM local (h)##PS'     , value = sun_data.utc_local )

    elif window_opened == "Atuadores"            :

        configure_item('Controle##AT'       , width = round( window_size[0]/3 ) - 20                                     , height = window_size[1] - 75               )
        configure_item('Controle##AT'       , x_pos = 10                                                                 , y_pos = 25                                 )
        configure_item('Retorno##AT'        , width = (window_size[0]//3)-10                                             , height = (window_size[1]//2)               )
        configure_item('Retorno##AT'        , x_pos = get_item_width('Controle##AT')+15                                  , y_pos = 25                                 )
        configure_item('Retorno M2##AT'     , width = (window_size[0]//3)-10                                             , height = (window_size[1]//2)               )
        configure_item('Retorno M2##AT'     , x_pos = get_item_width('Controle##AT')+get_item_width('Retorno M2##AT')+20 , y_pos = 25                                 )
        configure_item('Visualização##AT'   , width = (window_size[0]//3)*2 -15                                          , height = (window_size[1]//2)-85            )
        configure_item('Visualização##AT'   , x_pos = get_item_width('Controle##AT')+15                                  , y_pos = get_item_height('Retorno##AT')+35  )

        configure_item('Controle_child##AT'  , width = get_item_width('Controle##AT')-15       )
        configure_item('MotorGiro##AT'       , width = get_item_width('Controle##AT')-15       )
        configure_item('MotorElevação##AT'   , width = get_item_width('Controle##AT')-15       )

        configure_item('PORT##AT'            , width = get_item_width('Controle_child##AT')-15 )
        configure_item('BAUDRATE##AT'        , width = get_item_width('Controle_child##AT')-15 )
        configure_item('TIMEOUT##AT'         , width = get_item_width('Controle_child##AT')-15 )
        configure_item('Iniciar conexão##AT' , width = get_item_width('Controle_child##AT')-15 )

        configure_item('ResoluçãoM1##AT'     , width = get_item_width('MotorGiro##AT')-15      )
        configure_item('PassosM1##AT'        , width = get_item_width('MotorGiro##AT')-15      )
        configure_item('MicroPassosM1##AT'   , width = get_item_width('MotorGiro##AT')-15      )

        configure_item('ResoluçãoM2##AT'     , width = get_item_width('MotorElevação##AT')-15 )
        configure_item('PassosM2##AT'        , width = get_item_width('MotorElevação##AT')-15 )
        configure_item('MicroPassosM2##AT'   , width = get_item_width('MotorElevação##AT')-15 )

        resolucaoM1 = get_value('ResoluçãoM1##AT'  )
        passosM1    = get_value('PassosM1##AT'     )
        uPassosM1   = get_value('MicroPassosM1##AT')

        resolucaoM2 = get_value('ResoluçãoM2##AT'  )
        passosM2    = get_value('PassosM2##AT'     )
        uPassosM2   = get_value('MicroPassosM2##AT')

        try:
            read_from = comport.readlines(5)
            if read_from != []:
                serial_log.append( read_from ) 
            add_text('Serial: %s'%serial_log[-1])
        except:
            pass

    elif window_opened == "Atuação da base"      :
        configure_item('Infos_inferiores##MG', width = round(window_size[0]*3/5)-10, height = round( window_size[1]/4)-50   , x_pos = 10                          , y_pos = round( window_size[1]*3/4)+5   )
        configure_item('log##MG'             , width = round(window_size[0]*2/5)-25, height = round( window_size[1])-70     , x_pos = round(window_size[0]*3/5)+5 , y_pos = 25   )
        configure_item('Visualização##MG'    , width = round(window_size[0]*3/5)-10, height = round( window_size[1]*3/4)-25 , x_pos = 10                          , y_pos = 25   )
    
        configure_item('Configurações_M1##MG', width= get_item_width('log##MG')-15, height= 150 )

        configure_item('RPM_M1##MG', width= get_item_width('Configurações_M1##MG')-10 )
        configure_item('REDU_M1##MG', width= get_item_width('Configurações_M1##MG')-10 )
        configure_item('RPM_OUT_M1##MG', width= get_item_width('Configurações_M1##MG')-10 )

        set_value('RPM_OUT_M1##MG', value= get_value('RPM_M1##MG')*get_value('REDU_M1##MG')[0]/get_value('REDU_M1##MG')[1] )

    elif window_opened == "Atuação da elevação"  :
        configure_item('Infos_inferiores##ME', width = round(window_size[0]*3/5)-10 , height = round( window_size[1]/4)-50   , x_pos = 10                          , y_pos = round( window_size[1]*3/4)+5   )
        configure_item('log##ME'             , width = round(window_size[0]*2/5)-25 , height = round( window_size[1])-70     , x_pos = round(window_size[0]*3/5)+5 , y_pos = 25   )
        configure_item('Visualização##ME'    , width = round(window_size[0]*3/5)-10 , height = round( window_size[1]*3/4)-25 , x_pos = 10                          , y_pos = 25   )

        configure_item('Configurações_M2##ME', width= get_item_width('log##ME')-15  , height= 150)
        
        configure_item('RPM_M2##ME'          , width= get_item_width('Configurações_M2##ME')-10 )
        configure_item('REDU_M2##ME'         , width= get_item_width('Configurações_M2##ME')-10 )
        configure_item('RPM_OUT_M2##ME'      , width= get_item_width('Configurações_M2##ME')-10 )
        
        set_value('RPM_OUT_M2##ME', value = get_value('RPM_M2##ME')*get_value('REDU_M2##ME')[0]/get_value('REDU_M2##ME')[1] )

    elif window_opened == 'Configurações'        : 
        configure_item('Configurações##CONF', width = window_size[0]-25, height = window_size[1]-70, x_pos = 5, y_pos = 25 )

    configure_item( 'Sair##Sair', x_pos= (get_main_window_size()[0]//2)-100 , y_pos= (get_main_window_size()[1]//2)-100 )
    
    global num_wind
    if is_mouse_button_clicked(1):
        add_window('window-%s'%num_wind, width=100, height= 100, x_pos= int(get_mouse_pos()[0]), y_pos= int(get_mouse_pos()[1]) )
        num_wind += 1
    if is_mouse_button_clicked(2):
        print( get_mouse_pos() )

def hora_manual(sender, data):
    # Verifica a condição do CheckBox
    status = get_value('Hora manual')
    # Configuração dos parametros automáticos
    configure_item('Dia automatico', enabled = not status )
    configure_item('Hora automatica', enabled = not status)
    configure_item('Total segundos', enabled = not status)
    configure_item('Dia Juliano', enabled = not status)
    # Configuração dos parametros manuais 
    configure_item( "Hora arbitraria", enabled = status )
    configure_item( "Dia arbitrario", enabled = status )
    configure_item('Total segundos##', enabled = status )
    configure_item('Dia Juliano##', enabled = status)

def change_menu(sender, data):
    global window_opened 
    window_opened = sender
    # CLOSE ALL WINDOWS 
    for k in windows.keys():
        for i in windows[k]:
            hide_item(i)
    # OPEN THE RIGHT TAB WINDOW 
    to_open = windows[sender]
    for i in to_open:
        show_item(i)

# FUNÇÕES
def draw_sun_trajetory( name_drawboard, width, height, all_day = False, extremes = False ):
    # Ponto central e Raio 
    center = [width//2, height//2]
    r = width//2 - 20 if width+20 <= height else height//2 - 20

    # Desenho estático 
    draw_line( name_drawboard, p1 = [center[0] - r, center[1]], p2 = [center[0] + r, center[1]], color = color['gray'](155), thickness= 1 )
    
    # DESENHO DA LINHA DE NASCER DO SOL E POR DO SOL 
    ang = sun_data.get_azi_from_date( sun_data.rising )[1]
    draw_line( name_drawboard, p1 = center, p2 = [center[0] + r*cos(ang-math.pi/2), center[1] + r*sin(ang-math.pi/2)], color = color['orange'](155), thickness= 2 )
    ang = sun_data.get_azi_from_date( sun_data.sunset )[1] # [ alt , azi ]
    draw_line( name_drawboard, p1 = center, p2 = [center[0] + r*cos(ang-math.pi/2), center[1] + r*sin(ang-math.pi/2)], color = color['gray'](200), thickness= 2 )

    # Desenhos estáticos 
    draw_circle( name_drawboard, center, r, color['white'](200), fill = color['white'](10 ), thickness = 3 )
    draw_circle( name_drawboard, center, 3, color['white'](200), fill = color['white'](255), thickness = 2 )
    draw_text( name_drawboard, pos= [center[0] - (r + 20), center[1] -10 ], text = 'W', color = color['white'](200), size=20 )
    draw_text( name_drawboard, pos= [center[0] + (r +  5), center[1] -10 ], text = 'E', color = color['white'](200), size=20 )
    draw_text( name_drawboard, pos= [center[0] - 10 , center[1] - (r + 25)  ], text = 'N', color = color['white'](255), size=20 )
    
    # PEGA OS ANGULOS NOS PONTOS DA TRAJETÓRIA DO SOL 
    dots = sun_data.trajetory(100, all_day )

    # PONTOS DE ACORDO COM Azimute - Altitude 
    dots = [ [ x - math.pi/2 ,  y ] for x, y in dots ]
    dots = [ [ center[0] + cos(x)*r, center[1] + sin(x)*cos(y)*r ] for x, y in dots ]

    # DESENHO DO TRACEJADO E OS PONTOS COLORIDOS DE NASCER A POR DO SOL  
    draw_polyline( name_drawboard, dots, color= color['red'](155), thickness= 2, closed= False )
    for n, p in enumerate(dots):
        draw_circle( name_drawboard, p, radius = 2, color = [n*4, 255-n*2, n*2, 255] )
    
    # DESENHO DO SOL NA SUA POSIÇÃO 
    sun = [  sun_data.azi - math.pi/2, sun_data.alt ] 
    sun = [ center[0] + cos(sun[0])*r, center[1] + sin(sun[0])*cos(sun[1])*r ]
    
    draw_line( name_drawboard, p1 = center, p2 = sun, color = color['yellow'](200), thickness = 2 )
    draw_circle(name_drawboard, center = sun, radius = 10, color = color['yellow'](155), fill = color['yellow'](255) )

    if extremes: 
        min_date = sun_data.winter_solstice 

        max_date = sun_data.summer_solstice        
        sun_data.set_date( min_date )

def draw_semi_circle( name_draw, center, radius, angle_i, angle_f, color, segments = 360, closed = False, thickness = 1 ):
    angles = [ ((angle_f - angle_i)/segments)*n for n in range(segments) ] 
    points = [ [ center[0] + radius*cos(ang), center[1] - radius*sin(ang) ] for ang in angles ]
    draw_polyline ( name_draw, points = points, color= color, closed = closed, thickness= thickness )

def read_arq( name : str = 'CONFIG.txt'): 
    values = defaultdict( None )
    with open( name, 'r') as f:
        lines = f.readlines()
        for line in lines: 
            val = line.replace('\n','').replace(' ','').split('=') 
            if len(val) > 1 : 
                values[val[0]] = val[1]
    return values 

def write_arq(dic : dict, name : str = 'CONFIG.txt'):
    with open( name , 'w') as f: 
        for key in dic.keys():
            txt = key + '=' + dic[key] + '\n' 
            f.write( txt )

def update_values( dic : dict ):
    
    global LATITUDE , LONGITUDE, ALTITUDE
    global UTC_HOUR

    global motor_angle_base   , motor_angle_elevation
    
    global resolucaoM1, passosM1, uPassosM1
    global resolucaoM2, passosM2, uPassosM2 
    
    global window_opened

    #LATITUDE
    #LONGITUDE     
    #ALTURA        
    #UTC           
    #ALTITUDE      
    #POS_GIR       
    #POS_ELE       
    #RESOLUCAO_M1  
    #RESOLUCAO_M2 
    #PASSOSM1
    #PASSOSM2 
    #MICRO_PASSO_M1
    #MICRO_PASSO_M2
    #WINDOW_OPENED 
    pass 

## DESCOMENTAR A CONEXÃO SERIAL
CONNECTED = False
comport = 0 

def initComport(sender, data):
    global comport
    port     = get_value('PORT##AT')
    baudrate = get_value('BAUDRATE##AT')
    timeout  = get_value('TIMEOUT##AT')
    try:
        comport = serial.Serial( port= port, baudrate = int(baudrate), timeout= timeout )
        print("Comport conectada")
        CONNECTED = True 
    except: 
        print("Comport não esta disponível")
        CONNECTED = False

# MAIN WINDOW WITH MENU BAR 
with window('main-window', autosize = True ):
    with menu_bar("MenuBar"):
        add_menu_item( "Inicio"             , callback = change_menu )
        add_menu_item( "Visualização geral" , callback = change_menu )
        add_menu_item( "Posição do sol"     , callback = change_menu )
        add_menu_item( "Atuadores"          , callback = change_menu )
        add_menu_item( "Atuação da base"    , callback = change_menu )
        add_menu_item( "Atuação da elevação", callback = change_menu )
        add_menu_item( "Configurações"      , callback = change_menu )
        add_menu_item( 'Sair'               , callback = lambda sender, data : configure_item('Sair##Sair', show=True))

# INICIO - LOGO JET TOWERS 
with window('Header##IN' , x_pos = 10, y_pos = 25, no_move= True, no_close= True, no_title_bar= True, no_resize= True ):
    add_drawing('headerImage' )
    draw_image( 'headerImage', 'D:\Desktop\JetTowers\Tracker\img\\fundo.jpg'        , pmin = (0,0), pmax = (1,1), tag = 'headerImageTorre' ) 
    draw_image( 'headerImage', 'D:\Desktop\JetTowers\Tracker\img\JetTowers-Logo.png', pmin = (0,0), pmax = (1,1), tag = 'headerLogo')
with window('Lateral##IN', no_move= True, no_close= True, no_title_bar= True, no_resize= True):
    add_spacing( count = 4 )
    add_button("Visualização geral##IN" , arrow= False, callback = lambda sender, data : change_menu( 'Visualização geral'  , None)   )
    add_button("Posição do sol##IN"     , arrow= False, callback = lambda sender, data : change_menu( 'Posição do sol'      , None)   )
    add_button("Atuadores##IN"          , arrow= False, callback = lambda sender, data : change_menu( "Atuadores"           , None)   )
    add_button("Atuação da base##IN"    , arrow= False, callback = lambda sender, data : change_menu( "Atuação da base"     , None)   )
    add_button("Atuação da elevação##IN", arrow= False, callback = lambda sender, data : change_menu( "Atuação da elevação" , None)   )
    add_button("Configurações##IN"      , arrow= False, callback = lambda sender, data : change_menu( 'Configurações'       , None)   )
with window('Main##IN'   , no_move= True, no_close= True, no_title_bar= True, no_resize= True):
    pass

# JANELAS DA VIEW - VISUALIZAÇÃO GERAL 
with window('Solar_pos##VG'       , no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True ):
    add_text('Area para a posição do sol')
    add_drawing('Solar', width = get_item_width('Solar_pos##VG')-20, height = get_item_height('Solar_pos##VG')-50)
    draw_sun_trajetory('Solar',  get_item_width('Solar_pos##VG')-20,  get_item_height('Solar_pos##VG')-50 )
    add_progress_bar('progressive', width= get_item_width('Solar_pos##VG'), height=30 ) 
with window('Atuação##VG'         , no_move = True, no_resize = True, no_collapse = True, no_close = True ):
    add_text('Área para a atução da posição dos paineis solares')
    # Janela de desenho do motor da base
with window('AtuaçãoBase##VG'     , no_move = True, no_resize = True, no_collapse = True, no_close = True ):
    
    # Área de desenho 
    add_drawing('MotorBase', width = w-10, height = h-10)
    draw_circle('MotorBase', center, 75, color['white'](255), thickness=2 )
    draw_arrow('MotorBase', tag='Sun',   p1 = [ 0, 0 ], p2 = center, color = color['green'](155), thickness= 5, size=10)
    draw_arrow('MotorBase', tag='Motor', p1 = [ 0, 0 ], p2 = center, color = color['red'](155),   thickness= 5, size=10)
    draw_circle('MotorBase', center, 5, [255,255,0,175], fill=True )
    
with window('AtuaçãoElevação##VG' , no_move = True, no_resize = True, no_collapse = True, no_close = True ):
    # Área de desenho 
    add_drawing('MotorElevação', width= w-10, height=h-10)
    draw_circle('MotorElevação', center, r, color['white'](255), thickness=2 )
    draw_arrow('MotorElevação', tag='Sun',   p1 = [ 0, 0 ], p2 = center, color = color['green'](150), thickness= 5, size=10)
    draw_arrow('MotorElevação', tag='Motor', p1 = [ 0, 0 ], p2 = center, color = color['red'](200),   thickness= 5, size=10)
    draw_circle('MotorElevação', center, 5, color['yellow'](155), fill=True)

with window('log##VG'             , no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar = True ):
    #Informações gerais do sistema - Automático 
    add_text('Informações gerais do sistema')
    add_drag_float3('Dia automatico',format='%4.0f', speed=1, no_input= True)
    add_spacing(count=1)
    add_drag_float3('Hora automatica',format='%4.0f', speed=1, no_input= True)
    add_spacing(count=1)
    add_drag_float('Total segundos',format='%4.0f', speed=0.1, min_value = 0, max_value = 23*3600, no_input= True)
    add_spacing(count=1)
    add_drag_float('Dia Juliano',format='%4.0f', speed=0.1, min_value = 0, no_input= True)
    add_spacing(count=5)

    # Informações gerais do sistema - Manual 
    add_checkbox("Hora manual", default_value = False, callback= hora_manual )
    add_spacing(count=1)
    add_input_float3('Dia arbitrario', default_value= [2020, 12, 25], format='%.0f', enabled = False )
    add_spacing(count=1)
    add_input_float3('Hora arbitraria', default_value= [20, 30, 10], format='%.0f', enabled = False )
    add_spacing(count=1)
    add_drag_float('Total segundos##',format='%4.0f', speed=0.1, min_value = 0, max_value = 24*3600, no_input= True, enabled= False)
    add_spacing(count=1)
    add_drag_float('Dia Juliano##',format='%4.0f', speed=0.1, min_value = 0, no_input= True, enabled = False)
    add_spacing(count=10)
    
    # Definições de longitude e latitude local
    add_text('Definições de longitude e latitude local')
    add_input_float('Latitude', default_value= -29.165307659422155, format='%3.10f')
    add_spacing(count=1)
    add_input_float('Longitude', default_value= -54.89831672609559, format='%3.10f')
    add_spacing(count=10)

    # Informações do sol 
    add_text('Informacoes do sol')
    add_drag_float('Azimute',format='%4.2f', speed=1, no_input= True)
    add_spacing(count=1)
    add_drag_float('Altitude',format='%4.2f', speed=1, no_input= True)
    add_spacing(count=1)
    add_drag_float('Elevação (m)',format='%4.0f', speed=1, no_input= True)
    add_spacing(count=1)
    add_drag_float3('Horas de sol', format='%.0f', no_input= True)
    add_spacing(count=10)
    
    # Posições de interesse
    add_text("Posicoes de interesse")
    add_drag_float3('Nascer do sol',format='%.0f', speed=1, no_input= True)
    add_spacing(count=1)
    add_drag_float3('Culminante',format='%.0f', speed=1, no_input= True)
    add_spacing(count=1)
    add_drag_float3('Por do sol', format='%.0f', speed=1, no_input= True)
    add_spacing(count=1)

# JANELAS DA VIEW POSIÇÃO DO SOL ## PS      
with window('Visualização##PS'    , width = 800, height = 450, x_pos = 10 , y_pos = 25  , no_move = True, no_resize = True, no_collapse = True, no_close = True ):
    add_drawing('Solar##full', width = 800, height = 410 )
    draw_sun_trajetory('Solar##full', 800, 410, extremes= True )
with window('Altura##PS'          , width = 395, height = 270, x_pos = 10 , y_pos = 480 , no_move = True, no_resize = True, no_collapse = True, no_close = True ):
    # w, h = 390, 270
    raio = 220

    add_drawing('Altura##Solar', width = 380, height = 232)
    draw_polyline('Altura##Solar', [ [ 50, 10 ], [ 50, raio+10 ], [ raio+50, raio+10 ] ], color=color['white'](200), thickness= 2 )
    draw_semi_circle( 'Altura##Solar', [50, raio+10], raio, 0, math.radians(91), color['white'](200), segments= 90, thickness= 2)
    
    # RENDERIZAÇÃO 
    ang = sun_data.get_azi_from_date( sun_data.transit )[0] # [ alt , azi ]
    draw_line('Altura##Solar', [50, raio+10 ], [50 + raio*cos(ang), 230 - raio*sin(ang)], color = color['red'](200), thickness= 2 )
    
    ang = sun_data.alt
    draw_arrow("Altura##Solar", [ 50 + raio*cos(ang), 230 - raio*sin(ang)], [50, raio + 10], color= color['yellow'](200), thickness= 3, size= 10 ) 
    draw_text('Altura##Solar', [380-75, 10], "Altura:", color= color['white'](255), size=15 )
    draw_text('Altura##Solar', [380-75, 25], str( round(math.degrees(ang)) ) + 'º', color= color['white'](255), size=15 )   
with window('Azimute##PS'         , width = 395, height = 270, x_pos = 415, y_pos = 480 , no_move = True, no_resize = True, no_collapse = True, no_close = True ):
    add_drawing('Azimute##Solar', width = 380, height = 230)
    draw_circle('Azimute##Solar', center = [ 380//2, 230//2], radius= 100, color= color['white'](200), thickness= 2 )
    draw_line('Azimute##Solar', p1= [380//2 -100, 230//2], p2=  [380//2 +100, 230//2], color = color['gray'](200), thickness=2 )
    draw_text("Azimute##Solar", pos= [380//2 - 120, 230//2 -7.5], text='W', color=color['white'](200), size=20 )
    draw_text("Azimute##Solar", pos= [380//2 + 110, 230//2 -7.5], text='E', color=color['white'](200), size=20 )
    draw_text("Azimute##Solar", pos= [380//2-5, 230//2 -80], text= 'N', color= color['white'](255), size=20 )
    
    # RENDERIZAÇÃO
    ang = sun_data.get_azi_from_date( sun_data.rising )[1] # [ alt , azi ]
    draw_line('Azimute##Solar', p1 = [ 380//2, 230//2], p2 = [380//2 + 100*cos(ang-math.pi/2), 230//2 + 100*sin(ang-math.pi/2)], color = color['yellow'](200), thickness= 2 )
    ang = sun_data.get_azi_from_date( sun_data.sunset )[1] # [ alt , azi ]
    draw_line('Azimute##Solar', p1 = [ 380//2, 230//2], p2 = [380//2 + 100*cos(ang-math.pi/2), 230//2 + 100*sin(ang-math.pi/2)], color = color['gray'](200), thickness= 2 )
    ang = sun_data.azi 
    draw_arrow('Azimute##Solar', p2 = [ 380//2, 230//2], p1 = [380//2 + 100*cos(ang-math.pi/2), 230//2 + 100*sin(ang-math.pi/2)], color = color['red'](200), thickness= 2, size=10 )
    draw_text('Azimute##Solar', pos= [380-75, 10], text= "Azimute:", color= color['white'](255), size=15 )
    draw_text('Azimute##Solar', pos= [380-75, 25], text= str( round(math.degrees(ang)) ) + 'º', color= color['white'](255), size=15 )
    
    # FIM DA RENDERIZAÇÃO
    draw_circle('Azimute##Solar', center= [380//2, 230//2], radius= 3, color= color['white'](200), thickness=2, fill= color['black'](255))
with window('log##PS'             , width = 440, height = 725, x_pos = 815, y_pos = 25  , no_move = True, no_resize = True, no_collapse = True, no_close = True ):
    
    #Informações gerais do sistema - Automático 
    add_text('Informações de data e calculo')
    add_drag_float3('Data atual##PS'     ,format='%4.0f', speed=1, no_input= True)
    add_spacing(count=2)
    add_drag_float3('Data de calculo##PS',format='%4.0f', speed=1, no_input= True)
    add_spacing(count=5)

    add_text('Informações de configurações do sol')
    add_drag_float3('Nascer do sol##PS' ,format='%4.0f', speed=1, no_input= True)
    add_spacing(count=1)
    add_drag_float3('Transição##PS'     ,format='%4.0f', speed=1, no_input= True)
    add_spacing(count=1)
    add_drag_float3('Por do sol##PS'    ,format='%4.0f', speed=1, no_input= True)
    add_spacing(count=5)

    add_text('Informações gerais')
    add_drag_float3('Horas de luz##PS'   ,format='%4.0f', speed=1, no_input= True)
    add_spacing(count=1)
    add_drag_float('Altitude (º)##PS'    ,format='%4.0f', speed=0.1, min_value = 0, max_value = 23*3600, no_input= True)
    add_spacing(count=1)
    add_drag_float('Azimute (º)##PS'     ,format='%4.0f', speed=0.1, min_value = 0, no_input= True)
    add_spacing(count=5)

    # CORRIGIR A REGRA DA SOMBRA 
    add_text('Projeção de sombras')
    add_drag_float('Altura Obj (m)##PS'  ,format='%4.2f', default_value= 100, speed=0.1, max_value = 1205 )
    add_spacing(count=1)
    add_drag_float('Sombra (m)##PS'      ,format='%4.2f', speed=0.1, min_value = 0, no_input= True)
    add_spacing(count=5)

    add_text('Informações locais')
    add_input_float('Altura (m)##PS'       ,default_value= 425 , format='%4.0f', step = 5 )
    add_spacing(count=1)
    add_input_float('Latitude (º)##PS'     ,default_value= -29.165307659422155, format='%4.10f', step= 0.001 )
    add_spacing(count=1)
    add_input_float('Longitude (º)##PS'    ,default_value=  -54.89831672609559, format='%4.10f', step= 0.001 )
    add_spacing(count=1)
    add_drag_float('UTM local (h)##PS'     ,format='%4.0f', speed=0.1, min_value = 0, no_input= True)
    add_spacing(count=5)

# JANELAS DE ATUAÇÃO ## AT
with window('Controle##AT'        , no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True ):    

    add_spacing(count=2)
    add_text('CONFIGURAÇÕES DE COMUNICAÇÃO')

    # AJUSTA O CHILD DE ACORDO COM A WINDOW "Controle##AT" 
    with child('Controle_child##AT', width= get_item_width('Controle##AT')-15, height= 200 ):

        # FAZER UMA THREAD PARA ESCUTAR NOVAS CONEXÕES SERIAIS 
        add_text('Selecione a porta serial: ')
        add_combo('PORT##AT', default_value='COM11', items= port_list)
        add_spacing( count= 1 )

        add_text('Baudarate: ')
        add_combo('BAUDRATE##AT', default_value= '9600', items=[ '9600', '57600', '115200'], label='' )
        add_spacing( count= 1 )

        add_text('Timeout: ')
        add_input_int('TIMEOUT##AT', default_value= 1, label= '')
        add_spacing( count= 5 )

        add_button('Iniciar conexão##AT', callback= initComport )
    add_spacing(count= 5)

    # DEFNIÇÃO DOS MOTORES INDIVUDUAIS 
    add_text('DEFINIÇÃO DOS MOTORES DE PASSO')

    with child('MotorGiro##AT', width= get_item_width('Controle##AT')-15, height= 200):
        add_text("Motor de Rotação da base - Motor 1")
        add_spacing(count=2)
        add_text('Resolução:')
        add_input_float('ResoluçãoM1##AT', default_value= 1.8, format= '%3.2f', callback= lambda sender, data : set_value('PassosM1##AT', value= (360/get_value('ResoluçãoM1##AT') if get_value('ResoluçãoM1##AT') > 0 else 0 ) ), label = '' )
        add_spacing(count=2)

        add_text('Passos por volta:')
        add_drag_float('PassosM1##AT', default_value=  360 / 1.8, format='%5.2f', no_input= True, label='' )
        add_spacing(count= 2)
        add_text('Micro Passos do motor:')
        add_combo('MicroPassosM1##AT', default_value = '1/16', items= ['1', '1/2', '1/4', '1/8', '1/16', '1/32'], label='' )
    add_spacing(count= 2)

    with child('MotorElevação##AT',  width= get_item_width('Controle##AT')-15, height= 200 ):
        add_text("Motor de Rotação da base - Motor 2")
        add_spacing(count=2)
        add_text('Resolução:')
        add_input_float('ResoluçãoM2##AT', default_value= 1.8, format= '%3.2f', callback= lambda sender, data : set_value('PassosM2##AT', value= (360/get_value('ResoluçãoM2##AT') if get_value('ResoluçãoM2##AT') > 0 else 0 ) ), label = '' )
        add_spacing(count=2)
        add_text('Passos por volta:')
        add_drag_float('PassosM2##AT', default_value=  360 / 1.8, format='%5.2f', no_input= True, label='' )
        add_spacing(count= 2)
        add_text('Micro Passos do motor:')
        add_combo('MicroPassosM2##AT', label='', default_value = '1/16', items= ['1', '1/2', '1/4', '1/8', '1/16', '1/32'] ) 
with window('Retorno##AT'         , no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True):
    pass     
with window('Retorno M2##AT'      , no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True):
    ##add_drawing( 'engrenagem##AT', width= get_item_width("Retorno M2##AT"), height= get_item_height("Retorno M2##AT"))
    #add_image('engrenagem##AT', 'img/engrenagem.png', width= get_item_width("Retorno M2##AT"), height= get_item_height("Retorno M2##AT"))
    pass

with window('Visualização##AT'    , no_move = True, no_resize = True, no_collapse = True, no_close = True):
    #add_group('plot_group##AT', show= True, tip= 'Gráfico de posição no tempo dos motores de giro e elevação', horizontal= True)
    #add_plot
    add_input_text('ComportReader##AT', label= '' ) 

# JANELA DE ATUAÇÃO DO MOTOR DE GIRO 
with window('Visualização##MG'    , no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar = True):
    pass
with window('Infos_inferiores##MG', no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar = True):
    pass
with window('log##MG'             , no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar = True):
    
    add_spacing(count=2)
    add_text('CONFIGURAÇÕES DO MOTOR DE GIRO')
    with child('Configurações_M1##MG' ):
        add_text('Rotação entrada (rpm): ')
        add_input_float('RPM_M1##MG', default_value= 1750, format= '%10.2f', step= 1, label= '')
        add_spacing( count= 1 )

        add_text('Redução (entrada / saída):') 
        add_input_float2('REDU_M1##MG', default_value= [1, 20], format= '%10.0f', label= '')
        add_spacing( count= 1 )        
        
        add_text('Rotação saída:') 
        add_input_float('RPM_OUT_M1##MG', default_value= 0, format= '%10.2f', label= '', callback= lambda sender, data : set_value('RPM_M1##MG', value= (get_value('RPM_OUT_M1##MG')*get_value('REDU_M1##MG')[1]/get_value('REDU_M1##MG')[0]) ) )
        add_spacing( count= 1 )
    
# JANELA DE ATUAÇÃO DO MOTOR DE ELEVAÇÃO 
with window('Visualização##ME'    , no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar = True):
    configure_item('Visualização##ME', width = round(window_size[0]*3/5), height = round( window_size[1]*3/4), x_pos = 10, y_pos = 25   )
with window('Infos_inferiores##ME', no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar = True):
    pass
with window('log##ME'             , no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar = True):
    add_spacing(count=2)
    add_text('CONFIGURAÇÕES DO MOTOR DE ELEVAÇÃO')
    with child('Configurações_M2##ME'):
        add_text('Rotação entrada (rpm): ')
        add_input_float('RPM_M2##ME', default_value= 1750, format= '%10.2f', step= 1, label= '')
        add_spacing( count= 1 )
        
        add_text('Redução (entrada / saída):') 
        add_input_float2('REDU_M2##ME', default_value= [1, 20], format= '%10.0f', label= '')
        add_spacing( count= 1 )        
        
        add_text('Rotação saída:') 
        add_input_float('RPM_OUT_M2##ME', default_value= 0, format= '%10.2f', label= '', callback= lambda sender, data : set_value('RPM_M2##ME', value= (get_value('RPM_OUT_M2##ME')*get_value('REDU_M2##ME')[1]/get_value('REDU_M2##ME')[0]) ) )
        add_spacing( count= 1 )


def update_config():
    pass 

# VIEW DAS CONFIGURAÇÕES 
with window('Configurações##CONF' , no_resize = True, no_collapse = True, no_close = True, no_title_bar = True ):
    add_input_text('LATITUDE##config'             , default_value = str(LATITUDE)             , readonly = True )
    add_input_text('LONGITUDE##config'            , default_value = str(LONGITUDE)            , readonly = True )
    add_input_text('ALTITUDE##config'             , default_value = str(ALTITUDE)             , readonly = True )
    add_input_text('sun_angle_elevation##config'  , default_value = str(sun_angle_elevation)  , readonly = True )
    add_input_text('sun_angle_azimute##config'    , default_value = str(sun_angle_azimute)    , readonly = True )
    add_input_text('motor_angle_base##config'     , default_value = str(motor_angle_base)     , readonly = True )
    add_input_text('motor_angle_elevation##config', default_value = str(motor_angle_elevation), readonly = True )
    add_input_text('resolucaoM1##config'          , default_value = str(resolucaoM1)          , readonly = True )
    add_input_text('passosM1##config'             , default_value = str(passosM1)             , readonly = True )
    add_input_text('uPassosM1##config'            , default_value = str(uPassosM1)            , readonly = True )
    add_input_text('resolucaoM2##config'          , default_value = str(resolucaoM2)          , readonly = True )
    add_input_text('passosM2##config'             , default_value = str(passosM2)             , readonly = True )
    add_input_text('uPassosM2##config'            , default_value = str(uPassosM2)            , readonly = True )

# VIEW PARA SAIR DO SUPERVISÓRIO
with window('Sair##Sair'          , width= 175, height= 150, x_pos= (get_main_window_size()[0]//2)-100 , y_pos= (get_main_window_size()[1]//2)-100, no_resize = True, no_title_bar= True, show= False):
    add_text('     Deseja sair ?',)
    add_spacing(count= 10)
    add_group('group_sair##Sair', horizontal= True )
    add_button('Sim##Sair', width= 75, callback= lambda sender, data : sys.exit(0) )
    add_button('Não##Sair', width= 75, callback= lambda sender, data : configure_item('Sair##Sair', show = False) )

values_txt = read_arq( 'CONFIG.txt' ) 
update_values( values_txt )
write_arq( values_txt, 'CONFIG.txt' )

# Chamada de callbacks de rotina 
set_mouse_drag_callback(mouse_update, 10)
set_render_callback( render_update )

change_menu('Inicio', None )

# Inicia o dearpygui com a janela principal 
start_dearpygui( primary_window = 'main-window' )