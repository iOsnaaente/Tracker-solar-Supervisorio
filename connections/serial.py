import dearpygui.dearpygui as dpg
from connections.minimalModbus import Instrument

from connections.myModbus  import MyModbus 
from serial          import SerialException
from registry        import * 
from themes          import * 

import struct
import serial
import glob 
import sys  

# SERIAL 
COMP = MyModbus( )

def get_serial_ports( lenght : int = 25 ):
    if COMP.is_open:
        portList = [ COMP.COMPORT ]
    else: 
        portList = [] 
    if sys.platform.startswith('win'):  
        ports = ['COM%s' % (i + 1) for i in range( lenght )]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    else:
        print("Sistema Operacional não suportado")
    for port in ports:
        try:
            s = serial.Serial( port )
            s.close()
            portList.append(port)
        except (OSError, SerialException):
            pass
    COMP.seriais_available = portList
    return portList


def serial_try_to_connect( sender, data, user ): 
    global COMP 
    
    COMP.COMPORT = dpg.get_value(SERIAL_PORT)
    COMP.BAUDS   = int(dpg.get_value(SERIAL_BAUDRATE)) 
    COMP.TIMEOUT = dpg.get_value(SERIAL_TIMEOUT) 
    COMP.connect() 

    if COMP.is_open:
        dpg.show_item( 42_6 )
        dpg.show_item( 42_7 )
        dpg.bind_item_theme( item = 42_6, theme = theme_button_on  )
        dpg.bind_item_theme( item = 42_7, theme = theme_button_off )
        dpg.hide_item( 42_4 )
        dpg.set_value( SERIAL_CONNECTED, True)
    else:   
        dpg.hide_item( 42_6 )
        dpg.hide_item( 42_7 )
        dpg.show_item( 42_4 )
        dpg.set_value( SERIAL_CONNECTED, False)

def serial_refresh( sender, data, user ): 
    dpg.configure_item( 42_1_1, label = 'Procurando' ) 
    dpg.configure_item( 42_1  , items = get_serial_ports( 20 ) )
    dpg.configure_item( 42_1_1, label = 'Refresh' )

def serial_verify_connection(): 
    global COMP
    if not COMP.is_open: 
        dpg.hide_item( 42_6 )
        dpg.hide_item( 42_7 )
        dpg.show_item( 42_4 )
        dpg.set_value( SERIAL_CONNECTED, False)
    else: 
        if COMP.BUFFER_IN == []:
            dpg.set_value( 46_2_1_1, "CONECTADO!" )

def serial_close_connection(sender, data, user): 
    COMP.close()
    serial_verify_connection() 

def serial_update_values( ): 
    pass 

