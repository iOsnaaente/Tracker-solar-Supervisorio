import dearpygui.dearpygui  as dpg 
from utils.cliente_TCP      import *  
from registry               import * 
from themes                 import *
from functions              import *
import datetime as dt 
import math 

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
    if dpg.get_value( TCP_CONNECTED ) == True:    
        aux = ''
        for i in CMD_log:
            aux += i 
        dpg.configure_item( 63_1, default_value = aux )
    else: 
        dpg.configure_item( 63_1, default_value = 'DESCONECTADO' )
        count_TCP_rec = 0 

def init_TCP_connection( sender, data, user ): 
    IP   = "{}.{}.{}.{}".format( dpg.get_value( 6_2_1 )[0], dpg.get_value( 6_2_1 )[1], dpg.get_value( 6_2_1 )[2], dpg.get_value( 6_2_1 )[3])
    global TemperaturaTCP, AltitudeTCP, AzimuteTCP, HoraTCP 
    PORT = int( dpg.get_value( 62_2 ) ) 
    some = [] 
    AzimuteTCP     = Socket_NodeRed( name = 'Azimute'    )
    AltitudeTCP    = Socket_NodeRed( name = 'Altitude'   ) 
    TemperaturaTCP = Socket_NodeRed( name = 'Temperatura')  
    HoraTCP        = Socket_NodeRed( name = 'Hora')  
    if dpg.get_value(62_5) == True :
        if not AzimuteTCP.is_alive():
            AzimuteTCP.connect( IP, PORT )
        some.append(1)
    else: 
        some.append(0)
    if dpg.get_value(62_6) == True :
        if not AltitudeTCP.is_alive():
            AltitudeTCP.connect( IP, PORT+1 )
        some.append(1)
    else: 
        some.append(0)

    if dpg.get_value(62_7) == True :
        if not TemperaturaTCP.is_alive(): 
            TemperaturaTCP.connect( IP, PORT+2 )
        some.append(1)
    else: 
        some.append(0)
    
    if dpg.get_value(62_8) == True :
        if not HoraTCP.is_alive(): 
            HoraTCP.connect( IP, PORT+3 )
        some.append(1)
    else: 
        some.append(0)

    if any(some): dpg.set_value( TCP_CONNECTED, True )
    else:         dpg.set_value( TCP_CONNECTED, False )

def refresh_TCP_connection( sender, data, user ): 
    global CMD_log, count_TCP_rec
    if dpg.get_value( TCP_CONNECTED) == True: 
        aux = '[{}] Recv at: {}'.format( count_TCP_rec, dt.datetime.now().strftime('%d/%m/%Y - %H:%M:%S') ) + '\n'
        global TemperaturaTCP, AzimuteTCP, AltitudeTCP, HoraTCP
        if HoraTCP.is_alive():
            HoraTCP.send( dt.datetime.now().strftime('%d/%m/%Y - %I:%M:%S %p')  ) 
            aux += 'Hora: ' + str(HoraTCP.receive()) + '\n'
        if TemperaturaTCP.is_alive():
            TemperaturaTCP.send( str( dpg.get_frame_count() ))
            aux += 'Counter: ' + str(TemperaturaTCP.receive()) + '\n'
        if AzimuteTCP.is_alive():
            AzimuteTCP.send( str(  '%.2f'%math.degrees(dpg.get_value(AZIMUTE)) ) ) 
            aux += 'Azimute: ' + str(AzimuteTCP.receive()) + '\n'
        if AltitudeTCP.is_alive():
            AltitudeTCP.send( str( '%.2f'%math.degrees(dpg.get_value(ZENITE)) ) ) 
            aux += 'Altitude: ' + str(AltitudeTCP.receive()) + '\n'
        CMD_log.append( aux + '\n' )
        count_TCP_rec += 1 
        att_CMD_redNode() 

def att_TCP_connection(sender, data, user ) : 
    if dpg.get_value( TCP_CONNECTED) == True: 
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
    dpg.set_value( TCP_CONNECTED, False )

