# -*- coding: utf-8 -*-
"""
Funciones de lectura y escritura de datos
Autor: Mario Rodríguez Chaves
"""

import json

import globales


def sort_func(dic):
    return dic['INICIO'], dic['FIN']


def lee_entrada(archivo):
    # se abre el archivo que contiene el json
    with open(archivo, 'r') as json_file:
        datos = json.load(json_file)

    return datos


# función que calcula los tramos entre paradas y el tiempo que se tarda en recorrer cada tramo
# entrada:
#   datos: diccionario con los datos iniciales del problema
# salida:
#   t_parada: diccionario con los tramos de la vía y el tiempo en recorrer cada tramo
def calcula_tramos():
    t_parada = []

    # se almacenan los tiempos de ida y vuelta en listas
    t_ida = globales.T_IDA
    t_vuelta = globales.T_VUELTA
    n_paradas = globales.N_PARADAS

    # se almacenan las paradas de cambio de conductores
    cambios = globales.P_CAMBIO
    cambio_old = cambios[0]

    # se añade el tramo inicial a la lista de paradas
    t_parada.append({'INICIO': 1, 'FIN': cambios[0], 'DIRECCION': 1, 'TIEMPO': 0})
    t_parada.append({'INICIO': cambios[0], 'FIN': 1, 'DIRECCION': -1, 'TIEMPO': 0})

    # para cada parada de cambio (excepto la primera y la última)
    for cambio in cambios[1:]:
        # se añade el tramo a la lista de paradas
        t_parada.append({'INICIO': cambio_old, 'FIN': cambio, 'DIRECCION': 1, 'TIEMPO': 0})
        t_parada.append({'INICIO': cambio, 'FIN': cambio_old, 'DIRECCION': -1, 'TIEMPO': 0})
        # se almacena la parada actual en cambio_old
        cambio_old = cambio

    # se añade el tramo final a la lista de paradas
    t_parada.append({'INICIO': cambio_old, 'FIN': n_paradas, 'DIRECCION': 1, 'TIEMPO': 0})
    t_parada.append({'INICIO': n_paradas, 'FIN': cambio_old, 'DIRECCION': -1, 'TIEMPO': 0})

    # para el resto de paradas, se calcula el recorrido
    for tramo in t_parada:
        if tramo['DIRECCION'] > 0:
            p_ini = tramo['INICIO']
            p_fin = tramo['FIN']

            while p_ini < p_fin:
                tramo['TIEMPO'] += t_ida[p_ini - 1]
                p_ini += 1
        else:
            p_ini = tramo['FIN']
            p_fin = tramo['INICIO']

            while p_ini < p_fin:
                tramo['TIEMPO'] += t_vuelta[p_ini - 1]
                p_ini += 1

    # se devuelven las paradas ordenadas por la parada inicial
    return sorted(t_parada, key=sort_func)


# función que calcula el horario de un tren en tramos realizados y la hora a la que llega a cada tramo
def calcula_horario_tren(tramos, hora_ini, hora_fin, tren):
    paradas = globales.P_CAMBIO
    t_act = hora_ini
    t_fin = hora_fin
    direccion = globales.DIR_SALIDA

    if 1 not in paradas:
        paradas = [1] + paradas

    if globales.N_PARADAS not in paradas:
        paradas = paradas + [globales.N_PARADAS]

    p_ant = paradas.index(globales.P_SALIDA)
    p_act = p_ant

    horario = [{'TREN': tren, 'PARADA': paradas[p_act], 'TIEMPO': t_act}]

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
            t_act += globales.T_FINAL_1

        # si la parada anterior era la última, se cambia la direccion y se fija la parada actual a la última
        if p_act >= len(paradas):
            p_ant = len(paradas) - 1
            p_act = len(paradas) - 2
            direccion = -1
            t_act += globales.T_FINAL_N

        # se obtiene el tramo actual y se actualiza la hora actual del recorrido
        tramo_act = next(tramo for tramo in tramos if tramo['INICIO'] == paradas[p_ant] and tramo['FIN'] == paradas[p_act] and tramo['DIRECCION'] == direccion)
        t_act += tramo_act['TIEMPO']

        # se añade al horario el tramo actual
        horario.append({'TREN': tren, 'PARADA': paradas[p_act], 'TIEMPO': t_act})
        p_ant = p_act

    # si la parada inicial no es de cambio, se elimina del horario
    if 1 not in globales.P_CAMBIO:
        horario = list(filter(lambda hora: hora['PARADA'] != 1, horario))

    # si la parada final no es de cambio, se elimina del horario
    if globales.N_PARADAS not in globales.P_CAMBIO:
        horario = list(filter(lambda hora: hora['PARADA'] != globales.N_PARADAS, horario))

    return horario


def calcula_horario_trenes():
    tramos = calcula_tramos()
    horario = []
    for i in range(0, globales.N_TRENES):
        hora_ini = globales.INI_JORNADA[i]
        hora_fin = globales.FIN_JORNADA[i]
        horario = horario + calcula_horario_tren(tramos, hora_ini, hora_fin, i)
    return horario



