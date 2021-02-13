# -*- coding: utf-8 -*-
"""
Main
Autor: Mario Rodríguez Chaves
"""
import random as rnd
import numpy as np
import globales as glo
import pprint

import busqueda_local as bl
import funciones_auxiliares as aux
import exportacion_excel as ex
import greedy as greedy

import funciones_fitness as fitness

rnd.seed(0)
path = ".\\entrada_prueba.json"
glo.init(path)

# solucion = greedy.greedy()
# print(solucion)
# print(fitness.funcion_objetivo_3(solucion))

muy_malas = 0
malas = 0
buenas = 0
total_negativos = 0

peor = []
peor_fit = 0
mejor = []
mejor_fit = 1000
mas_neg = []
for i in range(0, 20000):
    rnd.seed(i)
    solucion = greedy.greedy()
    sol_list = list(solucion)
    if -1 in solucion:
        if sol_list.count(-1) == 1:
            malas += 1
            archivo = 'resultados.xlsx'
            titulo = 'a'
            sobreescribir = False
            ex.exportar_solucion(solucion, archivo, titulo, sobreescribir)
        else:
            muy_malas += 1

        if sol_list.count(-1) > list(mas_neg).count(-1):
            mas_neg = solucion
        total_negativos += sol_list.count(-1)
    else:
        buenas += 1
        es_buena, fit_new = fitness.funcion_objetivo_3(solucion)

        if fit_new < mejor_fit:
            mejor_fit = fit_new
            mejor = solucion

        if fit_new > peor_fit:
            peor_fit = fit_new
            peor = solucion

print('Total de soluciones buenas: ' + str(buenas))
print('Total de soluciones malas: ' + str(malas))
print('Total de soluciones muy malas: ' + str(muy_malas))


print('\nPorcentaje de soluciones buenas: ' + str(buenas / (malas + muy_malas + buenas) * 100))
if malas or muy_malas:
    print('Negativos medios por solucion mala: ' + str(total_negativos / (malas + muy_malas)))

print('\nMejor solucion factible:')
print(mejor)
print(mejor_fit)

print('\nPeor solucion factible:')
print(peor)
print(peor_fit)

# solucion = np.array(
# [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 0,
# 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2,
# 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3])
#
# for servicio in range(0, glo.N_SERVICIOS, 1):
#     indices = aux.calcula_periodos_servicio(solucion, servicio)
#     print(indices)
#     if indices != -1:
#         t_trabajo, t_descanso = aux.calcula_tiempos_servicio(indices)
#         print('t_trabajo: ' + str(t_trabajo) + ' t_descanso: ' + str(t_descanso))
#
# max_iter = 15000
# max_vecinos = len(glo.HORARIO_TRENES) * 100

# solucion_act = np.array(
# [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 0,
# 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2,
# 3, 3, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3])
#
#
# n_iter, solucion, fitness = bl.busqueda_local(max_iter, max_vecinos)
#
# for servicio in range(0, glo.N_SERVICIOS, 1):
#     indices = aux.calcula_periodos_servicio(solucion, servicio)
#     print('periodos totales: ' + str(indices))
#     print('periodos comprimidos: ' + str(aux.comprime_periodos(indices)))
#     if indices != -1:
#         indices.sort(key=lambda x: glo.HORARIO_TRENES[x[0]]['TIEMPO'])
#         t_trabajo, t_descanso = aux.calcula_tiempos_servicio(indices)
#         print('t_trabajo: ' + str(t_trabajo) + ' t_descanso: ' + str(t_descanso))
#
#
# archivo = 'resultados.xlsx'
# titulo = 'a'
# sobreescribir = False
# ex.exportar_solucion(solucion, archivo, titulo, sobreescribir)
