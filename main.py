# -*- coding: utf-8 -*-
"""
Main
Autor: Mario Rodríguez Chaves
"""

import random as rnd
import numpy as np
import pprint

import globales as glo
import busqueda_local as bl
import grasp
import greedy
import exportacion_excel as excel
import funciones_fitness as fitness

rnd.seed(0)
path = ".\\entrada_prueba.json"
glo.init(path)

max_iter = 200
max_iter_bl = 2000
max_vecinos_bl = 2000

RLC = 2
sol, fit = grasp.GRASP(RLC, max_iter, max_iter_bl, max_vecinos_bl)

iteraciones = [x for x, y, z in glo.RESULTADOS_GRASP]
resultados  = [y for x, y, z in glo.RESULTADOS_GRASP]

archivo = 'grasp.xlsx'
titulo = 'resultados por iteraciones'
sobreescribir = True

excel.crear_grafico(archivo, titulo, sobreescribir)
#
#
#

# max_iter = 15000
# max_vecinos = len(glo.HORARIO_TRENES) * 100
#
# solucion_act = np.array(
# [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 0,
# 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2,
# 3, 3, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3])
#
# solucion, fitness = bl.busqueda_local(solucion_act, max_iter, max_vecinos)
# print(fitness)
#
# archivo = 'resultados.xlsx'
# titulo = 'a'
# sobreescribir = False
# excel.exportar_solucion(solucion, archivo, titulo, sobreescribir)
