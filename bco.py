# -*- coding: utf-8 -*-
"""
Funciones del algoritmo de Bee Colony Optimization
Autor: Mario Rodríguez Chaves
"""

from random import randrange, random, randint
import numpy as np
from math import floor
from copy import deepcopy

import globales as glo
from funciones_fitness import funcion_objetivo

sigma = 2


# def normaliza_datos(array):
#     maximo = max(array)
#     minimo = min(array)
#
#     dividendo = maximo - minimo
#
#     return [(valor - minimo) / dividendo for valor in array]


# Función que obtiene candidatos nuevos para la siguiente etapa de la solución
# Los candidatos se obtenen a partir de una normal con centro en el candidato de la posición anterior
def obtiene_candidatos(solucion, etapa):
    # CAMBIAR ESTO, NO TIENE ABSOLUTO SENTIDO
    candidatos = np.random.normal(solucion['solucion'][etapa - 1], sigma, [solucion['abejas']])
    return [floor(i) % glo.N_SERVICIOS for i in candidatos]


# Función que genera la nueva tanda de soluciones parciales a partir de las actuales
def genera_soluciones(sol_parciales, etapa):
    # se crea una nueva lista de soluciones parciales
    sol_parciales_new = []

    # por cada solución parcial
    for sol in sol_parciales:
        # se obtienen tantos candidatos como abejas tenga la solución
        candidatos = obtiene_candidatos(sol, etapa)

        # para cada candidato
        for c in candidatos:
            sol_new = {}
            sol_new['solucion'] = sol['solucion'].copy()
            # se añade el valor escogido a la posición de la etapa actual
            sol_new['solucion'][etapa] = c
            # se reinicia el número de abejas
            sol_new['abejas'] = 1
            sol_new['periodos'] = sol['periodos'].copy()
            sol_new['fit'] = 0

            # se añade la solución parcial a la lista de nuevas soluciones
            sol_parciales_new.append(sol_new)

            # # se crea una copia de la solución parcial actual
            # sol_new = deepcopy(sol)
            # # se añade el valor escogido a la posición de la etapa actual
            # sol_new['solucion'][etapa] = c
            # # se reinicia el número de abejas
            # sol_new['abejas'] = 1
            # # se añade la solución parcial a la lista de nuevas soluciones
            # sol_parciales_new.append(sol_new)

    # se devuelve la lista generada
    return sol_parciales_new


def bco(n_abejas, n_iteraciones):
    # se inicializa la variable de resultados a vacio
    glo.RESULTADOS = []

    media = 0
    n_etapas = 0

    best_sol = []
    best_periodos = []
    best_fit = float('inf')
    # worst_sol = {'fit': -1}

    # inicializamos una lista con los indices de las paradas ordenados temporalmente
    paradas_ordenadas = [x for x in range(0, len(glo.HORARIO_TRENES))]
    paradas_ordenadas.sort(key=lambda x: glo.HORARIO_TRENES[x]['TIEMPO'])

    # se inicializa el contador de iteraciones
    it = 0
    while it < n_iteraciones:
        # inicialización de las soluciones
        sol_parciales = []
        for b in range(n_abejas):
            # escogemos un valor aleatorio dentro del rango de servicios
            # valor = randrange(0, glo.N_SERVICIOS - 1)
            # inicializamos la solución a vacio (-1)
            sol = np.full([len(glo.HORARIO_TRENES)], -1)
            # asignamos el primer valor
            # sol[0] = valor
            sol_parciales.append({'abejas': 1, 'fit': 0, 'solucion': sol, 'periodos': [[] for i in range(0, glo.N_SERVICIOS)]})

        # se calcula la función fitness de todas las soluciones iniciales
        # for sol in sol_parciales:
        #     sol['fit'], resultados = funcion_objetivo(sol['solucion'], sol['periodos'], sol['solucion'])

        # para cada etapa de la solución
        for etapa in paradas_ordenadas:
            abejas_libres = 0

            # las abejas generan soluciones parciales
            sol_parciales = genera_soluciones(sol_parciales, etapa)

            # se calcula el valor fitness de las soluciones
            for sol in sol_parciales:
                sol['fit'], resultados = funcion_objetivo(sol['solucion'], sol['periodos'], [sol['solucion'][etapa]])

            # se obtiene el tamaño actual de la población de soluciones antes de que se descarten
            tamanio_ant = len(sol_parciales)

            # se eliminan las soluciones nulas
            # abejas_libres = sum(map(lambda x: x['fit'] == float('inf'), sol_parciales))
            sol_parciales = [sol for sol in sol_parciales if sol['fit'] != float('inf')]

            # se ordenan las soluciones de forma ascendente según su fitness
            sol_parciales.sort(key=lambda x: x['fit'])

            # se calcula el número de abejas que se mantienen en su solución y el número de abejas libres
            sol_parciales = [sol_parciales[i] for i in range(len(sol_parciales)) if i / (len(sol_parciales) * 1.5) < random()]
            abejas_libres += tamanio_ant - len(sol_parciales)

            media += abejas_libres / tamanio_ant
            n_etapas += 1

            # print("etapa: " + str(etapa))
            # print("media local: " + str(abejas_libres / tamanio_ant))
            # print("media global: " + str(media/n_etapas))
            # print("\n")

            # print(len(sol_parciales))

            if len(sol_parciales) == 0:
                # print("Sin soluciones parciales posibles")
                break

            # se asignan las abejas libres a las soluciones restantes
            for i in range(abejas_libres):
                pos = randint(0, len(sol_parciales) - 1)
                sol_parciales[pos]['abejas'] += 1

        if len(sol_parciales) > 0:
            for sol in sol_parciales:
                if sol['fit'] < best_fit:
                    best_sol = sol['solucion']
                    best_fit = sol['fit']
                    best_periodos = sol['periodos']

                # if sol['fit'] > worst_sol['fit']:
                #     worst_sol = deepcopy(sol)

            fit, resultados = funcion_objetivo(best_sol, best_periodos, [])
            glo.RESULTADOS.append([it, fit, resultados, best_sol])
            it += 1
            print("it " + str(it) + ": " + str(fit))
    
    return best_sol, best_fit
