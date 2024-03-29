# -*- coding: utf-8 -*-
"""
Funciones del algoritmo de Enfriamiento Simulado
Autor: Mario Rodríguez Chaves
"""

from math import log, exp
from random import uniform

import globales as glo
import funciones_fitness as fitness
import busqueda_local as bl

# se indica cual es la función de generación de vecinos
genera_vecino = bl.genera_vecino


# algoritmo de enfriamiento simulado
def enfriamiento_simulado(sol_ini, max_iter):
    # se inicializa la variable de resultados a vacio
    glo.RESULTADOS = []

    # se inicializa la solucion actual y se calcula su fitness
    sol_act = sol_ini
    periodos_sol_act = [[] for i in range(0, glo.N_SERVICIOS)]
    glo.MODIFICADOS = [i for i in range(0, glo.N_SERVICIOS)]
    fit_act, resultados = fitness.funcion_objetivo(sol_ini, periodos_sol_act)

    # se inicializa la mejor solucion a la solucion actual
    best_sol = sol_act
    best_fit = fit_act

    # se inicializa el número de vecinos máximos por iteracion
    max_vecinos = 10 * len(sol_act)
    # se inicializa el valor de M
    M = max_iter / max_vecinos

    # se inicializa el valor inicial de temperatura a partir del fit obtenido
    mu = 0.3
    fi = mu
    # T = mu * fit_act / (-log(fi))
    T = 100
    # T_fin = 0.001
    # beta = (T - T_fin) / (M * T * T_fin)

    # se inicializa el iterador
    n_exitos = 1
    it = 0

    # mientras que se haya encontrado solución y muentras no se haya llegado al número máximo de iteraciones
    while n_exitos > 0 and it < max_iter:

        # se inicializa los contadores a 0
        n_vecinos = 0
        n_exitos = 0

        # mientras no se haya generado el número máximo de vecinos
        while n_vecinos < max_vecinos:
            # se genera un vecino nuevo
            sol_new = genera_vecino(sol_act)
            periodos_sol_new = periodos_sol_act.copy()
            # se comprueba que la solución es válida y se obtiene su fitness
            fit_new, resultados = fitness.funcion_objetivo(sol_new, periodos_sol_new)

            # si la solución es válida
            if fit_new != float('inf'):
                # se obtiene la diferencia entre el fit nuevo y el actual
                dif = fit_new - fit_act
                # se obtienen una probabilidad y se calcula el nivel de aceptación de la solución
                prob = uniform(0.0, 1.0)

                aceptacion = float('inf')
                if dif > 0:
                    aceptacion = exp(-dif / T)

                # si la solución es mejor o si se acepta la solución
                if dif < 0 or prob < aceptacion:

                    # if dif >= 0:
                    #     print('\nit = %d' % it)
                    #     print('T = %f' % T)
                    #     print('dif = %f' % dif)
                    #     print(-dif / T)
                    #     print('aceptacion = %f' % aceptacion)

                    # se fija la solución actual a la solución nueva
                    n_exitos += 1
                    sol_act = sol_new
                    fit_act = fit_new
                    periodos_sol_act = periodos_sol_new

                    resultados['temperatura'] = T
                    resultados['aceptacion'] = aceptacion

                    # se almacena el resultado obtenido
                    glo.RESULTADOS.append([it, fit_act, resultados, sol_act])

                    # si la solución obtenida es mejor que la mejor actual, se modifica la solucion mejor
                    if fit_act < best_fit:
                        best_sol = sol_act
                        best_fit = fit_act

            # se aumentan los contadores
            it += 1
            n_vecinos += 1

        # se calcula el nuevo grado de temperatura
        # T = T / (1 + beta * T)
        T = T * 0.9

    # se devuelve la mejor solución y su fit
    return best_sol, best_fit