def serial_capture_frames(): 
    global COMP, MSG_INIT, MSG_COUNT
    global MPE_LIST, MPE_COUNT, SPE_LIST
    global MPG_LIST, MPG_COUNT, SPG_LIST
    global MPE, MPG, ALTITUDE, AZIMUTE
    global MDE_LIST, MDG_LIST 
    global GPHG_ATT, GPHE_ATT
    global MS_GIRO, PS_GIRO, TM_GIRO, CNT_GIRO 
    global MS_ELE , PS_ELE , TM_ELE , CNT_ELE

    if COMP.is_open: 
        if COMP.BUFFER_IN: 
            for ind, byte in enumerate(COMP.BUFFER_IN[-1][:-1]):
                if byte == MSG_INIT[MSG_COUNT]: 
                    MSG_COUNT = MSG_COUNT +  1
                else:
                    MSG_COUNT = 0 
                if MSG_COUNT == 4: 
                    MSG_COUNT = 0
                    OP = COMP.BUFFER_IN[-1][ind+1]

                    if OP == ord('e'):
                        try:
                            value = COMP.BUFFER_IN[-1][ind+2:ind+6]
                            value = struct.unpack('f', value )[0]
                            dpg.set_value(MPE, value) 
                            MPE_LIST.append( dpg.get_value(MPE) )
                            SPE_LIST.append( dpg.get_value(ZENITE) )
                            #MDE_LIST.append( int ( dt.datetime.timestamp( dt.datetime.utcnow() - dt.timedelta(hours=3) ) ) )
                            MDE_LIST.append( MPE_COUNT ) 
                            MPE_COUNT += 1
                            
                            # ELEVAÇÂO
                            if value:
                                if len(MPE_LIST) > 1000:
                                    MPE_LIST.pop(0)
                                    SPE_LIST.pop(0)
                                    MDE_LIST.pop(0)
                            
                                dpg.configure_item( 45_1_1, x = MDE_LIST, y = MPE_LIST )
                                dpg.configure_item( 45_1_2, x = MDE_LIST, y = SPE_LIST )
                                dpg.set_axis_limits( 'x_axis_alt', ymin = MDE_LIST[0], ymax = MDE_LIST[-1])
                                
                                CNT_ELE += 1 
                                if CNT_ELE == 500:
                                    CNT_ELE = 0
                                    TM_ELE.append( MDE_LIST.pop(-1) )
                                    MS_ELE.append( MPE_LIST.pop(-1) )
                                    PS_ELE.append( SPE_LIST.pop(-1) )
                                    if len(MS_ELE) > 7_200:
                                        MS_ELE.pop(0)
                                        TM_ELE.pop(0)
                                        PS_ELE.pop(0)
                                    dpg.set_axis_limits( 51_20, ymin = TM_ELE[0], ymax = TM_ELE[-1] )
                                    dpg.configure_item ( 51_40, x    = TM_ELE   , y    = MS_ELE     )
                                    dpg.configure_item ( 51_50, x    = TM_ELE   , y    = PS_ELE     ) 

                        except struct.error as e:
                            print( e )

                    elif OP == ord('g'):
                        try: 
                            value = COMP.BUFFER_IN[-1][ind+2:ind+6]
                            value = struct.unpack('f', value )[0]
                            dpg.set_value(MPG, value) 
                            MPG_LIST.append( dpg.get_value(MPG) )
                            SPG_LIST.append( dpg.get_value(AZIMUTE) )
                            #MDG_LIST.append(dt.datetime.timestamp( dt.datetime.utcnow() - dt.timedelta( hours = 3 )) ) 
                            MDG_LIST.append( MPG_COUNT ) 
                            MPG_COUNT += 1
                            if value:
                                if len(MPG_LIST) > 1000:
                                    MPG_LIST.pop(0)
                                    SPG_LIST.pop(0)
                                    MDG_LIST.pop(0)
                                
                                dpg.set_axis_limits( 'x_axis_azi', ymin = MDG_LIST[0], ymax = MDG_LIST[-1])
                                dpg.configure_item( 44_11, x = MDG_LIST, y = MPG_LIST )
                                dpg.configure_item( 44_12, x = MDG_LIST, y = SPG_LIST )

                                CNT_GIRO += 1 
                                if CNT_GIRO == 500: 
                                    CNT_GIRO = 0 
                                    MS_GIRO.append( MPG_LIST.pop(-1) )
                                    PS_GIRO.append( SPG_LIST.pop(-1) )
                                    TM_GIRO.append( MDG_LIST.pop(-1)  )
                                    if len( MS_GIRO ) > 7_200:
                                        MS_GIRO.pop(0)
                                        PS_GIRO.pop(0)
                                        TM_GIRO.pop(0)
                                    dpg.set_axis_limits( 52_20, ymin = TM_GIRO[0], ymax=TM_GIRO[-1])
                                    dpg.configure_item ( 52_40, x = TM_GIRO, y = MS_GIRO)
                                    dpg.configure_item ( 52_50, x = TM_GIRO, y = PS_GIRO)
                                    
                        except struct.error as e:
                            print( e )

                    elif OP == ord('H'):
                        try:
                            value = COMP.BUFFER_IN[-1][ind+2:ind+8]
                            y, m, d, h, mn, s = struct.unpack( 'bbbbbb', value )
                            if y < 22 or y > 50 or m > 12 or d > 31:
                                if h >= 24 or mn >= 60 or s >= 60: 
                                    dpg.set_value( WRONG_DATETIME, True ) 
                            else: 
                                date = dt.datetime.now()
                                if y != date.year-2000 or m != date.month or d != date.day :
                                    dpg.set_value( WRONG_DATETIME, True ) 
                                elif h != date.hour or ( date.minute + 5 < mn < date.minute - 5 ):
                                    dpg.set_value( WRONG_DATETIME, True ) 
                                dpg.set_value( WRONG_DATETIME, False )
                        except:
                            print( 'Datetime error: Propably unpack requires a buffer of 6 bytes')
                            

      
