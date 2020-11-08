# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:30:17 2020

@author: mario
"""

import json
import pprint

path = ".\\entrada.json"


def lee_entrada(archivo):
    datos = {}
    t_distinta_parada = []
    t_misma_parada = []

    # se abre el archivo que contiene el json
    with open(archivo, 'r') as json_file:
        datos = json.load(json_file)

    # se almacenan las paradas de cambio de conductores
    cambios = datos["P_CAMBIO"]
    cambio_old = cambios[0]

    # se añade el tramo de ida y vuelta de la primera parada
    t_misma_parada.append({'inicio': cambios[0], 'fin': cambios[0], 'tiempo': 0})

    # para cada parada de cambio (excepto la primera y la última)
    for cambio in cambios[1:]:
        # se añade el tramo a la lista de paradas
        t_distinta_parada.append({'inicio': cambio_old, 'fin': cambio, 'tiempo': 0})
        t_distinta_parada.append({'inicio': cambio, 'fin': cambio_old, 'tiempo': 0})

        # se almacena la parada actual en cambio_old
        cambio_old = cambio

    # se añade el tramo de ida y vuelta de la segunda parada
    t_misma_parada.append({'inicio': cambios[-1], 'fin': cambios[-1], 'tiempo': 0})

    t_ida = datos['T_IDA']
    t_vuelta = datos['T_VUELTA']

    p_ini = 1
    p_fin = t_misma_parada[0]['inicio']

    while p_ini < p_fin:
        t_misma_parada[0]['tiempo'] += t_ida[p_ini - 1] + t_vuelta[p_ini - 1]
        p_ini += 1

    t_misma_parada[0]['tiempo'] += datos['T_FINAL_1']

    p_ini = t_misma_parada[1]['inicio']
    p_fin = datos['N_PARADAS']

    while p_ini < p_fin:
        t_misma_parada[1]['tiempo'] += t_ida[p_ini - 1] + t_vuelta[p_ini - 1]
        p_ini += 1

    t_misma_parada[1]['tiempo'] += datos['T_FINAL_N']

    for tramo in t_distinta_parada:
        if tramo['inicio'] < tramo['fin']:
            p_ini = tramo['inicio']
            p_fin = tramo['fin']

            while p_ini < p_fin:
                tramo['tiempo'] += t_ida[p_ini - 1]
                p_ini += 1
        else:
            p_ini = tramo['fin']
            p_fin = tramo['inicio']
            while p_ini < p_fin:
                tramo['tiempo'] += t_vuelta[p_ini - 1]
                p_ini += 1

    tiempos = t_misma_parada + t_distinta_parada
    return tiempos


pprint.pprint(lee_entrada(path))
