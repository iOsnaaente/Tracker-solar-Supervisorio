from datetime import datetime  

import serial
import glob
import sys

"""
    A função funciona tanto em Windows quanto em Linux 
    
    Testa todas as portas possíveis no computador e tenta abri-las
        Caso ele consiga, significa que a porta existe
        Caso a porta não possa ser aberta, ela existe
        Caso retorne Erro (SerialException), ela não existe
    
    Retorna uma lista com os nomes das portas disponíveis 

"""

def serialPorts( lenght = 25 ):

    # Abre se o SO for Windows
    if sys.platform.startswith('win'):  
        ports = ['COM%s' % (i + 1) for i in range( lenght )]

    # Abre se o SO for Linux
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
        
    # Caso não seja nenhum dos dois, ele não suporta
    else:
        print("Sistema Operacional não suportado")

    # Testa as portas disponíveis 
    portList = []
    for port in ports:
        try:
            s = serial.Serial( port )
            s.close()
            portList.append(port)
        except (OSError, serial.SerialException):
            pass

    return portList


def showSerialAvailable():
    listaPortas = serialPorts()
    if listaPortas is None:
        print("Não há portas Seriais abertas !!")
    else:
        for port in listaPortas:
            print(port, end="\n")


def initSerialListening(DEVICE, BAUDRATE, TIMEOUT):
    # Iniciando conexao serial
    #comport = serial.Serial('/dev/ttyUSB4', 9600, timeout=1)
    comport = serial.Serial(DEVICE, BAUDRATE, timeout=TIMEOUT)
    return comport


def txtComportsAvailable(path = './comportsList.txt', defalt = 'w' ):
    with open( path, defalt ) as FILE:
        comportList = serialPorts()
        for num, comport in enumerate(comportList):
            print( str( datetime.now() ), str(comport), str(num), end='\n', sep=',', file=FILE )