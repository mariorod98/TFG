# -*- coding: utf-8 -*-
"""
Funciones para crear un archivo xls
Autor: Mario Rodríguez Chaves
"""

from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
import os.path

import globales as glo

colores = ['ea9999', 'ffe599', 'b6d7a8', 'a2c4c9', 'd199ea', 'eac099', '999eea', 'ea99c7', 'ffffff']


def exportar_solucion(solucion, archivo, titulo, sobreescribir):
    if os.path.isfile(archivo) and not sobreescribir:
        wb = load_workbook(archivo)
    else:
        wb = Workbook()
        wb.remove(wb.active)

    wb.create_sheet(titulo)
    ws = wb.worksheets[-1]

    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    columna = 0
    fila = 2
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
