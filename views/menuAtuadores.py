from   utils.UART_comm      import UART_COM 
from   dearpygui.dearpygui  import *
from   registry             import * 
from   themes               import * 
import struct 
import math 

COMP = UART_COM( "" )

def att_CMD( ):
    global COMP 
    if COMP.connected == True:    
        COMP.read()
        MSG  = ''
        for n, row in enumerate( COMP.BUFFER_IN ):
            MSG += '[{}] '.format( COMP.COUNTER_IN + n - len(COMP.BUFFER_IN) )
            for collum in row: 
                MSG += chr(168) if collum < 32 or collum == 127 else chr(collum)
            MSG += '\n'
        configure_item( 46_2_1_1, default_value = MSG )
    else:
        configure_item( 46_2_1_1, default_value = 'DESCONECTADO!' )

#def get_params(): 
def get_zenith():
    global COMP 
    if COMP.BUFFER_IN:
        # Confere de trás para frente 
        for row in COMP.BUFFER_IN[::-1]:
            if row[:4] == b'init':
                try:  
                    value = row[4:8]
                    value = struct.unpack('f', value )[0]
                    return value 

                except struct.error as e:
                    print( e )


# CALLBACKS 
def att_motors_data( sender, data, user ):
    global COMP 
    if get_value(43_1) == 'de Passo':
        msg = 'INITZO'
        if user == 'Gir':
            msg += 'g'
            uStep = get_value( 43_2_1_3 )  
            if   uStep == '1'   : uStep = float(1 )
            elif uStep == '1/2 ': uStep = float(2 )
            elif uStep == '1/4 ': uStep = float(4 )
            elif uStep == '1/8 ': uStep = float(8 )
            elif uStep == '1/16': uStep = float(16) 
            elif uStep == '1/32': uStep = float(32)
            else:                 uStep = float(1 )
            set_value( 43_2_1_2, value= (360 / get_value( 43_2_1_1 ) if get_value( 43_2_1_1 ) > 0 else 0 ) ) 
            set_value( MG_Resolucao ,  get_value( 43_2_1_1 )      )     
            set_value( MG_Steps     ,  get_value( 43_2_1_2 )      ) 
            set_value( MG_uStep     ,  uStep                      ) 
            msg_bytes  =  struct.pack( 'f', get_value( 43_2_1_1 ) )
            msg_bytes +=  struct.pack( 'f', get_value( 43_2_1_2 ) )
            msg_bytes +=  struct.pack( 'f', uStep                 )
            for n in range( struct.calcsize('fff')):
                msg += chr( msg_bytes[n] )
        else:
            msg += 'e'
            uStep = get_value( 43_2_1_3 )  
            if   uStep == '1'   : uStep = float(1 )
            elif uStep == '1/2 ': uStep = float(2 )
            elif uStep == '1/4 ': uStep = float(4 )
            elif uStep == '1/8 ': uStep = float(8 )
            elif uStep == '1/16': uStep = float(16) 
            elif uStep == '1/32': uStep = float(32)
            else:                 uStep = float(1 )
            set_value( 43_2_2_2, value= (360 / get_value( 43_2_2_1 ) if get_value( 43_2_2_1 ) > 0 else 0 ) ) 
            set_value( ME_Resolucao , get_value( 43_2_2_1 ) )     
            set_value( ME_Steps     , get_value( 43_2_2_2 ) )
            set_value( ME_uStep     , uStep                 ) 
            msg_bytes  =  struct.pack( 'f', get_value( 43_2_2_1 ) )
            msg_bytes +=  struct.pack( 'f', get_value( 43_2_2_2 ) )
            msg_bytes +=  struct.pack( 'f', uStep                 )
            for n in range( struct.calcsize('fff')):
                msg += chr( msg_bytes[n] )
        
    else: 
        msg = 'INITzOc'
        set_value(VelAng_M1 , get_value(43_3_1_2) ) 
        set_value(VelAng_M2 , get_value(43_3_2_2) )
        msg_bytes  =  struct.pack( 'f', get_value(43_3_1_2) )
        msg_bytes +=  struct.pack( 'f', get_value(43_3_2_2) )
        for n in range( struct.calcsize('ff')):
            msg += chr( msg_bytes[n] )
    COMP.write( msg )

