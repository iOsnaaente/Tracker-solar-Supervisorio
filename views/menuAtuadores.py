from distutils.sysconfig import get_config_var
from tokenize import group
import dearpygui.dearpygui as dpg
from serial.serialutil import SerialException

from   registry             import * 
from   themes               import *

from datetime import datetime as dt 

import struct 
import math 

# FUNCTIONS 
def serial_verify_connection(): 
    global COMP
    if not COMP.connected: 
        dpg.hide_item( 42_6 )
        dpg.hide_item( 42_7 )
        dpg.show_item( 42_4 )
        dpg.set_value( SERIAL_CONNECTED, False)
    else: 
        if COMP.BUFFER_IN == []:
            dpg.set_value( 46_2_1_1, "CONECTADO!" )

def serial_capture_frames(): 
    global COMP, MSG_INIT, MSG_COUNT
    global MPE_LIST, MPE_COUNT, SPE_LIST
    global MPG_LIST, MPG_COUNT, SPG_LIST
    global MPE, MPG, ALTITUDE, AZIMUTE
    global MDE_LIST, MDG_LIST 
    global GPHG_ATT, GPHE_ATT

    for ind, byte in enumerate(COMP.BUFFER_IN[-1][:-1]):
        if byte == MSG_INIT[MSG_COUNT]: 
            MSG_COUNT = MSG_COUNT +  1
        else:
            MSG_COUNT = 0 

        if MSG_COUNT == 4: 
            MSG_COUNT = 0
            OP = COMP.BUFFER_IN[-1][ind+1]
            if OP == ord('e'):
                try:
                    value = COMP.BUFFER_IN[-1][ind+2:ind+6]
                    value = struct.unpack('f', value )[0]
                    dpg.set_value(MPE, value) 
                    MPE_LIST.append( dpg.get_value(MPE) )
                    SPE_LIST.append( dpg.get_value(ALTITUDE) )
                    #MDE_LIST.append( dt.timestamp( dt.utcnow() ) )
                    MDE_LIST.append( MPE_COUNT ) 
                    MPE_COUNT += 1
                    GPHE_ATT = True 
                except struct.error as e:
                    print( e )

            elif OP == ord('g'):
                try: 
                    value = COMP.BUFFER_IN[-1][ind+2:ind+6]
                    value = struct.unpack('f', value )[0]
                    dpg.set_value(MPG, value) 
                    MPG_LIST.append( dpg.get_value(MPG) )
                    SPG_LIST.append( dpg.get_value(AZIMUTE) )
                    #MDG_LIST.append( dt.timestamp( dt.utcnow() ) )
                    MDG_LIST.append( MPG_COUNT ) 
                    MPG_COUNT += 1
                    GPHG_ATT = True 
                except struct.error as e:
                    print( e )

def serial_atualize_cmd( ): 
    global COMP 
    if COMP.connected:    
        if COMP.read():
            serial_capture_frames() 
            MSG  = ''
            for n, row in enumerate( COMP.BUFFER_IN ):
                MSG += '[{}] '.format( COMP.COUNTER_IN + n - len(COMP.BUFFER_IN) )
                if dpg.get_value( CMD_MODE ) == 'ASCII': 
                    for collum in row: 
                        MSG += chr(168) if collum < 32 or collum == 127 else chr(collum)
                    MSG += '\n'
                elif dpg.get_value( CMD_MODE ) == 'HEX': 
                    for collum in row: 
                        if collum == 10: MSG += '\n'
                        else:            MSG += str(hex(168)) if collum < 32 or collum == 127 else str(hex(collum)) + ' '
                    MSG += '\n'

            dpg.set_value( 46_2_1_1, MSG )
    else:
        dpg.set_value( 46_2_1_1, "DESCONECTADO" ) 

