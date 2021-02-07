# -*- coding: utf-8 -*-
"""
Funciones fitness
Autor: Mario Rodríguez Chaves
"""

import numpy as np
import funciones_auxiliares as aux

import globales as glo


# RESTRICIONES DURAS
#   Un servicio no puede tener más de 4 horas de trabajo seguidas


# FUNCION 1
#   Se busca que la diferencia de tiempo entre los servicios sea la minima
#   Se busca que los servicios tengan un descanso de un tiempo minimo (hiperparametro) y que la diferencia
#   de descanso entre los servicios sea minima
def funcion_objetivo_1(solucion):
    tiempos_trabajo = np.empty(glo.N_SERVICIOS)    # lista con los tiempos de trabajo de los servicios
    tiempos_descanso = np.empty(glo.N_SERVICIOS)   # lista con los tiempos de descanso de los servicios

    # para cada servicio se comprueba que es válido y se obtiene el tiempo de trabajo y descanso
    for servicio in range(0, glo.N_SERVICIOS):

        # se obtiene un array con los periodos en los que el servicio está activo
        periodos = aux.calcula_periodos_servicio(solucion, servicio)

        if len(periodos) > 0:
            periodos.sort(key=lambda x: glo.HORARIO_TRENES[x[0]]['TIEMPO'])

            if not aux.valida_servicio(periodos):
                return False, 9999

            t_trabajo, t_descanso = aux.calcula_tiempos_servicio(periodos)

            tiempos_trabajo[servicio] = t_trabajo
            tiempos_descanso[servicio] = t_descanso
        else:
            tiempos_trabajo[servicio] = 0
            tiempos_descanso[servicio] = 0

    std_trabajo = tiempos_trabajo.std()
    std_descanso = tiempos_descanso.std()

    valor = std_trabajo + std_descanso

    return True, valor


def funcion_objetivo_2(solucion):
    optimo_trabajo = 170
    optimo_descanso = 30
    tiempos_trabajo = np.empty(glo.N_SERVICIOS)    # lista con los tiempos de trabajo de los servicios
    tiempos_descanso = np.empty(glo.N_SERVICIOS)   # lista con los tiempos de descanso de los servicios
    peso = 0.5

    # para cada servicio se comprueba que es válido y se obtiene el tiempo de trabajo y descanso
    for servicio in range(0, glo.N_SERVICIOS):
        # se obtiene un array con los periodos de trabajo del servicio
        periodos = aux.calcula_periodos_servicio(solucion, servicio)

        # si el servicio no tiene periodos de trabajo, se trata de una solución no factible
        if periodos == -1:
            return False, 9999

        # se ordenan cronológicamente los periodos de trabajo del servicio
        periodos.sort(key=lambda x: glo.HORARIO_TRENES[x[0]]['TIEMPO'])

        # si el servicio presenta inconsistencias, se trata de una solución no factible
        if not aux.valida_servicio(periodos):
            return False, 9999

        # se obtienen el tiempo de trabajo y descanso del servicio
        t_trabajo, t_descanso = aux.calcula_tiempos_servicio(periodos)

        tiempos_trabajo[servicio] = t_trabajo
        tiempos_descanso[servicio] = t_descanso

    # se calcula la media de tiempo de trabajo y descanso
    mean_trabajo = tiempos_trabajo.mean()
    mean_descanso = tiempos_descanso.mean()

    # se calcula la diferencia al óptimo de tiempo de trabajo y descanso
    diferencia_trabajo = abs(mean_trabajo - optimo_trabajo)
    diferencia_descanso = abs(mean_descanso - optimo_descanso)

    # se obtiene la desviación estándar de los tiempos de trabajo y descanso
    std_trabajo = tiempos_trabajo.std()
    std_descanso = tiempos_descanso.std()

    # se calcula el valor de la función fitness a partir de los datos obtenidos, aplicando sus respectivos pesos
    valor = peso * (std_trabajo + std_descanso) + (1-peso) * (diferencia_trabajo + diferencia_descanso)

    return True, valor


def funcion_objetivo_3(solucion):
    optimo_trabajo = 170
    optimo_descanso = 30
    n_periodos = 0

    tiempos_trabajo = np.empty(glo.N_SERVICIOS)    # lista con los tiempos de trabajo de los servicios
    tiempos_descanso = np.empty(glo.N_SERVICIOS)   # lista con los tiempos de descanso de los servicios
    peso1 = 1
    peso2 = 1
    peso3 = 3

    # para cada servicio se comprueba que es válido y se obtiene el tiempo de trabajo y descanso
    for servicio in range(0, glo.N_SERVICIOS):
        periodos = aux.calcula_periodos_servicio(solucion, servicio)

        if periodos == -1:
            return False, 9999

        n_periodos += len(periodos)
        periodos.sort(key=lambda x: glo.HORARIO_TRENES[x[0]]['TIEMPO'])

        if not aux.valida_servicio(periodos):
            return False, 9999

        t_trabajo, t_descanso = aux.calcula_tiempos_servicio(periodos)

        tiempos_trabajo[servicio] = t_trabajo
        tiempos_descanso[servicio] = t_descanso

    mean_trabajo = tiempos_trabajo.mean()
    mean_descanso = tiempos_descanso.mean()

    diferencia_trabajo = abs(mean_trabajo - optimo_trabajo)
    diferencia_descanso = abs(mean_descanso - optimo_descanso)

    std_trabajo = tiempos_trabajo.std()
    std_descanso = tiempos_descanso.std()

    valor = peso1 * (std_trabajo + std_descanso) + peso2 * (diferencia_trabajo + diferencia_descanso) + peso3 * n_periodos

    return True, valor
