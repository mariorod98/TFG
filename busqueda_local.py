# -*- coding: utf-8 -*-
"""
Funciones de la búsqueda local
Autor: Mario Rodríguez Chaves
"""

import random as rnd

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

    # devolvemos el vecino generado
    return vecino


# fijamos la función de generación de vecinos que queremos usar
genera_vecino = genera_vecino_1


# función de búsqueda local
def busqueda_local(sol_ini, max_iter, max_vecinos):
    # inicializamos el contador
    iter_act = 0

    # se calcula la solucion inicial
    solucion_act = sol_ini
    fitness_act, t_trabajo, t_descanso  = fitness.funcion_objetivo(solucion_act)
    best_t_trabajo = t_trabajo
    best_t_descanso = t_descanso

    # bucle principal
    while iter_act < max_iter:
        vecinos_generados = 0
        vecino_encontrado = False

        # se generan vecinos hasta que se encuentre uno mejor o se llegue al máximo de vecinos generados
        while vecinos_generados < max_vecinos and not vecino_encontrado:
            # se genera una nueva solución vecina
            solucion_new = genera_vecino(solucion_act)
            # se comprueba que la solución es válida y se obtiene su fitness
            fitness_new, t_trabajo, t_descanso = fitness.funcion_objetivo(solucion_new)

            # si es válida y el fitness es mejor, se reemplaza la solución actual por la nueva
            if fitness_new < fitness_act:
                vecino_encontrado = True
                solucion_act = solucion_new
                fitness_act = fitness_new
                best_t_trabajo = t_trabajo
                best_t_descanso = t_descanso

            # se actualiza el número de vecinos generado
            vecinos_generados += 1

        # si se ha llegado al máximo de vecinos generados, se termina la búsqueda local
        if not vecino_encontrado:
            break

        # se aumenta el número de iteraciones realizadas
        iter_act += 1

    # devolvemos la solución obtenida y su fitness
    return solucion_act, fitness_act, best_t_trabajo, best_t_descanso
