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
T_MIN_DESCANSO = 0     # tiempo mínimo entre dos periodos para que se considere un descanso
T_MAX_TRABAJO = 0       # tiempo máximo de trabajo continuo en un servicio
T_OPTIMO_TRABAJO = 0    # tiempo deseado de trabajo por servicio
T_OPTIMO_DESCANSO = 0   # tiempo deseado de descanso por servicio

HORARIO_TRENES = []     # conjunto de tuplas (TREN, PARADA, TIEMPO) que conforman el horario de la línea

RESULTADOS = []         # lista que almacenará los resultados obtenidos durante la ejecucion de un algoritmo
ARCHIVO_ENTRADA = ""
ARCHIVO_SALIDA = ""


# función que inicializa las globales
def init(datos):
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
    global T_MIN_DESCANSO
    global T_MAX_TRABAJO
    global HORARIO_TRENES
    global T_OPTIMO_DESCANSO
    global T_OPTIMO_TRABAJO
    global ARCHIVO_ENTRADA

    # se comprueba que exista la entrada N_TRENES y que sea int
    datos_correctos = 'N_TRENES' in datos.keys() and type(datos['N_TRENES']) is int
    if datos_correctos:
        N_TRENES = datos['N_TRENES']
    else:
        return False

    # se comprueba que exista la entrada INI_JORNADA, que sea una lista de tamaño N_TRENES y que sus valores sean int
    datos_correctos = 'INI_JORNADA' in datos.keys() and len(datos['INI_JORNADA']) == N_TRENES and \
                      len([i for i in datos['INI_JORNADA'] if type(i) is not int]) == 0
    if datos_correctos:
        INI_JORNADA = datos['INI_JORNADA']
    else:
        return False

    # se comprueba que exista la entrada FIN_JORNADA, que sea una lista de tamaño N_TRENES y que sus valores sean int
    datos_correctos = 'FIN_JORNADA' in datos.keys() and len(datos['FIN_JORNADA']) == N_TRENES and \
                      len([i for i in datos['FIN_JORNADA'] if type(i) is not int]) == 0
    if datos_correctos:
        FIN_JORNADA = datos['FIN_JORNADA']
    else:
        return False

    # se comprueba que exista la entrada N_PARADAS y que sea int
    datos_correctos = 'N_PARADAS' in datos.keys() and type(datos['N_PARADAS']) is int
    if datos_correctos:
        N_PARADAS = datos['N_PARADAS']
    else:
        return False

    # se comprueba que exista la entrada T_IDA, que sea una lista de tamaño N_PARADAS y que sus valores sean int
    datos_correctos = 'T_IDA' in datos.keys() and len(datos['T_IDA']) == N_PARADAS - 1 and \
                      len([i for i in datos['T_IDA'] if type(i) is not int]) == 0
    if datos_correctos:
        T_IDA = datos['T_IDA']
    else:
        return False

    # se comprueba que exista la entrada T_VUELTA, que sea una lista de tamaño N_PARADAS y que sus valores sean int
    datos_correctos = 'T_VUELTA' in datos.keys() and len(datos['T_VUELTA']) == N_PARADAS - 1 and \
                      len([i for i in datos['T_VUELTA'] if type(i) is not int]) == 0
    if datos_correctos:
        T_VUELTA = datos['T_VUELTA']
    else:
        return False

    # se comprueba que exista la entrada T_FINAL_1 y que sea int
    datos_correctos = 'T_FINAL_1' in datos.keys() and type(datos['T_FINAL_1']) is int
    if datos_correctos:
        T_FINAL_1 = datos['T_FINAL_1']
    else:
        return False

    # se comprueba que exista la entrada T_FINAL_N y que sea int
    datos_correctos = 'T_FINAL_N' in datos.keys() and type(datos['T_FINAL_N']) is int
    if datos_correctos:
        T_FINAL_N = datos['T_FINAL_N']
    else:
        return False

    # se comprueba que exista la entrada P_SALIDA, que sea int y que sea menor a N_PARADAS
    datos_correctos = 'P_SALIDA' in datos.keys() and type(datos['P_SALIDA']) is int and datos['P_SALIDA'] < N_PARADAS
    if datos_correctos:
        P_SALIDA = datos['P_SALIDA']
    else:
        return False

    # se comprueba que exista la entrada DIR_SALIDA, que sea int y que sea -1 o 1
    datos_correctos = 'DIR_SALIDA' in datos.keys() and type(datos['DIR_SALIDA']) is int and datos['DIR_SALIDA'] in [-1, 1]
    if datos_correctos:
        DIR_SALIDA = datos['DIR_SALIDA']
    else:
        return False

    # se comprueba que exista la entrada DIR_ALTERNA y que sea bool
    datos_correctos = 'DIR_ALTERNA' in datos.keys() and type(datos['DIR_ALTERNA']) is bool
    if datos_correctos:
        DIR_ALTERNA = datos['DIR_ALTERNA']
    else:
        return False

    # se comprueba que exista la entrada P_CAMBIO, que sea una lista de tamaño N_PARADAS y que sus valores sean int
    # y menores que N_PARADAS
    datos_correctos = 'P_CAMBIO' in datos.keys() and 0 < len(datos['P_CAMBIO']) <= N_PARADAS and \
                      len([i for i in datos['P_CAMBIO'] if type(i) is not int or i >= N_PARADAS]) == 0
    if datos_correctos:
        P_CAMBIO = datos['P_CAMBIO']
    else:
        return False

    # se comprueba que exista la entrada N_SERVICIOS y que sea int
    datos_correctos = 'N_SERVICIOS' in datos.keys() and type(datos['N_SERVICIOS']) is int
    if datos_correctos:
        N_SERVICIOS = datos['N_SERVICIOS']
    else:
        return False

    # se comprueba que exista la entrada T_MIN_DESCANSO y que sea int
    datos_correctos = 'T_MIN_DESCANSO' in datos.keys() and type(datos['T_MIN_DESCANSO']) is int
    if datos_correctos:
        T_MIN_DESCANSO = datos['T_MIN_DESCANSO']
    else:
        return False

    # se comprueba que exista la entrada T_MAX_TRABAJO y que sea int
    datos_correctos = 'T_MAX_TRABAJO' in datos.keys() and type(datos['T_MAX_TRABAJO']) is int
    if datos_correctos:
        T_MAX_TRABAJO = datos['T_MAX_TRABAJO']
    else:
        return False

    # se comprueba que exista la entrada T_OPTIMO_TRABAJO y que sea int
    datos_correctos = 'T_OPTIMO_TRABAJO' in datos.keys() and type(datos['T_OPTIMO_TRABAJO']) is int
    if datos_correctos:
        T_OPTIMO_TRABAJO = datos['T_OPTIMO_TRABAJO']
    else:
        return False

    # se comprueba que exista la entrada T_OPTIMO_DESCANSO y que sea int
    datos_correctos = 'T_OPTIMO_DESCANSO' in datos.keys() and type(datos['T_OPTIMO_DESCANSO']) is int
    if datos_correctos:
        T_OPTIMO_DESCANSO = datos['T_OPTIMO_DESCANSO']
    else:
        return False

    HORARIO_TRENES = lectura.calcula_horario_trenes()

    return True
