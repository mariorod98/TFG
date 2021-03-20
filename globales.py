# -*- coding: utf-8 -*-
"""
Constantes globales del programa
Autor: Mario Rodríguez Chaves
"""
import lectura_datos as lectura

N_TRENES = 0            # número de trenes operativos
INI_JORNADA = []        # tiempo de salida de los trenes durante la jornada, debe tener tamaño N_TRENES
FIN_JORNADA = []        # tiempo de fin de jornada de los trenes, debe tener tamaño N_TRENES
N_PARADAS = 0           # número de paradas de la línea
T_IDA = []              # tiempos de ida entre paradas (i a i+1), tiene que tener tamaño N_PARADAS - 1
T_VUELTA = []           # tiempo de vuelta entre paradas (i a i-1), tiene que tener tamaño N_PARADAS -1
T_FINAL_1 = 0           # tiempo de espera en la parada 1
T_FINAL_N = 0           # tiempo de espera en la parada final N
P_SALIDA = 0            # parada de salida de los trenes
DIR_SALIDA = 0          # dirección de salida de los trenes
DIR_ALTERNA = False     # especifica si los trenes alternan la dirección al salir o salen de la misma dirección
P_CAMBIO = []           # paradas habilitadas para el cambio entre conductores
N_SERVICIOS = 0         # número de servicios de la jornada
T_MIN_DESCANSOS = 0     # tiempo mínimo entre dos periodos para que se considere un descanso
T_MAX_TRABAJO = 0       # tiempo máximo de trabajo continuo en un servicio
T_OPTIMO_TRABAJO = 0    # tiempo deseado de trabajo por servicio
T_OPTIMO_DESCANSO = 0   # tiempo deseado de descanso por servicio

HORARIO_TRENES = []     # conjunto de tuplas (TREN, PARADA, TIEMPO) que conforman el horario de la línea

RESULTADOS = []         # lista que almacenará los resultados obtenidos durante la ejecucion de un algoritmo


# función que inicializa las globales
def init(path):
    global N_TRENES
    global INI_JORNADA
    global FIN_JORNADA
    global N_PARADAS
    global T_IDA
    global T_VUELTA
    global T_FINAL_1
    global T_FINAL_N
    global P_SALIDA
    global DIR_SALIDA
    global DIR_ALTERNA
    global P_CAMBIO
    global N_SERVICIOS
    global T_MIN_DESCANSOS
    global T_MAX_TRABAJO
    global HORARIO_TRENES
    global T_OPTIMO_DESCANSO
    global T_OPTIMO_TRABAJO

    datos = lectura.lee_entrada(path)

    N_TRENES          = datos['N_TRENES']
    INI_JORNADA       = datos['INI_JORNADA']
    FIN_JORNADA       = datos['FIN_JORNADA']
    N_PARADAS         = datos['N_PARADAS']
    T_IDA             = datos['T_IDA']
    T_VUELTA          = datos['T_VUELTA']
    T_FINAL_1         = datos['T_FINAL_1']
    T_FINAL_N         = datos['T_FINAL_N']
    P_SALIDA          = datos['P_SALIDA']
    DIR_SALIDA        = datos['DIR_SALIDA']
    DIR_ALTERNA       = datos['DIR_ALTERNA']
    P_CAMBIO          = datos['P_CAMBIO']
    N_SERVICIOS       = datos['N_SERVICIOS']
    T_MIN_DESCANSOS   = datos['T_MIN_DESCANSOS']
    T_MAX_TRABAJO     = datos['T_MAX_TRABAJO']
    T_OPTIMO_TRABAJO  = datos['T_OPTIMO_TRABAJO']
    T_OPTIMO_DESCANSO = datos['T_OPTIMO_DESCANSO']
    HORARIO_TRENES    = lectura.calcula_horario_trenes()
