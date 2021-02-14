# -*- coding: utf-8 -*-
"""
Funciones para crear un archivo xls
Autor: Mario Rodríguez Chaves
"""

from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
from openpyxl.chart import LineChart, Reference
import os.path

import globales as glo

colores = ['ea9999', 'ffe599', 'b6d7a8', 'a2c4c9', 'd199ea', 'eac099', '999eea', 'ea99c7', 'ffffff']
letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def abre_workbook(archivo, titulo, sobreescribir):
    if os.path.isfile(archivo) and not sobreescribir:
        wb = load_workbook(archivo)
    else:
        wb = Workbook()
        wb.remove(wb.active)

    wb.create_sheet(titulo)

    return wb


def exportar_solucion(solucion, archivo, titulo, sobreescribir):
    wb = abre_workbook(archivo, titulo, sobreescribir)
    ws = wb.worksheets[-1]

    columna = 0
    fila = 1
    i_ant = 0
    i = 0

    while i < len(solucion):
        if glo.HORARIO_TRENES[i]['TREN'] != glo.HORARIO_TRENES[i_ant]['TREN']:
            fila += 1
            columna = 0

        posicion = letras[columna] + str(fila)
        ws[posicion] = glo.HORARIO_TRENES[i]['TIEMPO']
        ws[posicion].fill = PatternFill(fill_type='solid',
                                        start_color=colores[solucion[i]],
                                        end_color=colores[solucion[i]])

        columna += 1
        i_ant = i
        i += 1

    wb.save(archivo)


def crear_grafico(archivo, titulo, sobreescribir):
    wb = abre_workbook(archivo, titulo, sobreescribir)
    ws = wb.worksheets[-1]

    iteraciones = [x for x, y, z in glo.RESULTADOS_GRASP]
    resultados = [y for x, y, z in glo.RESULTADOS_GRASP]

    # ws.append(iteraciones)
    # ws.append(resultados)

    for i in range(0, len(iteraciones)):
        ws.append([iteraciones[i], resultados[i]])

    values = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=len(iteraciones))
    chart = LineChart()
    chart.title = "Valor de la función fitness para cada iteración del algoritmo GRASP"
    chart.style = 13
    chart.y_axis.title = 'Fitness'
    chart.x_axis.title = 'Iteración'

    chart.add_data(values)

    ws.add_chart(chart, "E15")

    wb.save(archivo)
