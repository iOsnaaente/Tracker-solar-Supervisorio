import Tracker.Serial.myRegisters as rg

# CONFIGURAÇÕES DE RASTREAMENTO 
LATITUDE            = -29.16530765942215
LONGITUDE           = -54.89831672609559 
TEMPERATURE         =  298.5
PRESSURE            =  101.0

# MODBUS HOLDING REGISTER ADDRESSES
HR_STATE            = 0x00

HR_AZIMUTE          = 0x01
HR_ALTITUDE         = 0x03

HR_PV_MOTOR_GIR     = 0x05
HR_PV_MOTOR_ELE     = 0x07

HR_KP_GIR           = 0x09
HR_KI_GIR           = 0x0B
HR_KD_GIR           = 0x0D
HR_KP_ELE           = 0x0F
HR_KI_ELE           = 0x11
HR_KD_ELE           = 0x13

HR_GIR_STEP         = 0x15
HR_GIR_USTEP        = 0x17
HR_GIR_RATIO        = 0x19
HR_ELE_STEP         = 0x1B
HR_ELE_USTEP        = 0x1D
HR_ELE_RATIO        = 0x1F

HR_YEAR             = 0x21
HR_MONTH            = 0x22
HR_DAY              = 0x23
HR_HOUR             = 0x24
HR_MINUTE           = 0x25
HR_SECOND           = 0x26

HR_POS_MGIR         = 0x27
HR_POS_MELE         = 0x29

HR_LATITUDE         = 0x31 
HR_LONGITUDE        = 0x33
HR_TEMPERATURE      = 0x35  
HR_PRESSURE         = 0x37     
HR_ALTURA           = 0x39

# MODBUS INPUTS REGISTER ADDRESSES
INPUT_SENS_GIR      = 0x00
INPUT_SENS_ELE      = 0x02
INPUT_AZIMUTE       = 0x04
INPUT_ALTITUDE      = 0x06
INPUT_YEAR          = 0x07
INPUT_MONTH         = 0x08
INPUT_DAY           = 0x09
INPUT_HOUR          = 0x0A
INPUT_MINUTE        = 0x0B
INPUT_SECOND        = 0x0C
INPUT_SENS_CONF_GIR = 0x0D
INPUT_SENS_CONF_ELE = 0x0F

# MODBUS COILS REGISTER ADDRESSES
COIL_POWER          = 0X00
COIL_LED1_BLUE      = 0x01
COIL_LED1_RED       = 0x02
COIL_LED2_BLUE      = 0x03
COIL_LED2_RED       = 0x04
COIL_PRINT          = 0x05 
COIL_DATETIME_SYNC  = 0x06
COIL_FORCE_DATETIME = 0x07

# MODBUS DISCRETES REGISTER ADDRESSES
DISCRETE_POWERC_L    = 0x00
DISCRETE_WAITING     = 0x01
DISCRETE_TIME_STATUS = 0x02 
DISCRETE_LEVER1_L    = 0x03
DISCRETE_LEVER1_R    = 0x04
DISCRETE_LEVER2_L    = 0x05
DISCRETE_LEVER2_R    = 0x06


# STATES 
FAIL_STATE     = 0
AUTOMATIC      = 1
MANUAL         = 2
REMOTE         = 3
DEMO           = 4
IDLE           = 5
RESET          = 6
PRE_RETURNING  = 7
RETURNING      = 8
SLEEPING       = 9 


# DATA E HORA 
ANB = lambda year : True if (year%100 != 0 and year%4 == 0) or (year%100 == 0 and year%400 == 0) else False
DOM = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
UTC = -3 


## COMO AS LISTAS DE REGS E UART.REGS APONTAM PARA O MESMO ENDEREÇO,
## É INDIFERENTE O USO DA LISTA DENTRO DE UART.REGS.STACK OU O PRÓPRIO REGS.STACK 

# MODBUS REGISTER ARRAYS 
INPUTS    = rg.Registers( 0x0F, int )
# | 0x00 |  0x01 | 0x02 | 0x03 |   0x04 |   0x05 |     0x06 |          0x08 |     0x09 |          0x0B | 
# | YEAR | MONTH |  DAY | HOUR | MINUTE | SECOND | SENS_GIR | SENS_CONF_GIR | SENS_ELE | SENS_CONF_ELE |

HOLDINGS  = rg.Registers( 0x3F, int )
#         0x00 |   0x02 |   0x03 |   0x04 |    0x05 |         0x07 |   0x09 |   0x0A |   0x0B |     0x0C |  0x0E |
# PV_MOTOR_GIR | KP_GIR | KI_GIR | KD_GIR | AZIMUTE | PV_MOTOR_ELE | KP_ELE | KI_ELE | KD_ELE | ALTITUDE | STATE |           


DISCRETES = rg.Registers( 0x08, bool )
# |    0x00 |    0x01 |   0x02  |    0x03 |
# | LEVER1L | LEVER1R | LEVER2L | LEVER2R | 

COILS     = rg.Registers( 0x08, bool ) 
# |     0x00 |     0x01 |     0x02 |    0x03 |    0x04 | 
# | LED1BLUE | LED1RED  | LED2BLUE | LED2RED | POWERCL | 


HOLDINGS.set_regs_float( HR_LATITUDE, [ -29.16530765942215, -54.89831672609559 ,  298.5,  101.0 ] )


# LOCALIZATION LIST - GET_SUN_POSITION
LOCALIZATION = HOLDINGS.get_regs_float( HR_LATITUDE, 4 )
