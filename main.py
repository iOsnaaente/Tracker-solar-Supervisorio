# INICIO DO CONTEXTO DPG 
import dearpygui.dearpygui as dpg

# INICIO DO CONTEXTO 
dpg.create_context()
dpg.create_viewport( title = 'Jet Towers Tracker', min_width = 800, min_height = 600 )
dpg.setup_dearpygui()


# CONFIGURAÇÃO DA FONTE - INICIO DO COD. 
with dpg.font_registry():
    defont = dpg.add_font("fonts\\verdana.ttf", 14 )
dpg.bind_font( defont )


# HANDLER REGISTRIES - INICIO DO COD.
with dpg.handler_registry( tag = 'handler' ):
    #dpg.add_mouse_click_handler( button = dpg.mvMouseButton_Left, callback = lambda : print(dpg.get_mouse_pos()), user_data = 'draw_list' )
    pass 


# FUNCTIONS OF INICIALIZATION
from registry import * 
from themes   import * 
from time     import *


# IMPORTAÇÕES LOCAIS 
from views.menuInicio            import *
from views.menuVisualizacaoGeral import *
from views.menuAtuadores         import * 
from views.menuSensores          import * 
from views.menuRedNodeComm       import * 
from views.menuConfigurações     import * 
from connections.serial          import COMP

window_opened = '' 


# CALLBACKs
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
    resize_main()

def closing_dpg( sender, data, user ): 
    with dpg.window( pos = [ dpg.get_item_width('mainWindow')/2.5, dpg.get_item_height('mainWindow')/2.5]): 
        dpg.add_text( 'Obrigado por usar nosso programa\nEle irá encerrar em instantes' )
    sleep(2)
    dpg.stop_dearpygui() 

# MAIN FUNTIONS 
def resize_main( ):
    global window_opened
    if   window_opened == 'Inicio'             : resize_inicio()
    elif window_opened == 'Visualizacao geral' : resize_visualizacaoGeral()
    elif window_opened == 'Posicao do sol'     : lambda : print('resize_posicaoDoSol     (  )')
    elif window_opened == 'Atuadores'          : resize_atuador()     
    elif window_opened == 'Sensores'           : resize_sensores() 
    elif window_opened == 'Rednode comunicacao': resize_rednodecom() 
    elif window_opened == 'Configuracoes'      : resize_configuracoes() 

def render_main( ):
    global window_opened
    if   window_opened == 'Inicio'             : render_inicio()
    elif window_opened == 'Visualizacao geral' : render_visualizacaoGeral()
    elif window_opened == 'Posicao do sol'     : lambda : print('resize_posicaoDoSol     (  )')
    elif window_opened == 'Atuadores'          : render_atuador()     
    elif window_opened == 'Sensores'           : render_sensores()  
    elif window_opened == 'Rednode comunicacao': render_rednodecom()
    elif window_opened == 'Configuracoes'      : render_configuracao() 

def init_main( ): 
    # MAIN WINDOW 
    with dpg.window( tag = 'mainWindow', autosize = True, no_close = True, no_move = True, no_resize = True ): 
        with dpg.menu_bar(label = "MenuBar"):
            dpg.add_menu_item( label = "Inicio"             , callback = change_menu, user_data = "Inicio"              )
            dpg.add_menu_item( label = "Visualização geral" , callback = change_menu, user_data = "Visualizacao geral"  )
            dpg.add_menu_item( label = "Atuadores"          , callback = change_menu, user_data = "Atuadores"           )
            dpg.add_menu_item( label = "Sensores"           , callback = change_menu, user_data = "Sensores"            )
            dpg.add_menu_item( label = "RedNode Comunicacao", callback = change_menu, user_data = "Rednode comunicacao" )
            dpg.add_menu_item( label = "Configurações"      , callback = change_menu, user_data = "Configuracoes"       )
            dpg.add_menu_item( label = 'Sair'               , callback = closing_dpg                                    )


# INICIALIZAÇÔES
init_main             (         ) 
init_rednodecom       ( windows )
init_inicio           ( windows, change_menu )
init_atuador          ( windows ) 
init_visualizacaoGeral( windows )
init_sensores         ( windows )
init_configuracoes    ( windows )


# CONFIGURATIONS 
dpg.set_primary_window          ( 'mainWindow', True          )
dpg.set_viewport_large_icon     ( PATH + 'ico\\large_ico.ico' )
dpg.set_viewport_small_icon     ( PATH + 'ico\\small_ico.ico' )
dpg.set_viewport_resize_callback( resize_main                 )
dpg.maximize_viewport           (                             ) 


# SETA A JANELA INICIAL 
change_menu  ( None, None, 'Inicio' )


# START OF DPG VIEW 
dpg.show_viewport( )


while dpg.is_dearpygui_running(): 
    dpg.render_dearpygui_frame() 
    render_main() 
    
    # COM 60FPS TEM-SE 0.01667s PARA DAR 1 FRAME
    # A CADA 60 FRAME SE PASSAM 1 SEGUNDO 
    if dpg.get_frame_count() % 60 == 0: 
        if not dpg.get_value( HORA_MANUAL ): 
            SUN_DATA.set_date( dt.datetime.utcnow() )
            dpg.set_value( ZENITE , math.degrees(SUN_DATA.alt) ) 
            dpg.set_value( AZIMUTE, math.degrees(SUN_DATA.azi) )
            dpg.set_value( YEAR   , SUN_DATA.year   )
            dpg.set_value( MONTH  , SUN_DATA.month  )
            dpg.set_value( DAY    , SUN_DATA.day    )
            dpg.set_value( HOUR   , SUN_DATA.hour   )
            dpg.set_value( MINUTE , SUN_DATA.minute )
            dpg.set_value( SECOND , SUN_DATA.second )
            dpg.set_value( TOT_SECONDS, SUN_DATA.total_seconds )
            dpg.set_value( JULIANSDAY , SUN_DATA.dia_juliano )

        if dpg.get_frame_count() % 600 == 0: 
            if serial_comp_is_open():
                if dpg.get_value( WRONG_DATETIME ):
                    serial_write_message( None, None, 'INITHA')
                    print( 'mudamos a hora ')
                
        # PARA DAR 3.600 FRAMES TEM-SE 1 MINUTO  
        if dpg.get_frame_count() % 3_6000 == 0:
            if serial_comp_is_open():
                serial_write_message( None, None, 'INITCP')
                serial_request_diagnosis( None, None, None)
# CLOSE DPG 
dpg.destroy_context() 



