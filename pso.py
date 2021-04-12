# -*- coding: utf-8 -*-
"""
Funciones del algoritmo de Enfriamiento Simulado
Autor: Mario Rodríguez Chaves
"""
from random import uniform, randrange, random
from math import floor

from greedy import greedy
import funciones_fitness as fitness
import globales as glo


# Función obtiene vecindario
#   Devuelve el vecindario social de una partícula
# Parámetros de entrada
#   poblacion: lista que contiene la población de partículas
#   id_particula: índice de la partícula dentro de la lista de población
#   tam_vecindario: número de vecinos que tiene la particula
# Return: vecindario de la partícula
def obtiene_vecindario(poblacion, id_particula, tam_vecindario):
    # se calculan los vecinos que tiene la partícula a su izquierda
    izq = id_particula % tam_vecindario
    # se calculan los vecinos que tiene la partícula a su derecha
    dcha = min(id_particula + (tam_vecindario - izq - 1), len(poblacion))
    # se obtiene el vecindario de la partícula, incluida esta misma
    vecindario = [poblacion[p] for p in range(id_particula - izq, dcha + 1)]

    # se devuelve el vecindario obtenido
    return vecindario


# Función encuentra_mejor_vecindario
#   Función que encuentra a la particula con mejor fitness dentro del vecindario de otra partícula
# Parámetros de entrada
#   poblacion: lista que contiene la población de partículas
#   id_particula: índice de la partícula dentro de la lista de población
#   tam_vecindario: número de vecinos que tiene la particula
# Return: vecino con mejor fitness de la partícula (puede ser ella misma)
def encuentra_mejor_vecindario(poblacion, id_particula, tam_vecindario):
    # se obtiene el vecindario de la partícula
    vecindario = obtiene_vecindario(poblacion, id_particula, tam_vecindario)
    # se ordena en orden ascendente del valor del mejor fitness de la partícula
    vecindario.sort(key=lambda x: x['p_fitness'])

    # se devuelve el mejor vecino, el de fitness más bajo
    return vecindario[0]


# Función calcula_velocidad
#   Calcula la velocidad actual de una partícula
# Parámetros de entrada
#   particula: particula a la que se le va a calcular la velocidad
#   best_vecino: particula vecina con la mejor fitness que será usada para calcular la dirección de la partícula
def calcula_velocidad(particula, best_vecino):
    # se fijan los pesos de los componentes cognitivo y social
    p1 = p2 = 2

    # se calcula el componente cognitivo a partir de la mejor solución encontrada por la partícula
    cognitivo = p1 * random() * (particula['p_best'] - particula['X'])

    # se calcula el componente social a partir de la mejor solución de su vecindario
    social = p2 * random() * (best_vecino['p_best'] - particula['X'])

    # se sobreescribe la velocidad de la partícula añadiendo los componentes cognitivo y social a la velocidad actual
    particula['V'] = [particula['V'][i] + cognitivo[i] + social[i] for i in range(len(particula['V']))]


# Función desplaza_particula
#   Desplaza a la particula según su velocidad calculada anteriormente
# Parámetros de entrada
#   particula: particula que va a ser desplazada
def desplaza_particula(particula):
    # se desplaza la particula añadiendo su velocidad a su posición actual
    particula['X'] = [floor((particula['X'][i] + particula['V'][i]) % glo.N_SERVICIOS) for i in range(len(particula['X']))]


# Algoritmo PSO
#   Este algoritmo genera una población de partículas que se desplazan por el entorno de búsqueda
#   con una velocidad y dirección variables en cada iteración que les guía hacia mejores resultados
# Parámetros de entrada
#   tam_pob: tamaño de la población de partículas
#   tam_vec: tamaño del vecindario de una partícula
#   max_vel: máxima velocidad a la que puede ir una partícula
#   max_it:  número de iteraciones a realizar
#   LRC:     tamaño máximo de la lista de candidatos del algoritmo greedy
def pso(tam_pob, tam_vec, max_vel, max_it, LRC):
    # se inicializa la variable de resultados a vacio
    glo.RESULTADOS = []

    n_ev = 0
    n_inf = 0

    # se inicializa la mejor solución
    global_best = []
    global_best_fit = float('inf')
    global_best_res = []

    # se inicializa la población
    pob_actual = []
    for i in range(tam_pob):
        # se crea una partícula vacía
        particula = {}
        # se obtiene la solución inicial a partir de un greedy
        solucion = greedy(LRC)
        particula['X'] = solucion.copy()
        # se asigna la mejor solución a la solución inicial
        particula['p_best'] = solucion.copy()
        # se obtiene las velocidades inicial de forma aleatoria
        particula['V'] = [randrange(-max_vel, max_vel) for i in range(len(solucion))]
        # se fijan los fitness iniciales a inf (se calculan en la primera etapa del algoritmo)
        particula['x_fitness'] = float('inf')
        particula['p_fitness'] = float('inf')
        # se añade la partícula a la población
        pob_actual.append(particula)

    # se inicializa el contador de iteraciones
    it = 0

    # mientras no se llegue al máximo de iteraciones
    while it < max_it:
        # primero se calculan los fitness obtenidos
        #para cada partícula
        for particula in pob_actual:
            # se evalua la función objetivo
            particula['periodos'] = [[] for i in range(0, glo.N_SERVICIOS)]
            glo.MODIFICADOS = [i for i in range(0, glo.N_SERVICIOS)]
            fit, resultados = fitness.funcion_objetivo(particula['X'], particula['periodos'])
            particula['x_fitness'] = fit

            n_ev += 1
            if fit == float('inf'):
                n_inf += 1

            # si la posición actual es mejor que pBest, se fija la actual a pBest
            if fit < particula['p_fitness']:
                particula['p_fitness'] = fit
                particula['p_best'] = particula['X'].copy()

                # si la solución es mejor que la mejor global, se actualiza la mejor global
                if fit < global_best_fit:
                    global_best = particula['X'].copy()
                    global_best_fit = fit
                    global_best_res = resultados

        # ddespués se calcula la velocidad de la partícula y se desplaza
        # para cada partícula
        for p in range(tam_pob):
            particula = pob_actual[p]
            # se obtiene el mejor vecino
            best_vecino = encuentra_mejor_vecindario(pob_actual, p, tam_vec)
            # se calcula su nueva velocidad
            calcula_velocidad(particula, best_vecino)
            # se desplaza la partícula
            desplaza_particula(particula)

        # se aumenta el número de iteraciones
        it += 1

        # se almacenan los resultados
        glo.RESULTADOS.append([it, global_best_fit, global_best_res, global_best])

    print("Totales: " + str(n_ev))
    print("Válidas: " + str(n_ev - n_inf))
    print("No válidas: " + str(n_inf))
    print("% No válidas: " + str((n_inf / n_ev) * 100))

    # se devuelve la mejor solución encontrada
    return global_best, global_best_fit