def write_message(sender, data, user ):
    global COMP
    msg = get_value( 46_2_2_2 )
    set_value( 46_2_2_2, '' )
    COMP.write( msg )

def write_hour( sender, data, user ) : 
    global COMP
    # 'INITHO'
    msg  = user 
    date = get_value( 46_1_1_1 )
    hour = get_value( 46_1_1_2 ) 
    if date[0] > 31:    raise 'days out of range'
    if date[1] > 12:    raise 'months out of range'       
    if hour[0] > 60:    raise 'seconds out of range'
    if hour[1] > 60:    raise 'minutes out of range'
    if hour[2] > 23:    raise 'hours out of range'
    if date[2] > 2000:  date[2] -= 2000
    date = struct.pack( 'bbb', date[0], date[1], date[2] ) 
    msg += chr(date[0]) + chr(date[1]) + chr(date[2])
    hour = struct.pack( 'bbb', hour[0], hour[1], hour[2]) 
    msg += chr(hour[0]) + chr(hour[1]) + chr(hour[2])
    COMP.write( msg )

def write_motors_pos(sender, data, user ) : 
    global COMP
    # 'INITMO' or 'INITmO' 
    msg = user
    if user == 'INITMO': 
        values = struct.pack('ff', get_value(46_1_1_3)[0], get_value(46_1_1_3)[1] ) 
        for i in range( struct.calcsize('ff')): 
            msg += chr(values[i])    

    elif user == 'INITmO':
        msg   += 'g' if get_value(46_1_1_4_1) == 'Gir' else 'e'
        values = struct.pack('f', get_value(46_1_1_4_2) )            
        for i in range( struct.calcsize('f')): 
            msg += chr(values[i])  

    elif user == 'INITP':
        msg = user + get_value(46_1_1_5_2)
        values = struct.pack('f', get_value(46_1_1_5_1) )   
        msg = msg.encode() + values
        print( msg )

    COMP.write( msg )

def write_message_buttons(sender, data, user ):
    global COMP
    if get_value(CONNECTED) == True:
        msg = user if type(user) == str else str(user)
        COMP.write( msg )
        print( 'Enviando:', msg )

def change_motors_conf(sender, data, user):
    if data == 'de Passo':
        show_item(43_2_0)
        hide_item(43_3_0)
    elif data == 'Trifásicos': 
        show_item(43_3_0)
        hide_item(43_2_0)

def change_state_motor(sender, data, user ) : 
    global COMP
    msg = 'INITzOS'
    if user == 'm1':
        set_value( M1_ONorOFF, not get_value(M1_ONorOFF) ) 
        if get_value(M1_ONorOFF): 
            set_item_theme( sender, Motor_On  )
            msg += 'gO'
        else : 
            set_item_theme( sender, Motor_Off )
            msg += 'gF'
        configure_item(sender, label= 'Ligado' if get_value(M1_ONorOFF) == True else 'Desligado' )

    elif user == 'm2':
        set_value( M2_ONorOFF, not get_value(M2_ONorOFF) ) 
        if get_value(M2_ONorOFF): 
            set_item_theme( sender, Motor_On  )
            msg += 'eO'
        else : 
            set_item_theme( sender, Motor_Off )
            msg += 'eF'
        configure_item(sender, label= 'Ligado' if get_value(M2_ONorOFF) else 'Desligado' )

    COMP.write( msg )

def SR_refresh( sender, data, user ):
    global COMP
    configure_item( 42_1_1, label = 'Procurando' ) 
    seriais = COMP.get_serial_ports( 20 )
    configure_item( 42_1  , items = seriais )
    configure_item( 42_1_1, label = 'Refresh' )

def SR_try_connect( sender, data, user): 
    global COMP 
    SR_Port      = get_value( 42_1 )
    SR_Baudrate  = int(get_value( 42_2 ))
    SR_Timeout   = int(get_value( 42_3 ))
    COMP = UART_COM( SR_Port, baudrate = SR_Baudrate, timeout = SR_Timeout )
    if COMP.connected:
        print('CONECTADO')
        show_item( 42_6 )
        show_item( 42_7 )
        set_item_theme( 42_6, Motor_On  )
        set_item_theme( 42_7, Motor_Off )
        hide_item( 42_4 )
        set_value( CONNECTED, True)
    else:
        print('NÂO CONECTOU')      
        hide_item( 42_6 )
        hide_item( 42_7 )
        show_item( 42_4 )
        set_value( CONNECTED, False)

