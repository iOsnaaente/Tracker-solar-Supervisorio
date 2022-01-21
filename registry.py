import dearpygui.dearpygui  as dpg 
import datetime as dt 
import math 
import os 

from utils.Model     import SunPosition
from utils.UART_comm import UART_COM 

# SERIAL 
COMP = UART_COM( "" )

# GRAPHS 
MPE_LIST  = []
MDE_LIST  = [] 
SPE_LIST  = []
MPE_COUNT = 0
GPHE_ATT  = False 

MPG_LIST  = []
MDG_LIST  = [] 
SPG_LIST  = []
MPG_COUNT = 0
GPHG_ATT  = False

DOMINIO  = [] 

MSG_INIT    = [ ord(i) for i in 'init' ]
MSG_COUNT   = 0 

DOM         = [ 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro' ]

PATH        = os.path.dirname( __file__ )
PATH_IMG    = PATH + 'img\\'


COLOR = {
    "black"     : lambda alfa : [    0,    0,    0, alfa ],
    "red"       : lambda alfa : [  255,    0,    0, alfa ],
    "yellow"    : lambda alfa : [  255,  255,    0, alfa ],
    "green"     : lambda alfa : [    0,  255,    0, alfa ],
    "ciano"     : lambda alfa : [    0,  255,  255, alfa ],
    "blue"      : lambda alfa : [    0,    0,  255, alfa ],
    "magenta"   : lambda alfa : [  255,    0,  255, alfa ],
    "white"     : lambda alfa : [  255,  255,  255, alfa ],
    'gray'      : lambda alfa : [  155,  155,  155, alfa ],
    'orange'    : lambda alfa : [  255,   69,    0, alfa ],

    'on_color'  : lambda alfa : [ 0x3c, 0xb3, 0x71, alfa ],
    'on_hover'  : lambda alfa : [ 0x92, 0xe0, 0x92, alfa ],
    'on_click'  : lambda alfa : [ 0x20, 0xb2, 0xaa, alfa ],
    'off_color' : lambda alfa : [ 0xff, 0x45, 0x00, alfa ],
    'off_hover' : lambda alfa : [ 0xf0, 0x80, 0x80, alfa ],
    'off_click' : lambda alfa : [ 0x8b, 0x45, 0x13, alfa ],


    }

windows = {
            "Inicio"             : [  ],
            "Visualizacao geral" : [  ],
            "Posicao do sol"     : [  ],
            "Atuadores"          : [  ],
            "Atuacao da base"    : [  ],
            "Atuacao da elevacao": [  ],
            "Sensores"           : [  ],
            "Rednode comunicacao": [  ],
            "Configuracoes"      : [  ],
            'Sair'               : [  ],
            }


with dpg.value_registry( ) as registries:
    # POSIÇÃO GEOGRÁFICA CONSTANTE - PEGAR DE UM DOCUMENTO
    LATITUDE     = dpg.add_float_value ( parent = registries, default_value = -29.16530765942215      , tag = 99_99_1 ) 
    LONGITUDE    = dpg.add_float_value ( parent = registries, default_value = -54.89831672609559      , tag = 99_99_2 )
    ALTITUDE     = dpg.add_float_value ( parent = registries, default_value = 425                     , tag = 99_99_3 )
    UTC_HOUR     = dpg.add_int_value   ( parent = registries, default_value = -3                      , tag = 99_99_4 )
    
    # DADOS DOS MOTORES 
    #   GIRO 
    MPG              = dpg.add_float_value ( parent = registries, default_value = 425                 , tag = 99_99_5 )
    MG_VELANG        = dpg.add_float_value ( parent = registries, default_value = 1.0                 , tag = 99_99_6 )  
    MG_RESOLUCAO     = dpg.add_float_value ( parent = registries, default_value = 0.0                 , tag = 99_99_7 )
    MG_STEPS         = dpg.add_float_value ( parent = registries, default_value = 0.0                 , tag = 99_99_8 )
    MG_USTEP         = dpg.add_string_value( parent = registries, default_value = '1/16'              , tag = 99_99_9 )
    MG_ONOFF         = dpg.add_bool_value  ( parent = registries, default_value = False               , tag = 99_99_10 ) 
    #   ELEVAÇÃO
    MPE              = dpg.add_float_value ( parent = registries, default_value = 100                 , tag = 99_99_11 )
    ME_VELANG        = dpg.add_float_value ( parent = registries, default_value = 1.0                 , tag = 99_99_12 )  
    ME_RESOLUCAO     = dpg.add_float_value ( parent = registries, default_value = 0.0                 , tag = 99_99_13 )
    ME_STEPS         = dpg.add_float_value ( parent = registries, default_value = 0.0                 , tag = 99_99_14 )
    ME_USTEP         = dpg.add_string_value( parent = registries, default_value = '1/16'              , tag = 99_99_15 ) 
    ME_ONOFF         = dpg.add_bool_value  ( parent = registries, default_value = False               , tag = 99_99_16 ) 

    # DADOS DOS SENSORES 
    #   GIRO
    SPG              = dpg.add_float_value ( parent = registries, default_value = 180                 , tag = 99_99_17 )
    SDG              = dpg.add_int_value   ( parent = registries, default_value = 1                   , tag = 99_99_18 )
    #   ELEVAÇÃO
    SPE              = dpg.add_float_value ( parent = registries, default_value = 45                  , tag = 99_99_19 )
    SDE              = dpg.add_int_value   ( parent = registries, default_value = 1                   , tag = 99_99_20 )

    # DADOS TEMPORAIS 
    YEAR             = dpg.add_int_value    ( parent = registries, default_value = 1                  , tag = 99_99_21 )  
    MONTH            = dpg.add_int_value    ( parent = registries, default_value = 1                  , tag = 99_99_22 )  
    DAY              = dpg.add_int_value    ( parent = registries, default_value = 1                  , tag = 99_99_23 )  
    HOUR             = dpg.add_int_value    ( parent = registries, default_value = 1                  , tag = 99_99_24 )
    MINUTE           = dpg.add_int_value    ( parent = registries, default_value = 1                  , tag = 99_99_25 )  
    SECOND           = dpg.add_int_value    ( parent = registries, default_value = 1                  , tag = 99_99_26 )  
    TOT_SECONDS      = dpg.add_int_value    ( parent = registries, default_value = 1                  , tag = 99_99_27 )  
    JULIANSDAY       = dpg.add_int_value    ( parent = registries, default_value = 1                  , tag = 99_99_28 )  
    
    # DADOS DE MEDIÇÃO E MONITORAMENTO DO SOL 
    AZIMUTE          = dpg.add_float_value ( parent = registries, default_value = 0.0                 , tag = 99_99_29 )
    ZENITE           = dpg.add_float_value ( parent = registries, default_value = 0.0                 , tag = 99_99_30 )
    H_SUNRISE        = dpg.add_float4_value ( parent = registries, default_value = [0,0,0,0]          , tag = 99_99_31 )  
    H_CULMINANT      = dpg.add_float4_value ( parent = registries, default_value = [0,0,0,0]          , tag = 99_99_32 )  
    H_SUNSET         = dpg.add_float4_value ( parent = registries, default_value = [0,0,0,0]          , tag = 99_99_33 )  
    HT_DAYLIGHT      = dpg.add_float4_value ( parent = registries, default_value = [0,0,0,0]          , tag = 99_99_34 )  
    SR_AZIMUTE       = dpg.add_float_value  ( parent = registries, default_value = 0.0                , tag = 99_99_35 )  
    SS_AZIMUTE       = dpg.add_float_value  ( parent = registries, default_value = 0.0                , tag = 99_99_36 )  
    SC_ALTITUDE      = dpg.add_float_value  ( parent = registries, default_value = 0.0                , tag = 99_99_37 )  
    
    # SERIAL CONFIGURATIONS 
    SERIAL_CONNECTED = dpg.add_bool_value  ( parent = registries, default_value = False               , tag = 99_99_38 ) 
    SERIAL_PORT      = dpg.add_string_value( parent = registries, default_value = 'COM12'             , tag = 99_99_39 )
    SERIAL_BAUDRATE  = dpg.add_string_value( parent = registries, default_value = '115200'            , tag = 99_99_40 )
    SERIAL_TIMEOUT   = dpg.add_int_value   ( parent = registries, default_value = 1                   , tag = 99_99_41 )


    DAY2COMPUTE      = dpg.add_bool_value  ( parent = registries, default_value = False               , tag = 99_99_99_38 )
    TCP_CONNECTED    = dpg.add_bool_value  ( parent = registries, default_value = False               , tag = 99_99_99_39 ) 
    HORA_MANUAL      = dpg.add_bool_value  ( parent = registries, default_value = False               , tag = 99_99_99_41 )  
    
    # ATUADOR 
    CMD_MODE         = dpg.add_string_value( parent = registries, default_value = 'HEX'               , tag = 99_99_99_42 )


SUN_DATA = SunPosition( dpg.get_value(LATITUDE), dpg.get_value(LONGITUDE), dpg.get_value(ALTITUDE) )
SUN_DATA.update() 
dpg.set_value( SPE, math.degrees(SUN_DATA.alt) ) 
dpg.set_value( SPG, math.degrees(SUN_DATA.azi) ) 

date   = dt.datetime.utcnow()
dpg.set_value( YEAR  ,date.year   ) 
dpg.set_value( MONTH ,date.month  )
dpg.set_value( DAY   ,date.day    )
dpg.set_value( HOUR  ,date.hour   )  
dpg.set_value( MINUTE,date.minute ) 
dpg.set_value( SECOND,date.second ) 