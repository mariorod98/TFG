# -*- coding: utf-8 -*-
"""
Funciones auxiliares
Autor: Mario Rodríguez Chaves
"""

import numpy as np

import globales


# Función que devuelve los indices del array que tengan dicho valor
def obtiene_indices(array, valor):
    return np.where(array == valor)[0]


# si el periodo empieza en una parada intermedia, el intercambio de trabajadores se ha producido en la parada
# anterior, ya que a esta parada llega el trabajador del servicio actual. Por lo tanto, el trabajador empieza a
# trabajar en la parada anterior, que es cuando se produce el cambio de conductor. Si el periodo empieza en la
# primera parada del trayecto del tren, entonces se coge esa parada, ya que no hay una anterior.
def calcula_inicio_servicio(periodo):
    if periodo[0] == 0 or globales.HORARIO_TRENES[periodo[0]]['TREN'] != globales.HORARIO_TRENES[periodo[0] - 1]['TREN']:
        return periodo[0]
    else:
        return periodo[0] - 1


# Función que calcula los periodos de trabajo y descanso del servicio
def calcula_periodos_servicio_ant(solucion, servicio):
    periodos_trabajo = []                                   # periodos de trabajo del servicio
    indices_paradas = obtiene_indices(solucion, servicio)   # paradas de trabajo del servicio

    # si el servicio no tiene paradas, se devuelve vacio
    if len(indices_paradas) == 0:
        return []

    p_ant = indices_paradas[0]                      # parada anterior a la actual, inicializado a la primera parada
    p_ini_periodo = p_ant                           # parada de inicio de un periodo de trabajo,
                                                    # inicializado a la primera parada

    # para cada parada en la que se encuentre el servicio (a partir de la segunda)
    for p in indices_paradas[1:]:
        # si la parada actual no es contigua a la anterior o si el tren es distinto, entonces se ha cambiado de
        # periodo de trabajo
        if p - p_ant > 1 or globales.HORARIO_TRENES[p_ant]['TREN'] != globales.HORARIO_TRENES[p]['TREN']:
            periodos_trabajo.append([p_ini_periodo, p_ant])     # se añade el periodo
            p_ini_periodo = p                                   # se inicia un nuevo periodo con la parada actual
        p_ant = p                                               # se reasigna la parada anterior a la actual

    periodos_trabajo.append([p_ini_periodo, indices_paradas[-1]])       # se añade el último periodo

    return periodos_trabajo


def calcula_periodos_servicio(solucion, servicio):
    periodos_trabajo = []                                   # periodos de trabajo del servicio
    indices_paradas = obtiene_indices(solucion, servicio)   # paradas de trabajo del servicio
    nuevo_periodo = False

    # si el servicio no tiene paradas, se devuelve vacio
    if len(indices_paradas) == 0:
        return []

    p_ini_periodo = indices_paradas[0]              # parada anterior a la actual, inicializado a la primera parada
    p_fin_periodo = p_ini_periodo                   # parada de inicio de un periodo de trabajo,
                                                    # inicializado a la primera parada

    # para cada parada en la que se encuentre el servicio (a partir de la segunda)
    for p in indices_paradas[1:]:
        # si son paradas consecutivas
        if p - p_fin_periodo == 1:
            # si pertenecen a lineas distintas, se trata de periodos de trabajo distintos
            if globales.HORARIO_TRENES[p]['TREN'] != globales.HORARIO_TRENES[p_fin_periodo]['TREN']:
                nuevo_periodo = True
        else: # si no son paradas consecutivas
                

# calcula_periodos_trabajo(solucion, servicio, horario_trenes):
#     indices_servicio = obtiene_indices_servicio(solucion, servicio)
#     inicio_periodo = indices_servicio[0]
#     fin_periodo = inicio_periodo
#     for i in indices_servicio[1:]
#         if es_consecutiva(fin_periodo, i):
#             if horario_trenes[i].tren != fin_periodo.tren
#                 periodos += [inicio_periodo, fin_periodo]
#                 inicio_periodo = i
#         else
#             if horario_trenes[i].tiempo - horario_trenes[fin_periodo].tiempo >= tiempo_min_descanso
#                 periodos += [inicio_periodo, fin_periodo]
#                 inicio_periodo = i


# Función que valida que el servicio es consistente. Comprueba que el conductor no se encuentre en dos trenes distintos
# en algún momento.
def valida_servicio(indices_periodos_servicio):
    # para cada periodo de trabajo
    for i in range(0, len(indices_periodos_servicio), 1):
        # se obtienen la parada inicial y final del periodo, asi como el tiempo de inicio y fin
        inicio_i = calcula_inicio_servicio(indices_periodos_servicio[i])
        fin_i = indices_periodos_servicio[i][1]
        t_ini_i = globales.HORARIO_TRENES[inicio_i]['TIEMPO']
        t_fin_i = globales.HORARIO_TRENES[fin_i]['TIEMPO']

        # para cada periodo de trabajo a partir del actual
        for j in range(i+1, len(indices_periodos_servicio), 1):
            # se obtienen la parada inicial y final del periodo, asi como el tiempo de inicio y fin
            inicio_j = calcula_inicio_servicio(indices_periodos_servicio[j])
            fin_j = indices_periodos_servicio[j][1]
            t_ini_j = globales.HORARIO_TRENES[inicio_j]['TIEMPO']
            t_fin_j = globales.HORARIO_TRENES[fin_j]['TIEMPO']

            # se comprueba que los periodos no se solapan
            no_valido = t_ini_i <= t_ini_j <= t_fin_i               # el inicio del periodo j está dentro del periodo i
            no_valido = no_valido or t_ini_i <= t_fin_j <= t_fin_i  # el final del periodo j está dentro del periodo i
            no_valido = no_valido or t_ini_j <= t_ini_i <= t_fin_j  # el inicio del periodo i está dentro del periodo j
            no_valido = no_valido or t_ini_j <= t_fin_i <= t_fin_j  # el final del periodo i está dentro del periodo j

            # si se ha encontrado una inconsistencia, se termina la comprobación
            if no_valido:
                return False
    return True


# calcula los tiempos de trabajo y descanso de un servicio
# ahora mismo el tiempo entre periodos siempre es tiempo de descanso
def calcula_tiempos_servicio(indices_periodos_servicio):
    t_trabajo = 0                                   # tiempo de trabajo del servicio
    t_descanso = 0                                  # tiempo de descanso del servicio

    indice_ini = calcula_inicio_servicio(indices_periodos_servicio[0])
    t_fin_ant = globales.HORARIO_TRENES[indice_ini]['TIEMPO']

    # para cada periodo
    for periodo in indices_periodos_servicio:
        # se calcula el tiempo de trabajo del periodo
        indice_ini = calcula_inicio_servicio(periodo)
        t_ini = globales.HORARIO_TRENES[indice_ini]['TIEMPO']
        t_fin = globales.HORARIO_TRENES[periodo[1]]['TIEMPO']
        t_trabajo += t_fin - t_ini

        if t_ini - t_fin_ant < 0:
            print('tiempo de descanso negativo')

        t_descanso += t_ini - t_fin_ant
        t_fin_ant = t_fin

    return t_trabajo, t_descanso