def SR_close_connection(sender, data, user ): 
    global COMP
    COMP.close() 
    hide_item( 42_6 )         
    hide_item( 42_7 ) 
    show_item( 42_4 )


def change_menu(sender, data, user):
    print( sender, data, user )

def init_atuador( windows : dict ): 

    # Serial Config 
    with window( label = 'Serial'     , id = 42_0, width= 455, height= 330, pos = [10,25], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as serial_AT: 
        windows['Atuadores'].append( serial_AT )

        add_spacing(count = 1)
        add_text('CONFIGURAÇÕES DE COMUNICAÇÃO')

        add_text('Selecione a porta serial: ')
        add_combo( id = 42_1, default_value='COM12', items = ['COM1', 'COM4','COM12','COM15', 'COM16'] )
        add_same_line( )
        add_button(  id = 42_1_1, label='Refresh', callback = SR_refresh )
        add_spacing( count= 1 )

        add_text('Baudarate: ')
        add_combo( id = 42_2, default_value= '115200', items=[ '9600', '19200', '57600', '115200', '1000000'] )
        add_spacing( count = 1 )

        add_text('Timeout: ')
        add_input_int( id = 42_3, default_value= 1)
        add_spacing( count = 3 )

        add_button(label='Iniciar conexão',              id = 42_4 , callback= SR_try_connect      )
        add_button(label="CONECTADO"      , width = 150, id = 42_6                                 )
        add_same_line()
        add_button(label="DESCONECTAR"    , width = 150, id = 42_7, callback = SR_close_connection )
        add_spacing(count= 5)
        hide_item( 42_6)         
        hide_item( 42_7) 

    # Step Motors Config 
    with window( label = 'Motores'    , id = 43_0, width= 455, height= 480, pos = [10,360], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as config_AT:
        windows['Atuadores'].append( config_AT )
        add_text( 'CONFIGURAÇÃO DE ACIONAMENTO DOS MOTORES')
        add_spacing()

        # DEFNIÇÃO DOS MOTORES INDIVUDUAIS
        add_text('Motores ')
        add_same_line() 
        add_radio_button( id = 43_1, items = ['Trifásicos', 'de Passo'], default_value = 'de Passo', horizontal=True, callback = change_motors_conf)
        
        # DE PASSO 
        with child( id = 43_2_0, autosize_x =True, autosize_y = True): 
            add_text('DEFINIÇÃO DOS MOTORES DE PASSO')
            add_spacing( )
            with child( id = 43_2_1_0, label = 'MotorGiro'    , autosize_x=True, height = 200 ):
                add_text       ( "Motor de Rotação da base - Motor 1" )
                add_spacing    ( )
                add_text       ( 'Resolução:' )
                add_input_float( id = 43_2_1_1, default_value = 1.8       , format = '%3.2f', callback = att_motors_data, user_data = 'Gir', on_enter = True )
                add_spacing    ( )
                add_text       ( 'Micro Passos do motor:' )
                add_combo      ( id=43_2_1_3, default_value = '1/16'    , items  = ['1', '1/2', '1/4', '1/8', '1/16', '1/32'], callback= att_motors_data, user_data = 'Gir' )
                add_spacing    ( )
                add_text       ( 'Passos por volta:' )
                add_drag_float ( id = 43_2_1_2, default_value =  360 / 1.8, format = '%5.2f', no_input= True, callback= att_motors_data, user_data = 'Gir' )
            with child( id = 43_2_2_0, label = 'MotorElevação', autosize_x=True, height = 200 ):
                add_text       ( "Motor de Rotação da base - Motor 2")
                add_spacing    ( )
                add_text       ( 'Resolução:')
                add_input_float( id = 43_2_2_1, default_value = 1.8      , format = '%3.2f', callback = att_motors_data, user_data = 'Ele', on_enter = True )
                add_spacing    ( )
                add_text       ( 'Micro Passos do motor:')
                add_combo      ( id = 43_2_2_3, default_value = '1/16'   , items  = ['1', '1/2', '1/4', '1/8', '1/16', '1/32'], callback= att_motors_data, user_data = 'Ele' ) 
                add_spacing    ( )
                add_text       ( 'Passos por volta:')
                add_drag_float ( id = 43_2_2_2, default_value = 360 / 1.8, format ='%5.2f', no_input = True, callback = att_motors_data, user_data = 'Ele'  )
        
            set_item_theme(43_2_1_0, 'noborder')
            set_item_theme(43_2_2_0, 'noborder')

        # TRIFÁSICO 
        with child( id = 43_3_0, autosize_x=True, autosize_y=True ):
            add_text('DEFINIÇÃO DE ACIONAMENTO TRIFÁSICO')
            add_spacing( )
            with child( id = 43_3_1_0, label = 'MotorGiro'    ,autosize_x = True, height = 100 ):
                add_text       ( "Motor de Rotação da base - Motor 1" )
                add_spacing    ( )
                add_button     ( id = 43_3_1_1, label= 'Desligado'  ,  width = 250, callback = change_state_motor, user_data='m1')
                add_text       ( 'Velocidade angular M1:' )
                add_input_float( id = 43_3_1_2, label = 'Wo (rad/s)', default_value = get_value(VelAng_M1), format = '%3.2f', on_enter = True, callback = att_motors_data )
                # CORRIGIR A TROCA DE MENSAGEM PARA AJUSTAR AS VELOCIDADES

            add_spacing    ( )
            with child( id = 43_3_2_0, label = 'MotorElevação',autosize_x = True, height = 125 ):
                    add_text       ( "Motor de Rotação da base - Motor 2")
                    add_spacing    ( )
                    add_button     ( id = 43_3_2_1, label='Desligado', width=250, callback = change_state_motor, user_data='m2')
                    add_text       ( 'Velocidade angular M2:' )
                    add_input_float( id = 43_3_2_2, label = 'Wo (rad/s)', default_value = get_value(VelAng_M2), format = '%3.2f', on_enter = True, callback = att_motors_data )

                # CORRIGIR A TROCA DE MENSAGEM PARA AJUSTAR AS VELOCIDADES

            set_item_theme(43_3_1_0, 'noborder')
            set_item_theme(43_3_2_0, 'noborder')
            set_item_theme( 43_3_1_1, Motor_Off )
            set_item_theme( 43_3_2_1, Motor_Off )

        if get_value( 43_1 ) == 'de Passo':
            show_item(43_2_0)
            hide_item(43_3_0)
        else: 
            show_item(43_3_0)
            hide_item(43_2_0)
            
    # Azimute Draw 
    with window( label ='Azimute'     , id = 44_0, width= 495, height= 330, pos = [470,25], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as azimute_config_AT: 
        windows['Atuadores'].append( azimute_config_AT)
        with plot( id = 44_1_0, label = 'Azimute e angulo de giro', height = 312, width = 478, anti_aliased = True ): 
            add_plot_legend()
            add_plot_axis( mvXAxis, label = 'medição [n]', id = 'x_axis_azi' )
            set_axis_limits('x_axis_azi', 0, 1 )
            add_plot_axis( mvYAxis, label = 'Angulo [º]', id = 'y_axis_azi' )
            set_axis_limits( 'y_axis_azi', -5, 375 )
            add_line_series( [], [], id = 44_1_1, label = 'Sensor Giro', parent = 'y_axis_azi' )
            add_line_series( [], [], id = 44_1_2, label = 'Azimute sol', parent = 'y_axis_azi' ) 
     
    # Zenite / Altitude Draw 
    with window(label  = 'Zenite'     , id = 45_0, width= 495, height= 330, pos = [970,25], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as zenite_config_AT:
        windows['Atuadores'].append( zenite_config_AT )  
        with plot( id = 45_1_0, label = 'Zenite e angulo de elevação', height = 312, width = 478, anti_aliased = True ): 
            add_plot_legend()
            add_plot_axis( mvXAxis, label = 'medição [n]', id = 'x_axis_alt' )
            set_axis_limits_auto( 'x_axis_alt')
            add_plot_axis( mvYAxis, label = 'Angulo [º]', id = 'y_axis_alt' )
            set_axis_limits( 'y_axis_alt', -5, 100 )
            add_line_series( [], [], id = 45_1_1, label = 'Sensor Elevação', parent = 'y_axis_alt' )
            add_line_series( [], [], id = 45_1_2, label = 'Zenite sol', parent = 'y_axis_alt' ) 
        
    # General Draw 
    with window( label = 'Draw_Window', id = 46_0, width= 995, height= 480, pos = [470,360], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as draw_tracker_AT:
        windows['Atuadores'].append( draw_tracker_AT )  
    
        with menu_bar(label = "Draw_Window_Menu"):
            add_menu_item( label="State" , callback = change_menu, user_data = "State" )
            add_menu_item( label="Power" , callback = change_menu, user_data = "Power" )
            add_menu_item( label="Hora"  , callback = change_menu, user_data = "Hora" )
            add_menu_item( label="Print" , callback = change_menu, user_data = "Print" )
     
        with child(id = 46_1_0, width = (get_item_width(46_0)*0.3), border = False):
            add_text('Opções padrão de operação do sistema:')
            with child( id = 46_1_1_0, width = get_item_width(46_1_0), autosize_y=True, border = True ):
                add_button(label='send', callback = write_message_buttons, user_data='INITSO')
                add_same_line()
                add_text('S -> Parar o tracker')
                
                add_button(label='send', callback = write_message_buttons, user_data='INITDO')
                add_same_line()
                add_text('D -> Entra no modo Demo')
                
                add_button(label='send', callback = write_message_buttons, user_data='INITCO')
                add_same_line()
                add_text('C -> Continuar processo')
                
                add_button(label='send', callback = write_message_buttons, user_data='INITOO')
                add_same_line()
                add_text('O -> Ativar motores')
                
                add_button(label='send', callback = write_message_buttons, user_data='INITFO')
                add_same_line()
                add_text('F -> Desativar motores ')
                
                add_button(label='send', callback = write_message_buttons, user_data='INITGO')
                add_same_line()
                add_text('L -> Levers')                
                
                add_button(label='send', callback = write_message_buttons, user_data = 'INITPO')
                add_same_line()
                add_text('P -> Print data')
                
                add_spacing(count=3)
                
                add_button(label='send', callback = write_hour, user_data = 'INITHO' )
                add_same_line()
                add_text('H -> Trocar a hora')
                
                add_input_intx(id=46_1_1_1, size=3, default_value=[ 12, 5, 2021 ], max_value = 99, callback = write_hour, user_data = 'INITHO', on_enter = True )
                add_same_line()
                add_text('dd/mm/yy')
                
                add_input_intx(id=46_1_1_2, size=3, default_value=[ 15, 35, 10  ], max_value = 60, callback = write_hour, user_data = 'INITHO', on_enter = True ) 
                add_same_line()
                add_text('hh:mm:ss')
                
                add_spacing(count=3)

                add_button(label='send', callback = write_motors_pos, user_data = 'INITMO' )
                add_same_line()
                add_text('M -> Mover ambos motores')
                
                add_input_floatx(id=46_1_1_3, size=2, default_value=[ 12.05, 19.99], on_enter = True, callback = write_motors_pos, user_data = 'INITMO')
                
                add_spacing(count=3) 

                add_button(label='send', callback = write_motors_pos, user_data = 'INITmO' )
                add_same_line()
                add_text('m -> Mover um motore')
                add_input_float ( id = 46_1_1_4_2, default_value = 12, on_enter = True, callback = write_motors_pos, user_data = 'INITmO' )
                add_radio_button( id = 46_1_1_4_1, items = ['Gir', 'Ele'], default_value = 'Gir', horizontal = True ) 

                add_button(label='send', callback = write_motors_pos, user_data = 'INITP' )
                add_same_line()
                add_text('P -> Configurar variáveis de processo')
                add_input_float ( id = 46_1_1_5_1, default_value = 150, max_value=360, on_enter = True, callback = write_motors_pos, user_data = 'INITP' )
                add_radio_button( id = 46_1_1_5_2, items = ['V','D','I','P'], default_value = 'V', horizontal = True ) 

        add_same_line()
        with child( id = 46_2_0, width= (get_item_width(46_0)*0.7), autosize_y=True, border = False ):
            add_text( 'PICO_SM: RASPICO Serial Monitor')
            with child  ( id = 46_2_1_0, autosize_x = True, border = True):
                add_text( 'CMD:')       
                add_text( id = 46_2_1_1, default_value = 'DESCONECTADO!', tracked = True, track_offset = 1 )
            
            with child        ( id     = 46_2_2_0  , autosize_x = True , pos=[0, get_item_height(46_0)-54] ):
                add_group     ( id     = 46_2_2_1_0, horizontal = True )
                add_text      ( parent = 46_2_2_1_0, id = 46_2_2_1  , default_value =  "To send: "    )
                add_input_text( parent = 46_2_2_1_0, id = 46_2_2_2  , on_enter =  True , callback = write_message )
                add_button    ( parent = 46_2_2_1_0, label = 'send' , callback =  write_message )

    hide_item( 42_0)
    hide_item( 43_0)
    hide_item( 44_0)
    hide_item( 45_0)
    hide_item( 46_0)


def resize_atuador(): 
    cw = get_item_width( 1_0 ) / 1474
    ch = get_item_height( 1_0 )/ 841 

    # General Draw              46_0
    configure_item( 46_0     , width  = cw*995, height = ch*480, pos = [cw*470, ch*360] ) #[995, 480] -> Draw 
    configure_item( 46_1_0   , width  = (cw*995)*0.3     ) 
    configure_item( 46_2_0   , width  = (cw*995)*0.675   )
    configure_item( 46_2_1_0 , height = (cw*480)-100     )
    configure_item( 46_2_2_0 , pos    = [0, (cw*480)-54] )
    configure_item( 46_2_2_2 , width  = (cw*995)*0.525   )

    # Zenite / Altitude Draw    45_0 
    configure_item( 45_0  , width = cw*495, height = ch*330, pos = [cw*970, ch*25 ] ) #[495, 330] -> Zenite 
    configure_item( 45_1_0, width = cw*478, height = ch*312 )

    # Azimute Draw              44_0
    configure_item( 44_0  , width = cw*495, height = ch*330, pos = [cw*470, ch*25 ] ) #[495, 330] -> Azimue
    configure_item( 44_1_0, width = cw*478, height = ch*312 )

    # Step Motors Config        43_0 
    configure_item( 43_0, width = cw*455, height = ch*520, pos = [cw*10 , ch*320] ) #[455, 480] -> Motores

    # Serial Config             42_0 
    configure_item( 42_0, width = cw*455, height = ch*298, pos = [cw*10 , ch*25 ] ) #[455, 330] -> Serial

ME_list = []
MG_list = []
ZN_list = [] 
DOMINIO = []
COUNTER = 0 

from datetime import datetime as dt 
def render_atuador() : 
    global COMP, ME_list, MG_list, ZN_list, DOMINIO, COUNTER, last_zn
    while COMP.in_waiting() > 0:
        att_CMD()
        INIT  = b'init'
        count = 0
        if COMP.BUFFER_IN: 
            for n, r in enumerate( COMP.BUFFER_IN[-1] ): 
                if r == INIT[count]:    count += 1 
                else:                   count = 0 
                if count == 4:  
                    count = 0 
                    try: 
                        val = struct.unpack('f', COMP.BUFFER_IN[-1][n+1:n+5] )[0]
                    except:
                        continue
                    if val == 0:
                        continue
                    ZN_list.append( val )
                    ME_list.append( math.degrees(get_value( alt )) ) 
                    MG_list.append( math.degrees(get_value( azi )) )
                    DOMINIO.append( COUNTER )
                    COUNTER += 1
                    
                    if len(ZN_list) > 250: 
                        ZN_list.pop(0)
                    if len(ME_list) > 250: 
                        ME_list.pop(0)
                    if len(MG_list) > 250: 
                        MG_list.pop(0)
                    if len(DOMINIO) > 250: 
                        DOMINIO.pop(0)

                    last_zn = ZN_list[-1]

                    configure_item( 44_1_1, x = DOMINIO, y = ZN_list )
                    configure_item( 44_1_2, x = DOMINIO, y = MG_list )
                    configure_item( 45_1_1, x = DOMINIO, y = ME_list )

                    set_axis_limits('x_axis_azi', ymin = DOMINIO[0], ymax = DOMINIO[-1] )
                    set_axis_limits('x_axis_alt', ymin = DOMINIO[0], ymax = DOMINIO[-1] )

    cw = get_item_width( 1_0 ) / 1474
    ch = get_item_height( 1_0 )/ 841

def send_date_ajust_motor(): 
    msg    = 'INITPV'
    sun_data.update()
    value = struct.pack('f', math.degrees( sun_data.azi ) )   
    msg    = msg.encode() + value
    COMP.write( msg )