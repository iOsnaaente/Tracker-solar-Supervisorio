import dearpygui.dearpygui  as dpg

from   connections.serial   import * 
from   registry             import * 
from   themes               import *

import datetime as dt 


# FUNCTIONS 
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


# HANDLERS AND THEMES
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


# MAIN FUNCTIONS 
def init_atuador( windows : dict ): 
    # Serial Config 
    with dpg.window( label = 'Serial' , tag = 42_0, width= 455, height= 330, pos = [10,25], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as serial_AT: 
        windows['Atuadores'].append( serial_AT )

        dpg.add_spacer( height = 1 )
        dpg.add_text('CONFIGURAÇÕES DE COMUNICAÇÃO')
        dpg.add_text('Selecione a porta serial: ')
        with dpg.group( horizontal = True ):
            dpg.add_combo( tag = 42_1, default_value = 'COM12', items = ['COM1', 'COM4', 'COM5', 'COM10', 'COM12', 'COM15', 'COM16', 'COM20'], source = SERIAL_PORT )
            dpg.add_button(  tag = 42_1_1, label = 'Refresh', callback = serial_refresh )
        dpg.add_spacer( height = 1 )

        dpg.add_text('Baudarate (COM): ')
        dpg.add_combo( tag = 42_2, default_value = '115200', items=[ '9600', '19200', '57600', '115200', '1000000'], source = SERIAL_BAUDRATE )
        dpg.add_spacer( height = 1 )

        dpg.add_text('Timeout (ms): ')
        dpg.add_input_int( tag = 42_3, default_value = 150, source = SERIAL_TIMEOUT)
        dpg.add_spacer( height = 3 )
        
        dpg.add_text('Slave Address (ID): ')
        dpg.add_input_int( tag = 42_3_1, default_value = 0x12, source = SERIAL_SLAVE )
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
            def send_motor_conf( sender, data, user ): 
                if user == 'MG': 
                    s  = dpg.get_value( MG_STEPS )
                    us = int(dpg.get_value( MG_USTEP ).replace('1/', ''))
                    dpg.set_value( MG_RESOLUCAO, s/us )
                    COMP.write_holdings( COMP.HR_GIR_STEP, [int(s), int(us)] )
                elif user == 'ME': 
                    s  = dpg.get_value( ME_STEPS )
                    us = int(dpg.get_value( ME_USTEP ).replace('1/', ''))
                    dpg.set_value( ME_RESOLUCAO, s/us )
                    COMP.write_holdings( COMP.HR_ELE_STEP, [int(s), int(us)] ) 

                elif user == 'MTGIR':
                    pass 
                
                elif user == 'MTELE':
                    pass

            with dpg.child_window( tag = 43_2_0, autosize_x =True, autosize_y = True): 
                dpg.add_text('DEFINIÇÃO DOS MOTORES DE PASSO')
                dpg.add_spacer(  height = 15 )
                with dpg.child_window  ( tag = 43_21_0, label = 'MotorGiro'    , autosize_x=True, height = 190 ):
                    dpg.add_text       ( default_value = "Motor de Rotação da base - Motor G" )
                    dpg.add_text       ( default_value = 'Resolução:' )
                    dpg.add_input_float( tag = 43_21_1, default_value = 1.8    , format = '%3.2f', source = MG_STEPS, callback = send_motor_conf, user_data = 'MG', on_enter = True )
                    dpg.add_text       ( default_value = 'Micro Passos do motor:' )
                    dpg.add_combo      ( tag = 43_21_3, default_value = '1/16'    , items  = ['1', '1/2', '1/4', '1/8', '1/16', '1/32'], source = MG_USTEP, callback= send_motor_conf, user_data = 'MG' )
                    dpg.add_text       ( default_value = 'Passos por volta:' )
                    dpg.add_drag_float ( tag = 43_21_2, default_value =  360 / 1.8, format = '%5.2f', source = MG_RESOLUCAO, no_input = True, callback= send_motor_conf, user_data = 'MG' )
            
                with dpg.child_window  ( tag = 43_22_0, label = 'MotorElevação', autosize_x=True, height = 190 ):
                    dpg.add_text       ( default_value = "Motor de Rotação da base - Motor 2")
                    dpg.add_text       ( default_value = 'Resolução:')
                    dpg.add_input_float( tag = 43_22_1, default_value = 1.8      , format = '%3.2f', source = ME_STEPS, callback = send_motor_conf, user_data = 'ME', on_enter = True )
                    dpg.add_text       ( default_value = 'Micro Passos do motor:')
                    dpg.add_combo      ( tag = 43_22_3, default_value = '1/16'   , items  = ['1', '1/2', '1/4', '1/8', '1/16', '1/32'], source = ME_USTEP, callback= send_motor_conf, user_data = 'ME' ) 
                    dpg.add_text       ( default_value = 'Passos por volta:')
                    dpg.add_drag_float ( tag = 43_22_2, default_value = 360 / 1.8, format ='%5.2f', source = ME_RESOLUCAO, no_input = True, callback = send_motor_conf, user_data = 'ME'  )
        
            # TRIFÁSICO 
            with dpg.child_window( tag = 43_3_0, autosize_x=True, autosize_y=True ):
                dpg.add_text('DEFINIÇÃO DE ACIONAMENTO TRIFÁSICO')
                
                dpg.add_spacer( height = 15 )
                with dpg.child_window( tag = 43_3_1_0, label = 'MotorGiro'    ,autosize_x = True, height = 100 ):
                    dpg.add_text       ( "Motor de Rotação da base - Motor 1" )
                    dpg.add_spacer     ( )
                    dpg.add_button     ( tag = 43_3_1_1, label= 'Desligado'  ,  width = 250, callback = send_motor_conf, user_data='MTGIR')
                    dpg.add_text       ( 'Velocidade angular MG:' )
                    dpg.add_input_float( tag = 43_3_1_2, label = 'Wo (rad/s)', default_value = dpg.get_value(MG_VELANG), source = MG_VELANG, format = '%3.2f' )
                    # CORRIGIR A TROCA DE MENSAGEM PARA AJUSTAR AS VELOCIDADES
                
                dpg.add_spacer    ( height = 15 )
                with dpg.child_window( tag = 43_3_2_0, label = 'MotorElevação',autosize_x = True, height = 125 ):
                        dpg.add_text       ( "Motor de Rotação da base - Motor 2")
                        dpg.add_spacer     ( )
                        dpg.add_button     ( tag = 43_3_2_1, label='Desligado', width=250, callback = send_motor_conf, user_data='MTELE')
                        dpg.add_text       ( 'Velocidade angular ME:' )
                        dpg.add_input_float( tag = 43_3_2_2, label = 'Wo (rad/s)', default_value = dpg.get_value(ME_VELANG), source = ME_VELANG, format = '%3.2f' )

            change_menubar_motors( None, None, 'step')
            
    # Azimute Draw 
    with dpg.window( label ='Azimute'     , tag = 44_0, width= 495, height= 330, pos = [470,25], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as azimute_config_AT: 
        windows['Atuadores'].append( azimute_config_AT)
        
        with dpg.plot( tag = 44_1_0, parent = 44_0, label = 'Azimute e angulo de giro', height = 312, width = 478, anti_aliased = True ): 
            dpg.add_plot_legend( )
            dpg.add_plot_axis  ( dpg.mvXAxis, label = 'Medições [n]', tag = 'x_axis_azi', time = True, no_tick_labels = True )
            dpg.add_plot_axis  ( dpg.mvYAxis, label = 'Angulo [º]' , tag = 'y_axis_azi' )
            dpg.set_axis_limits( 'x_axis_azi',  0,   1 )
            dpg.set_axis_limits( 'y_axis_azi', -5, 375 )
            dpg.add_line_series( [], [], tag = 44_11, label = 'Sensor Giro', parent = 'y_axis_azi' )
            dpg.add_line_series( [], [], tag = 44_12, label = 'Azimute sol', parent = 'y_axis_azi' ) 
 
    # Zenite / Altitude Draw 
    with dpg.window(label  = 'Zenite'     , tag = 45_0, width= 495, height= 330, pos = [970,25], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as zenite_config_AT:
        windows['Atuadores'].append( zenite_config_AT )  
        
        with dpg.plot( tag = 45_1_0, label = 'Zenite e angulo de elevação', height = 312, width = 478, anti_aliased = True ): 
            dpg.add_plot_legend()
            dpg.add_plot_axis( dpg.mvXAxis, label = 'Medições [n]', tag = 'x_axis_alt', time = True, no_tick_labels = True  )
            dpg.add_plot_axis( dpg.mvYAxis, label = 'Angulo [º]', tag = 'y_axis_alt' )
            dpg.set_axis_limits_auto( 'x_axis_alt')
            dpg.set_axis_limits( 'y_axis_alt', -5, 95 )
            dpg.add_line_series( [], [], tag = 45_11, label = 'Sensor Elevação', parent = 'y_axis_alt' )
            dpg.add_line_series( [], [], tag = 45_12, label = 'Zenite sol', parent = 'y_axis_alt' ) 
        
    # General Draw 
    with dpg.window( label = 'Draw_Window', tag = 46_0, width= 995, height= 480, pos = [470,360], no_resize=True, no_move = True, no_collapse = True, no_close = True, no_title_bar = True) as draw_tracker_AT:
        windows['Atuadores'].append( draw_tracker_AT )  
    
        def change_menubar_conf( sender, data, user ): 
            dpg.hide_item(46_11_10)
            dpg.hide_item(46_11_20)
            dpg.hide_item(46_11_30)
            dpg.hide_item(46_11_40)
            dpg.hide_item(46_11_50)
            if   user == "State":     dpg.show_item(46_11_10)   
            elif user == "Power":     dpg.show_item(46_11_20)   
            elif user == "Date/Time": dpg.show_item(46_11_30)   
            elif user == "Control":   dpg.show_item(46_11_40)   
            elif user == "Diagnosis": dpg.show_item(46_11_50)   

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
                with dpg.child_window( tag = 46_11_10, width = dpg.get_item_width(46_1_0), autosize_y = True, autosize_x = True, border = True ):
                    with dpg.child_window ( tag = 46_11_111, width = -1, height = 37 ):
                        with dpg.group    ( tag = 46_11_112, horizontal = True ): 
                            dpg.add_button( tag = 46_11_113, label='send', callback = lambda s, d, u :  COMP.write_holdings( COMP.HR_STATE, COMP.PICO_AUTOMATIC ) )
                            dpg.add_text  ( tag = 46_11_114, default_value = 'Estado AUTOMÁTICO (A)')  
                        with dpg.tooltip  ( tag = 46_11_115, parent = dpg.last_item() ): 
                            dpg.add_text  ( tag = 46_11_116, default_value = 'Entra no estado de operação automático' )
                    
                    with dpg.child_window ( tag = 46_11_121, width = -1, height = 37 ): 
                        with dpg.group    ( tag = 46_11_122, horizontal = True ): 
                            dpg.add_button( tag = 46_11_123, label='send', callback = lambda s, d, u :  COMP.write_holdings( COMP.HR_STATE, COMP.PICO_MANUAL ))
                            dpg.add_text  ( tag = 46_11_124, default_value = 'Estado MANUAL (L)')  
                        with dpg.tooltip  ( tag = 46_11_125, parent = dpg.last_item() ): 
                            dpg.add_text  ( tag = 46_11_126, default_value = 'O Tracker passa a ser acionado pelo movimento manual dos Levers\npresos ao próprio Tracker.' )
                
                    with dpg.child_window ( tag = 46_11_131, width = -1, height = 37 ):
                        with dpg.group    ( tag = 46_11_132, horizontal = True ): 
                            dpg.add_button( tag = 46_11_133, label='send', callback = lambda s, d, u :  COMP.write_holdings( COMP.HR_STATE, COMP.PICO_DEMO ))
                            dpg.add_text  ( tag = 46_11_134, default_value = 'Estado DEMO (D)')
                        with dpg.tooltip  ( tag = 46_11_135, parent = dpg.last_item() ): 
                            dpg.add_text  ( tag = 46_11_136, default_value = 'Entra no modo de demonstração de movimento.\nO tracker inicia o movimento começando pelo inicio do dia!' )
                    
                    with dpg.child_window ( tag = 46_11_141, width = -1, height = 37 ):
                        with dpg.group    ( tag = 46_11_142, horizontal = True ): 
                            dpg.add_button( tag = 46_11_143, label='send', callback = lambda s, d, u :  COMP.write_holdings( COMP.HR_STATE, COMP.PICO_REMOTE ))
                            dpg.add_text  ( tag = 46_11_144, default_value = 'Estado REMOTE (C)')
                        with dpg.tooltip  ( tag = 46_11_145, parent = dpg.last_item() ): 
                            dpg.add_text  ( tag = 46_11_146, default_value = 'Volta para o estado de operação definido anteriormente.\nSó irá funcionar caso o Tracker tenha entrado em algum estado de \noperação diferente do atuomático ou remoto.' )
                    
                    with dpg.child_window ( tag = 46_11_151, width = -1, height = 37 ):
                        with dpg.group    ( tag = 46_11_152, horizontal = True ): 
                            dpg.add_button( tag = 46_11_153, label='send', callback = lambda s, d, u :  COMP.write_holdings( COMP.HR_STATE, COMP.PICO_IDLE ))
                            dpg.add_text  ( tag = 46_11_154, default_value = 'Estado IDLE (S)')
                        with dpg.tooltip  ( tag = 46_11_155, parent = dpg.last_item() ):
                            dpg.add_text  ( tag = 46_11_156, default_value = 'Coloca o Tracker em modo de espera. Ele não muda nenhum estado de operação, apenas entra em loop' )
                    
                    with dpg.child_window ( tag = 46_11_161, width = -1, height = 37 ):
                        with dpg.group    ( tag = 46_11_162, horizontal = True ): 
                            dpg.add_button( tag = 46_11_163, label='send', callback = lambda s, d, u :  COMP.write_holdings( COMP.HR_STATE, COMP.PICO_RESET  ))
                            dpg.add_text  ( tag = 46_11_164, default_value = 'Estado RESET (R)')
                        with dpg.tooltip  ( tag = 46_11_165, parent = dpg.last_item() ):
                            dpg.add_text  ( tag = 46_11_166, default_value = 'O Tracker irá dar reboot!' )

                # POWER 
                with dpg.child_window( tag = 46_11_20, width = dpg.get_item_width(46_1_0), autosize_y = True, autosize_x = True, border = True ):
                    with dpg.child_window ( tag = 46_11_211, width = -1, height = 37 ):
                        with dpg.group    ( tag = 46_11_212, horizontal = True ): 
                            dpg.add_button( tag = 46_11_213, label='send', callback = lambda s, d, u : COMP.write_coils( COMP.COIL_POWER, True) )
                            dpg.add_text  ( tag = 46_11_214, default_value = ' Ativar motores (O)')
                        with dpg.tooltip  ( tag = 46_11_215, parent = dpg.last_item() ):
                            dpg.add_text  ( tag = 46_11_216, default_value =  'Para ligar os motores, o Tracker conta com um sistema eletromecânico de acionamento\nAo enviar "O" o sistema ira ligar.\nAo enviar "F" o sistema iá desligar.')
                    
                    with dpg.child_window ( tag = 46_11_221, width = -1, height = 37 ): 
                        with dpg.group    ( tag = 46_11_222, horizontal = True ): 
                            dpg.add_button( tag = 46_11_223, label='send', callback = lambda s, d, u : COMP.write_coils( COMP.COIL_POWER, False ))
                            dpg.add_text  ( tag = 46_11_224, default_value = 'Desativar motores (F)')
                        with dpg.tooltip  ( tag = 46_11_225, parent = dpg.last_item() ):
                            dpg.add_text  ( tag = 46_11_226, default_value = 'Para ligar os motores, o Tracker conta com um sistema eletromecânico de acionamento\nAo enviar "O" o sistema ira ligar.\nAo enviar "F" o sistema iá desligar.')
                            
                # DATA E HORA
                with dpg.child_window( tag = 46_11_30, width = dpg.get_item_width(46_1_0), autosize_y = True, autosize_x = True, border = True ):
                    def send_data( sender, data, user ):
                        if user == 'IN':
                            data = [] 
                            for val in dpg.get_value( 46_11_1 )[:3]: data.append( int(val) )
                            for val in dpg.get_value( 46_11_2 )[:3]: data.append( int(val) )
                            data[0] = data[0] - 2000 if data[0] > 2000 else data[0]
                            if   data[1] > 12: return 0       
                            elif data[2] > 31: return 0
                            elif data[3] > 60: return 0
                            elif data[4] > 60: return 0
                            elif data[5] > 23: return 0
                            dpg.set_value( HORA_MANUAL, True )
                        elif user == 'NOW':
                            now = dt.datetime.now() 
                            data = [ now.year if now.year < 2000 else now.year - 2000, now.month, now.day, now.hour, now.minute, now.second ]
                            dpg.set_value( HORA_MANUAL, False )
                        COMP.write_holdings( COMP.HR_YEAR, data )

                    with dpg.child_window       ( tag = 46_11_311, width = -1, height = 110 ):
                        with dpg.group          ( tag = 46_11_312, horizontal = True ): 
                            dpg.add_button      ( tag = 46_11_313, label='send', callback = send_data, user_data = 'IN'  )
                            dpg.add_text        ( tag = 46_11_314, default_value = 'Enviar hora (H)')
                        with dpg.group          ( tag = 46_11_315, horizontal = True ): 
                            dpg.add_input_floatx( tag = 46_11_1  , size = 3, source = 23_6, format = '%.0f', max_value = 99, callback = send_data, on_enter = True, user_data = 'IN' )
                            dpg.add_text        ( tag = 46_11_317, default_value = 'yy/mm/dd')
                        with dpg.group          ( tag = 46_11_318, horizontal = True ): 
                            dpg.add_input_floatx( tag = 46_11_2  , size = 3, source = 23_7, format = '%.0f', max_value = 60, callback = send_data, on_enter = True, user_data = 'IN' ) 
                            dpg.add_text        ( tag = 46_11_320, default_value = 'hh:mm:ss') 
                        
                    with dpg.child_window ( tag = 46_11_21, width = -1, height = 37 ):
                        with dpg.group    ( tag = 46_11_22, horizontal = True ):
                            dpg.add_button( tag = 46_11_23, label='send', callback = send_data, user_data = 'NOW' )
                            dpg.add_text  ( tag = 46_11_24, default_value = 'Enviar datetime atual (HA)')
                     
                # CONTROL 
                with dpg.child_window( tag = 46_11_40, width = dpg.get_item_width(46_1_0), autosize_y = True, autosize_x = True, border = True ):
                    def send_control( sender, data, user ) : 
                        if user == 'BOTH': 
                            gir, ele = dpg.get_value(46_11_43)[0], dpg.get_value(46_11_43)[1]
                            COMP.write_holdings( COMP.HR_PV_MOTOR_GIR, gir )
                            COMP.write_holdings( COMP.HR_PV_MOTOR_ELE, ele )

                        elif user == 'SINGLE': 
                            if dpg.get_value(46_1_1_4_5) == 'Gir': 
                                COMP.write_holdings( COMP.HR_PV_MOTOR_GIR, dpg.get_value(46_1_1_4_4) )
                            else: 
                                COMP.write_holdings( COMP.HR_PV_MOTOR_ELE, dpg.get_value(46_1_1_4_4) )

                        elif user == 'PV': 
                            COMP.write_holdings( COMP.HR_AZIMUTE , dpg.get_value( AZIMUTE  ) ) 
                            COMP.write_holdings( COMP.HR_ALTITUDE, dpg.get_value( ALTITUDE ) ) 

                        elif user == 'PID': 
                            PARAM = dpg.get_value( 46_11_422 )
                            VALUE = dpg.get_value(46_1_1_4_1)
                            if dpg.get_value(46_11_45) == 'Gir': 
                                if   PARAM == 'P':  COMP.write_holdings( COMP.HR_KP_GIR, VALUE ) 
                                elif PARAM == 'D':  COMP.write_holdings( COMP.HR_KD_GIR, VALUE )  
                                elif PARAM == 'I':  COMP.write_holdings( COMP.HR_KI_GIR, VALUE )
                            else:
                                if   PARAM == 'P':  COMP.write_holdings( COMP.HR_KP_ELE, VALUE ) 
                                elif PARAM == 'D':  COMP.write_holdings( COMP.HR_KD_ELE, VALUE )  
                                elif PARAM == 'I':  COMP.write_holdings( COMP.HR_KI_ELE, VALUE )
                    with dpg.child_window       ( tag = 46_11_410, width = -1, height = 85 ):
                        with dpg.group          ( tag = 46_11_411, horizontal = True ):
                            dpg.add_button      ( tag = 46_11_412, label = 'send', callback = send_control, user_data = 'PID' )
                            dpg.add_text        ( tag = 46_11_413, default_value = 'Configurar variáveis de processo (P)')
                        with dpg.tooltip        ( tag = 46_11_414, parent = dpg.last_item() ):
                            dpg.add_text        ( tag = 46_11_415, default_value = 
                            'Configura as variáveis de processo::\n' +
                            '\tP = Proporcional:: \n\t\tCausa uma variação da posição em função do erro.\n' +
                            '\tD = Derivativo:: \n\t\tCausa uma varição proporcional à inclinação do erro.\n' + 
                            '\tI = Integrativo:: \n\t\tCausa uma variação proporcional ao tempo de correção.\n' +
                            '\nCada motor pode possuir um parâmetro próprio de correção. ')

                        with dpg.group          ( tag = 46_11_420, horizontal = True):
                            dpg.add_radio_button( tag = 46_11_421, items = ['Gir', 'Ele'], default_value = 'Gir', horizontal = True ) 
                            dpg.add_spacer( width = 25 )
                            dpg.add_radio_button( tag = 46_11_422, items = ['D','I','P'] , default_value = 'D'  , horizontal = True ) 
                        dpg.add_input_float     ( tag = 46_11_41 , width = -1            , default_value = 0.5  , max_value = 1 , on_enter   = True, callback = send_control, user_data = 'PID' )

                    with dpg.child_window   ( tag = 46_11_430, width = -1, height = 60   ): 
                        with dpg.group      ( tag = 46_11_431, horizontal = True ): 
                            dpg.add_button  ( tag = 46_11_432, label ='send', callback = send_control, user_data = 'BOTH' )
                            dpg.add_text    ( tag = 46_11_433, default_value = 'Mover ambos motores (M)')
                        with dpg.tooltip    ( tag = 46_11_434, parent = dpg.last_item() ): 
                            dpg.add_text    ( tag = 46_11_435, default_value = 'Envia os valores de angulos para os motores:\nDireita(Giro)\nEsquerda(Elevação)\n\nDigite o valor de cada angulo, pressione enter para validar e aperte no botão send para enviar\nEvita o envio acidental de angulos errados')
                        dpg.add_input_floatx( tag = 46_11_43 , width = -1, size = 2, default_value = [ 125, 45.5], on_enter = True, callback = send_control, user_data = 'BOTH')
                 
                    with dpg.child_window   ( tag = 46_11_440, width = -1, height = 85  ): 
                        with dpg.group      ( tag = 46_11_441, horizontal = True ):
                            dpg.add_button  ( tag = 46_11_442, label='send', callback = send_control, user_data = 'SINGLE' )
                            dpg.add_text    ( tag = 46_11_443, default_value ='Mover um motor (m)')
                        with dpg.tooltip    ( tag = 46_11_444, parent = dpg.last_item() ): 
                            dpg.add_text    ( tag = 46_11_445, default_value = 'Envia os valores de um angulo de motor.\nSelecione o motor pelo radio button gir e ele.\n\nDigite o valor do angulo, pressione enter para validar e aperte no botão send para enviar\nEvita o envio acidental de um angulo errado')
                        dpg.add_input_float ( tag = 46_11_44 , width = -1, default_value = 12, on_enter = True, callback = send_control, user_data = 'SINGLE' )
                        dpg.add_radio_button( tag = 46_11_45 , items = ['Gir', 'Ele'], default_value = 'Gir', horizontal = True ) 
                    
                    with dpg.child_window ( tag = 46_11_460, width = -1, height = 37  ): 
                        with dpg.group    ( tag = 46_11_461, horizontal = True ): 
                            dpg.add_button( tag = 46_11_462, label='send', callback = send_control, user_data = 'PV' )
                            dpg.add_text  ( tag = 46_11_463, default_value = "Enviar Zenite e Azimute local (PV)")
                    with dpg.tooltip      ( tag = 46_11_464, parent = dpg.last_item() ): 
                            dpg.add_text  ( tag = 46_11_465, default_value = 'Envia os valores de Azimute e Zenite mostrados nos plots (Hora calculada - Manual ou Automática!) ')

                # DIAGNÓSTICO 
                with dpg.child_window( tag = 46_11_50, width = dpg.get_item_width(46_1_0), autosize_y = True, autosize_x = True, border = True ):
                    def get_diagnosis( sender, data, user ):
                            dpg.set_value(  SPG     , COMP.read_input_float( COMP.INPUT_SENS_GIR ) )
                            dpg.set_value(  SPE     , COMP.read_input_float( COMP.INPUT_SENS_ELE ) )
                            dpg.set_value(  AZIMUTE , COMP.read_input_float( COMP.INPUT_AZIMUTE  ) )
                            dpg.set_value(  ALTITUDE, COMP.read_input_float( COMP.INPUT_ALTITUDE ) )
                            dpg.set_value(  YEAR    , COMP.read_inputs     ( COMP.INPUT_YEAR     ) )
                            dpg.set_value(  MONTH   , COMP.read_inputs     ( COMP.INPUT_MONTH    ) )
                            dpg.set_value(  DAY     , COMP.read_inputs     ( COMP.INPUT_DAY      ) )
                            dpg.set_value(  HOUR    , COMP.read_inputs     ( COMP.INPUT_HOUR     ) )
                            dpg.set_value(  MINUTE  , COMP.read_inputs     ( COMP.INPUT_MINUTE   ) )
                            dpg.set_value(  SECOND  , COMP.read_inputs     ( COMP.INPUT_SECOND   ) )

                    with dpg.child_window ( tag = 46_11_511, width = -1, height = 37 ): 
                        with dpg.group    ( tag = 46_11_512, horizontal = True ):    
                            dpg.add_button( tag = 46_11_513, label = 'send', callback = get_diagnosis, user_data = 'INITPA')
                            dpg.add_text  ( tag = 46_11_514, default_value = 'Todas informações (A)')
                        with dpg.tooltip  ( tag = 46_11_515, parent = dpg.last_item() ):
                            dpg.add_text  ( tag = 46_11_516, default_value = 'Printa todas as informações listadas abaixo de uma só vez')

                    with dpg.child_window ( tag = 46_11_521, width = -1, height = 37 ):
                        with dpg.group    ( tag = 46_11_522, horizontal = True ):    
                            dpg.add_button( tag = 46_11_523, label='send', callback = get_diagnosis, user_data = 'INITPS')
                            dpg.add_text  ( tag = 46_11_524, default_value = 'Diagnostico dos sensores (S)')
                        with dpg.tooltip  ( tag = 46_11_525, parent = dpg.last_item() ):
                            dpg.add_text  ( tag = 46_11_526, default_value = 'Printa o diagnóstico dos sensore::\n\tNúmero de erros\n\tImprecisão do imã\n\tEstado da conexão')
                    
                    with dpg.child_window ( tag = 46_11_531, width = -1, height = 37 ): 
                        with dpg.group    ( tag = 46_11_532, horizontal = True ):    
                            dpg.add_button( tag = 46_11_533, label = 'send', callback = get_diagnosis, user_data = 'INITPP')
                            dpg.add_text  ( tag = 46_11_534, default_value = 'Diagnóstico de posições (P)')
                        with dpg.tooltip  ( tag = 46_11_535, parent = dpg.last_item() ):
                            dpg.add_text  ( tag = 46_11_536, default_value = 'Printa as informações de posição medidas::\n\tDevio padrão das medições')
                    
                    with dpg.child_window ( tag = 46_11_541, width = -1, height = 37 ):
                        with dpg.group    ( tag = 46_11_542, horizontal = True ):    
                            dpg.add_button( tag = 46_11_543, label='send', callback = get_diagnosis, user_data = 'INITPD')
                            dpg.add_text  ( tag = 46_11_544, default_value = 'Diagnóstico de date e hora (D)')
                        with dpg.tooltip  ( tag = 46_11_545, parent = dpg.last_item() ):
                            dpg.add_text  ( tag = 46_11_546, default_value = 'Printa os valores de correção de data e hora::\n\tHora do tracker\n\tCorreções de hora feitas')
                    
                    with dpg.child_window ( tag = 46_11_551, width = -1, height = 37 ): 
                        with dpg.group    ( tag = 46_11_552, horizontal = True ):    
                            dpg.add_button( tag = 46_11_553, label='send', callback = get_diagnosis, user_data = 'INITPU')
                            dpg.add_text  ( tag = 46_11_554, default_value = 'Diagnóstico de serial (U)')
                        with dpg.tooltip  ( tag = 46_11_555, parent = dpg.last_item() ):
                            dpg.add_text  ( tag = 46_11_556, default_value = 'Printa informações de pacotes não recebidos')

                    with dpg.child_window ( tag = 46_11_561, width = -1, height = 37 ): 
                        with dpg.group    ( tag = 46_11_562, horizontal = True ):    
                            dpg.add_button( tag = 46_11_563, label='send', callback = get_diagnosis, user_data = 'INITPC')
                            dpg.add_text  ( tag = 46_11_564, default_value = 'Checar se a hora esta sincronizada (C)')
                        with dpg.tooltip  ( tag = 46_11_565, parent = dpg.last_item() ):
                            dpg.add_text  ( tag = 46_11_566, default_value = 'Verifica a possibilidade da hora do tracker estar errada e precisar de sincronização\nEsse é um problema que normalmente é corrigido automaticamento, no entanto, nada impede de ser feito manualmente')

                    with dpg.child_window ( tag = 46_11_671, width = -1, height = -1 ):
                        dpg.add_text      ( tag = 46_11_672, default_value = 'Nice')

                change_menubar_conf( None, None, 'State')

            with dpg.child_window( tag = 46_2_0, width= (dpg.get_item_width(46_0)*0.6), autosize_y = True, border = False, menubar = True ):
                dpg.add_text( 'PICO_SM: RP2040 Serial Monitor')
                with dpg.menu_bar(label = "child_menubar_cmd"):
                    dpg.add_menu_item( label = "ASCII" , callback = change_menubar_cmd, user_data = "ASCII" )
                    dpg.add_menu_item( label = "HEX"   , callback = change_menubar_cmd, user_data = "HEX"   )
                  
                with dpg.child_window  ( tag = 46_2_1_0, autosize_x = True, border = True ):
                    dpg.add_text( 'CMD:')     
                    dpg.add_text( tag = 46_2_1_1, default_value = 'DESCONECTADO!', tracked = True, track_offset = 1, )
                
    # Aply handlers 
    handlers_and_themes_atuador()

def resize_atuador(): 
    cw = dpg.get_item_width( 'mainWindow' )/ 1474
    ch = dpg.get_item_height( 'mainWindow')/ 841 

    # General Draw              46_0
    dpg.configure_item( 46_0     , width  = cw*995, height = ch*480, pos = [cw*470, ch*360] ) #[995, 480] -> Draw 
    dpg.configure_item( 46_1_0   , width  = (cw*995)*0.4     ) 
    dpg.configure_item( 46_2_0   , width  = (cw*995)*0.575   )
    dpg.configure_item( 46_2_1_0 , height = (cw*480)-77      )

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
    serial_atualize_actuator_cmd()
