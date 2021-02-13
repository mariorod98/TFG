# -*- coding: utf-8 -*-
"""
Funciones del algoritmo greedy para generar la solución inicial
Autor: Mario Rodríguez Chaves
"""

import numpy as np
import random as rnd

import funciones_auxiliares as aux
import globales as glo


# devuelve el elemento más prometedor entre los candidatos
def obtiene_candidatos_posibles(posicion, ultimas_paradas):
    # se inicializa el array de candidatos
    candidatos = []

    pos_ini = aux.calcula_inicio_periodo(posicion)
    # se obtiene el tiempo al que se llega a esa posicion
    t_posicion = glo.HORARIO_TRENES[pos_ini]['TIEMPO']

    for c in range(0, glo.N_SERVICIOS):
        # if c in ultimas_paradas:
        if ultimas_paradas[c]['TIEMPO'] <= t_posicion:
            candidatos.append(c)
        # else:
        #     candidatos.append(c)

    return candidatos


def selecciona_candidato(posicion, candidatos, ultimas_paradas):
    seleccionado = -1

    minimo = min(ultimas_paradas, key=lambda x: x['TIEMPO'])['TIEMPO']
    seleccionados = [c for c in candidatos if ultimas_paradas[c]['TIEMPO'] == minimo]

    if seleccionados:
        tren = glo.HORARIO_TRENES[posicion]['TREN']
        mismo_tren = [x for x in candidatos if ultimas_paradas[x]['TREN'] == tren]

        if mismo_tren:
            seleccionados.append(mismo_tren[0])

        seleccionado = rnd.choice(seleccionados)

    return seleccionado


def greedy():
    # inicializamos la solución a vacio
    solucion = np.empty([len(glo.HORARIO_TRENES)], dtype=np.int)

    # inicializamos una lista con los indices de las paradas ordenados temporalmente
    paradas_ordenadas = [x for x in range(0, len(glo.HORARIO_TRENES))]
    paradas_ordenadas.sort(key=lambda x: glo.HORARIO_TRENES[x]['TIEMPO'])

    ultimas_paradas = []
    for i in range(0, glo.N_SERVICIOS):
        ultimas_paradas.append({'TREN': -1, 'PARADA': -1, 'TIEMPO': -1})

    penultimas_paradas = ultimas_paradas.copy()

    i = 0
    while i < len(paradas_ordenadas):
        pos = paradas_ordenadas[i]
        candidatos = obtiene_candidatos_posibles(pos, ultimas_paradas)
        seleccionado = selecciona_candidato(pos, candidatos, ultimas_paradas)

        if seleccionado != -1:
            solucion[pos] = seleccionado
            penultimas_paradas[seleccionado] = ultimas_paradas[seleccionado]
            ultimas_paradas[seleccionado] = glo.HORARIO_TRENES[pos]
            i += 1
        else:
            parada_minima = min(ultimas_paradas, key=lambda x: x['TIEMPO'])
            indice = glo.HORARIO_TRENES.index(parada_minima)
            i = paradas_ordenadas.index(indice)
            ultimas_paradas = penultimas_paradas.copy()


    return solucion