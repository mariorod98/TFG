# -*- coding: utf-8 -*-
"""
Funciones de la búsqueda local
Autor: Mario Rodríguez Chaves
"""

import random as rnd
import numpy as np

import funciones_fitness as fitness
import globales as glo


# función que genera un vecino modificando el valor de una posición por otro
def genera_vecino_1(solucion):
    # generamos una copia de la solución
    vecino = solucion.copy()

    # obtenemos una posición aleatoria del vector y su valor
    pos = rnd.randint(0, len(solucion) - 1)
    valor = solucion[pos]

    # obtenemos un valor distinto
    while valor == solucion[pos]:
        valor = rnd.randint(0, glo.N_SERVICIOS - 1)

    # asignamos el valor al vecino
    vecino[pos] = valor

    # # si la posición escogida es la primera parada del metro, entonces hay que asignar también la segunda parada
    # # si la posición escogida es la segunda parada del metro, entonces hay que asignar también la primera parada
    # if pos == 0:
    #     # asignamos el valor al vecino
    #     vecino[pos] = valor
    #     vecino[pos + 1] = valor
    # elif pos == 1:
    #     # asignamos el valor al vecino
    #     vecino[pos] = valor
    #     vecino[pos - 1] = valor
    # else:
    #     tren_pos_act = glo.HORARIO_TRENES[pos]['TREN']
    #     tren_pos_1   = glo.HORARIO_TRENES[pos - 1]['TREN']
    #     tren_pos_2   = glo.HORARIO_TRENES[pos - 1]['TREN']
    #
    #     if tren_pos_act != tren_pos_1:
    #         # asignamos el valor al vecino
    #         vecino[pos] = valor
    #         vecino[pos + 1] = valor
    #     elif tren_pos_act == tren_pos_1 and tren_pos_act != tren_pos_2:
    #         # asignamos el valor al vecino
    #         vecino[pos] = valor
    #         vecino[pos - 1] = valor

    # devolvemos el vecino generado
    return vecino


# fijamos la función de generación de vecinos que queremos usar
genera_vecino = genera_vecino_1


# función de búsqueda local
def busqueda_local(sol_ini, max_iter, max_vecinos, almacena_resultados=False):
    # inicializamos el contador
    it = 0

    # si queremos mantener un registro de los resultados obtenidos
    if almacena_resultados:
        # se inicializa la variable de resultados a vacio
        glo.RESULTADOS = []

    # se calcula la solucion inicial
    sol_act = sol_ini
    fit_act, resultados_act  = fitness.funcion_objetivo(sol_act)

    # bucle principal
    while it < max_iter:
        vecinos_generados = 0
        vecino_encontrado = False

        # se generan vecinos hasta que se encuentre uno mejor o se llegue al máximo de vecinos generados
        while vecinos_generados < max_vecinos and not vecino_encontrado:
            # se genera una nueva solución vecina
            sol_new = genera_vecino(sol_act)
            # se comprueba que la solución es válida y se obtiene su fitness
            fit_new, resultados_new = fitness.funcion_objetivo(sol_new)

            # si es válida y el fitness es mejor, se reemplaza la solución actual por la nueva
            if fit_new < fit_act:
                vecino_encontrado = True
                sol_act = sol_new
                fit_act = fit_new
                resultados_act = resultados_new
                # print(sol_act)

                # si queremos mantener un registro de los resultados obtenidos
                if almacena_resultados:
                    # se almacena el resultado obtenido
                    glo.RESULTADOS.append([it, fit_act, resultados_act, sol_act])

            # se actualiza el número de vecinos generado
            vecinos_generados += 1

        # si se ha llegado al máximo de vecinos generados, se termina la búsqueda local
        if not vecino_encontrado:
            break

        # se aumenta el número de iteraciones realizadas
        it += 1

    # devolvemos la solución obtenida y su fitness
    return sol_act, fit_act, resultados_act
