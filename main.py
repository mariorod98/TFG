# -*- coding: utf-8 -*-
"""
Main
Autor: Mario Rodríguez Chaves
"""

import random as rnd

import globales as glo
import busqueda_local as bl
import grasp
import greedy
import enfriamiento_simulado as es
import exportacion_excel as excel

rnd.seed(100)
# path = ".\\entrada_prueba.json"
path = ".\\metro_granada.json"
archivo_resultados = 'resultados.xlsx'
glo.init(path)

# Se inicializan los parámetros
max_iter = 50000
max_vecinos = len(glo.HORARIO_TRENES) * 20
LRC = 2
sol_ini = greedy.greedy(LRC)

################################
# BUSQUEDA LOCAL               #
################################

# se ejecuta la búsqueda local
solucion, fit, resultados = bl.busqueda_local(sol_ini, max_iter, max_vecinos, True)

print('BUSQUEDA LOCAL')
print(solucion)
print('fit: ' + str(fit))

# se almacena la solución obtenida
# excel.exportar_solucion(solucion, archivo_resultados, 'bl_best', True)
excel.crear_hoja_servicios(solucion, archivo_resultados, 'bl_horario', True)

# se almacenan el gráfico de progresión del algoritmo
titulo_grafico = 'Resultados para cada iteración de la Búsqueda Local'
excel.aniade_graficos(titulo_grafico, archivo_resultados, 'bl_graficos', False)

################################
# ENFRIAMIENTO SIMULADO        #
################################
max_iter = 20000
# se ejecuta el enfriamiento simulado
solucion, fit = es.enfriamiento_simulado(sol_ini, max_iter)

print('\nENFRIAMIENTO SIMULADO')
print(solucion)
print('fit: ' + str(fit))

# se almacena la solución obtenida
# excel.exportar_solucion(solucion, archivo_resultados, 'es_best', False)
excel.crear_hoja_servicios(solucion, archivo_resultados, 'es_horario', False)

# se almacenan el gráfico de progresión del algoritmo
titulo_grafico = 'Resultados para cada iteración del Enfriamiento Simulado'
excel.aniade_graficos(titulo_grafico, archivo_resultados, 'es_graficos', False, True)


# ################################
# # GRASP                        #
# ################################
#
# # se asignan los valores de los parámetros
# max_iter = 10
# max_iter_bl = 3000
# max_vecinos_bl = 2000
#
# # se ejecuta el GRASP
# solucion, fit = grasp.GRASP(LRC, max_iter, max_iter_bl, max_vecinos_bl)
#
# print('\nGRASP')
# print(solucion)
# print('fit: ' + str(fit))
#
# # se almacena la solución obtenida
# # excel.exportar_solucion(solucion, archivo_resultados, 'grasp_best', False)
# excel.crear_hoja_servicios(solucion, archivo_resultados, 'grasp_horario', False)
#
# # se almacenan el gráfico de progresión del algoritmo
# titulo_grafico = 'Resultados para cada iteración del algoritmo GRASP'
# excel.aniade_graficos(titulo_grafico, archivo_resultados, 'grasp_graficos', False)

