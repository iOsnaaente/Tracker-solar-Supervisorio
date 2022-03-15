# importações de repositórios locais
from   Tracker.Time.Timanager       import FAKE_TIME
import Tracker.Sun.mySunposition    as sun 
import Tracker.Files.fileStatements as fs
import Tracker.Motor.myStepmotor    as stp
import Tracker.Time.myDatetime      as dt
import Tracker.Sensor.myAS5600      as sn
import Tracker.Serial.myModbus      as mmb
import Tracker.Controle.myPID       as mp
import Tracker.Manual.myLevers      as ml

# Variáveis constantes ou globais do PICO 
from constants import *

# Pinout das GPIOs do PICO 
from pinout    import *

# importação de repositórios padrões do sistema PICO 
import machine 
import time
import sys 


# Inicio da criação do objeto motores. Responsável pelo controle 
# de posição dos motores e controle automático quando os sensores
# falharem, por isso, as configurações de STEP, uSTEP e Ratio devem
# ser configuradas de acordo para evitar problemas de FAIL STATE 
Motors = stp.Motors( STEP_GIR, DIR_GIR, STEP_ELE, DIR_ELE, ENABLE_MTS, POWER      )
Motors.configure   ( Motors.GIR, pos = 0.0, step = 1.8, micro_step = 8, ratio = 1 )
Motors.configure   ( Motors.ELE, pos = 0.0, step = 1.8, micro_step = 8, ratio = 1 )
Motors.set_torque  ( False )

HOLDINGS.set_regs_float( HR_GIR_STEP, [ 1.8, 8, 1 ] ) 
HOLDINGS.set_regs_float( HR_ELE_STEP, [ 1.8, 8, 1 ] )


# Inicializando o protocolo de comunicação Modbus
Modbus = mmb.myModbusCommunication( 1, 115200, 0x12, tx  = machine.Pin(UART_TX) , rx  = machine.Pin(UART_RX), parity = 'even' )
print( 'Utilizando modo de comunicação Modbus:  ')
print( Modbus.myUART ,'\nSLAVE ADDRESS: ', Modbus.ADDR_SLAVE, "\nFunction code available: ", Modbus.FUNCTIONS_CODE_AVAILABLE )

# CADASTRA OS REGISTRADORES
Modbus.set_registers( DISCRETES, COILS, INPUTS, HOLDINGS )
print( 'Registradores cadastrados\n' )
print( 'Holdings  - Type: {} Len: {} {}'.format( Modbus.HOLDINGS.TYPE , Modbus.HOLDINGS.REGS , Modbus.HOLDINGS.STACK  )  )
print( 'Inputs    - Type: {} Len: {} {}'.format( Modbus.INPUTS.TYPE   , Modbus.INPUTS.REGS   , Modbus.INPUTS.STACK    )  )
print( 'Coils     - Type: {} Len: {} {}'.format( Modbus.COILS.TYPE    , Modbus.COILS.REGS    , Modbus.COILS.STACK     )  )
print( 'Discretes - Type: {} Len: {} {}'.format( Modbus.DISCRETES.TYPE, Modbus.DISCRETES.REGS, Modbus.DISCRETES.STACK )  , end = '\n\n' )
     

# Criação dos barramentos i2c usados para os sensores AS5600 e DS3231 
isc0   = machine.I2C ( 0, freq = 100000, sda = machine.Pin( SDA_DS  ), scl = machine.Pin( SCL_DS  ) ) 
isc1   = machine.I2C ( 1, freq = 100000, sda = machine.Pin( SDA_AS  ), scl = machine.Pin( SCL_AS  ) )
print( "Barramento I2C0: ", isc0, "Endereços no barramento: ", isc0.scan() )
print( 'Barramento I2C1: {} Endereços no barramento: {}\n'.format(isc1, isc1.scan()) ) 


