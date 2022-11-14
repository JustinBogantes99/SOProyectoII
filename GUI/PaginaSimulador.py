import sys
from time import sleep
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
        self.tamanio=(len(self.controller.fileContent)-1)+(len(self.controller.fileContent)*2)
        self.sim = None
        self.parent = parent
        self.simulador_optimo = None
        self.simulador_aging = None
        self.simulador_lru = None
        self.simulador_random = None
        self.simulador_secondchance = None
        self.simulador_usuario = None

        label = tk.Label(self, text="Aqui va el simulador con las tablas")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self,
            text="Correr simulacion",
            command=self.correr_simulacion,
        )
        switch_window_button.pack(side="bottom", fill=tk.X)
        self.tOptimo = threading.Thread(target=self.optimo)
        self.tAging = threading.Thread(target=self.aging)
        self.tRandom = threading.Thread(target=self.random)
        self.tLRU = threading.Thread(target=self.lru)
        self.tSecondChance = threading.Thread(target=self.secondchance)


    def crearLabels(self):
        #lista con los valores que tiene que mostrar cada proceso 
        representarValores= [ " Page ID ","PID","LOADED","L-ADDR","M-ADDR","D-ADDR","LOADED-T","Mark"]
        frme_venta_optimo=tk.Frame(self,width="400", height="300")
        frme_venta_optimo.place(x=220,y=170)
        #canvas creado en el frame
        my_canvas = tk.Canvas(frme_venta_optimo)
        my_canvas.config(width=400,height=300,)
        my_canvas.pack()
        #scrollbar que ubicado en el canvas
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
        for i in range(120):# self.tamanio*8 esto son la cantidad de procesos multiplicados por 8 ya que son 8 datos a representar
            print(i)
            labelsOpt+=[tk.Label(second_frame,text=str(i),bd=4)]
        #120/8=16
        filasLabel=16#(self.tamanio*8)//8
        MatrizLabelProcesoDatos=np.reshape(labelsOpt, (filasLabel, 8))#aca son 7 columnas con la cantidad de filas que seria los cantidad de procesos multiplicados por 8 /7
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

        for a in range(len(representarValores)): 
            labelsAlgo+=[tk.Label(Third_frame,text=representarValores[a],bd=4)]

        #print(txt)
        for i in range(self.tamanio*8):#esto son la cantidad de procesos multiplicados por 8 ya que son 8 datos a representar
            labelsAlgo+=[tk.Label(Third_frame,text=str(i),bd=4)]

        MatrizLabelProcesoDatosAlgoritmo= np.reshape(labelsAlgo, (filasLabel, 8))

        for x in range(len(MatrizLabelProcesoDatosAlgoritmo)):
            for y in range(len(MatrizLabelProcesoDatosAlgoritmo[0])):
                MatrizLabelProcesoDatosAlgoritmo[x][y].grid(row=x, column=y)
    # ESTA FUNCION ES PARA EDITAR TODOS LOS LABELS PARA QUE SE ACTUALICE LA GUI
    def draw(self):
        self.sim = self.parent.after(500, self.draw)
    # ESTA FUNCION SIRVE TEMPORALMENTE PARA CORRER EL DRAW Y EL OPTIMO
    def correr_simulacion(self):
        print("ALGORITMO", self.controller.algoritmo_escogido)
        self.tOptimo.start() # DONDE COLOCAR LOS JOINS?
        if self.controller.algoritmo_escogido == "Aging":
            self.tAging.start()
        if self.controller.algoritmo_escogido == "LRU":
            self.tLRU.start()
        if self.controller.algoritmo_escogido == "Second Chance":
            self.tSecondChance.start()
        if self.controller.algoritmo_escogido == "Random":
            self.tRandom.start()
        #self.crearLabels()
        self.draw()
        self.tOptimo.join()
        if self.controller.algoritmo_escogido == "Aging":
            self.tAging.join()
        if self.controller.algoritmo_escogido == "LRU":
            self.tLRU.join()
        if self.controller.algoritmo_escogido == "Second Chance":
            self.tSecondChance.join()
        if self.controller.algoritmo_escogido == "Random":
            self.tRandom.join()

        self.open_popup()
        sleep(10)

        sys.exit()

    def open_popup(self):
        print("INTENTANDOOOO")
        top= tk.Toplevel(self)
        top.geometry('750x250')
        top.title("Cerrando")
        tk.Label(top, text= "La memoria se liberará en 10 segundos. Después se cerrara el programa.", font=('Mistral 18 bold')).place(x=150,y=80)

    def debugcito(self):
        print(self.controller.seed)
        print(self.controller.algoritmo_escogido)

    def test(self):
        print(self.controller.fileContent)

    def optimo(self):
        self.simulador_optimo = Simulador("Optimo", self.controller.fileContent, self.controller.seed)
        self.simulador_optimo.correr_algoritmo()

    def aging(self):
        self.simulador_aging = Simulador("Aging", self.controller.fileContent, self.controller.seed)
        self.simulador_aging.correr_algoritmo()

    def lru(self):
        self.simulador_lru = Simulador("LRU", self.controller.fileContent, self.controller.seed)
        self.simulador_lru.correr_algoritmo()

    def random(self):
        self.simulador_random = Simulador("Random", self.controller.fileContent, self.controller.seed)
        self.simulador_random.correr_algoritmo()

    def secondchance(self):
        self.simulador_secondchance = Simulador("SecondChance", self.controller.fileContent, self.controller.seed)
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