def serial_atualize_actuator_cmd( ): 
    global COMP 
    if COMP.is_open and COMP.DEBUG_MSG: 
        print( 'Aqui não sei')   
        MSG = '' 
        while len(COMP.DEBUG_MSG) > 30: 
            COMP.DEBUG_MSG.pop() 
        for text in COMP.DEBUG_MSG: 
            MSG += text + '\n'

        dpg.set_value( 46_2_11, MSG )
        dpg.set_value( 53_1, MSG )
    else:
        dpg.set_value( 46_2_1_1, "DESCONECTADO" ) 



def serial_att_plots( ) : 
    global COMP    , MSG_INIT , MSG_COUNT
    global MPE_LIST, MPE_COUNT, SPE_LIST
    global MPG_LIST, MPG_COUNT, SPG_LIST
    global ALTITUDE, AZIMUTE
    global MPE     , MPG, CNT_ELE     

    try: 
        status = COMP._read_inputs( addr = COMP.INPUT_SENS_GIR, num = 4 )
        if status:  azi, _, alt, _ = status  
        else:       return 0 

        dpg.set_value(MPG, azi/100 ) 
        dpg.set_value(MPE, alt/100 ) 
        
        MPG_LIST.append( dpg.get_value(MPG)     )
        SPG_LIST.append( dpg.get_value(AZIMUTE) )
        
        MPE_LIST.append( dpg.get_value(MPE)     )
        SPE_LIST.append( dpg.get_value(ALTITUDE) )

        #MDG_LIST.append(dt.datetime.timestamp( dt.datetime.utcnow() - dt.timedelta( hours = 3 )) ) 
        MDG_LIST.append( MPG_COUNT ) 
        MPG_COUNT += 1
        
        #MDE_LIST.append( int ( dt.datetime.timestamp( dt.datetime.utcnow() - dt.timedelta(hours=3) ) ) )
        MDE_LIST.append( MPE_COUNT ) 
        MPE_COUNT += 1
        
        # ELEVAÇÂO
        if len(MPE_LIST) > 1000:
            MPE_LIST.pop(0)
            SPE_LIST.pop(0)
            MDE_LIST.pop(0)
        
        if len(MPG_LIST) > 1000:
            MPG_LIST.pop(0)
            SPG_LIST.pop(0)
            MDG_LIST.pop(0)

        dpg.configure_item ( 44_11       , x    = MDG_LIST   , y    = MPG_LIST    )
        dpg.configure_item ( 44_12       , x    = MDG_LIST   , y    = SPG_LIST    )
        dpg.set_axis_limits( 'x_axis_azi', ymin = MDG_LIST[0], ymax = MDG_LIST[-1])
        
        dpg.configure_item ( 45_11       , x    = MDE_LIST   , y    = MPE_LIST    )
        dpg.configure_item ( 45_12       , x    = MDE_LIST   , y    = SPE_LIST    )
        dpg.set_axis_limits( 'x_axis_alt', ymin = MDE_LIST[0], ymax = MDE_LIST[-1])
        

        CNT_ELE += 1 
        if CNT_ELE == 500:
            CNT_ELE = 0
            TM_ELE.append( MDE_LIST[-1] )
            MS_ELE.append( MPE_LIST[-1] )
            PS_ELE.append( SPE_LIST[-1] )
            if len(MS_ELE) > 7_200:
                MS_ELE.pop(0)
                TM_ELE.pop(0)
                PS_ELE.pop(0)
            dpg.set_axis_limits( 51_20, ymin = TM_ELE[0], ymax = TM_ELE[-1] )
            dpg.configure_item ( 51_40, x    = TM_ELE   , y    = MS_ELE     )
            dpg.configure_item ( 51_50, x    = TM_ELE   , y    = PS_ELE     ) 

            MS_GIRO.append( MPG_LIST[-1] )
            PS_GIRO.append( SPG_LIST[-1] )
            TM_GIRO.append( MDG_LIST[-1]  )
            if len( MS_GIRO ) > 7_200:
                MS_GIRO.pop(0)
                PS_GIRO.pop(0)
                TM_GIRO.pop(0)

            dpg.set_axis_limits( 52_20, ymin = TM_GIRO[0], ymax=TM_GIRO[-1])
            dpg.configure_item ( 52_40, x = TM_GIRO, y = MS_GIRO)
            dpg.configure_item ( 52_50, x = TM_GIRO, y = PS_GIRO)
    
    except:
        pass 

def serial_request_diagnosis():
    print( 'solicitar diagnosticos')

def serial_print_comp():
    print( 'serial: ', COMP )

def serial_comp_is_open():
    return COMP.is_open 