from dearpygui.dearpygui    import *
from utils.cliente_TCP      import *  
from registry               import * 
from themes                 import *

import datetime as dt 
import math 

PATH      = os.path.dirname( __file__ ).removesuffix('views')
PATH_IMG  = PATH + 'img\\'

MAX_REC_MENSAGE_TCP = 30 
count_TCP_rec = 0 

TemperaturaTCP : socket = 0 
AltitudeTCP : socket = 0 
AzimuteTCP : socket = 0 
HoraTCP : socket = 0 
CMD_log = [ ]

def att_CMD_redNode(): 
    global CMD_log, count_TCP_rec
    if len(CMD_log) > MAX_REC_MENSAGE_TCP: CMD_log.pop(0)
    if get_value( TCP_CONNECTED ) == True:    
        aux = ''
        for i in CMD_log:
            aux += i 
        configure_item( 6_3_1, default_value = aux )
    else: 
        configure_item( 6_3_1, default_value = 'DESCONECTADO' )
        count_TCP_rec = 0 

def init_TCP_connection( sender, data, user ): 
    IP   = "{}.{}.{}.{}".format( get_value( 6_2_1 )[0], get_value( 6_2_1 )[1], get_value( 6_2_1 )[2], get_value( 6_2_1 )[3])
    global TemperaturaTCP, AltitudeTCP, AzimuteTCP, HoraTCP 
    PORT = int( get_value( 6_2_2 ) ) 
    some = [] 
    AzimuteTCP     = Socket_NodeRed( name = 'Azimute'    )
    AltitudeTCP    = Socket_NodeRed( name = 'Altitude'   ) 
    TemperaturaTCP = Socket_NodeRed( name = 'Temperatura')  
    HoraTCP        = Socket_NodeRed( name = 'Hora')  
    if get_value(6_2_5) == True :
        if not AzimuteTCP.is_alive():
            AzimuteTCP.connect( IP, PORT )
        some.append(1)
    else: 
        some.append(0)
    if get_value(6_2_6) == True :
        if not AltitudeTCP.is_alive():
            AltitudeTCP.connect( IP, PORT+1 )
        some.append(1)
    else: 
        some.append(0)

    if get_value(6_2_7) == True :
        if not TemperaturaTCP.is_alive(): 
            TemperaturaTCP.connect( IP, PORT+2 )
        some.append(1)
    else: 
        some.append(0)
    
    if get_value(6_2_8) == True :
        if not HoraTCP.is_alive(): 
            HoraTCP.connect( IP, PORT+3 )
        some.append(1)
    else: 
        some.append(0)

    if any(some): 
        set_value( TCP_CONNECTED, True )
    else: 
        set_value( TCP_CONNECTED, False )

def refresh_TCP_connection( sender, data, user ): 
    global CMD_log, count_TCP_rec
    if get_value( TCP_CONNECTED) == True: 
        aux = '[{}] Recv at: {}'.format( count_TCP_rec, dt.datetime.now().strftime('%d/%m/%Y - %H:%M:%S') ) + '\n'
        global TemperaturaTCP, AzimuteTCP, AltitudeTCP, HoraTCP
        if HoraTCP.is_alive():
            HoraTCP.send( dt.datetime.now().strftime('%d/%m/%Y - %I:%M:%S %p')  ) 
            aux += 'Hora: ' + str(HoraTCP.receive()) + '\n'
        if TemperaturaTCP.is_alive():
            TemperaturaTCP.send( str( get_frame_count() ))
            aux += 'Counter: ' + str(TemperaturaTCP.receive()) + '\n'
        if AzimuteTCP.is_alive():
            AzimuteTCP.send( str(  '%.2f'%math.degrees(get_value(azi)) ) ) 
            aux += 'Azimute: ' + str(AzimuteTCP.receive()) + '\n'
        if AltitudeTCP.is_alive():
            AltitudeTCP.send( str( '%.2f'%math.degrees(get_value(alt)) ) ) 
            aux += 'Altitude: ' + str(AltitudeTCP.receive()) + '\n'
        CMD_log.append( aux + '\n' )
        count_TCP_rec += 1 
        att_CMD_redNode() 

def att_TCP_connection(sender, data, user ) : 
    if get_value( TCP_CONNECTED) == True: 
        init_TCP_connection(sender, data, user ) 
        
