from dearpygui.dearpygui         import *

from views.menuInicio            import *
from views.menuVisualizacaoGeral import *
from views.menuPosicaoDoSol      import *
from views.menuAtuadores         import * 
from views.menuSensores          import * 
from views.menuRedNodeComm       import * 
from views.menuConfigurações     import * 

from themes                      import * 
from registry                    import * 
from time                        import sleep, time 

sun_data.update_date()

window_opened = ''

def resize_mainwindow (  ):
    new_w = get_item_width ( 1_0 )
    new_h = get_item_height( 1_0 ) 
    if   window_opened == 'Inicio'             : resize_inicio           ( new_w, new_h ) 
    elif window_opened == 'Visualizacao geral' : resize_visualizacaoGeral(  ) 
    elif window_opened == 'Posicao do sol'     : resize_posicaoDoSol     (  )
    elif window_opened == 'Atuadores'          : resize_atuador          (  )     
    elif window_opened == 'Sensores'           : resize_sensores         (  )  
    elif window_opened == 'Rednode comunicacao': resize_rednodecom       ( new_w, new_h )  
    elif window_opened == 'Configuracoes'      : resize_configuracoes    (  )  

def change_menu(sender, app_data, user_data ):
    global window_opened 
    window_opened = user_data 
    # CLOSE ALL WINDOWS 
    for k in windows.keys():
        for i in windows[k]:
            dpg.hide_item(i)
    # OPEN THE RIGHT TAB WINDOW 
    to_open = windows[user_data]
    for i in to_open:
        dpg.show_item(i)
    resize_mainwindow() 

def configure_viewport():
    setup_viewport ( )
    set_viewport_large_icon( PATH + 'ico\\large_ico.ico'              )
    set_viewport_small_icon( PATH + 'ico\\small_ico.ico'              ) 
    set_viewport_min_height( height = 900                             ) 
    set_viewport_min_width ( width  = 1000                            ) 
    set_viewport_title     ( title  = 'JetTracker - Controle do sol'  )

    change_font() 
    
    maximize_viewport() 

    set_primary_window    ( main_window, True    )

    init_inicio           ( windows, change_menu )
    init_visualizacaoGeral( windows              ) 
    init_posicaoDoSol     ( windows              )
    init_atuador          ( windows              ) 
    init_sensores         ( windows              ) 
    init_rednodecom       ( windows              ) 
    init_configuracoes    ( windows              ) 

def closing_dpg( sender, data, user ): 
    with window( pos = [ get_item_width(10)/2.5, get_item_height(10)/2.5]): 
        add_text( 'Obrigado por usar nosso programa\nEle irá encerrar em instantes' )
    sleep(2)
    stop_dearpygui() 

# Main Window 
with window( label = 'Main Window', id = 1_0, autosize = True ) as main_window:
    with menu_bar(label = "MenuBar"):
        add_menu_item( label="Inicio"             , callback = change_menu, user_data = "Inicio"              )
        add_menu_item( label="Visualização geral" , callback = change_menu, user_data = "Visualizacao geral"  )
        #add_menu_item( label="Posição do sol"     , callback = change_menu, user_data = "Posicao do sol"      )
        add_menu_item( label="Atuadores"          , callback = change_menu, user_data = "Atuadores"           )
        #add_menu_item( label="Atuação da base"    , callback = change_menu, user_data = "Atuacao da base"     )
        #add_menu_item( label="Atuação da elevação", callback = change_menu, user_data = "Atuacao da elevacao" )
        add_menu_item( label="Sensores"           , callback = change_menu, user_data = "Sensores"            )
        add_menu_item( label="RedNode Comunicacao", callback = change_menu, user_data = "Rednode comunicacao" )
        add_menu_item( label="Configurações"      , callback = change_menu, user_data = "Configuracoes"       )
        add_menu_item( label='Sair'               , callback = closing_dpg                                    )

configure_viewport( )
add_resize_handler( main_window, callback = resize_mainwindow ) 
change_menu       ( None, None, 'Inicio' )

time_date = 0 
time_acum = 0 

#show_implot_demo() 

while is_dearpygui_running():
    if not get_frame_count() % 1: 
        if   window_opened == 'Inicio'             : render_inicio ()           # ID = 1_0     
        elif window_opened == 'Visualizacao geral' : render_visualizacaoGeral() # ID = 2_0                 
        elif window_opened == 'Posicao do sol'     : render_posicaoDoSol()      # ID = 3_0         
        elif window_opened == 'Atuadores'          : render_atuador()           # ID = 4_0         
        elif window_opened == 'Sensores'           : render_sensores()          # ID = 5_0         
        elif window_opened == 'Rednode comunicacao': render_rednodecom()        # ID = 6_0         
        elif window_opened == 'Configuracoes'      : render_configuracao()      # ID = 9_0         

    time_acum += get_delta_time()
    time_date += get_delta_time() 

    if time_acum > 1 and get_value(hora_manual) == False:
        sun_data.update_date()
        
        set_value ( day          , sun_data.day               )
        set_value ( month        , sun_data.month             )
        set_value ( year         , sun_data.year              )
        set_value ( second       , sun_data.second            )
        set_value ( minute       , sun_data.minute            )
        set_value ( hour         , sun_data.hour              )
        set_value ( total_seconds, sun_data.total_seconds     )
        set_value ( dia_juliano  , sun_data.dia_juliano       )

        set_value ( azi          , sun_data.azi               )
        set_value ( alt          , sun_data.alt               )  

        set_value ( sunrise_azi  , sun_data.azimute_sunrise   )  
        set_value ( sunset_azi   , sun_data.azimute_sunset    )  
        set_value ( culminant_alt, sun_data.elevation_transit )  
        
        # Se estiver conectado, pega os valores de azi do motor e alt 
        if get_value( CONNECTED) == True: 
            set_value ( MG_Angle , sun_data.azi               )                 
            set_value ( ME_Angle , sun_data.alt               )
        
        time_acum = 0 
        refresh_TCP_connection( None, None, None )
    
    if time_date > 60: 
        send_date_ajust_motor() 
        time_date = 0 

    render_dearpygui_frame() 
print('Volte Sempre')