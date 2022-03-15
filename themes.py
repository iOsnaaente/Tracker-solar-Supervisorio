import dearpygui.dearpygui as dpg 
from registry import COLOR, PATH

#   THEMES 
with dpg.theme( tag = 99_100_1 ) as global_theme:
    with dpg.theme_component( dpg.mvAll ):
        dpg.add_theme_color( dpg.mvThemeCol_Button      , (52, 140, 215), category = dpg.mvThemeCat_Core )
        dpg.add_theme_style( dpg.mvStyleVar_FrameRounding,        5      , category = dpg.mvThemeCat_Core )
        # um azul bem bonito -> 52, 140, 215 
        # um laranja bem bonito -> 255, 140, 23 

with dpg.theme( tag = 99_100_2 ) as theme_button_on:
    with dpg.theme_component( dpg.mvButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button       , COLOR['on_color'](255), category =  dpg.mvThemeCat_Core)
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, COLOR['on_hover'](255), category =  dpg.mvThemeCat_Core)

with dpg.theme( tag = 99_100_3 ) as theme_button_off:
    with dpg.theme_component( dpg.mvButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button       , COLOR['off_color'](255), category = dpg.mvThemeCat_Core)
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, COLOR['off_hover'](255), category = dpg.mvThemeCat_Core)

with dpg.theme( tag = 99_100_4 ) as theme_no_border:
    with dpg.theme_component( dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category = dpg.mvThemeCat_Core)

with dpg.theme( tag = 99_100_5 ) as theme_no_win_border:
    with dpg.theme_component( dpg.mvAll):
        dpg.add_theme_style( dpg.mvStyleVar_WindowBorderSize, 0 , category = dpg.mvThemeCat_Core )

with dpg.theme( tag = 46_99_100_01 ) as btn_win_bg_lcd: 
    with dpg.theme_component( dpg.mvButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button        , [37,37,37], category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered , [37,37,37], category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonActive  , [37,37,37], category = dpg.mvThemeCat_Core )

#   APPLY DEFAULT THEMES AND FONTS
dpg.bind_theme( global_theme )


#   FONTS 
with dpg.font_registry() as font_add: 
    default_font = dpg.add_font( PATH + '\\utils\\fonts\\verdana.ttf', 14, parent = font_add )
    dpg.bind_font( default_font )


