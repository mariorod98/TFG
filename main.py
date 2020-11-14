# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 17:30:17 2020

@author: mario
"""

import json
import pprint as pp

path = ".\\entrada.json"


def sort_func(dic):
    return dic['inicio'], dic['fin']


def lee_entrada(archivo):
    # se abre el archivo que contiene el json
    with open(archivo, 'r') as json_file:
        datos = json.load(json_file)

    return datos


def calcula_tramos_old(datos):
    t_distinta_parada = []
    t_misma_parada = []
    tiempos = []

    # se almacenan las paradas de cambio de conductores
    cambios = datos["P_CAMBIO"]
    cambio_old = cambios[0]

    # se añade el tramo de ida y vuelta de la primera parada
    t_misma_parada.append({'inicio': cambios[0], 'fin': cambios[0], 'tiempo': 0})

    # para cada parada de cambio (excepto la primera y la última)
    for cambio in cambios[1:]:
        # se añade el tramo a la lista de paradas
        t_distinta_parada.append({'inicio': cambio_old, 'fin': cambio, 'direccion': 1, 'tiempo': 0})
        t_distinta_parada.append({'inicio': cambio, 'fin': cambio_old, 'direccion': -1, 'tiempo': 0})

        # se almacena la parada actual en cambio_old
        cambio_old = cambio

    # se añade el tramo de ida y vuelta de la segunda parada
    t_misma_parada.append({'inicio': cambios[-1], 'fin': cambios[-1], 'tiempo': 0})

    # se almacenan los tiempos de ida y vuelta en listas
    t_ida = datos['T_IDA']
    t_vuelta = datos['T_VUELTA']

    # para la primera parada de cambio, se calcula el tiempo de ida y vuelta entre esta parada y el inicio de la línea
    p_ini = 1
    p_fin = t_misma_parada[0]['inicio']
    tiempos.append(t_misma_parada[0])

    while p_ini < p_fin:
        tiempos[0]['tiempo'] += t_ida[p_ini - 1] + t_vuelta[p_ini - 1]
        p_ini += 1

    tiempos[0]['tiempo'] += datos['T_FINAL_1']

    # para la última parada de cambio, se calcula el tiempo de ida y vuetla entre esta parada y el fin de la línea
    p_ini = t_misma_parada[-1]['inicio']
    p_fin = datos['N_PARADAS']
    tiempos.append(t_misma_parada[-1])

    while p_ini < p_fin:
        tiempos[-1]['tiempo'] += t_ida[p_ini - 1] + t_vuelta[p_ini - 1]
        p_ini += 1

    tiempos[-1]['tiempo'] += datos['T_FINAL_N']

    # para el resto de paradas, se calcula el recorrido
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

    tiempos = tiempos + t_distinta_parada
    return sorted(tiempos, key=sort_func)


# función que calcula los tramos entre paradas y el tiempo que se tarda en recorrer cada tramo
# entrada:
#   datos: diccionario con los datos iniciales del problema
# salida:
#   t_parada: diccionario con los tramos de la vía y el tiempo en recorrer cada tramo
def calcula_tramos(datos):
    t_parada = []
    tiempos = []

    # se almacenan los tiempos de ida y vuelta en listas
    t_ida = datos['T_IDA']
    t_vuelta = datos['T_VUELTA']
    n_paradas = datos['N_PARADAS']

    # se almacenan las paradas de cambio de conductores
    cambios = datos["P_CAMBIO"]
    cambio_old = cambios[0]

    # se añade el tramo inicial a la lista de paradas
    t_parada.append({'inicio': 1, 'fin': cambios[0], 'direccion': 1, 'tiempo': 0})
    t_parada.append({'inicio': cambios[0], 'fin': 1, 'direccion': -1, 'tiempo': 0})

    # para cada parada de cambio (excepto la primera y la última)
    for cambio in cambios[1:]:
        # se añade el tramo a la lista de paradas
        t_parada.append({'inicio': cambio_old, 'fin': cambio, 'direccion': 1, 'tiempo': 0})
        t_parada.append({'inicio': cambio, 'fin': cambio_old, 'direccion': -1, 'tiempo': 0})
        # se almacena la parada actual en cambio_old
        cambio_old = cambio

    # se añade el tramo final a la lista de paradas
    t_parada.append({'inicio': cambio_old, 'fin': n_paradas, 'direccion': 1, 'tiempo': 0})
    t_parada.append({'inicio': n_paradas, 'fin': cambio_old, 'direccion': -1, 'tiempo': 0})

    # para el resto de paradas, se calcula el recorrido
    for tramo in t_parada:
        if tramo['direccion'] > 0:
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

    # se devuelven las paradas ordenadas por la parada inicial
    return sorted(t_parada, key=sort_func)


# función que calcula el horario de un tren en tramos realizados y la hora a la que llega a cada tramo
def calcula_horario(datos, tramos):
    paradas = datos['P_CAMBIO']
    t_act = datos['INI_JORNADA']
    t_fin = datos['FIN_JORNADA']
    direccion = datos['DIR_SALIDA']

    if 1 not in paradas:
        paradas = [1] + paradas

    if datos['N_PARADAS'] not in paradas:
        paradas = paradas + [datos['N_PARADAS']]

    p_ant = paradas.index(datos['P_SALIDA'])
    p_act = p_ant

    horario = [{'parada': paradas[p_act], 'tiempo': t_act}]

    # mientras que no se haya terminado la jornada del tren
    while t_act < t_fin:
        # se obtiene la siguiente parada a visitar
        p_act = p_ant + direccion

        # si la parada anterior era la primera, se cambia la dirección, se fija la parada actuala la primera
        # y se añade el tiempo de espera en la parada
        if p_act < 0:
            p_ant = 0
            p_act = 1
            direccion = 1
            t_act += datos['T_FINAL_1']

        # si la parada anterior era la última, se cambia la direccion y se fija la parada actual a la última
        if p_act >= len(paradas):
            p_ant = len(paradas) - 1
            p_act = len(paradas) - 2
            direccion = -1
            t_act += datos['T_FINAL_N']

        # se obtiene el tramo actual y se actualiza la hora actual del recorrido
        tramo_act = next(tramo for tramo in tramos if tramo['inicio'] == paradas[p_ant] and tramo['fin'] == paradas[p_act] and tramo['direccion'] == direccion)
        t_act += tramo_act['tiempo']

        # se añade al horario el tramo actual
        horario.append({'parada': paradas[p_act], 'tiempo': t_act})
        p_ant = p_act

    # si la parada inicial no es de cambio, se elimina del horario
    if 1 not in datos['P_CAMBIO']:
        horario = list(filter(lambda hora: hora['parada'] != 1, horario))

    # si la parada final no es de cambio, se elimina del horario
    if datos['N_PARADAS'] not in datos['P_CAMBIO']:
        horario = list(filter(lambda hora: hora['parada'] != datos['N_PARADAS'], horario))

    return horario


datos = lee_entrada(path)
tramos = calcula_tramos(datos)
pp.pprint(tramos)
print('\n\n')
horario = calcula_horario(datos, tramos)
pp.pprint(horario)





