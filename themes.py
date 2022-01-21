import dearpygui.dearpygui as dpg 
from registry import color

with dpg.theme( default_theme = True ) as theme_id:
    dpg.add_theme_color( dpg.mvThemeCol_Button       , (52, 140, 215), category = dpg.mvThemeCat_Core )
    dpg.add_theme_style( dpg.mvStyleVar_FrameRounding,        5      , category = dpg.mvThemeCat_Core )
    # um azul bem bonito -> 52, 140, 215 
    # um laranja bem bonito -> 255, 140, 23 
    
with dpg.theme( id = dpg.generate_uuid() ) as Motor_On:
    dpg.add_theme_color( dpg.mvThemeCol_Button       , color['on_color'](255), category =  dpg.mvThemeCat_Core)
    dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, color['on_hover'](255), category =  dpg.mvThemeCat_Core)

with dpg.theme( id = dpg.generate_uuid() ) as Motor_Off:
    dpg.add_theme_color( dpg.mvThemeCol_Button       , color['off_color'](255), category = dpg.mvThemeCat_Core)
    dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, color['off_hover'](255), category = dpg.mvThemeCat_Core)

with dpg.theme( id = 'noborder'):
    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 0, category = dpg.mvThemeCat_Core)

with dpg.theme( id = 'no_win_border'):
    dpg.add_theme_style( dpg.mvStyleVar_WindowBorderSize, 0 , category = dpg.mvThemeCat_Core )
