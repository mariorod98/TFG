# -*- coding: utf-8 -*-
"""
Funciones del algoritmo greedy
Autor: Mario Rodríguez Chaves
"""

import numpy as np
import random as rnd

import funciones_auxiliares as aux
import globales as glo


# devuelve el elemento más prometedor entre los candidatos
def obtiene_candidatos_posibles(posicion, ultimas_paradas, solucion):
    # se inicializa el array de candidatos
    candidatos = []

    for c in range(0, glo.N_SERVICIOS):
        sol_new = solucion.copy()
        sol_new[posicion] = c
        periodos = aux.calcula_periodos_servicio(sol_new, c)
        periodos_comprimidos = aux.comprime_periodos(periodos)
        es_valido = aux.valida_servicio(periodos, periodos_comprimidos)
        if es_valido:
            candidatos.append(c)

    return candidatos


def selecciona_candidato(posicion, candidatos, ultimas_paradas, RLC):
    seleccionado = -1

    # minimo = min(ultimas_paradas, key=lambda x: x['TIEMPO'])['TIEMPO']
    # seleccionados = [c for c in candidatos if ultimas_paradas[c]['TIEMPO'] == minimo]

    paradas_ordenadas  = [x for x in range(0, len(ultimas_paradas), 1)]
    paradas_ordenadas.sort(key=lambda x: ultimas_paradas[x]['TIEMPO'])

    seleccionados = []
    for p in paradas_ordenadas:
        if p in candidatos:
            seleccionados.append(p)

        if len(seleccionados) == RLC: break

    if seleccionados:
        tren = glo.HORARIO_TRENES[posicion]['TREN']
        mismo_tren = [x for x in candidatos if ultimas_paradas[x]['TREN'] == tren]

        if mismo_tren:
            seleccionados.append(mismo_tren[0])
        seleccionado = rnd.choice(seleccionados)

    return seleccionado


def greedy(RLC):
    # inicializamos la solución a vacio
    solucion = np.full([len(glo.HORARIO_TRENES)], -1)

    # inicializamos una lista con los indices de las paradas ordenados temporalmente
    paradas_ordenadas = [x for x in range(0, len(glo.HORARIO_TRENES))]
    paradas_ordenadas.sort(key=lambda x: glo.HORARIO_TRENES[x]['TIEMPO'])

    ultimas_paradas = []
    for i in range(0, glo.N_SERVICIOS):
        ultimas_paradas.append({'TREN': -1, 'PARADA': -1, 'TIEMPO': -1})

    penultimas_paradas = ultimas_paradas.copy()

    it = 0
    i = 0
    while i < len(paradas_ordenadas):
        pos = paradas_ordenadas[i]
        candidatos = obtiene_candidatos_posibles(pos, ultimas_paradas, solucion)
        seleccionado = selecciona_candidato(pos, candidatos, ultimas_paradas, RLC)

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
            it += 1
            if it >= 5000:
                print("Se han generado 5 000 soluciones Greedy y ninguna ha sido válida.")
                exit(-1)

    return solucion
