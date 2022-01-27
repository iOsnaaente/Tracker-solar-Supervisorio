from email.policy import default
import dearpygui.dearpygui as dpg
import struct 
import time 
import math 

from serial   import SerialException
from registry import * 
from themes   import * 

from utils.UART_comm import UART_COM 

# SERIAL 
COMP = UART_COM( "" )

def serial_capture_frames(): 
    global COMP, MSG_INIT, MSG_COUNT
    global MPE_LIST, MPE_COUNT, SPE_LIST
    global MPG_LIST, MPG_COUNT, SPG_LIST
    global MPE, MPG, ALTITUDE, AZIMUTE
    global MDE_LIST, MDG_LIST 
    global GPHG_ATT, GPHE_ATT
    if COMP.is_open: 
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
                        #MDE_LIST.append( dt.timestamp( dt.utcnow() ) )
                        MDE_LIST.append( MPE_COUNT ) 
                        MPE_COUNT += 1
                        # ELEVAÇÂO
                        if MPE_LIST:
                            while len(MPE_LIST) > 1000:
                                MPE_LIST.pop(0)
                                MDE_LIST.pop(0)
                            dpg.configure_item( 45_1_1, x = MDE_LIST, y = MPE_LIST )
                            dpg.configure_item( 45_1_2, x = MDE_LIST, y = SPE_LIST )
                            dpg.set_axis_limits( 'x_axis_alt', ymin = MDE_LIST[0], ymax = MDE_LIST[-1])
                    except struct.error as e:
                        print( e )

                elif OP == ord('g'):
                    try: 
                        value = COMP.BUFFER_IN[-1][ind+2:ind+6]
                        value = struct.unpack('f', value )[0]
                        dpg.set_value(MPG, value) 
                        MPG_LIST.append( dpg.get_value(MPG) )
                        SPG_LIST.append( dpg.get_value(AZIMUTE) )
                        #MDG_LIST.append( dt.timestamp( dt.utcnow() ) )
                        MDG_LIST.append( MPG_COUNT ) 
                        MPG_COUNT += 1
                        if MPG_LIST:
                            while len(MPG_LIST) > 1000:
                                MPG_LIST.pop(0)
                                MDG_LIST.pop(0)
                            dpg.configure_item( 44_1_1, x = MDG_LIST, y = MPG_LIST )
                            dpg.configure_item( 44_1_2, x = MDG_LIST, y = SPG_LIST )
                            dpg.set_axis_limits( 'x_axis_azi', ymin = MDG_LIST[0], ymax = MDG_LIST[-1])
                    except struct.error as e:
                        print( e )
                
                elif OP == ord('D'):
                    NBYTES = COMP.BUFFER_IN[-1][ind+2]
                    msg = COMP.BUFFER_IN[-1][ind+3:]
                    if NBYTES < 70:
                        COMP.read()
                        msg += COMP.BUFFER_IN[-1]
                        if '\\\\'.encode() not in msg: 
                            serial_write_message(None, None, 'INITP' )
                            break
                    if NBYTES == len(msg)-2:
                        #try:
                        dpg.set_value( 54300, struct.unpack( 'f', msg[  : 4] )[0]                          )
                        dpg.set_value( 54301, struct.unpack( 'f', msg[ 4: 8] )[0]                          )
                        dpg.set_value( 54302, struct.unpack( 'f', msg[ 8:12] )[0]                          )
                        dpg.set_value( 54303, float( int.from_bytes( msg[12:23], 'little', signed = False ) ) )
                        dpg.set_value( 54304, struct.unpack( 'f', msg[23:27] )[0]                          )
                        dpg.set_value( 54305, struct.unpack( 'f', msg[27:31] )[0]                          )
                        dpg.set_value( 54306, struct.unpack( 'f', msg[31:35] )[0]                          )
                        dpg.set_value( 54307, struct.unpack( 'f', msg[35:39] )[0]                          )
                        dpg.set_value( 54308, struct.unpack( 'f', msg[39:43] )[0]                          )
                        dpg.set_value( 54309, struct.unpack( 'f', msg[43:47] )[0]                          )
                        dpg.set_value( 54310, float( int.from_bytes( msg[47:58], 'little', signed = False ) ) )
                        dpg.set_value( 54311, struct.unpack( 'f', msg[58:62] )[0]                          )
                        dpg.set_value( 54312, struct.unpack( 'f', msg[62:66] )[0]                          )
                        dpg.set_value( 54313, struct.unpack( 'f', msg[66:70] )[0]                          )
                        
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