## MAIN FUNCTIONS 
def resize_rednodecom( ) -> bool :
    nw, nh = dpg.get_item_width('mainWindow'), dpg.get_item_height( 'mainWindow') 
    dpg.configure_item( 61_10  , width = nw*0.99   , height = nh*0.3       )
    #dpg.configure_item( 61_12  , width = nw*0.99   , height = nh*0.28      )  
    #dpg.configure_item( 61_12  , pmin  = (-30,-30) , pmax = ( nw, nh*0.28 ))
    
    dpg.configure_item( 62_10   , width = nw*0.35    , height = nh*0.7-30    , pos = [10        , nh*0.31+20] )   
    
    dpg.configure_item( 63_10   , width = nw*0.65-20 , height = nh*0.7-30    , pos = [nw*0.35+15, nh*0.31+20] )


def init_rednodecom( windows : dict ):
    # NODE RED HEADER 
    with dpg.window( tag = 61_10, width = -1, height = -1, pos = [10,25]     , no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True ) as winRed: 
        windows['Rednode comunicacao'].append( winRed )
        header = add_image_loaded( PATH + "\\img\\nodeRed.PNG" )
        dpg.add_drawlist( tag = 61_11, width  = 100  , height = 100  )
        dpg.draw_image  ( tag = 61_12, parent = 61_11, texture_tag = header, pmin = (0,0), pmax = (1,1) )

    # CONFIGURAÇÔES
    with dpg.window( tag = 62_10, width = -1, height = -1, pos = [10, 0], no_resize = True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True   ) as winConfig: 
        windows['Rednode comunicacao'].append( winConfig )

        dpg.add_text      ( 'Configurações de conexão com o NODE RED:')
        with dpg.group( horizontal = True ):
            dpg.add_text      ( 'IP:\t' )
            dpg.add_drag_intx ( tag = 62_1, min_value = 0, max_value = 255   , size = 4, default_value = [127,0,0,1] )
        
        with dpg.group( horizontal = True ):
            dpg.add_text      ( 'Port:  ')
            dpg.add_input_int ( tag = 62_2,  min_value = 0, max_value = 2**16, default_value = 1205  )
    
        dpg.add_spacer    ( height = 5 ) 
        dpg.add_text      ('Tipo de conexão: ') 
        dpg.add_combo     ( tag = 62_3, default_value = 'TCP', items = ['TCP', 'UDP'] )
        dpg.add_text      ('Intervalo de transmissão: ')
        dpg.add_input_int ( tag = 62_4, default_value = 10, label='(seg)' )
        dpg.add_spacer( height = 3 )
        
        with dpg.group( horizontal = True ): 
            dpg.add_checkbox( tag = 62_5, label = 'Azimute'    , default_value = True, callback = att_TCP_connection )
            dpg.add_checkbox( tag = 62_6, label = 'Altitude'   , default_value = True, callback = att_TCP_connection )
            dpg.add_checkbox( tag = 62_7, label = 'Temperatura', default_value = True, callback = att_TCP_connection ) 
            dpg.add_checkbox( tag = 62_8, label = 'Hora'       , default_value = True, callback = att_TCP_connection ) 
        
        dpg.add_spacer( height = 3 ) 
        with dpg.group( horizontal = True ):
            dpg.add_button    ( tag = 62_9, label = 'Try to connect', callback = init_TCP_connection  )
            dpg.add_button    ( tag = 62_10, label = 'Desconnected', callback = close_TCP_connection   )
            dpg.add_button    ( tag = 62_11, label = 'Refresh', callback = refresh_TCP_connection   )
    
        dpg.bind_item_theme( 62_9, theme_button_on)
        dpg.bind_item_theme( 62_10, theme_button_off )

    # LOG
    with dpg.window ( tag = 63_10, width = -1 , height = -1, no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True   ) as winRedLog: 
        windows [ 'Rednode comunicacao'].append( winRedLog )
        dpg.add_text( tag = 63_2, default_value = "Log das mensagens comunicadas:")
        dpg.add_text( tag = 63_1, default_value = 'Desconectado', tracked = True, track_offset = 1 )

def render_rednodecom() :
    resize_rednodecom() 
