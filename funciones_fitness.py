# -*- coding: utf-8 -*-
"""
Funciones fitness
Autor: Mario Rodríguez Chaves
"""

import numpy as np
import funciones_auxiliares as aux

import globales as glo


# Función que calcula los tiempos de trabajo y descanso de los diferentes servicios
# Parámetros de entrada:
#   solucion: np array de valores que comprenden la solución
# Return: diccionario con todos los resultados obtenidos
#   n_periodos: número de periodos de trabajo totales
#   resultados['T_TRABAJO']: lista con los tiempos de trabajo de los servicios
#   resultados['T_DESCANSO']: lista con los tiempos de descanso de los servicios
def calcula_resultados(solucion):
    resultados = {'T_TRABAJO': np.empty(glo.N_SERVICIOS),   # lista con los tiempos de trabajo por servicio
                  'T_DESCANSO': np.empty(glo.N_SERVICIOS),  # lista con los tiempos de descanso por servicio
                  'N_PERIODOS': np.zeros(glo.N_SERVICIOS),  # número de periodos de trabajo por servicio
                  'T_JORNADA': np.zeros(glo.N_SERVICIOS)}   # tiempo total de jornada por servicio

    # para cada servicio se comprueba que es válido y se obtiene el tiempo de trabajo y descanso
    for servicio in range(0, glo.N_SERVICIOS):
        periodos = aux.calcula_periodos_servicio(solucion, servicio)

        if not periodos:
            return False, resultados

        resultados['N_PERIODOS'][servicio] = len(periodos)
        periodos.sort(key=lambda x: glo.HORARIO_TRENES[x[0]]['TIEMPO'])

        if not aux.valida_servicio(periodos):
            return False, resultados

        t_trabajo, t_descanso = aux.calcula_tiempos_servicio(periodos)

        resultados['T_TRABAJO'][servicio] = t_trabajo
        resultados['T_DESCANSO'][servicio] = t_descanso

        t_ini = glo.HORARIO_TRENES[periodos[0][0]]['TIEMPO']
        t_fin = glo.HORARIO_TRENES[periodos[-1][1]]['TIEMPO']

        resultados['T_JORNADA'][servicio] = t_fin - t_ini

    return True, resultados


# FUNCION 1
#   Se busca que la diferencia de tiempo entre los servicios sea la minima
#   Se busca que los servicios tengan un descanso de un tiempo minimo (hiperparametro) y que la diferencia
#   de descanso entre los servicios sea minima
# Parámetros de entrada:
#   solucion: np array de valores que comprenden la solución
# Return:
#   fitness: valor fitness de la función
#   resultados: métricas de la solución
def funcion_objetivo_1(solucion):
    # se obtienen los tiempos de trabajo y descanso de cada servicio
    es_valida, resultados = calcula_resultados(solucion)

    # si la solución no es válida, se devuelve valor infinito
    if not es_valida:
        return float('inf'), resultados

    # se calcula la desviación estándar del tiempo de trabajo y descanso
    std_trabajo = resultados['T_TRABAJO'].std()
    std_descanso = resultados['T_DESCANSO'].std()

    # el valor heurístico será la suma de las dos desviaciones
    valor = std_trabajo + std_descanso

    # devolvemos el valor obtenido
    return valor, resultados


# FUNCIÓN 2
#   Se busca que la diferencia de tiempo entre los servicios sea la minima
#   Se busca que los servicios tengan un descanso de un tiempo minimo (hiperparametro) y que la diferencia
#   de descanso entre los servicios sea minima
# Parámetros de entrada:
#   solucion: np array de valores que comprenden la solución
# Return:
#   fitness: valor fitness de la función
#   resultados: métricas de la solución
def funcion_objetivo_2(solucion):
    optimo_trabajo = 170
    optimo_descanso = 30
    peso = 0.5

    # se obtienen los tiempos de trabajo y descanso de cada servicio
    es_valida, resultados = calcula_resultados(solucion)

    # si la solución no es válida, se devuelve una fitness mala
    if not es_valida:
        return float('inf'), resultados

    # se calcula la media de tiempo de trabajo y descanso
    mean_trabajo = resultados['T_TRABAJO'].mean()
    mean_descanso = resultados['T_DESCANSO'].mean()

    # se calcula la diferencia al óptimo de tiempo de trabajo y descanso
    diferencia_trabajo = abs(mean_trabajo - optimo_trabajo)
    diferencia_descanso = abs(mean_descanso - optimo_descanso)

    # se obtiene la desviación estándar de los tiempos de trabajo y descanso
    std_trabajo = resultados['T_TRABAJO'].std()
    std_descanso = resultados['T_DESCANSO'].std()

    # se calcula el valor de la función fitness a partir de los datos obtenidos, aplicando sus respectivos pesos
    valor = peso * (std_trabajo + std_descanso) + (1 - peso) * (diferencia_trabajo + diferencia_descanso)

    return valor, resultados