def graphs_atualize():
    global GPHE_ATT, GPHG_ATT
    global MPG_LIST, MPG_COUNT
    global SPG_LIST, SPE_LIST
    global MPE_LIST, MPE_COUNT
    global MDE_LIST, MDG_LIST 

    if GPHG_ATT: 
        # GIRO 
        if MPG_LIST: 
            while len(MPG_LIST) > 1000:
                MPG_LIST.pop(0)
                MDG_LIST.pop(0)
            dpg.configure_item( 44_1_1, x = MDG_LIST, y = MPG_LIST )
            dpg.configure_item( 44_1_2, x = MDG_LIST, y = SPG_LIST )
            dpg.set_axis_limits( 'x_axis_azi', ymin = MDG_LIST[0], ymax = MDG_LIST[-1])
        GPHG_ATT = False 
    
    if GPHE_ATT:
        # ELEVAÇÂO
        if MPE_LIST:
            while len(MPE_LIST) > 1000:
                MPE_LIST.pop(0)
                MDE_LIST.pop(0)
            dpg.configure_item( 45_1_1, x = MDE_LIST, y = MPE_LIST )
            dpg.configure_item( 45_1_2, x = MDE_LIST, y = SPE_LIST )
            dpg.set_axis_limits( 'x_axis_alt', ymin = MDE_LIST[0], ymax = MDE_LIST[-1])
        GPHE_ATT = False 


# CALLBACKS 
def serial_refresh( sender, data, user ): 
    global COMP 
    dpg.configure_item( 42_1_1, label = 'Procurando' ) 
    dpg.configure_item( 42_1  , items = COMP.get_serial_ports( 20 ) )
    dpg.configure_item( 42_1_1, label = 'Refresh' )

def serial_try_to_connect( sender, data, user ): 
    global COMP 
    COMP = UART_COM( dpg.get_value(SERIAL_PORT), baudrate = int(dpg.get_value(SERIAL_BAUDRATE)), timeout = dpg.get_value(SERIAL_TIMEOUT) )
    if COMP.connected:
        dpg.show_item( 42_6 )
        dpg.show_item( 42_7 )
        dpg.bind_item_theme( item = 42_6, theme = theme_button_on  )
        dpg.bind_item_theme( item = 42_7, theme = theme_button_off )
        dpg.hide_item( 42_4 )
        dpg.set_value( SERIAL_CONNECTED, True)
    else:   
        dpg.hide_item( 42_6 )
        dpg.hide_item( 42_7 )
        dpg.show_item( 42_4 )
        dpg.set_value( SERIAL_CONNECTED, False)

def serial_write_message(sender, data, user ):
    global COMP
    ## Control Params 
    if user   == 'INITCM':
        user   = 'INITCM'.encode()
        user  += struct.pack('ff', dpg.get_value(46_1_1_4_3)[0], dpg.get_value(46_1_1_4_3)[1] )
    if user   == 'INITCP':
        user   = 'INITCM'.encode()
        user  += struct.pack('ff', dpg.get_value(AZIMUTE), dpg.get_value(ALTITUDE) )
        print(dpg.get_value(AZIMUTE), dpg.get_value(ALTITUDE))
        
    elif user == 'INITCm':
        user   = 'INITCm'.encode()
        user  += 'G'.encode() if dpg.get_value(46_1_1_4_5) == 'Gir' else 'E'.encode()
        user  += struct.pack('f', dpg.get_value(46_1_1_4_4))
    elif user == 'INITCp':
        user   =  'INITC'.encode()
        user  +=  'G'.encode() if dpg.get_value(46_1_1_4_21) == 'Gir' else 'E'.encode()
        user  +=  dpg.get_value(46_1_1_4_22)
        user  +=  struct.pack( 'f', dpg.get_value(46_1_1_4_1) )

    ## Datetime Params 
    elif user == "INITH": 
        user  = "INITH".encode() 
        date  = dpg.get_value( 46_1_1_1 )
        hour  = dpg.get_value( 46_1_1_2 ) 
        if date[0] > 31:    raise 'days out of range'
        if date[1] > 12:    raise 'months out of range'       
        if hour[0] > 60:    raise 'seconds out of range'
        if hour[1] > 60:    raise 'minutes out of range'
        if hour[2] > 23:    raise 'hours out of range'
        if date[2] > 2000:  date[2] -= 2000
        user += struct.pack( 'bbb', date[0], date[1], date[2])
        user += struct.pack( 'bbb', hour[0], hour[1], hour[2])

    if user == 'manual_send':
        user = dpg.get_value(46_2_2_2)

    try: 
        if type( user ) == bytes: COMP.write( user )
        elif type( user ) == str: COMP.write( user.encode() )
    except SerialException as e:
        print( e )
    print( sender, data, user )

