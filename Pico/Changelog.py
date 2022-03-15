__author__     = "Bruno Gabriel F. Sampaio"
__version__    = "2.0.0"
__company__    = "Jet Towers - Telecomunicações // http://www.jettowers.com.br/"
__maintainer__ = "Bruno Gabriel F. Sampaio"
__email__      = "bruno.sampaio@acad.ufsm.br"
__status__     = "Prototype"
 
""" Protótipo de criação de um rastreador solar - Tracker
    
    Firmware utilizado em um Raspberry pi Pico para controle
    de motores de passo que realizam o rastreamento solar
    garantindo mais geração elétrica a partir de painéis
    fotovoltáicos.
    
    Versão 2.0.0::
        >>> Implementado registradores e protocolo Modbus
        >>> Comunicação via interrupção de caracteres
            >>> Mais rápida
            >>> Mais simples
            >>> Maior confiança
        >>> Funções de Debug 
    
    Versão 1.2.0::
        >>> Rotinas de diagnóstico implementadas
        >>> Correções de datetime com o supervisório
        >>> Leitura dos sensores mais estável ( Correções do I2C)
    
    Versão 1.1.0::
        >>> Estabilidade de testes com o uso do RenameMainDotPy firmware no Pico    
    
    
    Versão 1.0.1::
        >>> Várias correções de bugs
        >>> Sistema mais estável
            >>> Boa comunicação entre Supervisório e RASP 
    
    Versão 1.0.0::
        >>> REPL usado para debug e comunicação via UART
            >>> Monitoramento REPL via USB
            >>> Comunicação via UART
        >>> Correção dos diretórios do Pico::
            >>> Criação de módulos para cada sistema
            >>> Divisão de responsabilidade entre casa sistema
    
    Versão 0.9.4::
        >>> Sensores AS5600::
            >>> Leitura dos sensores AS5600 via I2C
            >>> Sensoriamento preciso 
        >>> Uso do RTC interno do Pico para comparação com o DS3231
            >>> Redundancia de horários
        >>> Controle PID dos motores
        
        
    Versão 0.9.3::
        >>> Mudança do controle dos motores usando os PIOs
        >>> Sensor para medição da posição AS5600
            >>> Sensor 12 bits de resolução
    
    Versão 0.9.2::
        >>> Nova tentativa de rastreamento da posição dos motores
        >>> Código AS5043A para encoder Magnético
            >>> Foram feitas medições utilizando o encoder magnético 
            >>> Resultados positivos para o rastreio
            --- Contra é o valor do sensor 
    
    Versão 0.9.1::
        >>> Criação do arquivo Acell.py para os dados do acelerometro
        >>> A partir dos teste do acelerometro
            >>> Os valores obtidos foram inconclusivos para a finalidade
            >>> Resultados não reproduzem o esperado devido a tremulação do sistema
        >>> Acelerometro não será usado
        >>> Criação das funções de acionamento dos motores via relé 
        >>> Pesquisa de encoderes magnéticos AS5043A
    
    Versão 0.9.0::
        >>> Testes com sensores de posição do motor::
            >>> Acelerometro e giroscópio 
    
    Versão 0.8.1::
        >>> Adaptação da placa de desenvolvimento::
            >>> Acrescimo do relé de acionamento dos motores
        >>> Criação de um design de PCI para o sistema::
            >>> Fritzing 
    
    Versão 0.8.0::
        >>> Correção da comunicação serial.
        >>> Criação variáveis de estado::
            >>> STATES::
                >>> AUTOMATIC_SLEEPING # Dormindo esperando um novo dia começar 
                    AUTOMATIC_BACKWARD # Retorna para a posição inicial do novo dia
                    AUTOMATIC_TRACKING # Rastreia o sol em um dia normal 
                    WAKE_UP            # Opção de inicio. É chamado quando o Rasp liga
                    MANUAL_CONTROLING  # Ativa o controle por Levers 
                    MANUAL_STOPING     # Para o rastreio do tracker
                    MANUAL_DEMO        # Segue o sol de forma acelerada ( Demonstração ) 
        
    Versão  0.7.0::
        >>> Criação do módulo Timanager::
            >>> Junção de Timer e Manager.
            >>> Realiza todo controle de passagem de tempo
                e movimento decorrente desse periodo.
    
    Versão 0.6.0::
        >>> Correção do movimento de retorno do Tracker::
            >>>Segundo teste de funcionamento::
                >>> Controle de retorno OK.
        >>> Rastreio solar em funcionamento.
                
    Versão 0.5.2::
        >>> Movimentação acelerada do movimento real de rastreio::
            >>>Primeiro teste de funcionamento::
                >>> Movimentação OK 
                >>> Dados precisos OK
                >>> Controle de retorno FAIL
    
    Versão 0.5.1::
        >>> Extinção das Threads::
            >>> Extinção do uso de threads para os Levers.
            >>> Extinção do uso de threads para a Serial.
        >>> Rastreio solar funcionando parcialmente.
        
    Versão  0.5.0::
        >>> Levers::
            >>> Criação da Classe Levers para controle manual dos
                motores via alavancas presas à placa de desenvolvimento.
            >>> Evitando poluição de código para esse controle::
                >>> Levers possuem o método get_state que retornam os
                    valores dos levers
                >>> Possuem também (dois/quarto) valores de entradas digitais
                    para fazerem os acionamentos de acordo com o valor
                    dos levers.
        >>> Threads::
            >>> Criação de Threads para o controle dos Levers e/ou comunicação
                serial.
            
    Versão  0.4.0::
        >>> Const. Evitando poluição do escopo principal (main),
            separou-se as constantes em outro file.py chamado Const
        >>> FileStatements. Criação de um file.py FileStatements
            que guarda as funções de escrita Flash do RasPico::
            >>> Ainda não é possível ler a posição dos motores, por isso
                as posições são contadas e salvas em um arquivo .txt 
            
    Versão  0.3.0::
        >>> Serial comunication. Ponta pé inicial da comunicação serial
            utilizando structs pack e unpack. Funcional, mas incompleto.
            >>> Utilização do inicializador 'INIT' 
            
    Versão  0.2.0::
        >>> Finalização da Classe StepMotors::
            >>> Adição dos nanoSteps que guardam decimais do movimento dos motores.
            >>> StepMotors agora esta mais organizado e limpo.
            >>> Funcionando 100% porém falta documentar.
        >>> Criação da função get_twilights() dentro de SunPosition::
            >>> Função responsável por pegar os horários de crepusculos do dia.
            
    Versão  0.1.4::
        >>> Correção da classe StepMotors. Separação da classe Motors
            em duas classes distintas. Motors e Motor ( pai e filho).
        >>> Correção no código do DS3231.
        >>> Documentação do código do DS3231. Agora esta 100%.
        
    Versão 0.1.3::
        >>> Criação da interface DS3231.
            >>> Faltam ajustes, porém é possível pegar os valores de date e hora.
        
    
    Versão  0.1.2::
        >>> Criação da interface StepMotors para fazer o controle dos motores de passo.
        >>> Finalização do código SunPosition de rastreio solar.
            >>> Código Funcionando.
            >>> Documentado
        
    Versão  0.1.1::
        >>> Correções no código SunPosition de rastreio solar. Definição
            final de como será feito a computação das posições de azimute
            e zenite( altitude ) sem o uso de classes.
            >>> Função Compute() realiza todos os cálculos.
                >>> Parametros de LOCALIZAÇÃO e DATETIME
            
    Versão 0.1.0::
        >>> Estruturação do primeiro modelo funcional.
        >>> Definição de todo o escopo do Firmware.
            >>> Rastreio solar - SunPosition
            >>> Contagem da hora - DS3231
            >>> Controle dos motores - StepMotors
            
    Versão 0.0.1::
        >>> Migração do código em C ( Arduino ) para Python ( MicroPython)
     
"""

