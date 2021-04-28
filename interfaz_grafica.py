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

        for F in (MenuPrincipal, MenuManual, MenuImportar, MenuExportar, MenuManual):
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
                                      command=lambda: ventana.cambia_frame(MenuManual))
        self.boton_manual.pack(pady=20, padx=10)

        self.boton_importar = tk.Button(self, text="Importar configuración desde un archivo json",
                                        command=lambda: ventana.cambia_frame(MenuImportar))
        self.boton_importar.pack(pady=20, padx=10)


class MenuManual(tk.Frame):
    def __init__(self, master, ventana):
        super().__init__(master)
        self.titulo = tk.Label(self, text="Estás en el menú manual")
        self.titulo.pack(pady=10, padx=10)

        # Entry N_TRENES
        self.frame_n_trenes = tk.Frame(self)
        self.frame_n_trenes.pack(pady=5)

        self.label_n_trenes = tk.Label(self.frame_n_trenes, text="Número de trenes:")
        self.label_n_trenes.pack(side=tk.LEFT)

        self.entry_n_trenes = tk.Entry(self.frame_n_trenes, width=4)
        self.entry_n_trenes.pack(side=tk.RIGHT)

        # Entry N_PARADAS
        self.frame_n_paradas = tk.Frame(self)
        self.frame_n_paradas.pack(pady=5)

        self.label_n_paradas = tk.Label(self.frame_n_paradas, text="Número de paradas:")
        self.label_n_paradas.pack(side=tk.LEFT)

        self.entry_n_paradas = tk.Entry(self.frame_n_paradas, width=4)
        self.entry_n_paradas.pack(side=tk.RIGHT)

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
        self.entry_p_salida = tk.Entry(self)
        self.entry_p_salida.pack(pady=5)

        # ENTRY P_CAMBIO
        self.entry_p_cambio = tk.Entry(self)
        self.entry_p_cambio.pack(pady=5)

        # ENTRY N_SERVICIOS
        self.entry_n_servicios = tk.Entry(self)
        self.entry_n_servicios.pack(pady=5)


        # OBJETIVO DE TIEMPOS
        self.frame_objetivos = tk.Frame(self)
        self.frame_objetivos.pack(pady=5)

        self.label_objetivos = tk.Label(self.frame_objetivos, text="Objetivos que el horario debe cumplir (minutos).")
        self.label_objetivos.pack(side=tk.TOP)

        # Entry T_MIN_DESCANSO
        self.frame_t_min_descanso = tk.Frame(self.frame_objetivos)
        self.frame_t_min_descanso.pack(pady=5)

        self.label_t_min_descanso = tk.Label(self.frame_t_min_descanso, text="Tiempo mínimo de descanso:")
        self.label_t_min_descanso.pack(side=tk.LEFT)

        self.entry_t_min_descanso = tk.Entry(self.frame_t_min_descanso)
        self.entry_t_min_descanso.pack(side=tk.RIGHT)

        # Entry T_MAX_TRABAJO
        self.frame_t_max_trabajo = tk.Frame(self.frame_objetivos)
        self.frame_t_max_trabajo.pack(pady=5)

        self.label_t_max_trabajo = tk.Label(self.frame_t_max_trabajo, text="Tiempo máximo de trabajo continuo:")
        self.label_t_max_trabajo.pack(side=tk.LEFT)

        self.entry_t_max_trabajo = tk.Entry(self.frame_t_max_trabajo)
        self.entry_t_max_trabajo.pack(side=tk.RIGHT)

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

        # Option DIR_SALIDA
        self.frame_dir_salida = tk.Frame(self)
        self.frame_dir_salida.pack(pady=5)

        self.label_dir_salida = tk.Label(self.frame_dir_salida, text="¿Hacia qué extremo sale el primer tren?")
        self.label_dir_salida.pack(side=tk.TOP)

        self.option_dir_salida_1 = tk.Radiobutton(self.frame_dir_salida, text="Primera parada")
        self.option_dir_salida_1.pack(side=tk.LEFT)

        self.option_dir_salida_2 = tk.Radiobutton(self.frame_dir_salida, text="Última parada")
        self.option_dir_salida_2.pack(side=tk.RIGHT)

        # Option DIR_ALTERNA
        self.frame_dir_alterna = tk.Frame(self)
        self.frame_dir_alterna.pack(pady=5)

        self.label_dir_alterna = tk.Label(self.frame_dir_alterna, text="¿Los trenes salen en direcciones alternas?")
        self.label_dir_alterna.pack(side=tk.TOP)

        self.option_dir_alterna_1 = tk.Radiobutton(self.frame_dir_alterna, text="Sí")
        self.option_dir_alterna_1.pack(side=tk.LEFT)

        self.option_dir_alterna_2 = tk.Radiobutton(self.frame_dir_alterna, text="No")
        self.option_dir_alterna_2.pack(side=tk.RIGHT)

        # Button VOLVER
        self.boton_volver = tk.Button(self, text="Volver",
                                      command=lambda: ventana.cambia_frame(MenuPrincipal))
        self.boton_volver.pack()


class MenuImportar(tk.Frame):
    def __init__(self, master, ventana):
        super().__init__(master)
        self.titulo = tk.Label(self, text="Introduzca la ruta del archivo json")
        self.titulo.pack(pady=10, padx=10)

        self.texto_path = tk.Text(self, height=1, width=50)
        self.texto_path.pack(pady=10, padx=10)

        self.boton_cargar_archivo = tk.Button(self, text='Examinar archivo',
                                              command=lambda: self.cargar_archivo())
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

    def cargar_archivo(self):
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
                                      command=lambda: ventana.cambia_frame(MenuImportar))
        self.boton_volver.pack()

        self.texto_estado = tk.Message(self, text="Configurando horario... Esta acción puede tardar varios minutos.")

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
