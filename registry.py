import dearpygui.dearpygui  as dpg 
import os 

from utils.Model            import SunPosition
from serial                 import Serial

COMP        = Serial() 
DOM         = [ 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro' ]
PATH        = os.path.dirname( __file__ )
PATH_IMG    = PATH + '\\utils\\img\\'

color = {
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

def add_image_loaded( img_path ):
    w, h, c, d = dpg.load_image( img_path )
    with dpg.texture_registry() as reg_id : 
        return dpg.add_static_texture( w, h, d, parent = reg_id )

def change_font():
    with dpg.font_registry( id = 'fonts' ):
            dpg.add_font( PATH + '\\fonts\\verdana.ttf', 14, default_font=True, parent='fonts')

with dpg.value_registry( id = 99_99_0 ) as registries:
    LATITUDE     = dpg.add_string_value( parent = registries, default_value = '-29.16530765942215', id = 99_99_1 ) 
    LONGITUDE    = dpg.add_string_value( parent = registries, default_value = '-54.89831672609559', id = 99_99_2 )
    
    MG_uStep     = dpg.add_string_value( parent = registries, default_value = '1/16'              , id = 99_99_11 )
    ME_uStep     = dpg.add_string_value( parent = registries, default_value = '1/16'              , id = 99_99_14 ) 
    
    ALTITUDE     = dpg.add_float_value   ( parent = registries, default_value = 425                 , id = 99_99_3 )
    UTC_HOUR     = dpg.add_int_value   ( parent = registries, default_value = -3                  , id = 99_99_4 )
    
    DAY_2Compute = dpg.add_bool_value  ( parent = registries, default_value = False               , id = 99_99_5 )
    
    CONNECTED    = dpg.add_bool_value  ( parent = registries, default_value = False               , id = 99_99_6_0 ) 
    TCP_CONNECTED= dpg.add_bool_value  ( parent = registries, default_value = False               , id = 99_99_6_1 ) 
    
    M1_ONorOFF   = dpg.add_bool_value  ( parent = registries, default_value = False               , id = 99_99_7 ) 
    M2_ONorOFF   = dpg.add_bool_value  ( parent = registries, default_value = False               , id = 99_99_8 ) 
    
    MG_Resolucao = dpg.add_float_value ( parent = registries, default_value = 0.0                 , id = 99_99_9 )
    MG_Steps     = dpg.add_float_value ( parent = registries, default_value = 0.0                 , id = 99_99_10 )
    ME_Resolucao = dpg.add_float_value ( parent = registries, default_value = 0.0                 , id = 99_99_12 )
    ME_Steps     = dpg.add_float_value ( parent = registries, default_value = 0.0                 , id = 99_99_13 )
    
    MG_Angle     = dpg.add_float_value ( parent = registries, default_value = 0.0                 , id = 99_99_15 )
    ME_Angle     = dpg.add_float_value ( parent = registries, default_value = 0.0                 , id = 99_99_16 )
    
    MGSR_Angle   = dpg.add_float_value ( parent = registries, default_value = 0.0                 , id = 99_99_17 )
    MESR_Angle   = dpg.add_float_value ( parent = registries, default_value = 0.0                 , id = 99_99_18 )
    VelAng_M1    = dpg.add_float_value ( parent = registries, default_value = 1.0                 , id = 99_99_19 )  
    VelAng_M2    = dpg.add_float_value ( parent = registries, default_value = 1.0                 , id = 99_99_20 )  
    
    sundaylight  = dpg.add_float4_value ( parent = registries, default_value = [0,0,0,0]          , id = 99_99_21 )  
    sunrise      = dpg.add_float4_value ( parent = registries, default_value = [0,0,0,0]          , id = 99_99_22 )  
    sunset       = dpg.add_float4_value ( parent = registries, default_value = [0,0,0,0]          , id = 99_99_23 )  
    sunculminant = dpg.add_float4_value ( parent = registries, default_value = [0,0,0,0]          , id = 99_99_24 )  
    
    day          = dpg.add_int_value    ( parent = registries, default_value = 1                  , id = 99_99_25 )  
    month        = dpg.add_int_value    ( parent = registries, default_value = 1                  , id = 99_99_26 )  
    year         = dpg.add_int_value    ( parent = registries, default_value = 1                  , id = 99_99_27 )  
    second       = dpg.add_int_value    ( parent = registries, default_value = 1                  , id = 99_99_28 )  
    minute       = dpg.add_int_value    ( parent = registries, default_value = 1                  , id = 99_99_29 )  
    hour         = dpg.add_int_value    ( parent = registries, default_value = 1                  , id = 99_99_30 )

    total_seconds= dpg.add_int_value    ( parent = registries, default_value = 1                  , id = 99_99_31 )  
    dia_juliano  = dpg.add_int_value    ( parent = registries, default_value = 1                  , id = 99_99_32 )  
    
    hora_manual  = dpg.add_bool_value   ( parent = registries, default_value = False              , id = 99_99_33 )  
    
    sunrise_azi  = dpg.add_float_value  ( parent = registries, default_value = 0.0                , id = 99_99_34 )  
    sunset_azi   = dpg.add_float_value  ( parent = registries, default_value = 0.0                , id = 99_99_35 )  
    culminant_alt= dpg.add_float_value  ( parent = registries, default_value = 0.0                , id = 99_99_36 )  
    
    azi          = dpg.add_float_value ( parent = registries, default_value = 0.0                 , id = 99_99_37 )
    alt          = dpg.add_float_value ( parent = registries, default_value = 0.0                 , id = 99_99_38 )
     
sun_data     = SunPosition( dpg.get_value(LATITUDE), dpg.get_value(LONGITUDE), dpg.get_value(ALTITUDE) )
sun_data.update() 
