from .shared_imports import *
from General.Simulador import Simulador
import random
import threading
import numpy as np
from tkinter import *
class PaginaSimulador(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.simulador_optimo = None
        self.simulador_aging = None
        self.simulador_lru = None
        self.simulador_random = None
        self.simulador_secondchance = None
        self.simulador_usuario = None
        label = tk.Label(self, text="Aqui va el simulador con las tablas")
        label.pack(padx=10, pady=10)

        txt_button = tk.Button(
            self,
            text="Mostrar lista de procesos del txt",
            command=self.test,
        )
        txt_button.pack(side="bottom", fill=tk.X)

        representarValores= [ " Page ID ","PID","LOADED","L-ADDR","M-ADDR","D-ADDR","LOADED-T","Mark"]

        frme_venta_optimo=tk.Frame(self,width="400", height="300")
        frme_venta_optimo.place(x=220,y=170)

        my_canvas = tk.Canvas(frme_venta_optimo)
        my_canvas.config(width=400,height=300,)
        my_canvas.pack()
        
        my_scrollbar = ttk.Scrollbar(frme_venta_optimo, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
        
        second_frame = Frame(my_canvas)
        my_canvas.create_window((0,0), window=second_frame)

        labelsOpt=[]
        labelsAlgo=[]
        
        for j in range(len(representarValores)):#esto son la cantidad de procesos multiplicados por 8 ya que son 8 datos a representar
            labelsOpt+=[tk.Label(second_frame,text=representarValores[j],bd=4)]

        for i in range(120):#esto son la cantidad de procesos multiplicados por 8 ya que son 8 datos a representar
            labelsOpt+=[tk.Label(second_frame,text=str(i),bd=4)]
        
        

        MatrizLabelProcesoDatos=np.reshape(labelsOpt, (16, 8))#aca son 7 columnas con la cantidad de filas que seria los cantidad de procesos multiplicados por 8 /7
        for x in range(len(MatrizLabelProcesoDatos)):
            for y in range(len(MatrizLabelProcesoDatos[0])):
                MatrizLabelProcesoDatos[x][y].grid(row=x, column=y)

        #segundo label
        frme_venta_algoritmo=tk.Frame(self,width="400", height="300")
        frme_venta_algoritmo.place(x=950,y=170)

        my_canvasTable2 = tk.Canvas(frme_venta_algoritmo)
        my_canvasTable2.config(width=400,height=300,)
        my_canvasTable2.pack()

        my_scrollbarTable2 = ttk.Scrollbar(frme_venta_algoritmo, orient=VERTICAL, command=my_canvasTable2.yview)
        my_scrollbarTable2.pack(side=RIGHT, fill=Y)

        # Configure The Canvas
        my_canvasTable2.configure(yscrollcommand=my_scrollbarTable2.set)
        my_canvasTable2.bind('<Configure>', lambda e: my_canvasTable2.configure(scrollregion = my_canvasTable2.bbox("all")))

        Third_frame = Frame(my_canvasTable2)
        my_canvasTable2.create_window((0,0), window=Third_frame)

        for a in range(len(representarValores)):#esto son la cantidad de procesos multiplicados por 8 ya que son 8 datos a representar
            labelsAlgo+=[tk.Label(Third_frame,text=representarValores[a],bd=4)]

        for i in range(120):#esto son la cantidad de procesos multiplicados por 8 ya que son 8 datos a representar
            labelsAlgo+=[tk.Label(Third_frame,text=str(i),bd=4)]

        MatrizLabelProcesoDatosAlgoritmo= np.reshape(labelsAlgo, (16, 8))

        for x in range(len(MatrizLabelProcesoDatosAlgoritmo)):
            for y in range(len(MatrizLabelProcesoDatosAlgoritmo[0])):
                MatrizLabelProcesoDatosAlgoritmo[x][y].grid(row=x, column=y)

        optimo_button = tk.Button(
            self,
            text="Correr optimo",
            command=self.optimo,
        )
        optimo_button.pack(side="bottom", fill=tk.X)

        aging_button = tk.Button(
            self,
            text="Correr aging",
            command=self.aging,
        )
        aging_button.pack(side="bottom", fill=tk.X)

        lru_button = tk.Button(
            self,
            text="Correr lru",
            command=self.lru,
        )
        lru_button.pack(side="bottom", fill=tk.X)

        random_button = tk.Button(
            self,
            text="Correr random",
            command=self.random,
        )
        random_button.pack(side="bottom", fill=tk.X)

        secondchance_button = tk.Button(
            self,
            text="Correr secondchance",
            command=self.secondchance,
        )
        secondchance_button.pack(side="bottom", fill=tk.X)

        switch_window_button = tk.Button(
            self,
            text="Debug",
            command=self.correr_simulacion,
        )
        switch_window_button.pack(side="bottom", fill=tk.X)
        test = str(random.randint(0, 5))

        self.label_test = tk.Label(self, text=test)
        self.label_test.place(x=500, y=500)

        
        self.t1 = threading.Thread(target=self.optimo)
        self.t2 = threading.Thread(target=self.lru)
    # ESTA FUNCION ES PARA EDITAR TODOS LOS LABELS PARA QUE SE ACTUALICE LA GUI
    def draw(self):
        self.label_test['text'] = str(random.randint(0, 5))
        self.parent.after(500, self.draw)
    # ESTA FUNCION SIRVE TEMPORALMENTE PARA CORRER EL DRAW Y EL OPTIMO
    def correr_simulacion(self):
        self.t1.start() # DONDE COLOCAR LOS JOINS?
        self.draw()

    def test(self):
        print(self.controller.fileContent)

    def optimo(self):
        self.simulador_optimo = Simulador("Optimo", self.controller.fileContent)
        self.simulador_optimo.correr_algoritmo()

    def aging(self):
        self.simulador_aging = Simulador("Aging", self.controller.fileContent)
        self.simulador_aging.correr_algoritmo()

    def lru(self):
        self.simulador_lru = Simulador("LRU", self.controller.fileContent)
        self.simulador_lru.correr_algoritmo()

    def random(self):
        self.simulador_random = Simulador("Random", self.controller.fileContent)
        self.simulador_random.correr_algoritmo()

    def secondchance(self):
        self.simulador_secondchance = Simulador("SecondChance", self.controller.fileContent)
        self.simulador_secondchance.correr_algoritmo()

class PaginaDebugger(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Para utilizar proximamente para ver prints del proceso")
        label.pack(padx=10, pady=10)
        switch_window_button = ttk.Button(
            self, text="De vuelta al simulador", command=lambda: controller.show_frame(PaginaSimulador)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)
