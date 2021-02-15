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

rnd.seed(125)
path = ".\\entrada_prueba.json"
glo.init(path)

# Se inicializan los parámetros
max_iter = 15000
max_vecinos = len(glo.HORARIO_TRENES) * 100
LRC = 2
sol_ini = greedy.greedy(LRC)


################################
# BUSQUEDA LOCAL               #
################################

# se ejecuta la búsqueda local
solucion, fit = bl.busqueda_local(sol_ini, max_iter, max_vecinos)

print('BUSQUEDA LOCAL')
print(solucion)
print('fit: ' + str(fit))

# se almacena la solución obtenida
archivo = 'resultados_2.xlsx'
titulo = 'best_bl'
sobreescribir = True
excel.exportar_solucion(solucion, archivo, titulo, sobreescribir)


################################
# ENFRIAMIENTO SIMULADO        #
################################

# se ejecuta el enfriamiento simulado
solucion, fit = es.enfriamiento_simulado(sol_ini, max_iter)

print('\nENFRIAMIENTO SIMULADO')
print(solucion)
print('fit: ' + str(fit))

# se almacena la solución obtenida
archivo = 'resultados_2.xlsx'
titulo = 'best_es'
sobreescribir = False
excel.exportar_solucion(solucion, archivo, titulo, sobreescribir)

# se almacenan el gráfico de progresión del algoritmo
archivo = 'resultados_2.xlsx'
titulo = 'grafico_es'
sobreescribir = False
titulo_grafico = 'Valor de la función fitness para cada iteración del Enfriamiento Simulado'
excel.crear_grafico(titulo_grafico, archivo, titulo, sobreescribir)


################################
# GRASP                        #
################################

# se asignan los valores de los parámetros
max_iter = 200
max_iter_bl = 5000
max_vecinos_bl = 2500

# se ejecuta el GRASP
sol, fit = grasp.GRASP(LRC, max_iter, max_iter_bl, max_vecinos_bl)

print('\nGRASP')
print(solucion)
print('fit: ' + str(fit))

# se almacena la solución obtenida
archivo = 'resultados_2.xlsx'
titulo = 'best_grasp'
sobreescribir = False
excel.exportar_solucion(solucion, archivo, titulo, sobreescribir)

# se almacenan el gráfico de progresión del algoritmo
archivo = 'resultados_2.xlsx'
titulo = 'grafico_grasp'
sobreescribir = False
titulo_grafico = 'Valor de la función fitness para cada iteración del algoritmo GRASP'
excel.crear_grafico(titulo_grafico, archivo, titulo, sobreescribir)