# Criação do objeto TIME que esta atrelado ao relógio RTC
# Responsável pela administração do tempo e temporizadores 
# de alarmes para Wake-up 
try:
    Time = dt.Datetime( isc0  )
    INPUTS.set_regs      ( INPUT_YEAR        , Time.DS.get_datetime()[:-1]      )
    HOLDINGS.set_regs    ( HR_YEAR           , Time.RTC.get_datetime()          )
    COILS.set_reg_bool   ( COIL_DATETIME_SYNC, Time.SYNC                        )
    
    TIME     , TIME_STATUS = Time.get_datetime( )
    fake_time              = FAKE_TIME        ( LOCALIZATION, INPUTS.get_regs( INPUT_YEAR, 6 ) )
    AZIMUTE  , ALTITUDE    = sun.compute      ( LOCALIZATION,  TIME )
    
    print( "DS3231 e Relógio RTC inicializados.\nHora registrada no DS3231 ( [yy/mm/dd - hh:mn:ss] {} - Sync: {}\n".format( INPUTS.get_regs( INPUT_YEAR, 6), COILS.get_reg_bool(COIL_DATETIME_SYNC) ) )
    
# Se o DS3231 não estiver de acordo, não tem como o Tracker
# entrar em operação e será obrigado a resetar 
except:
    print( "Relógio não inicializou, erro crítico.") 
    print( "Entrando em modo de reinicialização!\n") 
    machine.soft_reset() 
    

# INICIA OS LEVERS PARA CONTROLE MANUAL 
levers = ml.Lever_control( [BUTTON_GP, BUTTON_GM], [BUTTON_EP, BUTTON_EM], [LED1_RED, LED1_BLUE] )
print( "Levers inicializados (Modo Manual)\n")


# Tenta instanciar os sensores de posição AS5600 
# Caso os sensores estejam vivos, seta-se as configurações de 
# incialização ( escrita de 0 nos endereços [0:11] )
# Caso os sensores não estejam funcionando, deve-se colocar 
# o Tracker em modo FAIL-STATE 
ASGIR  = sn.AS5600 ( isc0, startAngle =   0 )
ASELE  = sn.AS5600 ( isc1, startAngle = 331 )


if (ASGIR.set_config ( ) == True) and ( ASELE.set_config() == True ) :
    SENS_GIR = ASGIR.degAngle()
    INPUTS.set_reg_float(  INPUT_SENS_GIR , SENS_GIR if SENS_GIR != False else 0.0  )
    INPUTS.set_reg_float  ( INPUT_SENS_CONF_GIR, ASGIR.get_config() )
    
    SENS_ELE = ASELE.degAngle()
    INPUTS.set_reg_float  ( INPUT_SENS_ELE , SENS_ELE if SENS_ELE != False else 0.0 )
    INPUTS.set_reg_float  ( INPUT_SENS_CONF_ELE, ASELE.get_config() )
    
    # Setar posição dos motores de passo para FAIL STATE
    Motors.GIR.position = SENS_GIR if SENS_GIR != False else 0.0  
    Motors.ELE.position = SENS_ELE if SENS_ELE != False else 0.0
    
    HOLDINGS.set_reg_float( HR_POS_MGIR, Motors.GIR.position ) 
    HOLDINGS.set_reg_float( HR_POS_MELE, Motors.ELE.position )
    
    HOLDINGS.set_reg      ( HR_STATE, AUTOMATIC )
    
    print( "Sensores AS5600 de Giro e Elevação inicializados e configurados. Prontos para uso.")

else:
    HOLDINGS.set_reg( HR_STATE, FAIL_STATE )
    print( 'Erro na inicialização do AS5600 de Giro. Verificar barramento I2C!')
    

# Cada motor possui um PID para correção da posição
# Instanciamento dos PIDs de cada motor
PID_GIR = mp.PID( PV = 100, Kp = 0.55, Kd = 0.25, Ki = 0.15 )
PID_ELE = mp.PID( PV = 100, Kp = 0.55, Kd = 0.25, Ki = 0.15 )

# Atualizaão do angulo para calculo de correção. Há diferenças 
# entre a atualização e computação dos angulos de correção
PID_GIR.att( INPUTS.get_reg_float( INPUT_SENS_GIR ) )
PID_ELE.att( INPUTS.get_reg_float( INPUT_SENS_ELE ) )

HOLDINGS.set_regs_float( HR_KP_GIR, [ PID_GIR.Kp, PID_GIR.Ki, PID_GIR.Kd] ) 
HOLDINGS.set_regs_float( HR_KP_ELE, [ PID_ELE.Kp, PID_ELE.Ki, PID_ELE.Kd] )

