# -*- coding: utf-8 -*-
"""
Funciones del GRASP
Autor: Mario Rodríguez Chaves
"""

import globales as glo
import busqueda_local as bl
import greedy
import funciones_fitness as fitness
import exportacion_excel as excel
import funciones_auxiliares as aux

def GRASP(RLC, max_iter, max_iter_bl, max_vecinos_bl):
    glo.RESULTADOS_GRASP = []

    it = 0
    best_sol = []
    best_fit = 100000
    while it < max_iter:
        sol_ini = greedy.greedy(RLC)
        es_valido, fit_ini = fitness.funcion_objetivo(sol_ini)

        sol_act, fit_act = bl.busqueda_local(sol_ini, max_iter_bl, max_vecinos_bl)

        if fit_act < best_fit:
            best_sol = sol_act
            best_fit = fit_act

        it += 1
        print('it= ' + str(it) + ' ' + str(fit_act))
        print(sol_act)

        glo.RESULTADOS_GRASP.append([it, fit_act, sol_act])

    return best_sol, best_fit
