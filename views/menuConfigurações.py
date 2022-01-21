from dearpygui.dearpygui import *

def theme_color( sender, data, user ):
    with theme( default_theme=True):
        add_theme_color( user[0], [data[0]*255, data[1]*255, data[2]*255, data[3]*255], category=user[1])

def theme_style( sender, data, user ):  
    with theme( default_theme=True):
        if type(data) == int or type(data) == bool : 
            add_theme_style( user[0], data, category = mvThemeCat_Core)
        elif type(data) == list:
            add_theme_style( user[0], x = data[0], y = data[1], category = mvThemeCat_Core)
        else:
            print( data, user, len(data), type(data)) 

def init_configuracoes( windows : dict ): 

    with window( label = 'Configurações_Estilo'  , id = 9_1_0, pos = [50,50], width = 500, height = 500, no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True ) as style_CONFG:
        windows['Configuracoes'].append( style_CONFG )

        add_text( 'Configurações de janela' )
        add_checkbox     ( label = 'WindowBorderSize'   , callback = theme_style, user_data=[mvStyleVar_WindowBorderSize], default_value = True                                                  )
        add_slider_int   ( label = 'WindowMinSize   '   , callback = theme_style, user_data=[mvStyleVar_WindowMinSize]   , default_value = 0        , min_value = 0 , max_value = 1400           )
        add_slider_intx  ( label = 'WindowPadding'      , callback = theme_style, user_data=[mvStyleVar_WindowPadding]   , default_value = [5,5]    , size = 2, min_value = 0 , max_value = 25   )
        add_slider_floatx( label = 'WindowTitleAlign'   , callback = theme_style, user_data=[mvStyleVar_WindowTitleAlign], default_value = [0.5,0.5], size = 2, min_value = 0 , max_value = 2    )
        add_slider_floatx( label = 'WindowRouding'      , callback = theme_style, user_data=[mvStyleVar_WindowRounding]  , default_value = [1,1]    , size = 2, min_value = 0 , max_value = 1    )
        
        add_spacing() 
        add_text( 'Configurações de Childs')
        add_checkbox     ( label = 'ChildBorderSize'    , callback = theme_style, user_data=[mvStyleVar_ChildBorderSize], default_value = True)        
        add_slider_int   ( label = 'ChildRounding'      , callback = theme_style, user_data=[mvStyleVar_ChildRounding]  , default_value = 5 , min_value = 0  , max_value = 10   )    
        
        add_spacing() 
        add_text( 'Configurações de PopUp')
        add_checkbox     ( label = 'PopupBorderSize'    , callback = theme_style, user_data=[mvStyleVar_PopupBorderSize], default_value = False )        
        add_slider_int   ( label = 'PopupRounding'      , callback = theme_style, user_data=[mvStyleVar_PopupRounding], default_value = 5 , min_value = 0  , max_value = 10    )    
        
        add_spacing() 
        add_text( 'Configurações de Frames')
        add_checkbox     ( label = 'FrameBorderSize'    , callback = theme_style, user_data=[mvStyleVar_FrameBorderSize], default_value = False )        
        add_slider_floatx( label = 'FramePadding'       , callback = theme_style, user_data=[mvStyleVar_FramePadding], default_value = [5,4], size = 2, min_value=0, max_value = 10 )    
        add_slider_float ( label = 'FrameRounding'      , callback = theme_style, user_data=[mvStyleVar_FrameRounding], default_value = 5    , min_value = 0, max_value = 10   )   

        add_spacing() 
        add_text( 'Configurações de Itens')
        add_slider_intx  ( label = 'ItemSpacing'        , callback = theme_style, user_data=[mvStyleVar_ItemSpacing], default_value = [10,4], size = 2,  min_value = 5, max_value = 25 )    
        add_slider_intx  ( label = 'ItemInnerSpacing'   , callback = theme_style, user_data=[mvStyleVar_ItemInnerSpacing], default_value = [5,5] , size = 2,  min_value = 0, max_value = 10 )        
        
        add_spacing() 
        add_text( 'Configurações de Scroll')
        add_slider_int   ( label = 'ScrollbarSize'      , callback = theme_style, user_data = [mvStyleVar_ScrollbarSize], default_value = 15 , min_value = 0, max_value = 20 )    
        add_slider_int   ( label = 'ScrollbarRounding'  , callback = theme_style, user_data = [mvStyleVar_ScrollbarRounding], default_value = 2  , min_value = 0, max_value = 20 )        

        add_spacing() 
        add_text( 'Outras configurações')
        add_slider_intx  ( label = 'CellPadding'         , callback = theme_style, user_data=[mvStyleVar_CellPadding]       , default_value = [5,5]     , size = 2, min_value = 0, max_value = 20 )    
        add_slider_int   ( label = 'IndentSpacing'       , callback = theme_style, user_data=[mvStyleVar_IndentSpacing]     , default_value = 5                                                   )    
        add_slider_int   ( label = 'GrabMinSize'         , callback = theme_style, user_data=[mvStyleVar_GrabMinSize]       , default_value = 20                                                  )    
        add_slider_int   ( label = 'GrabRounding'        , callback = theme_style, user_data=[mvStyleVar_GrabRounding]      , default_value = 3                   , min_value = 0, max_value = 10 )    
        add_slider_floatx( label = 'ButtonAling'         , callback = theme_style, user_data=[mvStyleVar_ButtonTextAlign]   , default_value = [0.5, 0.5], size = 2, min_value = 0, max_value = 1  )    
        add_slider_floatx( label = 'SelectableTextAlign' , callback = theme_style, user_data=[mvStyleVar_SelectableTextAlign], default_value = [0.5, 0.5], size = 2, min_value = 0, max_value = 1  )

    with window( label = 'Configurações_Colors'  , id = 9_2_0, pos = [50,50], width = 700, height = 500, no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True ) as colors_CONFG:
        windows['Configuracoes'].append( colors_CONFG )
        add_color_edit( label = 'mvThemeCol_Text                 ', id =generate_uuid(), default_value = (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_Text, mvThemeCat_Core] ) 
        add_color_edit( label = 'mvThemeCol_TextDisabled         ', id =generate_uuid(), default_value = (0.50 * 255, 0.50 * 255, 0.50 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_TextDisabled, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_WindowBg             ', id =generate_uuid(), default_value = (0.06 * 255, 0.06 * 255, 0.06 * 255, 0.94 * 255), callback = theme_color, user_data=[mvThemeCol_WindowBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ChildBg              ', id =generate_uuid(), default_value = (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), callback = theme_color, user_data=[mvThemeCol_ChildBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_PopupBg              ', id =generate_uuid(), default_value = (0.08 * 255, 0.08 * 255, 0.08 * 255, 0.94 * 255), callback = theme_color, user_data=[mvThemeCol_PopupBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_Border               ', id =generate_uuid(), default_value = (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255), callback = theme_color, user_data=[mvThemeCol_Border, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_BorderShadow         ', id =generate_uuid(), default_value = (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), callback = theme_color, user_data=[mvThemeCol_BorderShadow, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_FrameBg              ', id =generate_uuid(), default_value = (0.16 * 255, 0.29 * 255, 0.48 * 255, 0.54 * 255), callback = theme_color, user_data=[mvThemeCol_FrameBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_FrameBgHovered       ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255), callback = theme_color, user_data=[mvThemeCol_FrameBgHovered, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_FrameBgActive        ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255), callback = theme_color, user_data=[mvThemeCol_FrameBgActive, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TitleBg              ', id =generate_uuid(), default_value = (0.04 * 255, 0.04 * 255, 0.04 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_TitleBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TitleBgActive        ', id =generate_uuid(), default_value = (0.16 * 255, 0.29 * 255, 0.48 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_TitleBgActive, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TitleBgCollapsed     ', id =generate_uuid(), default_value = (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.51 * 255), callback = theme_color, user_data=[mvThemeCol_TitleBgCollapsed, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_MenuBarBg            ', id =generate_uuid(), default_value = (0.14 * 255, 0.14 * 255, 0.14 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_MenuBarBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ScrollbarBg          ', id =generate_uuid(), default_value = (0.02 * 255, 0.02 * 255, 0.02 * 255, 0.53 * 255), callback = theme_color, user_data=[mvThemeCol_ScrollbarBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ScrollbarGrab        ', id =generate_uuid(), default_value = (0.31 * 255, 0.31 * 255, 0.31 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_ScrollbarGrab, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ScrollbarGrabHovered ', id =generate_uuid(), default_value = (0.41 * 255, 0.41 * 255, 0.41 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_ScrollbarGrabHovered, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ScrollbarGrabActive  ', id =generate_uuid(), default_value = (0.51 * 255, 0.51 * 255, 0.51 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_ScrollbarGrabActive, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_CheckMark            ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_CheckMark, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_SliderGrab           ', id =generate_uuid(), default_value = (0.24 * 255, 0.52 * 255, 0.88 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_SliderGrab, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_SliderGrabActive     ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_SliderGrabActive, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_Button               ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255), callback = theme_color, user_data=[mvThemeCol_Button, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ButtonHovered        ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_ButtonHovered, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ButtonActive         ', id =generate_uuid(), default_value = (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_ButtonActive, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_Header               ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.31 * 255), callback = theme_color, user_data=[mvThemeCol_Header, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_HeaderHovered        ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255), callback = theme_color, user_data=[mvThemeCol_HeaderHovered, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_HeaderActive         ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_HeaderActive, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_Separator            ', id =generate_uuid(), default_value = (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255), callback = theme_color, user_data=[mvThemeCol_Separator, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_SeparatorHovered     ', id =generate_uuid(), default_value = (0.10 * 255, 0.40 * 255, 0.75 * 255, 0.78 * 255), callback = theme_color, user_data=[mvThemeCol_SeparatorHovered, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_SeparatorActive      ', id =generate_uuid(), default_value = (0.10 * 255, 0.40 * 255, 0.75 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_SeparatorActive, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ResizeGrip           ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.20 * 255), callback = theme_color, user_data=[mvThemeCol_ResizeGrip, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ResizeGripHovered    ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255), callback = theme_color, user_data=[mvThemeCol_ResizeGripHovered, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ResizeGripActive     ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.95 * 255), callback = theme_color, user_data=[mvThemeCol_ResizeGripActive, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_Tab                  ', id =generate_uuid(), default_value = (0.18 * 255, 0.35 * 255, 0.58 * 255, 0.86 * 255), callback = theme_color, user_data=[mvThemeCol_Tab, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TabHovered           ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255), callback = theme_color, user_data=[mvThemeCol_TabHovered, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TabActive            ', id =generate_uuid(), default_value = (0.20 * 255, 0.41 * 255, 0.68 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_TabActive, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TabUnfocused         ', id =generate_uuid(), default_value = (0.07 * 255, 0.10 * 255, 0.15 * 255, 0.97 * 255), callback = theme_color, user_data=[mvThemeCol_TabUnfocused, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TabUnfocusedActive   ', id =generate_uuid(), default_value = (0.14 * 255, 0.26 * 255, 0.42 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_TabUnfocusedActive, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_DockingPreview       ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.70 * 255), callback = theme_color, user_data=[mvThemeCol_DockingPreview, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_DockingEmptyBg       ', id =generate_uuid(), default_value = (0.20 * 255, 0.20 * 255, 0.20 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_DockingEmptyBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_PlotLines            ', id =generate_uuid(), default_value = (0.61 * 255, 0.61 * 255, 0.61 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_PlotLines, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_PlotLinesHovered     ', id =generate_uuid(), default_value = (1.00 * 255, 0.43 * 255, 0.35 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_PlotLinesHovered, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_PlotHistogram        ', id =generate_uuid(), default_value = (0.90 * 255, 0.70 * 255, 0.00 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_PlotHistogram, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_PlotHistogramHovered ', id =generate_uuid(), default_value = (1.00 * 255, 0.60 * 255, 0.00 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_PlotHistogramHovered, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TableHeaderBg        ', id =generate_uuid(), default_value = (0.19 * 255, 0.19 * 255, 0.20 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_TableHeaderBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TableBorderStrong    ', id =generate_uuid(), default_value = (0.31 * 255, 0.31 * 255, 0.35 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_TableBorderStrong, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TableBorderLight     ', id =generate_uuid(), default_value = (0.23 * 255, 0.23 * 255, 0.25 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_TableBorderLight, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TableRowBg           ', id =generate_uuid(), default_value = (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), callback = theme_color, user_data=[mvThemeCol_TableRowBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TableRowBgAlt        ', id =generate_uuid(), default_value = (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.06 * 255), callback = theme_color, user_data=[mvThemeCol_TableRowBgAlt, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_TextSelectedBg       ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.35 * 255), callback = theme_color, user_data=[mvThemeCol_TextSelectedBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_DragDropTarget       ', id =generate_uuid(), default_value = (1.00 * 255, 1.00 * 255, 0.00 * 255, 0.90 * 255), callback = theme_color, user_data=[mvThemeCol_DragDropTarget, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_NavHighlight         ', id =generate_uuid(), default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[mvThemeCol_NavHighlight, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_NavWindowingHighlight', id =generate_uuid(), default_value = (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.70 * 255), callback = theme_color, user_data=[mvThemeCol_NavWindowingHighlight, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_NavWindowingDimBg    ', id =generate_uuid(), default_value = (0.80 * 255, 0.80 * 255, 0.80 * 255, 0.20 * 255), callback = theme_color, user_data=[mvThemeCol_NavWindowingDimBg, mvThemeCat_Core]  )
        add_color_edit( label = 'mvThemeCol_ModalWindowDimBg     ', id =generate_uuid(), default_value = (0.80 * 255, 0.80 * 255, 0.80 * 255, 0.35 * 255), callback = theme_color, user_data=[mvThemeCol_ModalWindowDimBg, mvThemeCat_Core]  )
    
    with window( label = 'Configurações_Diversos', id = 9_3_0, pos = [50,50], width = 300, height = 500, no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True ) as others_CONFG:
        windows['Configuracoes'].append( others_CONFG ) 
        w, h = get_item_width(9_3_0), get_item_height(9_3_0)
        add_text( 'Área de visualização das configurações', bullet = True ) 
        add_button(       label = 'Isto é um botão '        , width = w*0.9 , height = 50 )
        add_button(       label = 'E isso é um botão '      , width = w*0.44, height = 50 )
        add_same_line()
        add_button(       label= 'lado a lado '             , width = w*0.44, height = 50 )
        add_color_button( label = 'Isto é um botão colorido', width = w*0.9 , height = 50 , default_value = (55,102, 231,200) )
        add_spacing()
        add_radio_button( label = 'Radio button', items=['Isto', 'é', 'um', 'Radio', 'button'], horizontal = True )
        add_spacing()
        add_checkbox(     label = 'CheckBox 1')
        add_same_line()
        add_checkbox(     label = 'CheckBox 2')
        add_same_line()
        add_checkbox(     label = 'CheckBox 3')
        add_spacing() 
        with child( width = w*0.9, height = 100, label = 'Isto é um Child', border = True  ):
            add_text( 'Isto é uma Child')
            add_drawlist(  id = 9_3_1, label = 'Isto é um Draw_list' , width = 200     , height = 400  )
            draw_text( parent = 9_3_1, text  = 'Isto é um Draw_List' , pos   = [10,0]  , size   = 15   )
            draw_text( parent = 9_3_1, text  = 'Super longo'         , pos   = [10,20] , size   = 15   )
            draw_text( parent = 9_3_1, text  = 'Viu só'              , pos   = [10,380], size   = 15   )
        
        add_text('Clique aqui para abrir um ... ', id = 9_3_2 )
        with popup( parent = 9_3_2, mousebutton = mvMouseButton_Left):
            add_text( 'POPUP')
            add_button( label = 'Popup Com Botão também')
        
        add_spacing() 
        add_text( 'Um exemplo de color picker', bullet = True  ) 
        add_color_picker() 

def resize_configuracoes():
    w, h = get_item_width( 1_0 ), get_item_height( 1_0 ) 
    configure_item( 9_1_0, pos = [ 10            , 25 ], width = (w*(1/3))//1, height = (h*0.965)//1 ) 
    configure_item( 9_2_0, pos = [ w*(1/3)   + 10, 25 ], width = (w*(7/15)-5 )//1, height = (h*0.965)//1 ) 
    configure_item( 9_3_0, pos = [ w*(12/15) + 5 , 25 ], width = (w*(3/15)-10)//1, height = (h*0.965)//1 ) 

def render_configuracao():
    pass 

# ATUALIZAR AS CORES PADRÃO E FAZER O BOTÃO DE SALVAR AS CONFIGURAÇÕES