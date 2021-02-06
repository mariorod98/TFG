# -*- coding: utf-8 -*-
"""
Funciones de la búsqueda local
Autor: Mario Rodríguez Chaves
"""

import random as rnd
import numpy as np

import funciones_fitness as fitness


# Función que genera un vecino modificando el valor de una posición
def genera_vecino_1(solucion, n_servicios):
    vecino = solucion.copy()
    pos = rnd.randint(0, len(solucion) - 1)
    valor = solucion[pos]

    while valor == solucion[pos]:
        valor = rnd.randint(0, n_servicios - 1)

    vecino[pos] = valor

    return vecino


def genera_vecino_2(solucion, n_servicios):
    vecino = solucion.copy()
    pos_ini = max(rnd.randint(0, len(solucion) - 1), 0)
    pos_fin = min(rnd.randint(pos_ini - 2, pos_ini + 2), len(solucion))
    valor = rnd.randint(0, n_servicios - 1)

    vecino[pos_ini:pos_fin] = valor
    return vecino


def busqueda_local(n_servicios, max_iter, max_vecinos):
    iter_act = 0

    # se calcula la solucion inicial
    # solucion_act = np.array(
                 # [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 0,
                 # 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2,
                 # 3, 3, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3])
    solucion_act=np.array(
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
    fitness_act = fitness.funcion_objetivo_3(n_servicios, solucion_act)[1]

    # bucle principal
    while iter_act < max_iter:
        vecinos_generados = 0
        vecino_encontrado = False

        print('iter: ' + str(iter_act))
        print(solucion_act)
        print(fitness_act)
        # se generan vecinos hasta que se encuentre uno mejor o se llegue al máximo de vecinos generados
        while vecinos_generados < max_vecinos and not vecino_encontrado:
            # se genera una nueva solución vecina
            solucion_new = genera_vecino_2(solucion_act, n_servicios)
            # se comprueba que la solución es válida y se obtiene su fitness
            es_valida, fitness_new = fitness.funcion_objetivo_3(n_servicios, solucion_new)

            # si es válida y el fitness es mejor, se reemplaza la solución actual por la nueva
            if es_valida and fitness_new < fitness_act:
                vecino_encontrado = True
                solucion_act = solucion_new
                fitness_act = fitness_new

            # se actualiza el número de vecinos generado
            vecinos_generados += 1

        # si se ha llegado al máximo de vecinos generados, se termina la búsqueda local
        if not vecino_encontrado:
            break

        # se aumenta el número de iteraciones realizadas
        iter_act += 1

    return iter_act, solucion_act, fitness_act
