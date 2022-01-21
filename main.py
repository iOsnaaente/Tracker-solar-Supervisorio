# INICIO DO CONTEXTO DPG 
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport( title = 'Jet Towers Tracker', min_width = 800, min_height = 600 )
dpg.setup_dearpygui()

print( dpg.get_dearpygui_version() ) 

# FUNCTIONS OF INICIALIZATION
from registry import * 
from themes   import * 
from time     import *

# LOCAL
from views.menuInicio            import *
from views.menuVisualizacaoGeral import *
#from views.menuPosicaoDoSol      import *

from views.menuAtuadores         import * 
#from views.menuSensores          import * 
#from views.menuRedNodeComm       import * 
#from views.menuConfigurações     import * 

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
    elif window_opened == 'Sensores'           : lambda : print('resize_sensores         (  )') 
    elif window_opened == 'Rednode comunicacao': lambda : print('resize_rednodecom       (  )') 
    elif window_opened == 'Configuracoes'      : lambda : print('resize_configuracoes    (  )') 

def render_main( ):
    global window_opened
    if   window_opened == 'Inicio'             : render_inicio()
    elif window_opened == 'Visualizacao geral' : render_visualizacaoGeral() 
    elif window_opened == 'Posicao do sol'     : lambda : print('render_posicaoDoSol     (  )')
    elif window_opened == 'Atuadores'          : render_atuador()     
    elif window_opened == 'Sensores'           : lambda : print('render_sensores         (  )') 
    elif window_opened == 'Rednode comunicacao': lambda : print('render_rednodecom       (  )') 
    elif window_opened == 'Configuracoes'      : lambda : print('render_configuracoes    (  )') 



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

# HANDLER REGISTRIES 
with dpg.handler_registry( tag = 'handler' ):
    #dpg.add_mouse_click_handler( button = dpg.mvMouseButton_Left, callback = lambda : print(dpg.get_mouse_pos()), user_data = 'draw_list' )
    pass 



# CONFIGURATIONS 
dpg.set_primary_window          ( 'mainWindow', True          )
dpg.set_viewport_large_icon     ( PATH + 'ico\\large_ico.ico' )
dpg.set_viewport_small_icon     ( PATH + 'ico\\small_ico.ico' )
dpg.set_viewport_resize_callback( resize_main                 )
dpg.maximize_viewport           (                             ) 

# INICIALIZAÇÔES
init_inicio           ( windows, change_menu )
init_atuador          ( windows ) 
init_visualizacaoGeral( windows )

change_menu  ( None, None, 'Inicio' )


# START OF DPG VIEW 
dpg.show_viewport( )
while dpg.is_dearpygui_running(): 
    dpg.render_dearpygui_frame() 
    render_main() 

    if dpg.get_frame_count() % 100 == 0: 
        SUN_DATA.update() 
        dpg.set_value( ZENITE, math.degrees(SUN_DATA.alt)  ) 
        dpg.set_value( AZIMUTE, math.degrees(SUN_DATA.azi) )

        
    

# CLOSE DPG 
dpg.destroy_context() 