# FUNCIÓN 3
#   Se busca que la diferencia de tiempo entre los servicios sea la minima
#   Se busca que los servicios tengan un descanso de un tiempo minimo (hiperparametro) y que la diferencia
#   de descanso entre los servicios sea minima
#   Se busca que los periodos de trabajo de cada servicio sean los menores posibles
# Parámetros de entrada:
#   solucion: np array de valores que comprenden la solución
# Return:
#   fitness: valor fitness de la función
#   resultados: métricas de la solución
def funcion_objetivo_3(solucion):
    optimo_trabajo = glo.T_OPTIMO_TRABAJO
    optimo_descanso = glo.T_OPTIMO_DESCANSO
    peso1 = 1
    peso2 = 1
    peso3 = 3

    # se obtienen los tiempos de trabajo y descanso de cada servicio
    es_valida, resultados = calcula_resultados(solucion)

    # si la solución no es válida, se devuelve una fitness mala
    if not es_valida:
        return float('inf'), resultados

    mean_trabajo = resultados['T_TRABAJO'].mean()
    mean_descanso = resultados['T_DESCANSO'].mean()

    diferencia_trabajo = abs(mean_trabajo - optimo_trabajo)
    diferencia_descanso = abs(mean_descanso - optimo_descanso)

    std_trabajo = resultados['T_TRABAJO'].std()
    std_descanso = resultados['T_DESCANSO'].std()

    sum_n_periodos = resultados['N_PERIODOS'].sum()

    valor = peso1 * (std_trabajo + std_descanso) + \
            peso2 * (diferencia_trabajo + diferencia_descanso) + \
            peso3 * sum_n_periodos

    return valor, resultados


# FUNCIÓN 4
#   Se busca que la diferencia de tiempo entre los servicios sea la minima
#   Se busca que los servicios tengan un descanso de un tiempo minimo (hiperparametro) y que la diferencia
#   de descanso entre los servicios sea minima
#   Se busca que los periodos de trabajo de cada servicio sean los menores posibles
#   Se busca que la jornada de trabajo sea completa y no partida.
# Parámetros de entrada:
#   solucion: np array de valores que comprenden la solución
# Return:
#   fitness: valor fitness de la función
#   resultados: métricas de la solución
def funcion_objetivo_4(solucion):
    optimo_trabajo = glo.T_OPTIMO_TRABAJO
    optimo_descanso = glo.T_OPTIMO_DESCANSO

    peso1 = 0.8
    peso2 = 0.2

    # se obtienen los tiempos de trabajo y descanso de cada servicio
    es_valida, resultados = calcula_resultados(solucion)

    # si la solución no es válida, se devuelve una fitness mala
    if not es_valida:
        return float('inf'), resultados

    mean_trabajo = resultados['T_TRABAJO'].mean()
    mean_descanso = resultados['T_DESCANSO'].mean()

    diferencia_trabajo = abs(mean_trabajo - optimo_trabajo)
    diferencia_descanso = abs(mean_descanso - optimo_descanso)

    std_trabajo = resultados['T_TRABAJO'].std()
    std_descanso = resultados['T_DESCANSO'].std()

    mean_n_periodos = resultados['N_PERIODOS'].mean()
    mean_t_jornada = resultados['T_JORNADA'].mean()

    valor = (peso1 * (diferencia_trabajo + diferencia_descanso)
             + peso2 * (std_trabajo + std_descanso)) * \
            mean_n_periodos

    return valor, resultados


funcion_objetivo = funcion_objetivo_4
