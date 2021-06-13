"""
Funciones y clases de interfaz gráfica
Autor: Mario Rodríguez Chaves
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import globales as glo
import grasp
import exportacion_excel as excel
import lectura_datos as lectura


datos = {}
introduccion_manual = False


class Aplicacion(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.geometry('800x600')
        self.wm_title('Generador de horarios')

        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MenuPrincipal, MenuManualTrenes, MenuManualParadas, MenuManualObjetivos, MenuImportar, MenuExportar):
            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.cambia_frame(MenuPrincipal)

    def cambia_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MenuPrincipal(tk.Frame):
    def __init__(self, master, ventana):
        super().__init__(master)
        self.titulo = tk.Label(self, text="Seleccione cómo configuar la línea del Metro")
        self.titulo.pack(pady=10, padx=10)

        self.boton_manual = tk.Button(self, text="Añadir configuración manualmente",
                                      command=lambda: ventana.cambia_frame(MenuManualTrenes))
        self.boton_manual.pack(pady=20, padx=10)

        self.boton_importar = tk.Button(self, text="Importar configuración desde un archivo json",
                                        command=lambda: ventana.cambia_frame(MenuImportar))
        self.boton_importar.pack(pady=20, padx=10)


class MenuManualTrenes(tk.Frame):
    def __init__(self, master, ventana):
        super().__init__(master)

        global introduccion_manual
        introduccion_manual = True

        self.titulo = tk.Label(self, text="Estás en el menú manual")
        self.titulo.pack(pady=10, padx=10)
        
        # Entry N_TRENES
        self.frame_n_trenes = tk.Frame(self)
        self.frame_n_trenes.pack(pady=5)

        self.label_n_trenes = tk.Label(self.frame_n_trenes, text="Número de trenes:")
        self.label_n_trenes.pack(side=tk.LEFT)

        self.entry_n_trenes = tk.Entry(self.frame_n_trenes, width=4)
        self.entry_n_trenes.pack(side=tk.RIGHT)

        # INICIO Y FIN DE JORNADAS DE TRENES
        self.frame_jornadas = tk.Frame(self)
        self.frame_jornadas.pack(pady=5)

        self.label_jornadas = tk.Label(self.frame_jornadas, text="Horarios de los trenes (HH:MM).")
        self.label_jornadas.pack(side=tk.TOP)

        # Entry INI_JORNADA
        self.frame_ini_jornada = tk.Frame(self.frame_jornadas)
        self.frame_ini_jornada.pack(side=tk.LEFT)

        self.label_ini_jornada = tk.Label(self.frame_ini_jornada, text="Salida de la estación:")
        self.label_ini_jornada.pack(side=tk.LEFT)

        self.entry_ini_jornada = tk.Entry(self.frame_ini_jornada)
        self.entry_ini_jornada.pack(side=tk.RIGHT)

        # Entry FIN_JORNADA
        self.frame_fin_jornada = tk.Frame(self.frame_jornadas)
        self.frame_fin_jornada.pack(side=tk.RIGHT)

        self.label_fin_jornada = tk.Label(self.frame_fin_jornada, text="Llegada a la estación:")
        self.label_fin_jornada.pack(side=tk.LEFT)

        self.entry_fin_jornada = tk.Entry(self.frame_fin_jornada)
        self.entry_fin_jornada.pack(side=tk.RIGHT)

        # Option DIR_SALIDA
        self.dir_salida = tk.IntVar()
        self.dir_salida.set(-1)

        self.frame_dir_salida = tk.Frame(self)
        self.frame_dir_salida.pack(pady=5)

        self.label_dir_salida = tk.Label(self.frame_dir_salida, text="¿Hacia qué extremo sale el primer tren?")
        self.label_dir_salida.pack(side=tk.TOP)

        self.option_dir_salida_1 = tk.Radiobutton(self.frame_dir_salida, variable=self.dir_salida, value=-1,
                                                  text="Primera parada")
        self.option_dir_salida_1.pack(side=tk.LEFT)

        self.option_dir_salida_2 = tk.Radiobutton(self.frame_dir_salida, variable=self.dir_salida, value=1,
                                                  text="Última parada")
        self.option_dir_salida_2.pack(side=tk.RIGHT)

        # Option DIR_ALTERNA
        self.dir_alterna = tk.BooleanVar()
        self.dir_alterna.set(True)

        self.frame_dir_alterna = tk.Frame(self)
        self.frame_dir_alterna.pack(pady=5)

        self.label_dir_alterna = tk.Label(self.frame_dir_alterna,
                                          text="¿Los trenes salen en direcciones alternas?")
        self.label_dir_alterna.pack(side=tk.TOP)

        self.option_dir_alterna_1 = tk.Radiobutton(self.frame_dir_alterna, variable=self.dir_alterna, value=True, text="Sí")
        self.option_dir_alterna_1.pack(side=tk.LEFT)

        self.option_dir_alterna_2 = tk.Radiobutton(self.frame_dir_alterna, variable=self.dir_alterna, value=False, text="No")
        self.option_dir_alterna_2.pack(side=tk.RIGHT)

        # Frame botonera
        self.frame_botones = tk.Frame(self)
        self.boton_volver = tk.Button(self.frame_botones, text="Volver",
                                      command=lambda: ventana.cambia_frame(MenuPrincipal))
        self.boton_siguiente = tk.Button(self.frame_botones, text="Siguiente",
                                      command=lambda: self.valida_datos(ventana))

        self.frame_botones.pack(pady=5)
        self.boton_volver.pack(side=tk.LEFT, padx=5)
        self.boton_siguiente.pack(side=tk.RIGHT, padx=5)

        # Texto errores
        self.texto_errores = tk.StringVar()
        self.label_errores = tk.Label(self, textvariable=self.texto_errores)
        self.label_errores.pack()

    def valida_datos(self, ventana):
        errores = ""

        # se comprueba que el número de trenes es un número y es mayor o igual que 1
        n_trenes = self.entry_n_trenes.get()
        if not n_trenes.isdigit() or int(n_trenes) < 1:
            errores = errores + "El nº de trenes no ha sido introducido correctamente.\n"
            n_trenes = -1
        else:
            n_trenes = int(n_trenes)

        # se comprueba que el número de inicios de jornada es igual al número de trenes
        # y que cada inicio de jornada sea un número mayor que 0
        valor = self.entry_ini_jornada.get()
        ini_jornada = valor.split(",")

        if len(ini_jornada) != n_trenes:
            errores = errores + "El nº de inicios de jornada no coincide con el número de trenes.\n"
        else:
            for valor in ini_jornada:
                sin_espacios = valor.replace(" ", "")
                if not sin_espacios.isdigit() or int(valor) < 0:
                    errores = errores + "Los inicios de jornada deben ser en minutos y separados por coma. Ej: 360, 370, 380.\n"
                    break

        # se comprueba que el número de fin de jornada es igual al número de trenes
        # y que cada fin de jornada sea un número mayor que 0
        valor = self.entry_fin_jornada.get()
        fin_jornada = valor.split(",")

        if len(fin_jornada) != n_trenes:
            errores = errores + "El nº de fines de jornada no coincide con el número de trenes.\n"
        else:
            for valor in fin_jornada:
                valor.replace(" ", "")
                if not sin_espacios.isdigit() or int(valor) < 0:
                    errores = errores + "Los fines de jornada deben ser en minutos y separados por coma. Ej: 360, 370, 380.\n"
                    break

        # si no ha habido errores, se almacenan los valores en el diccionario
        if errores == "":
            datos['N_TRENES'] = n_trenes
            datos['INI_JORNADA'] = [int(i) for i in ini_jornada]
            datos['FIN_JORNADA'] = [int(i) for i in fin_jornada]
            datos['DIR_SALIDA'] = self.dir_salida.get()
            datos['DIR_ALTERNA'] = self.dir_alterna.get()
            ventana.cambia_frame(MenuManualParadas)

        self.texto_errores.set(errores)


class MenuManualParadas(tk.Frame):
    def __init__(self, master, ventana):
        super().__init__(master)
        self.titulo = tk.Label(self, text="Estás en el menú manual")
        self.titulo.pack(pady=10, padx=10)

        # Entry N_PARADAS
        self.frame_n_paradas = tk.Frame(self)
        self.frame_n_paradas.pack(pady=5)

        self.label_n_paradas = tk.Label(self.frame_n_paradas, text="Número de paradas:")
        self.label_n_paradas.pack(side=tk.LEFT)

        self.entry_n_paradas = tk.Entry(self.frame_n_paradas, width=4)
        self.entry_n_paradas.pack(side=tk.RIGHT)

        # TIEMPOS DE IDA Y VUELTA
        self.frame_tiempos = tk.Frame(self)
        self.frame_tiempos.pack(pady=5)

        self.label_tiempos = tk.Label(self.frame_tiempos, text="Tiempo de los trayectos entre estaciones (en minutos).")
        self.label_tiempos.pack(side=tk.TOP)

        # Entry T_IDA
        self.frame_t_ida = tk.Frame(self.frame_tiempos)
        self.frame_t_ida.pack(side=tk.LEFT)

        self.label_t_ida = tk.Label(self.frame_t_ida, text="Dir. última parada:")
        self.label_t_ida.pack(side=tk.LEFT)

        self.entry_t_ida = tk.Entry(self.frame_t_ida)
        self.entry_t_ida.pack(side=tk.RIGHT)

        # Entry T_VUELTA
        self.frame_t_vuelta = tk.Frame(self.frame_tiempos)
        self.frame_t_vuelta.pack(side=tk.RIGHT)

        self.label_t_vuelta = tk.Label(self.frame_t_vuelta, text="Dir. primera parada:")
        self.label_t_vuelta.pack(side=tk.LEFT)

        self.entry_t_vuelta = tk.Entry(self.frame_t_vuelta)
        self.entry_t_vuelta.pack(side=tk.RIGHT)

        # TIEMPOS DE ESPERA
        self.frame_espera = tk.Frame(self)
        self.frame_espera.pack(pady=5)

        self.label_espera = tk.Label(self.frame_espera, text="Tiempo de espera en el extremo de la línea (minutos).")
        self.label_espera.pack(side=tk.TOP)

        # Entry T_FINAL_1
        self.frame_t_final_1 = tk.Frame(self.frame_espera)
        self.frame_t_final_1.pack(side=tk.LEFT)

        self.label_t_final_1 = tk.Label(self.frame_t_final_1, text="En la parada 1:")
        self.label_t_final_1.pack(side=tk.LEFT)

        self.entry_t_final_1 = tk.Entry(self.frame_t_final_1, width=3)
        self.entry_t_final_1.pack(side=tk.RIGHT)

        # Entry T_FINAL_1
        self.frame_t_final_n = tk.Frame(self.frame_espera)
        self.frame_t_final_n.pack(side=tk.RIGHT)

        self.label_t_final_n = tk.Label(self.frame_t_final_n, text="En la parada n:")
        self.label_t_final_n.pack(side=tk.LEFT)

        self.entry_t_final_n = tk.Entry(self.frame_t_final_n, width=3)
        self.entry_t_final_n.pack(side=tk.RIGHT)

        # Entry P_SALIDA
        self.frame_p_salida = tk.Frame(self)
        self.frame_p_salida.pack(pady=5)

        self.label_n_trenes = tk.Label(self.frame_p_salida, text="Parada de salida:")
        self.label_n_trenes.pack(side=tk.LEFT)

        self.entry_p_salida = tk.Entry(self.frame_p_salida)
        self.entry_p_salida.pack(side=tk.LEFT)

        # ENTRY P_CAMBIO
        self.frame_p_cambio = tk.Frame(self)
        self.frame_p_cambio.pack(pady=5)

        self.label_p_cambio = tk.Label(self.frame_p_cambio, text="Parada de cambio:")
        self.label_p_cambio.pack(side=tk.LEFT)

        self.entry_p_cambio = tk.Entry(self.frame_p_cambio)
        self.entry_p_cambio.pack(side=tk.RIGHT)

        # Frame botonera
        self.frame_botones = tk.Frame(self)
        self.boton_volver = tk.Button(self.frame_botones, text="Volver",
                                      command=lambda: ventana.cambia_frame(MenuManualTrenes))
        self.boton_siguiente = tk.Button(self.frame_botones, text="Siguiente",
                                      command=lambda: self.valida_datos(ventana))

        self.frame_botones.pack(pady=5)
        self.boton_volver.pack(side=tk.LEFT, padx=5)
        self.boton_siguiente.pack(side=tk.RIGHT, padx=5)

        # Texto errores
        self.texto_errores = tk.StringVar()
        self.label_errores = tk.Label(self, textvariable=self.texto_errores)
        self.label_errores.pack()

    def valida_datos(self, ventana):
        errores = ""

        # se comprueba que el número de paradas es un número y es mayor o igual que 1
        n_paradas = self.entry_n_paradas.get()
        if not n_paradas.isdigit() or int(n_paradas) < 1:
            errores = errores + "El nº de paradas no ha sido introducido correctamente.\n"
            n_paradas = -1
        else:
            n_paradas = int(n_paradas)

        # se comprueba que el número de tiempos de ida es igual al número de paradas - 1
        # y que cada tiempo de ida sea un número mayor que 0
        valor = self.entry_t_ida.get()
        t_ida = valor.split(",")

        if len(t_ida) != (n_paradas - 1):
            errores = errores + "El nº de tiempos de ida debe ser igual al número de paradas - 1. Ej. si nº paradas es 5, debe haber 4 elementos.\n"
        else:
            for valor in t_ida:
                sin_espacios = valor.replace(" ", "")
                if not sin_espacios.isdigit() or int(valor) < 0:
                    errores = errores + "Los tiempos de ida deben ser en minutos y separados por coma. Ej: 2, 4, 1.\n"
                    break

        # se comprueba que el número de tiempos de vuelta es igual al número de paradas - 1
        # y que cada tiempo de vuelta sea un número mayor que 0
        valor = self.entry_t_vuelta.get()
        t_vuelta = valor.split(",")

        if len(t_vuelta) != (n_paradas - 1):
            errores = errores + "El nº de tiempos de ida debe ser igual al número de paradas - 1. Ej. si nº paradas es 5, debe haber 4 elementos.\n"
        else:
            for valor in t_vuelta:
                sin_espacios = valor.replace(" ", "")
                if not sin_espacios.isdigit() or int(valor) < 0:
                    errores = errores + "Los tiempos de ida deben ser en minutos y separados por coma. Ej: 2, 4, 1.\n"
                    break

        # se comprueba que el tiempo de espera en la parada 1 es un número y es mayor o igual que 1
        t_final_1 = self.entry_t_final_1.get()
        if not t_final_1.isdigit() or int(t_final_1) < 0:
            errores = errores + "El tiempo de espera en la primera parada no ha sido introducido correctamente.\n"

        # se comprueba que el tiempo de espera en la parada n es un número y es mayor o igual que 1
        t_final_n = self.entry_t_final_n.get()
        if not t_final_n.isdigit() or int(t_final_n) < 0:
            errores = errores + "El tiempo de espera en la última parada no ha sido introducido correctamente.\n"

        # se comprueba que la parada de salida sea un número entre 0 y el máximo
        p_salida = self.entry_p_salida.get()
        if not p_salida.isdigit() or 0 > int(p_salida) or int(p_salida) >= n_paradas:
            errores = errores + "La parada de salida debe ser un número entre 0 y el número de paradas.\n"

        # se comprueba que el número de paradas de cambio es igual al número de trenes
        # y que el número de cada parada está entre 0 y el máximo
        valor = self.entry_p_cambio.get()
        p_cambio = valor.split(",")

        if len(p_cambio) > n_paradas or len(p_cambio) == 0:
            errores = errores + "El nº de paradas de intercambio debe ser entre 1 y el número de paradas.\n"
        else:
            for valor in p_cambio:
                sin_espacios = valor.replace(" ", "")
                if not sin_espacios.isdigit() or 0 > int(valor) or int(valor) >= n_paradas:
                    errores = errores + "Las paradas de intercambio deben ser números entre 0 y el número de paradas. Ej: 3, 6, 7.\n"
                    break

        # si no ha habido errores, se almacenan los valores en el diccionario
        if errores == "":
            datos['N_PARADAS'] = n_paradas
            datos['T_IDA'] = [int(i) for i in t_ida]
            datos['T_VUELTA'] = [int(i) for i in t_vuelta]
            datos['T_FINAL_1'] = int(t_final_1)
            datos['T_FINAL_N'] = int(t_final_n)
            datos['P_SALIDA'] = int(p_salida)
            datos['P_CAMBIO'] = [int(i) for i in p_cambio]
            ventana.cambia_frame(MenuManualObjetivos)

        self.texto_errores.set(errores)


class MenuManualObjetivos(tk.Frame):
    def __init__(self, master, ventana):
        super().__init__(master)
        self.titulo = tk.Label(self, text="Estás en el menú manual")
        self.titulo.pack(pady=10, padx=10)

        # ENTRY N_SERVICIOS
        self.frame_n_servicios = tk.Frame(self)
        self.frame_n_servicios.pack(pady=5)

        self.label_n_servicios = tk.Label(self.frame_n_servicios, text="Número de servicios:")
        self.label_n_servicios.pack(side=tk.LEFT)

        self.entry_n_servicios = tk.Entry(self.frame_n_servicios)
        self.entry_n_servicios.pack(pady=5)

        # OBJETIVO DE TIEMPOS
        self.frame_objetivos = tk.Frame(self)
        self.frame_objetivos.pack(pady=5)

        self.label_objetivos = tk.Label(self.frame_objetivos, text="Objetivos que el horario debe cumplir (minutos).")
        self.label_objetivos.pack(side=tk.TOP)

        # Entry T_MAX_TRABAJO
        self.frame_t_max_trabajo = tk.Frame(self.frame_objetivos)
        self.frame_t_max_trabajo.pack(pady=5)

        self.label_t_max_trabajo = tk.Label(self.frame_t_max_trabajo, text="Tiempo máximo de trabajo continuo:")
        self.label_t_max_trabajo.pack(side=tk.LEFT)

        self.entry_t_max_trabajo = tk.Entry(self.frame_t_max_trabajo)
        self.entry_t_max_trabajo.pack(side=tk.RIGHT)

        # Entry T_MIN_DESCANSO
        self.frame_t_min_descanso = tk.Frame(self.frame_objetivos)
        self.frame_t_min_descanso.pack(pady=5)

        self.label_t_min_descanso = tk.Label(self.frame_t_min_descanso, text="Tiempo mínimo de descanso:")
        self.label_t_min_descanso.pack(side=tk.LEFT)

        self.entry_t_min_descanso = tk.Entry(self.frame_t_min_descanso)
        self.entry_t_min_descanso.pack(side=tk.RIGHT)

        # Entry T_OPTIMO_TRABAJO
        self.frame_t_optimo_trabajo = tk.Frame(self.frame_objetivos)
        self.frame_t_optimo_trabajo.pack(pady=5)

        self.label_t_optimo_trabajo = tk.Label(self.frame_t_optimo_trabajo, text="Objetivo de tiempo de trabajo:")
        self.label_t_optimo_trabajo.pack(side=tk.LEFT)

        self.entry_t_optimo_trabajo = tk.Entry(self.frame_t_optimo_trabajo)
        self.entry_t_optimo_trabajo.pack(side=tk.RIGHT)

        # Entry T_OPTIMO_DESCANSO
        self.frame_t_optimo_descanso = tk.Frame(self.frame_objetivos)
        self.frame_t_optimo_descanso.pack(pady=5)

        self.label_t_optimo_descanso = tk.Label(self.frame_t_optimo_descanso, text="Objetivo de tiempo de descanso:")
        self.label_t_optimo_descanso.pack(side=tk.LEFT)

        self.entry_t_optimo_descanso = tk.Entry(self.frame_t_optimo_descanso)
        self.entry_t_optimo_descanso.pack(side=tk.RIGHT)

        # Frame botonera
        self.frame_botones = tk.Frame(self)
        self.boton_volver = tk.Button(self.frame_botones, text="Volver",
                                      command=lambda: ventana.cambia_frame(MenuManualParadas))
        self.boton_siguiente = tk.Button(self.frame_botones, text="Siguiente",
                                         command=lambda: self.valida_datos(ventana))

        self.frame_botones.pack(pady=5)
        self.boton_volver.pack(side=tk.LEFT, padx=5)
        self.boton_siguiente.pack(side=tk.RIGHT, padx=5)

        # Texto errores
        self.texto_errores = tk.StringVar()
        self.label_errores = tk.Label(self, textvariable=self.texto_errores)
        self.label_errores.pack()

    def valida_datos(self, ventana):
            errores = ""

            # se comprueba que el número de servicios es un número y es mayor o igual que 1
            n_servicios = self.entry_n_servicios.get()
            if not n_servicios.isdigit() or int(n_servicios) < 1:
                errores = errores + "El nº de servicios no ha sido introducido correctamente.\n"
            else:
                n_servicios = int(n_servicios)

            # se comprueba que el tiempo máximo de trabajo es un número y es mayor o igual que 1
            t_max_trabajo = self.entry_t_max_trabajo.get()
            if not t_max_trabajo.isdigit() or int(t_max_trabajo) < 1:
                errores = errores + "El tiempo máximo de trabajo no ha sido introducido correctamente.\n"
            else:
                t_max_trabajo = int(t_max_trabajo)

            # se comprueba que el tiempo mínimo de descanso es un número y es mayor o igual que 1
            t_min_descanso = self.entry_t_min_descanso.get()
            if not t_min_descanso.isdigit() or int(t_min_descanso) < 1:
                errores = errores + "El tiempo mínimo de descanso no ha sido introducido correctamente.\n"
            else:
                t_min_descanso = int(t_min_descanso)

            # se comprueba que el tiempo óptimo de trabajo es un número y es mayor o igual que 1
            t_optimo_trabajo = self.entry_t_optimo_trabajo.get()
            if not t_optimo_trabajo.isdigit() or int(t_optimo_trabajo) < 1:
                errores = errores + "El tiempo óptimo de trabajo no ha sido introducido correctamente.\n"
            else:
                t_optimo_trabajo = int(t_optimo_trabajo)

            # se comprueba que el tiempo óptimo de descanso es un número y es mayor o igual que 1
            t_optimo_descanso = self.entry_t_optimo_descanso.get()
            if not t_optimo_descanso.isdigit() or int(t_optimo_descanso) < 1:
                errores = errores + "El tiempo óptimo de descanso no ha sido introducido correctamente.\n"
            else:
                t_optimo_descanso = int(t_optimo_descanso)

            # si no ha habido errores, se almacenan los valores en el diccionario
            if errores == "":
                datos['N_SERVICIOS'] = n_servicios
                datos['T_MAX_TRABAJO'] = t_max_trabajo
                datos['T_MIN_DESCANSO'] = t_min_descanso
                datos['T_OPTIMO_TRABAJO'] = t_optimo_trabajo
                datos['T_OPTIMO_DESCANSO'] = t_optimo_descanso

                if glo.init(datos):
                    ventana.cambia_frame(MenuExportar)
                else:
                    errores = errores + "No se han podido importar los datos al problema. Por favor, compruebe todos los datos introducidos."

            self.texto_errores.set(errores)


class MenuImportar(tk.Frame):
    def __init__(self, master, ventana):
        super().__init__(master)

        global introduccion_manual
        introduccion_manual = False

        self.titulo = tk.Label(self, text="Introduzca la ruta del archivo json")
        self.titulo.pack(pady=10, padx=10)

        self.texto_path = tk.Text(self, height=1, width=50)
        self.texto_path.pack(pady=10, padx=10)

        self.boton_cargar_archivo = tk.Button(self, text='Examinar archivo',
                                              command=lambda: self.carga_archivo())
        self.boton_cargar_archivo.pack(pady=10, padx=10)

        self.boton_aceptar = tk.Button(self, text='Siguiente',
                                       command=lambda: ventana.cambia_frame(MenuExportar))
        self.boton_aceptar['state'] = 'disabled'
        self.boton_aceptar.pack(pady=10, padx=10)

        self.boton_volver = tk.Button(self, text="Volver",
                                      command=lambda: ventana.cambia_frame(MenuPrincipal))
        self.boton_volver.pack()

        self.texto_error = tk.Message(self,
                                      text="Ha habido un error al cargar el archivo, compruebe que la sintaxis es "
                                           "correcta")

    def carga_archivo(self):
        ruta = askopenfilename(
            filetypes=[("Archivos json", "*.json"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return

        self.texto_path.delete("1.0", tk.END)
        self.texto_path.insert(tk.END, ruta)
        exito = lectura.lee_entrada(ruta)

        if exito:
            self.boton_aceptar['state'] = 'normal'
            self.texto_error.pack_forget()
        else:
            self.boton_aceptar['state'] = 'disabled'
            self.texto_error.pack(pady=10, padx=10)


class MenuExportar(tk.Frame):
    def __init__(self, master, ventana):
        super().__init__(master)
        self.titulo = tk.Label(self, text="Introduzca el nombre del archivo excel")
        self.titulo.pack(pady=10, padx=10)

        self.texto_path = tk.Text(self, height=1, width=50)
        self.texto_path.pack(pady=10, padx=10)

        self.boton_cargar_archivo = tk.Button(self, text='Examinar archivo',
                                              command=lambda: self.guarda_archivo())
        self.boton_cargar_archivo.pack(pady=10, padx=10)

        self.boton_aceptar = tk.Button(self, text='Calcular horario',
                                       command=lambda: self.calcula_horario())
        self.boton_aceptar['state'] = 'disabled'
        self.boton_aceptar.pack(pady=10, padx=10)

        self.boton_volver = tk.Button(self, text="Volver",
                                      command=lambda: self.ventana_anterior(ventana))
        self.boton_volver.pack()

        self.texto_estado = tk.Message(self, text="Configurando horario... Esta acción puede tardar varios minutos.")

    def ventana_anterior(self, ventana):
        if introduccion_manual:
            ventana.cambia_frame(MenuManualObjetivos)
        else:
            ventana.cambia_frame(MenuImportar)

    def guarda_archivo(self):
        ruta = asksaveasfilename(defaultextension='.xls', filetypes=[("Archivo Excel", '*.xlsx')])
        if ruta is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        self.texto_path.delete("1.0", tk.END)
        self.texto_path.insert(tk.END, ruta)
        glo.ARCHIVO_SALIDA = ruta
        self.boton_aceptar['state'] = 'normal'

    def calcula_horario(self):
        self.texto_estado.configure(text='Configurando horario... Esta acción puede tardar varios minutos.')
        self.texto_estado.pack(pady=10, padx=10)

        # se asignan los valores de los parámetros
        max_iter = 10
        max_iter_bl = 3000
        max_vecinos_bl = 2000
        LRC = 2

        # se ejecuta el GRASP
        solucion, fit = grasp.GRASP(LRC, max_iter, max_iter_bl, max_vecinos_bl)
        print('\nGRASP')
        print(solucion)
        print('fit: ' + str(fit))

        # se almacena la solución obtenida
        excel.crear_hoja_servicios(solucion, 'grasp_horario', True)

        # se almacenan el gráfico de progresión del algoritmo
        titulo_grafico = 'Resultados para cada iteración del algoritmo GRASP'
        excel.aniade_graficos(titulo_grafico, 'grasp_graficos', False)

        self.texto_estado.configure(text='Horario configurado.')


if __name__ == '__main__':
    app = Aplicacion()
    app.mainloop()
