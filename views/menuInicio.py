import os 
PATH     = os.path.dirname( __file__ ).removesuffix('views')
PATH_IMG = PATH + 'utils\\img\\'

import sys 
sys.path.insert(0, PATH )

import time 

import dearpygui.dearpygui as dpg 
from   functions import add_image_loaded
from   themes import *


# REGISTRIES ESPECIFIC 
img_fundo = add_image_loaded( PATH_IMG + 'fundo.jpg' )
img_logo  = add_image_loaded( PATH_IMG + 'JetTowers-Logo.png' )
img_inic  = add_image_loaded( PATH_IMG + 'init_img\\' + 'inic.png')
img_posi  = add_image_loaded( PATH_IMG + 'init_img\\' + 'posi.jpg')
img_atua  = add_image_loaded( PATH_IMG + 'init_img\\' + 'atua.png')
img_sens  = add_image_loaded( PATH_IMG + 'init_img\\' + 'sens.png')
img_comu  = add_image_loaded( PATH_IMG + 'init_img\\' + 'comu.jpg') 
img_conf  = add_image_loaded( PATH_IMG + 'init_img\\' + 'conf.png') 

# CALLBACKS 
def hover_buttons ( handler , data, user ):    
    if   data == 1_2_11 : dpg.configure_item( 1_3_1_1, texture_tag = img_inic ) 
    elif data == 1_2_22 : dpg.configure_item( 1_3_1_1, texture_tag = img_posi ) 
    elif data == 1_2_33 : dpg.configure_item( 1_3_1_1, texture_tag = img_atua ) 
    elif data == 1_2_44 : dpg.configure_item( 1_3_1_1, texture_tag = img_sens ) 
    elif data == 1_2_55 : dpg.configure_item( 1_3_1_1, texture_tag = img_comu ) 
    elif data == 1_2_66 : dpg.configure_item( 1_3_1_1, texture_tag = img_conf ) 

def closing_dpg( sender, data, user ): 
    with dpg.window( pos = [ dpg.get_item_width('mainWindow')/2.5, dpg.get_item_height('mainWindow')/2.5]): 
        dpg.add_text( 'Obrigado por usar nosso programa\nEle irá encerrar em instantes' )
    time.sleep(2)
    dpg.stop_dearpygui() 


# HANDLER_REGISTERS / THEMES 
def handlers_and_themes_inicio(): 
    with dpg.item_handler_registry( ) as handler_hover:
        dpg.add_item_hover_handler( callback = hover_buttons )
    dpg.bind_item_handler_registry( item = 1_2_11, handler_registry = handler_hover )
    dpg.bind_item_handler_registry( item = 1_2_22, handler_registry = handler_hover )
    dpg.bind_item_handler_registry( item = 1_2_33, handler_registry = handler_hover )
    dpg.bind_item_handler_registry( item = 1_2_44, handler_registry = handler_hover )
    dpg.bind_item_handler_registry( item = 1_2_55, handler_registry = handler_hover )
    dpg.bind_item_handler_registry( item = 1_2_66, handler_registry = handler_hover )

    dpg.bind_item_theme( 1_1, theme_no_win_border)
    dpg.bind_item_theme( 1_2, theme_no_win_border)
    dpg.bind_item_theme( 1_3, theme_no_win_border)

