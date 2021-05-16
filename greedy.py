# -*- coding: utf-8 -*-
"""
Funciones del algoritmo greedy
Autor: Mario Rodríguez Chaves
"""

import numpy as np
import random as rnd

import funciones_auxiliares as aux
import globales as glo


# genera una lista con todos los candidatos FACTIBLES
def obtiene_candidatos_posibles(posicion, ultimas_paradas, solucion):
    # se inicializa el array de candidatos
    candidatos = []

    # para cada posible candidato
    for c in range(0, glo.N_SERVICIOS):
        # se genera una copia de la solución actual
        sol_new = solucion.copy()
        # se añade el candidato a la solución
        sol_new[posicion] = c
        # se comprueba si la solución es válida
        periodos = aux.calcula_periodos_servicio(sol_new, c)
        periodos_comprimidos = aux.comprime_periodos(periodos)
        es_valido = aux.valida_servicio(periodos, periodos_comprimidos)
        # si es válida, se añade el candidato a la lista
        if es_valido:
            candidatos.append(c)

    # se devuelve la lista con todos los candidatos factibles
    return candidatos


# Función que genera la LRC y selecciona un candidato de la lista de candidatos
def selecciona_candidato(posicion, candidatos, ultimas_paradas, LRC):
    seleccionado = -1

    # minimo = min(ultimas_paradas, key=lambda x: x['TIEMPO'])['TIEMPO']
    # seleccionados = [c for c in candidatos if ultimas_paradas[c]['TIEMPO'] == minimo]

    # se ordenan las tuplas de paradas segun la hora de llegada
    paradas_ordenadas  = [x for x in range(0, len(ultimas_paradas), 1)]
    paradas_ordenadas.sort(key=lambda x: ultimas_paradas[x]['TIEMPO'])

    # se inicializa la lista de candidatos
    seleccionados = []

    # para cada parada en orden temporal
    for p in paradas_ordenadas:
        # si la parada está en las candidatas
        if p in candidatos:
            seleccionados.append(p)

        if len(seleccionados) == LRC: break

    if seleccionados:
        tren = glo.HORARIO_TRENES[posicion]['TREN']
        mismo_tren = [x for x in candidatos if ultimas_paradas[x]['TREN'] == tren]

        if mismo_tren:
            seleccionados.append(mismo_tren[0])
        seleccionado = rnd.choice(seleccionados)

    return seleccionado


#   LRC: Lista restringida de candidatos
def greedy(LRC):
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
        seleccionado = selecciona_candidato(pos, candidatos, ultimas_paradas, LRC)

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
