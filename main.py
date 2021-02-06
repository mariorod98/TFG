# -*- coding: utf-8 -*-
"""
Main
Autor: Mario Rodríguez Chaves
"""
import random as rnd
import numpy as np
import globales

import busqueda_local as bl
import funciones_auxiliares as aux
import exportacion_excel as ex
import greedy as greedy

rnd.seed(1)
path = ".\\entrada_prueba.json"
globales.init(path)

print(globales.HORARIO_TRENES)

# max_iter = 15000
# max_vecinos = len(globales.HORARIO_TRENES) * 100
#
# solucion_act = np.array(
# [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 0,
# 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2,
# 3, 3, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3])
#
# greedy.greedy(globales.N_SERVICIOS, globales.HORARIO_TRENES)

#
# n_iter, solucion, fitness = bl.busqueda_local(n_servicios, horario_trenes, max_iter, max_vecinos)
#
# for servicio in range(0, n_servicios, 1):
#     indices = aux.calcula_periodos_servicio(solucion, horario_trenes, servicio)
#     print(indices)
#     if indices != -1:
#         indices.sort(key=lambda x: horario_trenes[x[0]]['TIEMPO'])
#         t_trabajo, t_descanso = aux.calcula_tiempos_servicio(indices, horario_trenes)
#         print('t_trabajo: ' + str(t_trabajo) + ' t_descanso: ' + str(t_descanso))
#
#
# archivo = 'resultados.xlsx'
# titulo = 'a'
# sobreescribir = True
# ex.exportar_solucion(solucion, horario_trenes, archivo, titulo, sobreescribir)
