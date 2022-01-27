import dearpygui.dearpygui as dpg
from matplotlib.pyplot import table 

from connections.serial import COMP
from connections.serial import *
from registry           import * 

import math 
import time 

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
    with dpg.window(tag = 5_1_0, no_title_bar=True, no_move=True, no_resize=True, no_close=True, no_collapse=True) as WinPltM1:
        windows['Sensores'].append(WinPltM1)
        with dpg.plot(tag = 5_1_1, label="Sensor do Motor 1 (Giro)", width=700, height=200, anti_aliased=True ) :
            dpg.add_plot_legend()
            
            dpg.add_plot_axis( dpg.mvXAxis, label="Tempo (h)", tag = 5_1_2 )
            dpg.set_axis_limits( dpg.last_item(), ymin = 0, ymax = 100 )
            dpg.add_plot_axis( dpg.mvYAxis, label="Graus (º)", tag = 5_1_3 )
            dpg.set_axis_limits( dpg.last_item(), ymin = 0, ymax = 360 )
            
            dpg.add_line_series([i for i in range(100)], [ (360)*(0.75**i)*(1-0.75)**(1-0.75) for i in range(1, 100+1) ]                 , label = "Bernoulli", tag = 5_1_4 , parent = 5_1_3 )
            dpg.add_line_series([i for i in range(100)], [ (3600)*((math.e**(-50))*50**i)/math.factorial(i)   for i in range(1, 100+1) ] , label = "Poison"   , tag = 5_1_5 , parent = 5_1_3 )

    with dpg.window(id=5_2_0,  no_title_bar=True, no_move=True, no_resize=True, no_close=True, no_collapse=True) as WinPltM2:
        windows['Sensores'].append(WinPltM2)
        with dpg.plot( id=5_2_1, label="Sensor do Motor 2 (Giro)", width=700, height=200, anti_aliased=True) :
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Tempo (h)", tag = 5_2_2 )
            dpg.set_axis_limits( dpg.last_item(), ymin = 0, ymax = 100 )
            
            dpg.add_plot_axis( dpg.mvYAxis, label="Graus (º)", tag = 5_2_3 )
            dpg.set_axis_limits( dpg.last_item(), ymin = 0, ymax = 370 )         
            dpg.add_line_series([i for i in range(100)], [ (360*20)*(1/(10*math.sqrt(2*math.pi)))*math.e**(-((i-50)**2)/(2*10**2)) for i in range(1, 100+1) ], label = "Gauss"     , tag = 5_2_4, parent = 5_2_3 )
            dpg.add_line_series([i for i in range(100)], [ 350/(1+math.e**(-i))   for i in range(1, 100+1) ]                                                 , label = "Sigmoidal" , tag = 5_2_5, parent = 5_2_3 )

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
        
        row_names = ["Gir", 'PV', "Error", 'Conf', "D", "I", "P", "Ele", 'PV', "Error", 'Conf', "D", "I", "P" ]
        with dpg.table( tag = 54_3_0, header_row = True, label = 'Diagnosis uC Pico'):
            dpg.add_table_column( label = 'Variável')
            dpg.add_table_column( label = 'Diagnostico' )
            dpg.add_table_column( label = 'Medição' )
            for n, row in enumerate( row_names ):
                with dpg.table_row():
                    # Collum 1 
                    with dpg.table_cell():
                        dpg.add_text( row )
                    # Collum 2 
                    with dpg.table_cell():
                        dpg.add_drag_float( tag = 54_3_00 + n, default_value = random.randint(0,1000), no_input = True  ) 
                    # Collum 3
                    with dpg.table_cell():
                        dpg.add_drag_float( tag = 54_3_50 + n, default_value = random.randint(0,1000), no_input = True  ) 

def render_sensores() : 
    serial_capture_frames() 
    serial_atualize_actuator_cmd()                    
    dpg.set_value( 54350, dpg.get_value(MPG) )
    dpg.set_value( 54351, dpg.get_value(AZIMUTE) )
    dpg.set_value( 54352, abs(dpg.get_value(MPG)-dpg.get_value(AZIMUTE)) )
    dpg.set_value( 54353, 0  )
    dpg.set_value( 54354, 0  )
    dpg.set_value( 54355, 0  )
    dpg.set_value( 54356, 0  )
    dpg.set_value( 54357, dpg.get_value(MPE) )
    dpg.set_value( 54358, dpg.get_value(ZENITE) )
    dpg.set_value( 54359, abs(dpg.get_value(MPE)-dpg.get_value(ZENITE)) )
    dpg.set_value( 54350, 0  )
    dpg.set_value( 54361, 0  )
    dpg.set_value( 54362, 0  )
    dpg.set_value( 54363, 0  )