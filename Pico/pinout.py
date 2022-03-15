# TOP VIEW  -  VARIÁVEIS USADAS NAS GPIOs DO RASPICO 

# LEFT SIDE 
#----------------
STEP_GIR    = 0 
STEP_ELE    = 1 
STEP_GEN    = 2

DIR_GIR     = 3
DIR_ELE     = 4
DIR_GEN     = 5 

BUTTON_GP   = 6 
BUTTON_GM   = 7

BUTTON_EP   = 8
BUTTON_EM   = 9

LED1_RED    = 10
LED1_BLUE   = 11
LED2_RED    = 12
LED2_BLUE   = 13

ENABLE_MTS  = 14

POWER       = 15
#-----------------

# RIGTH SIDE
#----------------
SDA_DS      = 16 
SCL_DS      = 17

SDA_AS      = 18
SCL_AS      = 19 

UART_TX     = 20 
UART_RX     = 21

LED_BUILTIN = 25

NONE_22     = 22 
NONE_23     = 23 
NONE_24     = 24 
NONE_26     = 26 
NONE_27     = 27 
NONE_28     = 28 


#-----------------

import machine

LED1_RED_PIN  = machine.Pin( LED1_RED , machine.Pin.OUT)
LED2_RED_PIN  = machine.Pin( LED2_RED , machine.Pin.OUT)
LED1_BLUE_PIN = machine.Pin( LED1_BLUE, machine.Pin.OUT)
LED2_BLUE_PIN = machine.Pin( LED2_BLUE, machine.Pin.OUT)