def close_TCP_connection( sender, data, user ): 
    global TemperaturaTCP, AzimuteTCP, AltitudeTCP
    if TemperaturaTCP.is_alive():
        TemperaturaTCP.close( )
    if AzimuteTCP.is_alive():
        AzimuteTCP.close()
    if AltitudeTCP.is_alive():
        AltitudeTCP.close()
    if HoraTCP.is_alive():
        HoraTCP.close()
    set_value( TCP_CONNECTED, False )

def resize_rednodecom( nw : int , nh : int ) -> bool :
    configure_item( 6_1_0   , width = nw*0.99   , height = nh*0.3       )
    configure_item( 6_1_1_0 , width = nw*0.99   , height = nh*0.28      )  
    configure_item( 6_1_1_1 , pmin  = (-30,-30) , pmax = ( nw, nh*0.28 ))
    configure_item( 6_2_0   , width = nw*0.35    , height = nh*0.7-30    , pos = [10        , nh*0.31+20] )   
    configure_item( 6_3_0   , width = nw*0.65-20 , height = nh*0.7-30    , pos = [nw*0.35+15, nh*0.31+20] )

def init_rednodecom( windows : dict ):
    w, h = get_item_width(1_0), get_item_height( 1_0 ) 
    
    # NODE RED HEADER 
    with window( id = 6_1_0, width = w*0.99, height = h*0.3   , pos = [10,25]     , no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True ) as winRed: 
        windows['Rednode comunicacao'].append( winRed )
        header = add_image_loaded(PATH_IMG + "nodeRed.png" )
        add_drawlist( id = 6_1_1_0 )
        draw_image  ( id = 6_1_1_1, parent = 6_1_1_0, texture_id = header, pmin = (0,0), pmax = (1,1) )

    # CONFIGURAÇÔES
    with window( id = 6_2_0, width = w*0.5 , height = h*0.7-25, pos = [10, h*0.31], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True   ) as winConfig: 
        windows['Rednode comunicacao'].append( winConfig )

        add_text      ( 'Configurações de conexão com o NODE RED:')
        add_text      ( 'IP:\t' )
        add_same_line ( )
        add_drag_intx ( id = 6_2_1, min_value = 0, max_value = 255   , size = 4, default_value = [127,0,0,1] )
        add_text      ( 'Port:  ')
        add_same_line ( )
        add_input_int ( id = 6_2_2,  min_value = 0, max_value = 2**16, default_value = 1205  )
        
        add_spacing   ( count = 5 ) 
        add_text      ('Tipo de conexão: ') 
        add_combo     ( id = 6_2_3, default_value = 'TCP', items = ['TCP', 'UDP'] )
        add_text      ('Intervalo de transmissão: ')
        add_input_int ( id = 6_2_4, default_value = 10, label='(seg)' )

        add_spacing( count = 3 )
        with group( horizontal = True ): 
            add_checkbox( id = 6_2_5, label = 'Azimute'    , default_value = True, callback = att_TCP_connection )
            add_checkbox( id = 6_2_6, label = 'Altitude'   , default_value = True, callback = att_TCP_connection )
            add_checkbox( id = 6_2_7, label = 'Temperatura', default_value = True, callback = att_TCP_connection ) 
            add_checkbox( id = 6_2_8, label = 'Hora'       , default_value = True, callback = att_TCP_connection ) 

        add_spacing( count = 3 ) 
        add_button    ( id = 6_2_9, label = 'Try to connect', callback = init_TCP_connection  )
        add_same_line ( ) 
        add_button    ( id = 6_2_10, label = 'Desconnected', callback = close_TCP_connection   )
        add_same_line ( ) 
        add_button    ( id = 6_2_11, label = 'Refresh', callback = refresh_TCP_connection   )
        set_item_theme( 6_2_9, Motor_On )
        set_item_theme( 6_2_10, Motor_Off )

    # LOG
    with window ( id = 6_3_0, width = w*0.5-25 , height = h*0.7-25, pos = [w*0.5+15, h*0.31], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True   ) as winRedLog: 
        windows [ 'Rednode comunicacao'].append( winRedLog )
        add_text( "Log das mensagens comunicadas:")
        add_text( id = 6_3_1, default_value = 'Desconectado', tracked = True, track_offset = 1 )

def render_rednodecom() :
    w, h = get_item_width(1_0), get_item_height(1_0)
    resize_rednodecom( w, h ) 