print( "PID do motor de GIR configurado: Kd Ki Kp: {} {} {} - PV_gir: {}  ".format( PID_GIR.Kd, PID_GIR.Ki, PID_GIR.Kp, PID_GIR.PV ) )
print( "PID do motor de ELE configurado: Kd Ki Kp: {} {} {} - PV_ele: {}\n".format( PID_ELE.Kd, PID_ELE.Ki, PID_ELE.Kp, PID_ELE.PV ) )



# AO CONTRARIO, TODA VEZ QUE FOR PRECISO USAR OS VALORES
# DE REGISTRADORES, DEVE-SE PEGAR ESSES VALORES  
def update_configurations():
    # HOLDINGS
    # Set the RTC datetime 
    y,m,d,h,n,s = HOLDINGS.get_regs( HR_YEAR, 6 ) 
    Time.set_RTC_datetime( y,m,d,h,n,s)
    
    if HOLDINGS.get_reg( HR_STATE ) == AUTOMATIC and COILS.get_reg_bool( COIL_FORCE_DATETIME) == True:
        Time.set_DS_datetime( y,m,d,h,n,s )
        COILS.set_reg_bool( COIL_DATETIME_SYNC, Time.SYNC )
        COILS.set_reg_bool( COIL_FORCE_DATETIME, False ) 
        
    # Set the motors configuration
    posGIR, posELE    = HOLDINGS.get_regs_float( HR_POS_MGIR, 2 )
    
    sGIR, usGIR, rGIR = HOLDINGS.get_regs_float( HR_GIR_STEP, 3 )
    Motors.configure( Motors.GIR, posGIR, sGIR, usGIR, rGIR )
    
    sELE, usELE, rELE = HOLDINGS.get_regs_float( HR_ELE_STEP, 3 )
    Motors.configure( Motors.ELE, posELE, sELE, usELE, rELE )
    
    # set the PID configs 
    PID_GIR.Kp = HOLDINGS.get_reg_float( HR_KP_GIR )
    PID_GIR.Kd = HOLDINGS.get_reg_float( HR_KD_GIR )
    PID_GIR.Ki = HOLDINGS.get_reg_float( HR_KI_GIR )
    PID_ELE.Kp = HOLDINGS.get_reg_float( HR_KP_ELE )
    PID_ELE.Kd = HOLDINGS.get_reg_float( HR_KD_ELE )
    PID_ELE.Ki = HOLDINGS.get_reg_float( HR_KI_ELE )
    
    
    #COILS
    LED1_BLUE_PIN.value( COILS.get_reg_bool( COIL_LED1_BLUE ) ) 
    LED1_RED_PIN.value ( COILS.get_reg_bool( COIL_LED1_RED  ) ) 
    LED2_BLUE_PIN.value( COILS.get_reg_bool( COIL_LED2_BLUE ) ) 
    LED2_RED_PIN.value ( COILS.get_reg_bool( COIL_LED2_RED  ) )
    Motors.set_torque  ( COILS.get_reg_bool( COIL_POWER     ) )


'''# --------------------------------------- INICIO DO LOOP ---------------------------------------------------------------------------#'''
last_print = time.ticks_ms()

POS_ELE = 0.0 
POS_GIR = 0.0 

LAST_STATE = 0