# MAIN FUNCTIONS 
def resize_inicio( ):
    w, h = dpg.get_item_width( 'mainWindow'), dpg.get_item_height('mainWindow')
    dpg.configure_item( 1_1 , width = w-15     , height = h*3/10    , pos = [ 10       , 25             ] )
    dpg.configure_item( 1_2 , width = w/3      , height = h*6.60/10 , pos = [ 10       , (h//10)*3 + 20 ] )
    dpg.configure_item( 1_3 , width = w*2/3-20 , height = h*6.60/10 , pos = [ w//3 + 15, (h//10)*3 + 35 ] )

    w_header , h_header  = dpg.get_item_width( 1_1 ), dpg.get_item_height( 1_1 )
    dpg.configure_item( 1_1_1_0 , width = w_header-16 , height = h_header-16 ) # HEADER 
    dpg.configure_item( 1_1_1_1 , pmin  = (-30,-30)   , pmax   = ( w, round( h*3/10)*2 ))
    dpg.configure_item( 1_1_1_2 , pmin  = (10,10)     , pmax   = (350,200) )

    v_spacing = dpg.get_item_height( 1_2 ) // 7  # LATERAL 
    dpg.configure_item( 1_2_11, width = w//3 - 15, height = v_spacing ) 
    dpg.configure_item( 1_2_22, width = w//3 - 15, height = v_spacing ) 
    dpg.configure_item( 1_2_33, width = w//3 - 15, height = v_spacing ) 
    dpg.configure_item( 1_2_44, width = w//3 - 15, height = v_spacing ) 
    dpg.configure_item( 1_2_55, width = w//3 - 15, height = v_spacing ) 
    dpg.configure_item( 1_2_66, width = w//3 - 15, height = v_spacing )  

    dpg.configure_item( 1_3_1_0, width = (w*2/3-20)*0.99 , height = (h*6.60/10)*0.875 )
    dpg.configure_item( 1_3_1_1, pmax  = [ (w*2/3-20)*0.99 , (h*6.60/10)*0.8750 ]  )
    dpg.configure_item( 1_3_1_2, pos   = [ (w*2/3-20)*0.99//3 , 50 ])


def render_inicio( ):
    if dpg.get_frame_count() % 5 == 0: 
        resize_inicio()   

def init_inicio( windows :dict, callback ): 
    with dpg.window( label = 'Header' , tag = 1_1, pos = [10, 25], no_move  = True , no_close    = True, no_title_bar= True, no_resize= True ) as Header_IN:    
        windows['Inicio'].append( Header_IN )
        dpg.add_drawlist( tag = 1_1_1_0, width= dpg.get_item_width( 1_1 )-16, height= dpg.get_item_height( 1_1 ) - 16 )
        dpg.draw_image  ( parent = 1_1_1_0, tag = 1_1_1_1, label = 'imgFundo', texture_tag = img_fundo, pmin = (0,0), pmax = (1,1) ) 
        dpg.draw_image  ( parent = 1_1_1_0, tag = 1_1_1_2, label = 'imgLogo' , texture_tag = img_logo , pmin = (0,0), pmax = (1,1) )

    with dpg.window( label = 'Lateral', tag = 1_2, no_move= True , no_close = True , no_title_bar= True, no_resize= True ) as Lateral_IN:
        windows['Inicio'].append( Lateral_IN )
        dpg. add_spacer( )
        dpg.add_button(  label = "Visualização geral" , tag = 1_2_11, arrow  = False, callback = callback, user_data   = "Visualizacao geral"  )
        dpg.add_button(  label = "Atuadores"          , tag = 1_2_33, arrow  = False, callback = callback, user_data   = "Atuadores"           )
        dpg.add_button(  label = "Sensores"           , tag = 1_2_44, arrow  = False, callback = callback, user_data   = "Sensores"            )
        dpg.add_button(  label = "RedNode Comunicaçaõ", tag = 1_2_55, arrow  = False, callback = callback, user_data   = "Rednode comunicacao" )
        dpg.add_button(  label = "Configurações"      , tag = 1_2_66, arrow  = False, callback = callback, user_data   = "Configuracoes"       )
        dpg.add_button(  label = "Sair"               , tag = 1_2_22, arrow  = False, callback = closing_dpg                                   )

    with dpg.window( label = 'Main'   , tag = 1_3, no_move= True , no_close = True , no_title_bar= True, no_resize= True) as Main_IN:
        windows['Inicio'].append( Main_IN )
        dpg.add_drawlist( tag = 1_3_1_0, width = 1000, height = 1000 )
        dpg.draw_image  ( parent = 1_3_1_0, tag = 1_3_1_1, label = 'imgMain', texture_tag = img_inic, pmin = (0,0), pmax = (100,100) ) 
        dpg.draw_text( pos = [500/500], text = '', tag = 1_3_1_2, size = 20 )
    
    resize_inicio() 
    handlers_and_themes_inicio()