def serial_close_connection(sender, data, user): 
    global COMP
    COMP.close()
    serial_verify_connection() 

def change_menubar_cmd( sender, data, user ):
    dpg.set_value( CMD_MODE, user )
    if COMP.connected:
        MSG  = ''
        for n, row in enumerate( COMP.BUFFER_IN ):
            MSG += '[{}] '.format( COMP.COUNTER_IN + n - len(COMP.BUFFER_IN) )
            if user == 'ASCII': 
                for collum in row: 
                    MSG += chr(168) if collum < 32 or collum == 127 else chr(collum)
                MSG += '\n'
            elif user == 'HEX': 
                for collum in row: 
                    MSG += str(hex(168)) if collum < 32 or collum == 127 else str(hex(collum)) + ' '
                MSG += '\n'
        dpg.set_value( 46_2_1_1, MSG )

# MAIN FUNCTIONS 
def handlers_and_themes_atuador():
    dpg.bind_item_theme( item = 43_2_0  , theme = theme_no_border  )
    dpg.bind_item_theme( item = 43_2_1_0, theme = theme_no_border )
    dpg.bind_item_theme( item = 43_2_2_0, theme = theme_no_border )
    dpg.bind_item_theme( item = 43_3_0  , theme = theme_no_border  )
    dpg.bind_item_theme( item = 43_3_1_0, theme = theme_no_border  )
    dpg.bind_item_theme( item = 43_3_2_0, theme = theme_no_border  )
    dpg.bind_item_theme( item = 43_3_1_1, theme = theme_button_off )
    dpg.bind_item_theme( item = 43_3_2_1, theme = theme_button_off )
    dpg.hide_item( 42_0)
    dpg.hide_item( 43_0)
    dpg.hide_item( 44_0)
    dpg.hide_item( 45_0)
    dpg.hide_item( 46_0)

