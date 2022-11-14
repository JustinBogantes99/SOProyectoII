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

        

        switch_window_button = tk.Button(
            self,
            text="Correr simulacion",
            command=self.correr_simulacion,
        )
        switch_window_button.pack(side="bottom", fill=tk.X)
         #Labels de estadisticas
        Optlabel_TSimulado = tk.Label(self, text="SIM-TIME")
        Optlabel_TSimuladoData = tk.Label(self, text=" ")

        Optlabel_Procesos = tk.Label(self, text="Procesos")
        Optlabel_ProcesosData = tk.Label(self, text=" ")

        Optlabel_URAM = tk.Label(self, text="RAM")
        Optlabel_URAMData = tk.Label(self, text=" ")

        Optlabel_UVRAM = tk.Label(self, text="VRAM")
        Optlabel_UVRAMData = tk.Label(self, text=" ")

        Optlabel_LPages = tk.Label(self, text="Loaded Pages")
        Optlabel_LPagesData = tk.Label(self, text=" ")        

        Optlabel_UPages = tk.Label(self, text="Unloaded Pages")
        Optlabel_UPagesData = tk.Label(self, text=" ")  

        Optlabel_Ttrashing = tk.Label(self, text="Trashing  Time")
        Optlabel_TTrashingData = tk.Label(self, text=" ") 

        Optlabel_TrashingPercent = tk.Label(self, text="Trashing Time %")
        Optlabel_TrashingPercentData  = tk.Label(self, text=" ")

        Optlabel_Frag = tk.Label(self, text="Fragmentacion")
        Optlabel_FragData  = tk.Label(self, text=" ")   

        label_TSimulado = tk.Label(self, text="SIM-TIME")
        label_TSimuladoData = tk.Label(self, text=" ")

        label_Procesos = tk.Label(self, text="Procesos")
        label_ProcesosData = tk.Label(self, text=" ")

        label_URAM = tk.Label(self, text="RAM")
        label_URAMData = tk.Label(self, text=" ")

        label_UVRAM = tk.Label(self, text="VRAM")
        label_UVRAMData = tk.Label(self, text=" ")

        label_LPages = tk.Label(self, text="Loaded Pages")
        label_LPagesData = tk.Label(self, text=" ")        

        label_UPages = tk.Label(self, text="Unloaded Pages")
        label_UPagesData = tk.Label(self, text=" ")  

        label_Ttrashing = tk.Label(self, text="Trashing  Time")
        label_TTrashingData = tk.Label(self, text=" ") 

        label_TrashingPercent = tk.Label(self, text="Trashing Time %")
        label_TrashingPercentData  = tk.Label(self, text=" ")   

        label_Frag = tk.Label(self, text="Fragmentacion")
        label_FragData  = tk.Label(self, text=" ")       

        #Posicion de los labels de estadisticas

        Optlabel_TSimulado.place(x=150, y=500)
        Optlabel_TSimuladoData.place(x=250 ,y=500)

        Optlabel_Procesos.place(x=150, y= 520) 
        Optlabel_ProcesosData.place(x=250, y= 520) 

        Optlabel_URAM.place(x=150, y= 540) 
        Optlabel_URAMData.place(x=250, y= 540)  

        Optlabel_UVRAM.place(x=150, y= 560)
        Optlabel_UVRAMData.place(x=250, y= 560)   

        Optlabel_LPages.place(x=150, y= 580)
        Optlabel_LPagesData.place(x=250, y= 580)    

        Optlabel_UPages.place(x=150, y= 600)
        Optlabel_UPagesData.place(x=250, y= 600)

        Optlabel_Ttrashing.place(x=150, y= 620)
        Optlabel_TTrashingData.place(x=250, y= 620)

        Optlabel_TrashingPercent.place(x=150, y= 640)
        Optlabel_TrashingPercentData.place(x=250, y= 640)

        Optlabel_Frag.place(x=150, y= 660)
        Optlabel_FragData.place(x=250, y= 660)



        label_TSimulado.place(x=850, y=500)
        label_TSimuladoData.place(x=850 ,y=500)

        label_Procesos.place(x=850, y= 520) 
        label_ProcesosData.place(x=250, y= 520) 

        label_URAM.place(x=850, y= 540) 
        label_URAMData.place(x=250, y= 540)  

        label_UVRAM.place(x=850, y= 560)
        label_UVRAMData.place(x=250, y= 560)   

        label_LPages.place(x=850, y= 580)
        label_LPagesData.place(x=250, y= 580)    

        label_UPages.place(x=850, y= 600)
        label_UPagesData.place(x=250, y= 600)

        label_Ttrashing.place(x=850, y= 620)
        label_TTrashingData.place(x=250, y= 620)

        label_TrashingPercent.place(x=850, y= 640)
        label_TrashingPercentData.place(x=250, y= 640)

        label_Frag.place(x=850, y= 660)
        label_FragData.place(x=250, y= 660)

        self.tOptimo = threading.Thread(target=self.optimo)
        self.tAging = threading.Thread(target=self.aging)
        self.tRandom = threading.Thread(target=self.random)
        self.tLRU = threading.Thread(target=self.lru)
        self.tSecondChance = threading.Thread(target=self.secondchance)

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
