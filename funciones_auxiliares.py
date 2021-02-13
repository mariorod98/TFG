# -*- coding: utf-8 -*-
"""
Funciones auxiliares
Autor: Mario Rodríguez Chaves
"""

import numpy as np

import globales as glo


# Función que devuelve los indices del array que tengan dicho valor
def obtiene_indices(array, valor):
    return np.where(array == valor)[0]


# si el periodo empieza en una parada intermedia, el intercambio de trabajadores se ha producido en la parada
# anterior, ya que a esta parada llega el trabajador del servicio actual. Por lo tanto, el trabajador empieza a
# trabajar en la parada anterior, que es cuando se produce el cambio de conductor. Si el periodo empieza en la
# primera parada del trayecto del tren, entonces se coge esa parada, ya que no hay una anterior.
def calcula_inicio_periodo(posicion):
    if posicion == 0 or glo.HORARIO_TRENES[posicion]['TREN'] != glo.HORARIO_TRENES[posicion - 1]['TREN']:
        return posicion
    else:
        return posicion - 1


# Función que calcula los periodos de trabajo de un servicio
# Trabaja con la solución ordenada temporalmente
# Primero se obtienen todos los periodos de paradas consecutivas
def calcula_periodos_servicio(solucion, servicio):
    periodos = []  # periodos de trabajo del servicio
    indices_paradas = obtiene_indices(solucion, servicio)  # paradas de trabajo del servicio

    # se ordenan los índices de forma temporal
    lista_aux = list(indices_paradas)
    lista_aux.sort(key=lambda x: glo.HORARIO_TRENES[x]['TIEMPO'])
    indices_paradas = np.array(lista_aux)

    # si el servicio no tiene paradas, se devuelve vacio
    if len(indices_paradas) == 0:
        return []

    # parada anterior a la actual, inicializado a la primera parada
    p_ini_periodo = calcula_inicio_periodo(indices_paradas[0])
    p_fin_periodo = indices_paradas[0]  # parada de inicio de un periodo de trabajo,

    # para cada parada en la que se encuentre el servicio (a partir de la segunda)
    for p in indices_paradas[1:]:
        # si la parada actual no es contigua a la anterior o si el tren es distinto,
        # entonces se ha cambiado de periodo de trabajo
        if p - p_fin_periodo > 1 or glo.HORARIO_TRENES[p_fin_periodo]['TREN'] != glo.HORARIO_TRENES[p]['TREN']:
            periodos.append([p_ini_periodo, p_fin_periodo])  # se añade el periodo
            p_ini_periodo = calcula_inicio_periodo(p)  # se inicia un nuevo periodo con la parada actual

        # se indica que la parada actual es la última parada del periodo
        p_fin_periodo = p

    # se añade el periodo final a la lista
    periodos.append([p_ini_periodo, p_fin_periodo])

    # se devuelve la lista de periodos final
    return periodos


def comprime_periodos(periodos):
    # se inicializa una lista vacia con los periodos finales
    periodos_comprimidos = []

    # para cada periodo de trabajo
    for periodo in periodos:
        # si la lista final no está vacía
        if periodos_comprimidos:
            # se calcula la diferencia de tiempos
            parada_fin = periodos_comprimidos[-1][1]
            parada_ini = periodo[0]
            diferencia_tiempos = glo.HORARIO_TRENES[parada_ini]['TIEMPO'] \
                                 - glo.HORARIO_TRENES[parada_fin]['TIEMPO']

            # si la diferencia de tiempos entre el periodo actual es un descanso, se añade
            # el periodo actual a la lista de periodos
            if diferencia_tiempos >= glo.T_MIN_DESCANSOS:
                periodos_comprimidos.append(periodo)
            else:  # si no hay tiempo para un descanso
                # se combina el periodo actual con el anterior para formar un mismo periodo
                periodos_comprimidos[-1][1] = periodo[1]
        else:  # si no hay elementos en la lista final, se añade el primero
            periodos_comprimidos.append(periodo)

    return periodos_comprimidos


# Función que valida que el servicio es consistente. Comprueba que el conductor no se encuentre en dos trenes distintos
# en algún momento.
def valida_servicio(periodos):
    # para cada periodo de trabajo
    for i in range(0, len(periodos), 1):
        # se obtienen la parada inicial y final del periodo, asi como el tiempo de inicio y fin
        inicio_i = periodos[i][0]
        fin_i = periodos[i][1]
        t_ini_i = glo.HORARIO_TRENES[inicio_i]['TIEMPO']
        t_fin_i = glo.HORARIO_TRENES[fin_i]['TIEMPO']

        # para cada periodo de trabajo a partir del actual
        for j in range(i + 1, len(periodos), 1):
            # se obtienen la parada inicial y final del periodo, asi como el tiempo de inicio y fin
            inicio_j = periodos[j][0]
            fin_j = periodos[j][1]
            t_ini_j = glo.HORARIO_TRENES[inicio_j]['TIEMPO']
            t_fin_j = glo.HORARIO_TRENES[fin_j]['TIEMPO']

            # se comprueba que los periodos no se solapan
            no_valido = t_ini_i <= t_ini_j <= t_fin_i  # el inicio del periodo j está dentro del periodo i
            no_valido = no_valido or t_ini_i <= t_fin_j <= t_fin_i  # el final del periodo j está dentro del periodo i
            no_valido = no_valido or t_ini_j <= t_ini_i <= t_fin_j  # el inicio del periodo i está dentro del periodo j
            no_valido = no_valido or t_ini_j <= t_fin_i <= t_fin_j  # el final del periodo i está dentro del periodo j

            # si se ha encontrado una inconsistencia, se termina la comprobación
            if no_valido:
                return False
    return True


# calcula los tiempos de trabajo y descanso de un servicio
# ahora mismo el tiempo entre periodos siempre es tiempo de descanso
def calcula_tiempos_servicio(periodos):
    t_trabajo = 0  # tiempo de trabajo del servicio
    t_descanso = 0  # tiempo de descanso del servicio
    t_fin_ant = False

    periodos_comprimidos = comprime_periodos(periodos)

    # para cada periodo
    for periodo in periodos_comprimidos:
        # se calcula el tiempo de trabajo del periodo
        t_ini = glo.HORARIO_TRENES[periodo[0]]['TIEMPO']
        t_fin = glo.HORARIO_TRENES[periodo[1]]['TIEMPO']
        t_trabajo += t_fin - t_ini

        if t_ini - t_fin_ant < 0:
            print('tiempo de descanso negativo')

        if t_fin_ant:
            t_descanso += t_ini - t_fin_ant

        t_fin_ant = t_fin

    return t_trabajo, t_descanso
