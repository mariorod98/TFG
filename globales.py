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
P_CAMBIO = []           # paradas habilitadas para el cambio entre conductores
N_SERVICIOS = 0         # número de servicios de la jornada

HORARIO_TRENES = []     # conjunto de tuplas (TREN, PARADA, TIEMPO) que conforman el horario de la línea


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
    global P_CAMBIO
    global N_SERVICIOS
    global HORARIO_TRENES

    datos = lectura.lee_entrada(path)

    N_TRENES        = datos["N_TRENES"]
    INI_JORNADA     = datos["INI_JORNADA"]
    FIN_JORNADA     = datos["FIN_JORNADA"]
    N_PARADAS       = datos["N_PARADAS"]
    T_IDA           = datos["T_IDA"]
    T_VUELTA        = datos["T_VUELTA"]
    T_FINAL_1       = datos["T_FINAL_1"]
    T_FINAL_N       = datos["T_FINAL_N"]
    P_SALIDA        = datos["P_SALIDA"]
    DIR_SALIDA      = datos["DIR_SALIDA"]
    P_CAMBIO        = datos["P_CAMBIO"]
    N_SERVICIOS     = datos["N_SERVICIOS"]
    HORARIO_TRENES  = lectura.calcula_horario_trenes()