def serial_atualize_actuator_cmd( ): 
    global COMP 
    if COMP.is_open:    
        if COMP.read():
            serial_capture_frames() 
            MSG  = ''
            for n, row in enumerate( COMP.BUFFER_IN ):
                MSG += '[{}] '.format( COMP.COUNTER_IN + n - len(COMP.BUFFER_IN) )
                if dpg.get_value( CMD_MODE ) == 'ASCII': 
                    for collum in row: 
                        MSG += chr(168) if collum < 32 or collum == 127 else chr(collum)
                    MSG += '\n'
                elif dpg.get_value( CMD_MODE ) == 'HEX': 
                    for collum in row: 
                        if collum == 10: MSG += '\n'
                        else:            MSG += str(hex(168)) if collum < 32 or collum == 127 else str(hex(collum)) + ' '
                    MSG += '\n'
            dpg.set_value( 46_2_1_1, MSG )
            dpg.set_value( 53_1, MSG )
    else:
        dpg.set_value( 46_2_1_1, "DESCONECTADO" ) 

def serial_refresh( sender, data, user ): 
    global COMP 
    dpg.configure_item( 42_1_1, label = 'Procurando' ) 
    dpg.configure_item( 42_1  , items = COMP.get_serial_ports( 20 ) )
    dpg.configure_item( 42_1_1, label = 'Refresh' )

def serial_try_to_connect( sender, data, user ): 
    global COMP 
    COMP = UART_COM( dpg.get_value(SERIAL_PORT), baudrate = int(dpg.get_value(SERIAL_BAUDRATE)), timeout = dpg.get_value(SERIAL_TIMEOUT) )
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

def serial_write_message(sender, data, user ):
    global COMP
    ## Control Params 
    if user   == 'INITCM':
        user   = 'INITCM'.encode()
        user  += struct.pack('ff', dpg.get_value(46_1_1_4_3)[0], dpg.get_value(46_1_1_4_3)[1] )
    if user   == 'INITCP':
        user   = 'INITCM'.encode()
        user  += struct.pack('ff', dpg.get_value(AZIMUTE), dpg.get_value(ZENITE) )
        print(dpg.get_value(AZIMUTE), dpg.get_value(ZENITE))
        
    elif user == 'INITCm':
        user   = 'INITCm'.encode()
        user  += 'G'.encode() if dpg.get_value(46_1_1_4_5) == 'Gir' else 'E'.encode()
        user  += struct.pack('f', dpg.get_value(46_1_1_4_4))
    elif user == 'INITCp':
        user   =  'INITC'.encode()
        user  +=  'G'.encode() if dpg.get_value(46_1_1_4_21) == 'Gir' else 'E'.encode()
        user  +=  dpg.get_value(46_1_1_4_22)
        user  +=  struct.pack( 'f', dpg.get_value(46_1_1_4_1) )

    ## Datetime Params 
    elif user == "INITH": 
        user  = "INITH".encode() 
        date  = dpg.get_value( 46_1_1_1 )
        hour  = dpg.get_value( 46_1_1_2 ) 
        if date[0] > 31:    raise 'days out of range'
        if date[1] > 12:    raise 'months out of range'       
        if hour[0] > 60:    raise 'seconds out of range'
        if hour[1] > 60:    raise 'minutes out of range'
        if hour[2] > 23:    raise 'hours out of range'
        if date[2] > 2000:  date[2] -= 2000
        user += struct.pack( 'bbb', date[0], date[1], date[2])
        user += struct.pack( 'bbb', hour[0], hour[1], hour[2])

    if user == 'manual_send':
        user = dpg.get_value(46_2_2_2)

    try: 
        if type( user ) == bytes: COMP.write( user )
        elif type( user ) == str: COMP.write( user.encode() )
    except SerialException as e:
        print( e )

    print( "Dentro de connections.serial: Sender {}  data {}  user {}".format(sender, data, user ))


def serial_request_diagnosis( sender, data, user ):
    global COMP
    if COMP.is_open:
        COMP.write( 'INITP' )     
    else: 
        print( "COMP NOT OPEN ")

def serial_close_connection(sender, data, user): 
    global COMP
    COMP.close()
    serial_verify_connection() 

def serial_print_comp():
    print( 'serial: ', COMP )

def serial_comp_is_open():
    return COMP.is_open 