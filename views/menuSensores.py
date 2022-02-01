import dearpygui.dearpygui as dpg

from connections.serial    import *
from registry              import * 

import random 

## MAIN FUNCTIONS 
def resize_sensores(): 
    new_w, new_h = dpg.get_item_width('mainWindow'), dpg.get_item_height('mainWindow')
    dpg.configure_item( 5_1_0, width = new_w*0.65   , height = new_h*0.4   , pos = [10, 25]           )
    dpg.configure_item( 5_2_0, width = new_w*0.65   , height = new_h*0.4   , pos = [10, new_h*0.4+30] )
    dpg.configure_item( 5_3_0, width = new_w*0.65   , height = new_h*0.2-40, pos = [10, new_h*0.8+35] )
    dpg.configure_item( 5_4_0, width = new_w*0.35-20, height = new_h-30    , pos = [new_w*0.65+15,25] )
    dpg.configure_item( 5_1_1, width = new_w*0.639  , height = new_h*0.375                            )
    dpg.configure_item( 5_2_1, width = new_w*0.639  , height = new_h*0.375                            )

def init_sensores( windows : dict ):       
    with dpg.window(tag = 51_0, no_title_bar=True, no_move=True, no_resize=True, no_close=True, no_collapse=True) as WinPltM1:
        windows['Sensores'].append(WinPltM1)
        with dpg.plot(tag = 51_1, label="Sensor do Motor 1 (Giro)", width=700, height=200, anti_aliased=True ) :
            dpg.add_plot_legend()
            with dpg.plot_axis( dpg.mvXAxis, label="Tempo (h)", tag = 51_20 ):
                dpg.set_axis_limits( 51_20, ymin = 0, ymax = 1000 )
            with dpg.plot_axis( dpg.mvYAxis, label="Graus (º)", tag = 51_30 ):
                dpg.set_axis_limits( 51_30, ymin = -5, ymax = 370 )         
                dpg.add_line_series( [ ], [ ] , label = "Posição Motor Giro"   , tag = 51_40 , parent = 51_30 )
                dpg.add_line_series( [ ], [ ] , label = "Posição Sol - Azimute", tag = 51_50 , parent = 51_30 )

    with dpg.window( tag = 52_0,  no_title_bar=True, no_move=True, no_resize=True, no_close=True, no_collapse=True) as WinPltM2:
        windows['Sensores'].append(WinPltM2)
        with dpg.plot( tag = 52_1, label="Sensor do Motor 2 (Elevação)", width=700, height=200, anti_aliased=True) :
            dpg.add_plot_legend()
            with dpg.plot_axis( dpg.mvXAxis, label="Tempo (h)", tag = 52_20 ):
                dpg.set_axis_limits( 52_20, ymin = 0, ymax = 1000 )
            with dpg.plot_axis( dpg.mvYAxis, label="Graus (º)", tag = 52_30 ):
                dpg.set_axis_limits( 52_30, ymin = -5, ymax = 370 )         
                dpg.add_line_series([ ], [ ], label = "Posição Motor Elevação", tag = 52_40 , parent = 52_30 )
                dpg.add_line_series([ ], [ ], label = "Posição Sol - Zenite"  , tag = 52_50 , parent = 52_30 )
                
    with dpg.window(id=5_3_0, no_title_bar=True, no_move=True, no_resize=True, no_close=True, no_collapse=True) as WinPltMx:
        windows['Sensores'].append(WinPltMx)
        dpg.add_text('Log dos sensores (Rasp)')
        dpg.add_text( tag = 53_1, default_value = 'DESCONECTADO!' )

    with dpg.window(id=5_4_0, no_close=True, no_move=True, no_resize=True, no_title_bar=True, no_collapse=True ) as Comandos: 
        windows['Sensores'].append(Comandos)
        with dpg.group( horizontal = True ):    
            dpg.add_text('Diagnósticos:')   
            dpg.add_button( label = 'Solicitar diagnósticos', tag = 5_4_1, callback = serial_request_diagnosis ) 
        dpg.add_text( '', tag = 5_4_2 )
        
        row_names = ["\tGir", '\tPV', "\tError", '\tConf', "\tD", "\tI", "\tP", "\tEle", '\tPV', "\tError", '\tConf', "\tD", "\tI", "\tP" ]
        with dpg.table( tag = 54_3_0, header_row = True, label = 'Diagnosis uC Pico'):
            dpg.add_table_column( label = '\tVariável')
            dpg.add_table_column( label = '\tDiagnostico' )
            dpg.add_table_column( label = '\tMedição' )
            for n, row in enumerate( row_names ):
                with dpg.table_row():
                    # Collum 1 
                    with dpg.table_cell():
                        dpg.add_input_text( tag = 54_3_90 + n, default_value = row, width = -1, enabled = False, track_offset = 0.5  )
                    # Collum 2 
                    with dpg.table_cell():
                        dpg.add_drag_float( tag = 54_3_00 + n, default_value = random.randint(0,1000), width = -1, no_input = True  ) 
                    # Collum 3
                    with dpg.table_cell():
                        dpg.add_drag_float( tag = 54_3_50 + n, default_value = random.randint(0,1000), width = -1, no_input = True  ) 
            
    dpg.set_value( 54353, 0  )
    dpg.set_value( 54354, 0  )
    dpg.set_value( 54355, 0  )
    dpg.set_value( 54356, 0  )
    dpg.set_value( 54360, 0  )
    dpg.set_value( 54361, 0  )
    dpg.set_value( 54362, 0  )
    dpg.set_value( 54363, 0  )


def diagnosis_atualize_window():
    dpg.set_value( 54350, dpg.get_value(MPG) )
    dpg.set_value( 54351, dpg.get_value(AZIMUTE) )
    dpg.set_value( 54352, abs(dpg.get_value(MPG)-dpg.get_value(AZIMUTE)) )
    dpg.set_value( 54357, dpg.get_value(MPE) )
    dpg.set_value( 54358, dpg.get_value(ZENITE) )
    dpg.set_value( 54359, abs(dpg.get_value(MPE)-dpg.get_value(ZENITE)) )

def render_sensores() : 
    
    serial_capture_frames() 
    serial_atualize_actuator_cmd()                
    diagnosis_atualize_window() 
