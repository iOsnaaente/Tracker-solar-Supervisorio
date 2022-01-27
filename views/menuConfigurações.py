import dearpygui.dearpygui as dpg 

# CALLBACKS 
def theme_color( sender, data, user ):
    with dpg.theme( default_theme=True) as theme_set_color:
        with dpg.theme_component( dpg.mvAll): 
            dpg.add_theme_color( user[0], [data[0]*255, data[1]*255, data[2]*255, data[3]*255], category = user[1])
    #dpg.bind_theme( theme_set_color )
    print( 'Não implementado Themes color ainda' ) 

def theme_style( sender, data, user ):  
    with dpg.theme() as theme_set_style:
        with dpg.theme_component( dpg.mvAll ):
            if type(data) == int or type(data) == bool : 
                dpg.add_theme_style( user[0], data, category = dpg.mvThemeCat_Core)
            elif type(data) == list:
                dpg.add_theme_style( user[0], x = data[0], y = data[1], category = dpg.mvThemeCat_Core)
            else:
                print( data, user, len(data), type(data)) 
    print( 'Não implementado Themes style ainda' ) 
    ##dpg.bind_theme( theme_set_style )


# MAIN FUNCTIONS 
def init_configuracoes( windows : dict ): 
    with dpg.window( label = 'Configurações_Estilo'  , tag = 9_1_0, pos = [50,50], width = 500, height = 500, no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True ) as style_CONFG:
        windows['Configuracoes'].append( style_CONFG )
        dpg.add_text( 'Configurações de janela' )
        dpg.add_checkbox     ( label = 'WindowBorderSize'   , tag = 101_99_1 ,callback = theme_style, user_data = [dpg.mvStyleVar_WindowBorderSize], default_value = True                                                  )
        dpg.add_slider_int   ( label = 'WindowMinSize   '   , tag = 101_99_2 ,callback = theme_style, user_data = [dpg.mvStyleVar_WindowMinSize]   , default_value = 0        , min_value = 0 , max_value = 1400           )
        dpg.add_slider_intx  ( label = 'WindowPadding'      , tag = 101_99_3 ,callback = theme_style, user_data = [dpg.mvStyleVar_WindowPadding]   , default_value = [5,5]    , size = 2, min_value = 0 , max_value = 25   )
        dpg.add_slider_floatx( label = 'WindowTitleAlign'   , tag = 101_99_4 ,callback = theme_style, user_data = [dpg.mvStyleVar_WindowTitleAlign], default_value = [0.5,0.5], size = 2, min_value = 0 , max_value = 2    )
        dpg.add_slider_floatx( label = 'WindowRouding'      , tag = 101_99_5 ,callback = theme_style, user_data = [dpg.mvStyleVar_WindowRounding]  , default_value = [1,1]    , size = 2, min_value = 0 , max_value = 1    )
        dpg.add_spacer() 
        dpg.add_text( 'Configurações de Childs')
        dpg.add_checkbox     ( label = 'ChildBorderSize'    , tag = 101_99_6 ,callback = theme_style, user_data = [dpg.mvStyleVar_ChildBorderSize], default_value = True)        
        dpg.add_slider_int   ( label = 'ChildRounding'      , tag = 101_99_7 ,callback = theme_style, user_data = [dpg.mvStyleVar_ChildRounding]  , default_value = 5 , min_value = 0  , max_value = 10   )    
        dpg.add_spacer() 
        dpg.add_text( 'Configurações de PopUp')
        dpg.add_checkbox     ( label = 'PopupBorderSize'    , tag = 101_99_8 ,callback = theme_style, user_data = [dpg.mvStyleVar_PopupBorderSize], default_value = False )        
        dpg.add_slider_int   ( label = 'PopupRounding'      , tag = 101_99_9 ,callback = theme_style, user_data = [dpg.mvStyleVar_PopupRounding], default_value = 5 , min_value = 0  , max_value = 10    )    
        dpg.add_spacer() 
        dpg.add_text( 'Configurações de Frames')
        dpg.add_checkbox     ( label = 'FrameBorderSize'    , tag = 101_99_10 ,callback = theme_style, user_data = [dpg.mvStyleVar_FrameBorderSize], default_value = False )        
        dpg.add_slider_floatx( label = 'FramePadding'       , tag = 101_99_11 ,callback = theme_style, user_data = [dpg.mvStyleVar_FramePadding], default_value = [5,4], size = 2, min_value=0, max_value = 10 )    
        dpg.add_slider_float ( label = 'FrameRounding'      , tag = 101_99_12 ,callback = theme_style, user_data = [dpg.mvStyleVar_FrameRounding], default_value = 5    , min_value = 0, max_value = 10   )   
        dpg.add_spacer() 
        dpg.add_text( 'Configurações de Itens')
        dpg.add_slider_intx  ( label = 'ItemSpacing'        , tag = 101_99_13 ,callback = theme_style, user_data = [dpg.mvStyleVar_ItemSpacing], default_value = [10,4], size = 2,  min_value = 5, max_value = 25 )    
        dpg.add_slider_intx  ( label = 'ItemInnerSpacing'   , tag = 101_99_14 ,callback = theme_style, user_data = [dpg.mvStyleVar_ItemInnerSpacing], default_value = [5,5] , size = 2,  min_value = 0, max_value = 10 )        
        dpg.add_spacer() 
        dpg.add_text( 'Configurações de Scroll')
        dpg.add_slider_int   ( label = 'ScrollbarSize'      , tag = 101_99_15 ,callback = theme_style, user_data = [dpg.mvStyleVar_ScrollbarSize], default_value = 15 , min_value = 0, max_value = 20 )    
        dpg.add_slider_int   ( label = 'ScrollbarRounding'  , tag = 101_99_16 ,callback = theme_style, user_data = [dpg.mvStyleVar_ScrollbarRounding], default_value = 2  , min_value = 0, max_value = 20 )        
        dpg.add_spacer() 
        dpg.add_text( 'Outras configurações')
        dpg.add_slider_intx  ( label = 'CellPadding'        , tag = 101_99_17 ,callback = theme_style, user_data=[dpg.mvStyleVar_CellPadding]       , default_value = [5,5]     , size = 2, min_value = 0, max_value = 20 )    
        dpg.add_slider_int   ( label = 'IndentSpacing'      , tag = 101_99_18 ,callback = theme_style, user_data=[dpg.mvStyleVar_IndentSpacing]     , default_value = 5                                                   )    
        dpg.add_slider_int   ( label = 'GrabMinSize'        , tag = 101_99_19 ,callback = theme_style, user_data=[dpg.mvStyleVar_GrabMinSize]       , default_value = 20                                                  )    
        dpg.add_slider_int   ( label = 'GrabRounding'       , tag = 101_99_20 ,callback = theme_style, user_data=[dpg.mvStyleVar_GrabRounding]      , default_value = 3                   , min_value = 0, max_value = 10 )    
        dpg.add_slider_floatx( label = 'ButtonAling'        , tag = 101_99_21 ,callback = theme_style, user_data=[dpg.mvStyleVar_ButtonTextAlign]   , default_value = [0.5, 0.5], size = 2, min_value = 0, max_value = 1  )    
        dpg.add_slider_floatx( label = 'SelectableTextAlign', tag = 101_99_22 ,callback = theme_style, user_data=[dpg.mvStyleVar_SelectableTextAlign], default_value = [0.5, 0.5], size = 2, min_value = 0, max_value = 1  )

    with dpg.window( label = 'Configurações_Colors'  , tag = 9_2_0, pos = [50,50], width = 700, height = 500, no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True ) as colors_CONFG:
        windows['Configuracoes'].append( colors_CONFG )
        dpg.add_color_edit( label = 'mvThemeCol_Text                 ', tag = 100_99_1 , default_value = (1.00 * 255, 1.00 * 255, 1.00 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_Text,                 dpg.mvThemeCat_Core] ) 
        dpg.add_color_edit( label = 'mvThemeCol_TextDisabled         ', tag = 100_99_2 , default_value = (0.50 * 255, 0.50 * 255, 0.50 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TextDisabled,         dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_WindowBg             ', tag = 100_99_3 , default_value = (0.06 * 255, 0.06 * 255, 0.06 * 255, 0.94 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_WindowBg,             dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ChildBg              ', tag = 100_99_4 , default_value = (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ChildBg,              dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_PopupBg              ', tag = 100_99_5 , default_value = (0.08 * 255, 0.08 * 255, 0.08 * 255, 0.94 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_PopupBg,              dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_Border               ', tag = 100_99_6 , default_value = (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_Border,               dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_BorderShadow         ', tag = 100_99_7 , default_value = (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_BorderShadow,         dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_FrameBg              ', tag = 100_99_8 , default_value = (0.16 * 255, 0.29 * 255, 0.48 * 255, 0.54 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_FrameBg,              dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_FrameBgHovered       ', tag = 100_99_9 , default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_FrameBgHovered,       dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_FrameBgActive        ', tag = 100_99_10, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_FrameBgActive,        dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TitleBg              ', tag = 100_99_11, default_value = (0.04 * 255, 0.04 * 255, 0.04 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TitleBg,              dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TitleBgActive        ', tag = 100_99_12, default_value = (0.16 * 255, 0.29 * 255, 0.48 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TitleBgActive,        dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TitleBgCollapsed     ', tag = 100_99_13, default_value = (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.51 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TitleBgCollapsed,     dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_MenuBarBg            ', tag = 100_99_14, default_value = (0.14 * 255, 0.14 * 255, 0.14 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_MenuBarBg,            dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ScrollbarBg          ', tag = 100_99_15, default_value = (0.02 * 255, 0.02 * 255, 0.02 * 255, 0.53 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ScrollbarBg,          dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ScrollbarGrab        ', tag = 100_99_16, default_value = (0.31 * 255, 0.31 * 255, 0.31 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ScrollbarGrab,        dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ScrollbarGrabHovered ', tag = 100_99_17, default_value = (0.41 * 255, 0.41 * 255, 0.41 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ScrollbarGrabHovered, dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ScrollbarGrabActive  ', tag = 100_99_18, default_value = (0.51 * 255, 0.51 * 255, 0.51 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ScrollbarGrabActive,  dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_CheckMark            ', tag = 100_99_19, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_CheckMark,            dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_SliderGrab           ', tag = 100_99_20, default_value = (0.24 * 255, 0.52 * 255, 0.88 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_SliderGrab,           dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_SliderGrabActive     ', tag = 100_99_21, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_SliderGrabActive,     dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_Button               ', tag = 100_99_22, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.40 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_Button,               dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ButtonHovered        ', tag = 100_99_23, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ButtonHovered,        dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ButtonActive         ', tag = 100_99_24, default_value = (0.06 * 255, 0.53 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ButtonActive,         dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_Header               ', tag = 100_99_25, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.31 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_Header,               dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_HeaderHovered        ', tag = 100_99_26, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_HeaderHovered,        dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_HeaderActive         ', tag = 100_99_27, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_HeaderActive,         dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_Separator            ', tag = 100_99_28, default_value = (0.43 * 255, 0.43 * 255, 0.50 * 255, 0.50 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_Separator,            dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_SeparatorHovered     ', tag = 100_99_29, default_value = (0.10 * 255, 0.40 * 255, 0.75 * 255, 0.78 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_SeparatorHovered,     dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_SeparatorActive      ', tag = 100_99_30, default_value = (0.10 * 255, 0.40 * 255, 0.75 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_SeparatorActive,      dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ResizeGrip           ', tag = 100_99_31, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.20 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ResizeGrip,           dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ResizeGripHovered    ', tag = 100_99_32, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.67 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ResizeGripHovered,    dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ResizeGripActive     ', tag = 100_99_33, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.95 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ResizeGripActive,     dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_Tab                  ', tag = 100_99_34, default_value = (0.18 * 255, 0.35 * 255, 0.58 * 255, 0.86 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_Tab,                  dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TabHovered           ', tag = 100_99_35, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.80 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TabHovered,           dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TabActive            ', tag = 100_99_36, default_value = (0.20 * 255, 0.41 * 255, 0.68 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TabActive,            dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TabUnfocused         ', tag = 100_99_37, default_value = (0.07 * 255, 0.10 * 255, 0.15 * 255, 0.97 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TabUnfocused,         dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TabUnfocusedActive   ', tag = 100_99_38, default_value = (0.14 * 255, 0.26 * 255, 0.42 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TabUnfocusedActive,   dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_DockingPreview       ', tag = 100_99_39, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.70 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_DockingPreview,       dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_DockingEmptyBg       ', tag = 100_99_40, default_value = (0.20 * 255, 0.20 * 255, 0.20 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_DockingEmptyBg,       dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_PlotLines            ', tag = 100_99_41, default_value = (0.61 * 255, 0.61 * 255, 0.61 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_PlotLines,            dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_PlotLinesHovered     ', tag = 100_99_42, default_value = (1.00 * 255, 0.43 * 255, 0.35 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_PlotLinesHovered,     dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_PlotHistogram        ', tag = 100_99_43, default_value = (0.90 * 255, 0.70 * 255, 0.00 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_PlotHistogram,        dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_PlotHistogramHovered ', tag = 100_99_44, default_value = (1.00 * 255, 0.60 * 255, 0.00 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_PlotHistogramHovered, dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TableHeaderBg        ', tag = 100_99_45, default_value = (0.19 * 255, 0.19 * 255, 0.20 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TableHeaderBg,        dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TableBorderStrong    ', tag = 100_99_46, default_value = (0.31 * 255, 0.31 * 255, 0.35 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TableBorderStrong,    dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TableBorderLight     ', tag = 100_99_47, default_value = (0.23 * 255, 0.23 * 255, 0.25 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TableBorderLight,     dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TableRowBg           ', tag = 100_99_48, default_value = (0.00 * 255, 0.00 * 255, 0.00 * 255, 0.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TableRowBg,           dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TableRowBgAlt        ', tag = 100_99_49, default_value = (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.06 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TableRowBgAlt,        dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_TextSelectedBg       ', tag = 100_99_50, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 0.35 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_TextSelectedBg,       dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_DragDropTarget       ', tag = 100_99_51, default_value = (1.00 * 255, 1.00 * 255, 0.00 * 255, 0.90 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_DragDropTarget,       dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_NavHighlight         ', tag = 100_99_52, default_value = (0.26 * 255, 0.59 * 255, 0.98 * 255, 1.00 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_NavHighlight,         dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_NavWindowingHighlight', tag = 100_99_53, default_value = (1.00 * 255, 1.00 * 255, 1.00 * 255, 0.70 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_NavWindowingHighlight,dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_NavWindowingDimBg    ', tag = 100_99_54, default_value = (0.80 * 255, 0.80 * 255, 0.80 * 255, 0.20 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_NavWindowingDimBg,    dpg.mvThemeCat_Core]  )
        dpg.add_color_edit( label = 'mvThemeCol_ModalWindowDimBg     ', tag = 100_99_55, default_value = (0.80 * 255, 0.80 * 255, 0.80 * 255, 0.35 * 255), callback = theme_color, user_data=[dpg.mvThemeCol_ModalWindowDimBg,     dpg.mvThemeCat_Core]  )
    
    with dpg.window( label = 'Configurações_Diversos', tag = 9_3_0, pos = [50,50], width = 300, height = 500, no_move = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True ) as others_CONFG:
        windows['Configuracoes'].append( others_CONFG ) 
        w, h = dpg.get_item_width(9_3_0), dpg.get_item_height(9_3_0)
        dpg.add_text( 'Área de visualização das configurações', bullet = True ) 
        dpg.add_button(       label = 'Isto é um botão '        , width = w*0.9 , height = 50 )
        with dpg.group( horizontal = True ):
            dpg.add_button(       label = 'E isso é um botão '      , width = w*0.44, height = 50 )
            dpg.add_button(       label= 'lado a lado '             , width = w*0.44, height = 50 )
        dpg.add_color_button( label = 'Isto é um botão colorido', width = w*0.9 , height = 50 , default_value = (55,102, 231,200) )
        dpg.add_spacer()
        dpg.add_radio_button( label = 'Radio button', items=['Isto', 'é', 'um', 'Radio', 'button'], horizontal = True )
        dpg.add_spacer()
        with dpg.group( horizontal = True ):
            dpg.add_checkbox(     label = 'CheckBox 1')
            dpg.add_checkbox(     label = 'CheckBox 2')
            dpg.add_checkbox(     label = 'CheckBox 3')
        dpg.add_spacer() 
        with dpg.child_window( width = w*0.9, height = 100, label = 'Isto é um Child', border = True  ):
            dpg.add_text( 'Isto é uma Child')
            dpg.add_drawlist(  tag = 9_3_1, label = 'Isto é um Draw_list' , width = 200     , height = 400  )
            dpg.draw_text( parent = 9_3_1, text  = 'Isto é um Draw_List' , pos   = [10,0]  , size   = 15   )
            dpg.draw_text( parent = 9_3_1, text  = 'Super longo'         , pos   = [10,20] , size   = 15   )
            dpg.draw_text( parent = 9_3_1, text  = 'Viu só'              , pos   = [10,380], size   = 15   )
        
        dpg.add_text('Clique aqui para abrir um ... ', tag = 9_3_2 )
        with dpg.popup( parent = 9_3_2, mousebutton = dpg.mvMouseButton_Left):
            dpg.add_text( 'POPUP')
            dpg.add_button( label = 'Popup Com Botão também')
        
        dpg.add_spacer() 
        dpg.add_text( 'Um exemplo de color picker', bullet = True  ) 
        dpg.add_color_picker() 

def resize_configuracoes():
    w, h = dpg.get_item_width( 'mainWindow' ), dpg.get_item_height( 'mainWindow' ) 
    dpg.configure_item( 91_0, pos = [ 10            , 25 ], width = (w*(1/3))//1, height = (h*0.965)//1 ) 
    dpg.configure_item( 92_0, pos = [ w*(1/3)   + 10, 25 ], width = (w*(7/15)-5 )//1, height = (h*0.965)//1 ) 
    dpg.configure_item( 93_0, pos = [ w*(12/15) + 5 , 25 ], width = (w*(3/15)-10)//1, height = (h*0.965)//1 ) 

def render_configuracao():
    pass 

# ATUALIZAR AS CORES PADRÃO E FAZER O BOTÃO DE SALVAR AS CONFIGURAÇÕES