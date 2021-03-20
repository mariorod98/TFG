# -*- coding: utf-8 -*-
"""
Funciones del GRASP
Autor: Mario Rodríguez Chaves
"""

import globales as glo
import busqueda_local as bl
import greedy


# función GRASP
def GRASP(LRC, max_iter, max_iter_bl, max_vecinos_bl):
    # se inicializa la variable de resultados a vacio
    glo.RESULTADOS = []

    # se inicializa el contador y la solución inicial
    it = 0
    best_sol = []
    best_fit = 100000

    # para cada iteración
    while it < max_iter:
        # se genera una solución inicial a partir del greedy
        sol_ini = greedy.greedy(LRC)
        # se aplica una búsqueda local a la solución generada
        sol_act, fit_act, resultados = bl.busqueda_local(sol_ini, max_iter_bl, max_vecinos_bl)

        # si la solución actual es mejor que la mejor encontrada, se modifica la mejor
        if fit_act < best_fit:
            best_sol = sol_act
            best_fit = fit_act

        # se aumenta el contador
        it += 1

        print('it= ' + str(it) + ' ' + str(fit_act))
        # print(sol_act)

        # se almacenan los resultados
        glo.RESULTADOS.append([it, fit_act, resultados, sol_act])

    # se devuelve la mejor solución y su fitness
    return best_sol, best_fit
