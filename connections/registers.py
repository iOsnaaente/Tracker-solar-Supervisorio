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

# OPERATION STATES 
PICO_FAIL_STATE      = 0x00
PICO_AUTOMATIC       = 0x01
PICO_MANUAL          = 0x02
PICO_REMOTE          = 0x03
PICO_DEMO            = 0x04
PICO_IDLE            = 0x05
PICO_RESET           = 0x06
PICO_PRE_RETURNING   = 0x07
PICO_RETURNING       = 0x08
PICO_SLEEPING        = 0x09 

from connections.minimalModbus import Instrument
from connections.minimalModbus import MODE_RTU 

COM = Instrument( 'COM12', 0x12, baudrate = 115200, mode = MODE_RTU, debug = True )
COM.write_bit( COIL_POWER, True )