def init_atuador( windows : dict ): 
    # Serial Config 
    with dpg.window( label = 'Serial' , tag = 42_0, width= 455, height= 330, pos = [10,25], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as serial_AT: 
        windows['Atuadores'].append( serial_AT )

        dpg.add_spacer( height = 1 )
        dpg.add_text('CONFIGURAÇÕES DE COMUNICAÇÃO')
        dpg.add_text('Selecione a porta serial: ')
        with dpg.group( horizontal = True ):
            dpg.add_combo( tag = 42_1, default_value = 'COM12', items = ['COM1', 'COM4', 'COM5', 'COM10', 'COM12', 'COM15', 'COM16'], source = SERIAL_PORT )
            dpg.add_button(  tag = 42_1_1, label = 'Refresh', callback = serial_refresh )
        dpg.add_spacer( height = 1 )

        dpg.add_text('Baudarate: ')
        dpg.add_combo( tag = 42_2, default_value = '115200', items=[ '9600', '19200', '57600', '115200', '1000000'], source = SERIAL_BAUDRATE )
        dpg.add_spacer( height = 1 )

        dpg.add_text('Timeout: ')
        dpg.add_input_int( tag = 42_3, default_value = 1, source = SERIAL_TIMEOUT)
        dpg.add_spacer( height = 3 )

        dpg.add_button(label ='Iniciar conexão',              tag = 42_4 , callback = serial_try_to_connect      )
        with dpg.group( horizontal = True ):
            dpg.add_button(label ="CONECTADO"      , width = 150, tag = 42_6                                 )
            dpg.add_button(label ="DESCONECTAR"    , width = 150, tag = 42_7, callback = serial_close_connection )
        dpg.add_spacer(height = 5)
        dpg.hide_item( 42_6)         
        dpg.hide_item( 42_7) 

    # Step Motors Config 
    with dpg.window( label = 'Motores'    , tag = 43_0, width= 455, height= 480, pos = [10,360], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as config_AT:
        windows['Atuadores'].append( config_AT )

        def change_menubar_motors(sender, data, user ): 
            if user == 'step':
                dpg.show_item(43_2_0)
                dpg.hide_item(43_3_0)
            elif user == 'trif': 
                dpg.show_item(43_3_0)
                dpg.hide_item(43_2_0)

        dpg.add_text( 'CONFIGURAÇÃO DE ACIONAMENTO DOS MOTORES')
        # MENUBAR DE DEFNIÇÃO DOS MOTORES
        with dpg.child_window( autosize_x =True, autosize_y = True, menubar = True ):
            with dpg.menu_bar(label = "menubar_motors"):
                dpg.add_menu_item( label = "Motor de passo"  , callback = change_menubar_motors, user_data = 'step' )
                dpg.add_menu_item( label = "Motor Trifásico" , callback = change_menubar_motors, user_data = 'trif' )

            # DE PASSO 
            with dpg.child_window( tag = 43_2_0, autosize_x =True, autosize_y = True): 
                dpg.add_text('DEFINIÇÃO DOS MOTORES DE PASSO')
                dpg.add_spacer(  height = 15 )
                with dpg.child_window( tag = 43_2_1_0, label = 'MotorGiro'    , autosize_x=True, height = 200 ):
                    dpg.add_text       ( "Motor de Rotação da base - Motor G" )
                    dpg.add_text       ( 'Resolução:' )
                    dpg.add_input_float( tag = 43_2_1_1, default_value = 1.8    , format = '%3.2f', source = MG_RESOLUCAO, callback = serial_write_message, user_data = 'Gir', on_enter = True )
                    dpg.add_text       ( 'Micro Passos do motor:' )
                    dpg.add_combo      ( id=43_2_1_3, default_value = '1/16'    , items  = ['1', '1/2', '1/4', '1/8', '1/16', '1/32'], source = MG_USTEP, callback= serial_write_message, user_data = 'Gir' )
                    dpg.add_text       ( 'Passos por volta:' )
                    dpg.add_drag_float ( tag = 43_2_1_2, default_value =  360 / 1.8, format = '%5.2f', source = MG_STEPS, no_input = True, callback= serial_write_message, user_data = 'Gir' )
            
                with dpg.child_window( tag = 43_2_2_0, label = 'MotorElevação', autosize_x=True, height = 200 ):
                    dpg.add_text       ( "Motor de Rotação da base - Motor 2")
                    dpg.add_text       ( 'Resolução:')
                    dpg.add_input_float( tag = 43_2_2_1, default_value = 1.8      , format = '%3.2f', source = ME_RESOLUCAO, callback = serial_write_message, user_data = 'Ele', on_enter = True )
                    dpg.add_text       ( 'Micro Passos do motor:')
                    dpg.add_combo      ( tag = 43_2_2_3, default_value = '1/16'   , items  = ['1', '1/2', '1/4', '1/8', '1/16', '1/32'], source = ME_USTEP, callback= serial_write_message, user_data = 'Ele' ) 
                    dpg.add_text       ( 'Passos por volta:')
                    dpg.add_drag_float ( tag = 43_2_2_2, default_value = 360 / 1.8, format ='%5.2f', source = ME_STEPS, no_input = True, callback = serial_write_message, user_data = 'Ele'  )
        
            # TRIFÁSICO 
            with dpg.child_window( tag = 43_3_0, autosize_x=True, autosize_y=True ):
                dpg.add_text('DEFINIÇÃO DE ACIONAMENTO TRIFÁSICO')
                
                dpg.add_spacer( height = 15 )
                with dpg.child_window( tag = 43_3_1_0, label = 'MotorGiro'    ,autosize_x = True, height = 100 ):
                    dpg.add_text       ( "Motor de Rotação da base - Motor 1" )
                    dpg.add_spacer     ( )
                    dpg.add_button     ( tag = 43_3_1_1, label= 'Desligado'  ,  width = 250, callback = serial_write_message, user_data='m1')
                    dpg.add_text       ( 'Velocidade angular MG:' )
                    dpg.add_input_float( tag = 43_3_1_2, label = 'Wo (rad/s)', default_value = dpg.get_value(MG_VELANG), source = MG_VELANG, format = '%3.2f', on_enter = True, callback = serial_write_message )
                    # CORRIGIR A TROCA DE MENSAGEM PARA AJUSTAR AS VELOCIDADES
                
                dpg.add_spacer    ( height = 15 )
                with dpg.child_window( tag = 43_3_2_0, label = 'MotorElevação',autosize_x = True, height = 125 ):
                        dpg.add_text       ( "Motor de Rotação da base - Motor 2")
                        dpg.add_spacer     ( )
                        dpg.add_button     ( tag = 43_3_2_1, label='Desligado', width=250, callback = serial_write_message, user_data='m2')
                        dpg.add_text       ( 'Velocidade angular ME:' )
                        dpg.add_input_float( tag = 43_3_2_2, label = 'Wo (rad/s)', default_value = dpg.get_value(ME_VELANG), source = ME_VELANG, format = '%3.2f', on_enter = True, callback = serial_write_message )

            change_menubar_motors( None, None, 'step')
            
    # Azimute Draw 
    with dpg.window( label ='Azimute'     , tag = 44_0, width= 495, height= 330, pos = [470,25], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as azimute_config_AT: 
        windows['Atuadores'].append( azimute_config_AT)
        
        with dpg.plot( tag = 44_1_0, parent = 44_0, label = 'Azimute e angulo de giro', height = 312, width = 478, anti_aliased = True ): 
            dpg.add_plot_legend( )
            dpg.add_plot_axis  ( dpg.mvXAxis, label = 'medição [n]', tag = 'x_axis_azi',)
            dpg.add_plot_axis  ( dpg.mvYAxis, label = 'Angulo [º]' , tag = 'y_axis_azi' )
            dpg.set_axis_limits( 'x_axis_azi',  0,   1 )
            dpg.set_axis_limits( 'y_axis_azi', -5, 375 )
            dpg.add_line_series( [], [], tag = 44_1_1, label = 'Sensor Giro', parent = 'y_axis_azi' )
            dpg.add_line_series( [], [], tag = 44_1_2, label = 'Azimute sol', parent = 'y_axis_azi' ) 
 

    # Zenite / Altitude Draw 
    with dpg.window(label  = 'Zenite'     , tag = 45_0, width= 495, height= 330, pos = [970,25], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as zenite_config_AT:
        windows['Atuadores'].append( zenite_config_AT )  
        
        with dpg.plot( tag = 45_1_0, label = 'Zenite e angulo de elevação', height = 312, width = 478, anti_aliased = True ): 
            dpg.add_plot_legend()
            dpg.add_plot_axis( dpg.mvXAxis, label = 'medição [n]', tag = 'x_axis_alt' )
            dpg.add_plot_axis( dpg.mvYAxis, label = 'Angulo [º]', tag = 'y_axis_alt' )
            dpg.set_axis_limits_auto( 'x_axis_alt')
            dpg.set_axis_limits( 'y_axis_alt', -5, 370 )
            dpg.add_line_series( [], [], tag = 45_1_1, label = 'Sensor Elevação', parent = 'y_axis_alt' )
            dpg.add_line_series( [], [], tag = 45_1_2, label = 'Zenite sol', parent = 'y_axis_alt' ) 
        
    # General Draw 
    with dpg.window( label = 'Draw_Window', tag = 46_0, width= 995, height= 480, pos = [470,360], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as draw_tracker_AT:
        windows['Atuadores'].append( draw_tracker_AT )  
    
        def change_menubar_conf( sender, data, user ): 
            dpg.hide_item(46_1_1_1_0)
            dpg.hide_item(46_1_1_2_0)
            dpg.hide_item(46_1_1_3_0)
            dpg.hide_item(46_1_1_4_0)
            dpg.hide_item(46_1_1_5_0)
            if   user == "State":     dpg.show_item(46_1_1_1_0)   
            elif user == "Power":     dpg.show_item(46_1_1_2_0)   
            elif user == "Date/Time": dpg.show_item(46_1_1_3_0)   
            elif user == "Control":   dpg.show_item(46_1_1_4_0)   
            elif user == "Diagnosis": dpg.show_item(46_1_1_5_0)   

        with dpg.group( horizontal = True):
            with dpg.child_window(tag = 46_1_0, width = (dpg.get_item_width(46_0)*0.4), border = False, menubar = True):
                dpg.add_text('Opções padrão de operação do sistema:')
                with dpg.menu_bar(label = "child_menubar_conf"):
                    dpg.add_menu_item( label = "State"       , callback = change_menubar_conf, user_data = "State"     )
                    dpg.add_menu_item( label = "Power"       , callback = change_menubar_conf, user_data = "Power"     )
                    dpg.add_menu_item( label = "Date/Time"   , callback = change_menubar_conf, user_data = "Date/Time" )
                    dpg.add_menu_item( label = "Control"     , callback = change_menubar_conf, user_data = "Control"   )
                    dpg.add_menu_item( label = "Diagnosis"   , callback = change_menubar_conf, user_data = "Diagnosis" )
            
                # STATES 
                with dpg.child_window( tag = 46_1_1_1_0, width = dpg.get_item_width(46_1_0), autosize_y = True, autosize_x = True, border = True ):
                    with dpg.group( horizontal = True ): 
                        dpg.add_button(label='send', callback = serial_write_message, user_data='INITSS')
                        dpg.add_text('S -> Parar o tracker')
                    with dpg.group( horizontal = True ): 
                        dpg.add_button(label='send', callback = serial_write_message, user_data='INITSD')
                        dpg.add_text('D -> Entra no modo Demo')
                    with dpg.group( horizontal = True ): 
                        dpg.add_button(label='send', callback = serial_write_message, user_data='INITSC')
                        dpg.add_text('C -> Continuar processo')
                    with dpg.group( horizontal = True ): 
                        dpg.add_button(label='send', callback = serial_write_message, user_data='INITSL')
                        dpg.add_text('L -> Levers')  
                    with dpg.group( horizontal = True ): 
                        dpg.add_button(label='send', callback = serial_write_message, user_data='INITSA')
                        dpg.add_text('A -> Automatic')  
                
                # POWER 
                with dpg.child_window( tag = 46_1_1_2_0, width = dpg.get_item_width(46_1_0), autosize_y = True, autosize_x = True, border = True ):
                    with dpg.group( horizontal = True ): 
                        dpg.add_button(label='send', callback = serial_write_message, user_data='INITWO')
                        dpg.add_text('O -> Ativar motores')

                    with dpg.group( horizontal = True ): 
                        dpg.add_button(label='send', callback = serial_write_message, user_data='INITWF')
                        dpg.add_text('F -> Desativar motores ')
                    
                # DATA E HORA
                with dpg.child_window( tag = 46_1_1_3_0, width = dpg.get_item_width(46_1_0), autosize_y = True, autosize_x = True, border = True ):
                    dpg.add_button(label='send', callback = serial_write_message, user_data = 'INITH' )
                    dpg.group( horizontal = True )
                    dpg.add_text('H -> Trocar a hora')
                
                    dpg.add_input_intx( tag =46_1_1_1, size=3, default_value=[ 12, 5, 2021 ], max_value = 99, callback = serial_write_message, user_data = 'INITH', on_enter = True )
                    dpg.group( horizontal = True )
                    dpg.add_text('dd/mm/yy')
                
                    dpg.add_input_intx( tag =46_1_1_2, size=3, default_value=[ 15, 35, 10  ], max_value = 60, callback = serial_write_message, user_data = 'INITH', on_enter = True ) 
                    dpg.group( horizontal = True )
                    dpg.add_text('hh:mm:ss') 
                
                # CONTROL 
                with dpg.child_window( tag = 46_1_1_4_0, width = dpg.get_item_width(46_1_0), autosize_y = True, autosize_x = True, border = True ):
                    with dpg.group( horizontal = True ):
                        dpg.add_button(label='send', callback = serial_write_message, user_data = 'INITCp' )
                        dpg.add_text('P -> Configurar variáveis de processo')
                    dpg.add_input_float ( tag = 46_1_1_4_1, default_value = 0.5, max_value=1, on_enter = True, callback = serial_write_message, user_data = 'INITCp' )
                    with dpg.group( horizontal = True):
                        dpg.add_radio_button( tag = 46_1_1_4_21, items = ['Gir', 'Ele'], default_value = 'Gir', horizontal = True ) 
                        dpg.add_radio_button( tag = 46_1_1_4_22, items = ['D','I','P'], default_value = 'D', horizontal = True ) 

                    with dpg.group( horizontal = True ): 
                        dpg.add_button(label='send', callback = serial_write_message, user_data = 'INITCM' )
                        dpg.add_text('M -> Mover ambos motores')
                    dpg.add_input_floatx( tag = 46_1_1_4_3, size=2, default_value=[ 12.05, 19.99], on_enter = True, callback = serial_write_message, user_data = 'INITMO')
                 
                    with dpg.group( horizontal = True ):
                        dpg.add_button(label='send', callback = serial_write_message, user_data = 'INITCm' )
                        dpg.add_text('m -> Mover um motore')
                    dpg.add_input_float ( tag = 46_1_1_4_4, default_value = 12, on_enter = True, callback = serial_write_message, user_data = 'INITCm' )
                    dpg.add_radio_button( tag = 46_1_1_4_5, items = ['Gir', 'Ele'], default_value = 'Gir', horizontal = True ) 
                    
                    with dpg.group( horizontal = True ): 
                        dpg.add_button(label='send', callback = serial_write_message, user_data = 'INITCP' )
                        dpg.add_text("P -> Envia Zenite e Azimute como PV")
                    
                # DIAGNÓSTICO 
                with dpg.child_window( tag = 46_1_1_5_0, width = dpg.get_item_width(46_1_0), autosize_y = True, autosize_x = True, border = True ):
                    with dpg.group( horizontal = True ):    
                        dpg.add_button(label='send', callback = serial_write_message, user_data = 'INITPA')
                        dpg.add_text('A -> All info')
                    with dpg.group( horizontal = True ):    
                        dpg.add_button(label='send', callback = serial_write_message, user_data = 'INITPS')
                        dpg.add_text('S -> Sensor Diagnosis')
                    with dpg.group( horizontal = True ):    
                        dpg.add_button(label='send', callback = serial_write_message, user_data = 'INITPP')
                        dpg.add_text('P -> Print Positions')
                    with dpg.group( horizontal = True ):    
                        dpg.add_button(label='send', callback = serial_write_message, user_data = 'INITPZ')
                        dpg.add_text('Z -> Zenite')
                    with dpg.group( horizontal = True ):    
                        dpg.add_button(label='send', callback = serial_write_message, user_data = 'INITPH')
                        dpg.add_text('H -> Altitude')
                change_menubar_conf( None, None, 'State')

            with dpg.child_window( tag = 46_2_0, width= (dpg.get_item_width(46_0)*0.6), autosize_y = True, border = False, menubar = True ):
                dpg.add_text( 'PICO_SM: RP2040 Serial Monitor')
                with dpg.menu_bar(label = "child_menubar_cmd"):
                    dpg.add_menu_item( label = "ASCII" , callback = change_menubar_cmd, user_data = "ASCII" )
                    dpg.add_menu_item( label = "HEX"   , callback = change_menubar_cmd, user_data = "HEX"   )
                  
                with dpg.child_window  ( tag = 46_2_1_0, autosize_x = True, border = True ):
                    dpg.add_text( 'CMD:')     
                    dpg.add_text( tag = 46_2_1_1, default_value = 'DESCONECTADO!', tracked = True, track_offset = 1, )
                
                with dpg.child_window     ( tag   = 46_2_2_0  , autosize_x = True , pos=[0, dpg.get_item_height(46_0)-54] ):
                    with dpg.group        ( tag   = 46_2_2_1_0, horizontal = True ):
                        dpg.add_text      ( tag   = 46_2_2_1  , default_value =  "To send: "    )
                        dpg.add_input_text( tag   = 46_2_2_2  , on_enter =  True , callback = serial_write_message, user_data = 'manual_send' )
                        dpg.add_button    ( label = 'send'    , callback =  serial_write_message, user_data = 'manual_send' )
    handlers_and_themes_atuador()

def resize_atuador(): 
    cw = dpg.get_item_width( 'mainWindow' )/ 1474
    ch = dpg.get_item_height( 'mainWindow')/ 841 

    # General Draw              46_0
    dpg.configure_item( 46_0     , width  = cw*995, height = ch*480, pos = [cw*470, ch*360] ) #[995, 480] -> Draw 
    dpg.configure_item( 46_1_0   , width  = (cw*995)*0.4     ) 
    dpg.configure_item( 46_2_0   , width  = (cw*995)*0.575   )
    dpg.configure_item( 46_2_1_0 , height = (cw*480)-100     )
    dpg.configure_item( 46_2_2_0 , pos    = [0, (cw*480)-54] )
    dpg.configure_item( 46_2_2_2 , width  = (cw*995)*0.525   )
    # Zenite / Altitude Draw    45_0 
    dpg.configure_item( 45_0  , width = cw*495, height = ch*330, pos = [cw*970, ch*25 ] ) #[495, 330] -> Zenite 
    dpg.configure_item( 45_1_0, width = cw*478, height = ch*312 )
    # Azimute Draw              44_0
    dpg.configure_item( 44_0  , width = cw*495, height = ch*330, pos = [cw*470, ch*25 ] ) #[495, 330] -> Azimue
    dpg.configure_item( 44_1_0, width = cw*478, height = ch*312 )
    # Step Motors Config        43_0 
    dpg.configure_item( 43_0, width = cw*455, height = ch*520, pos = [cw*10 , ch*320] ) #[455, 480] -> Motores
    # Serial Config             42_0 
    dpg.configure_item( 42_0, width = cw*455, height = ch*298, pos = [cw*10 , ch*25 ] ) #[455, 330] -> Serial

def render_atuador() : 
    serial_verify_connection()
    serial_atualize_cmd()
    if GPHE_ATT or GPHG_ATT:
        graphs_atualize()
    
    if dpg.get_frame_count() % 10000 == 0:
        serial_write_message( None, None, 'INITCP')



