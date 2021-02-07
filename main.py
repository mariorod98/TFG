# -*- coding: utf-8 -*-
"""
Main
Autor: Mario Rodríguez Chaves
"""
import random as rnd
import numpy as np
import globales as glo

import busqueda_local as bl
import funciones_auxiliares as aux
import exportacion_excel as ex
import greedy as greedy

rnd.seed(1)
path = ".\\entrada_prueba.json"
glo.init(path)

print(glo.HORARIO_TRENES)

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

max_iter = 15000
max_vecinos = len(glo.HORARIO_TRENES) * 100

solucion_act = np.array(
[0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 0,
1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2,
3, 3, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3])


n_iter, solucion, fitness = bl.busqueda_local(max_iter, max_vecinos)

for servicio in range(0, glo.N_SERVICIOS, 1):
    indices = aux.calcula_periodos_servicio(solucion, servicio)
    print('periodos totales: ' + str(indices))
    print('periodos comprimidos: ' + str(aux.comprime_periodos(indices)))
    if indices != -1:
        indices.sort(key=lambda x: glo.HORARIO_TRENES[x[0]]['TIEMPO'])
        t_trabajo, t_descanso = aux.calcula_tiempos_servicio(indices)
        print('t_trabajo: ' + str(t_trabajo) + ' t_descanso: ' + str(t_descanso))


archivo = 'resultados.xlsx'
titulo = 'a'
sobreescribir = True
ex.exportar_solucion(solucion, archivo, titulo, sobreescribir)