while True:
    time_spend_by_loop = time.ticks_ms()
    
    # Timmer via software para não usar interrupção de Timmer via hardware e conflitar com interrupção das mensagens Modbus 
    if (time.ticks_ms() - last_print > 2500) and (COILS.get_reg_bool( COIL_PRINT) == True ):
        LED1_RED_PIN(1)
        MSG  = 'STATE:\t\t{}\n'.format( HOLDINGS.get_reg( HR_STATE ) ) 
        MSG += 'Datetime:\t{}\n'.format( Time.get_datetime())
        MSG += "Giro:\n"
        MSG += "Kd Ki Kp:\t{}\t\t{}\t\t{}\n"   .format( PID_GIR.Kd, PID_GIR.Ki, PID_GIR.Kp )
        MSG += "Sens:\t\t{}\tReg. read:\t{}\n" .format( ASGIR.degAngle(), INPUTS.get_reg_float( INPUT_SENS_GIR ) ) 
        MSG += "PV(GIR):\t{}  \nError:\t\t{}\nPID:\t\t{}\n".format( PID_GIR.PV, PID_GIR.error_real, PID_GIR.compute( INPUTS.get_reg_float( INPUT_SENS_GIR ) ) )
        MSG += "\nElevação:\n"
        MSG += "Kd Ki Kp:\t{}\t\t{}\t\t{}\n"   .format( PID_ELE.Kd, PID_ELE.Ki, PID_ELE.Kp )
        MSG += "Sens:\t\t{}\tReg. read:\t{} \n".format( ASELE.degAngle(), INPUTS.get_reg_float(INPUT_SENS_ELE)  )
        MSG += "PV(ELE):\t{}  \nError:\t\t{}\nPID:\t\t{}\n".format( PID_ELE.PV, PID_ELE.error_real, PID_ELE.compute( INPUTS.get_reg_float( INPUT_SENS_ELE ) ) )
        MSG += "\nAZIMUTE: \t{}  \tReg. read:\t{}\n".format( AZIMUTE , INPUTS.get_reg_float( INPUT_AZIMUTE  ) )
        MSG += "ALTITUDE:\t{}  \tReg. read:\t{}\n".format( ALTITUDE, INPUTS.get_reg_float( INPUT_ALTITUDE ) )
        
        MSG += "FAIL STATE:\tGIR:{}\t\tELE:{}\n".format( HOLDINGS.get_reg_float( HR_POS_MGIR ), HOLDINGS.get_reg_float( HR_POS_MGIR ) ) 
        
        MSG += '\nHoldings  - Type: {} Len: {} {}\n'.format( HOLDINGS.TYPE , HOLDINGS.REGS , HOLDINGS.STACK  )   
        MSG += 'Inputs    - Type: {} Len: {} {}\n'.format( INPUTS.TYPE   , INPUTS.REGS   , INPUTS.STACK    )  
        MSG += 'Coils     - Type: {} Len: {} {}\n'.format( COILS.TYPE    , COILS.REGS    , COILS.STACK     )  
        MSG += 'Discretes - Type: {} Len: {} {}\n\n'.format( DISCRETES.TYPE, DISCRETES.REGS, DISCRETES.STACK )  
        sys.stdout.write( MSG )
        last_print = time.ticks_ms() 
        LED1_RED_PIN(0)
    

    # SETAR OS REGISTRADORES DE INPUTS
    SENS_GIR = ASGIR.degAngle()
    SENS_ELE = ASELE.degAngle()
    
    if SENS_ELE == False or SENS_GIR == False: 
        HOLDINGS.set_reg      ( HR_STATE        , FAIL_STATE )
        continue 
    else: 
        HOLDINGS.set_reg_float( HR_POS_MGIR, SENS_GIR )
        HOLDINGS.set_reg_float( HR_POS_MELE, SENS_ELE )
        INPUTS.set_reg_float  ( INPUT_SENS_GIR , SENS_GIR )
        INPUTS.set_reg_float  ( INPUT_SENS_ELE , SENS_ELE )

    # SETAR A DATA E HORA
    TIME, TIME_STATUS = Time.get_datetime()
    INPUTS.set_regs        ( INPUT_YEAR          , TIME[:-1]   )
    DISCRETES.set_reg_bool ( DISCRETE_TIME_STATUS, TIME_STATUS )
    

    # SETA O AZIMUTE E ALTITUDE DE INPUT COM O VALOR CALCULADO
    AZIMUTE, ALTITUDE = sun.compute( LOCALIZATION,  TIME )
    INPUTS.set_reg_float ( INPUT_AZIMUTE       , AZIMUTE     )
    INPUTS.set_reg_float ( INPUT_ALTITUDE      , ALTITUDE    )
    

    # Confere se foi recebido alguma mensagem para atualização das variáveis  
    if Modbus.has_message == True:
        update_configurations(  )
        Modbus.has_message = False 


    # Entra nos estados de operação
    STATE = HOLDINGS.get_reg( HR_STATE )
    if STATE == AUTOMATIC:
        # SETA O PV DO PID COM O AZIMUTE E ZENITE  
        PID_GIR.set_PV( INPUTS.get_reg_float ( INPUT_AZIMUTE  ) ) 
        PID_ELE.set_PV( INPUTS.get_reg_float ( INPUT_ALTITUDE ) )
        
        # SETA O PV DOS MOTORES PARA FUTUROS FAIL STATES 
        HOLDINGS.set_reg_float ( HR_PV_MOTOR_GIR, PID_GIR.PV ) 
        HOLDINGS.set_reg_float ( HR_PV_MOTOR_ELE, PID_ELE.PV )
    
        # Se a altitude for menor que 0 então o sol já se pôs e o tracker deve retornar
        # para a posição inicial ( do novo dia ) e aguardar até o sol nascer.
        if ALTITUDE < 0 :
            HOLDINGS.set_reg( HR_STATE, PRE_RETURNING )
            LAST_STATE = AUTOMATIC 
            continue 
        
        # COMPUTA O MOVIMENTO NECESSÁRIO PARA CORREÇÃO DOS MOTORES 
        POS_GIR = PID_GIR.compute( INPUTS.get_reg_float( INPUT_SENS_GIR ) ) 
        POS_ELE = PID_ELE.compute( INPUTS.get_reg_float( INPUT_SENS_ELE ) )
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == FAIL_STATE: 
        if ASGIR.degAngle(): 
            INPUTS.set_reg_float(  INPUT_SENS_GIR , SENS_GIR if SENS_GIR != False else INPUTS.get_reg_float(INPUT_SENS_GIR) )
            HOLDINGS.set_reg( HR_STATE, AUTOMATIC )
            continue
        else: 
            HOLDINGS.set_reg( HR_STATE, FAIL_STATE )
        if ASELE.degAngle():
            INPUTS.set_reg_float(  INPUT_SENS_ELE , SENS_ELE if SENS_ELE != False else INPUTS.get_reg_float(INPUT_SENS_ELE) )
            HOLDINGS.set_reg( HR_STATE, AUTOMATIC )
            continue
        else: 
            HOLDINGS.set_reg( HR_STATE, FAIL_STATE )
        
        # SETA O PV DO PID COM O AZIMUTE E ZENITE  
        PID_GIR.set_PV( HOLDINGS.get_reg_float ( INPUT_AZIMUTE  ) ) 
        PID_ELE.set_PV( HOLDINGS.get_reg_float ( INPUT_ALTITUDE ) )
        
        # Se a altitude for menor que 0 então o sol já se pôs e o tracker deve retornar
        # para a posição inicial ( do novo dia ) e aguardar até o sol nascer.
        if ALTITUDE < 0 :
            HOLDINGS.set_reg( HR_STATE, PRE_RETURNING )
            LAST_STATE = AUTOMATIC 
            continue 
        
        # COMPUTA O MOVIMENTO NECESSÁRIO PARA CORREÇÃO DOS MOTORES 
        POS_GIR = PID_GIR.compute( INPUTS.get_reg_float( HR_POS_MGIR ) ) 
        POS_ELE = PID_ELE.compute( INPUTS.get_reg_float( HR_POS_MELE ) )
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    elif STATE == PRE_RETURNING:
        NEW_AZIMUTE    = sun.get_sunrising( LOCALIZATION, TIME        ) 
        NEW_AZIMUTE, _ = sun.compute       ( LOCALIZATION, NEW_AZIMUTE )
        HOLDINGS.set_reg_float             ( HR_AZIMUTE  , NEW_AZIMUTE )
        HOLDINGS.set_reg                   ( HR_STATE    , RETURNING   )

    elif STATE == RETURNING:
        # Verifica a distancia do PV_NEW_DAY
        DIFF = abs( INPUTS.get_reg_float( INPUT_SENS_GIR ) - HOLDINGS.get_reg_float( HR_AZIMUTE ) )
        if DIFF > 5: 
            POS_ELE = 0.0
            POS_GIR = 2.5
            
        else: 
            PID_GIR.set_PV( HOLDINGS.get_reg_float ( HR_AZIMUTE  ) ) 
            PID_ELE.set_PV( 1 ) 
            # COMPUTA O MOVIMENTO NECESSÁRIO PARA CORREÇÃO DOS MOTORES 
            POS_GIR = PID_GIR.compute( INPUTS.get_reg_float( INPUT_SENS_GIR ) ) 
            POS_ELE = PID_ELE.compute( INPUTS.get_reg_float( INPUT_SENS_ELE ) )

            if ( abs(POS_GIR) < 0.5 ) and ( abs(POS_ELE) < 0.5 ):
                if LAST_STATE == AUTOMATIC:
                    HOLDINGS.set_reg( HR_STATE, SLEEPING )
                elif LAST_STATE == DEMO:
                    HOLDINGS.set_reg( HR_STATE, DEMO ) 
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == MANUAL:
        # PEGA O ESTADO DOS LEVERS 
        status = levers.check( )
        if   status[0] == True:            POS_ELE =  1
        elif status[1] == True:            POS_ELE = -1
        else:                              POS_ELE =  0
        if   status[2] == True:            POS_GIR =  1
        elif status[3] == True:            POS_GIR = -1
        else:                              POS_GIR =  0

        Motors.move( POS_ELE, POS_GIR )
        HOLDINGS.set_reg_float( HR_PV_MOTOR_GIR, Motors.get_gir_position() ) 
        HOLDINGS.set_reg_float( HR_PV_MOTOR_ELE, Motors.get_ele_position() )    
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == REMOTE:
        # PEGA O AZIMUTE E ZENITE DOS HOLDINGS AO INVÉS DOS INPUTS 
        PID_GIR.set_PV( HOLDINGS.get_reg_float( HR_AZIMUTE  )   )
        PID_ELE.set_PV( HOLDINGS.get_reg_float( HR_ALTITUDE )   )
        POS_GIR = PID_GIR.compute( INPUTS.get_reg_float( INPUT_SENS_GIR ) ) 
        POS_ELE = PID_ELE.compute( INPUTS.get_reg_float( INPUT_SENS_ELE ) )
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == IDLE:
        continue
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == SLEEPING:
        if ALTITUDE > 0:
            COILS.set_reg_bool( COIL_POWER, True      ) 
            HOLDINGS.set_reg  ( HR_STATE  , AUTOMATIC )
            Modbus.has_message = True 
        else:
            if COILS.get_reg_bool( COIL_POWER ) == True: 
                COILS.set_reg_bool( COIL_POWER, False )
                Modbus.has_message = True 
        continue
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == RESET:
        machine.soft_reset()    
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    elif STATE == DEMO:
        TIME = fake_time.compute()
        AZIMUTE, ALTITUDE = sun.compute( LOCALIZATION,  TIME )
        time.sleep(0.5) 
        
        if LAST_STATE != DEMO or ALTITUDE < 0: 
            LAST_STATE = DEMO
            fake_time.compute_new_day()
            HOLDINGS.set_reg( HR_STATE, PRE_RETURNING )
            continue 
        
        COILS.set_reg_bool( COIL_POWER, False )
        COILS.set_reg_bool( COIL_PRINT, False )
        
        HOLDINGS.set_reg_float( HR_AZIMUTE , AZIMUTE  )
        HOLDINGS.set_reg_float( HR_ALTITUDE, ALTITUDE )

        PID_GIR.set_PV( HOLDINGS.get_reg_float( HR_AZIMUTE  ) ) 
        PID_ELE.set_PV( HOLDINGS.get_reg_float( HR_ALTITUDE ) )
        
        POS_GIR = PID_GIR.compute( INPUTS.get_reg_float( INPUT_AZIMUTE  ) )
        POS_ELE = PID_ELE.compute( INPUTS.get_reg_float( INPUT_ALTITUDE ) )
        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
      
    # MOVE OS MOTORES 
    Motors.move( POS_ELE*0.05, POS_GIR*0.05 )

    # SALVA A NOVA POSIÇÃO DOS MOTORES
    HOLDINGS.set_reg_float( HR_POS_MGIR, Motors.GIR.position ) 
    HOLDINGS.set_reg_float( HR_POS_MELE, Motors.ELE.position )


    # Tempo de looping do Pico
    dt = (time.ticks_ms() - time_spend_by_loop )
    if dt <= 25:
        time.sleep_ms( 25 - dt )