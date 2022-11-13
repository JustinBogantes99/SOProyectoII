from .shared_imports import *
from General.Simulador import Simulador

class PaginaSimulador(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.simulador_optimo = None
        self.simulador_usuario = None
        label = tk.Label(self, text="Aqui va el simulador con las tablas")
        label.pack(padx=10, pady=10)

        txt_button = tk.Button(
            self,
            text="Mostrar lista de procesos del txt",
            command=self.test,
        )
        txt_button.pack(side="bottom", fill=tk.X)

        representarValores= [ " Page ID ","PID","LOADED","L-ADDR","M-ADDR","LOADED-T","Mark"]
        frme_venta_optimo=tk.Frame(self, parent,width=400,height=300,bg="#FFE4B5")
        frme_venta_optimo.place(x=20,y=100)

        frme_venta_algoritmo=tk.Frame(self, parent,width=400,height=300,bg="blue")
        frme_venta_algoritmo.place(x=750,y=100)
        
        labelsOpt=[]
        labelsAlgo=[]

        for i in range(len(representarValores)):
            labelsOpt+=[tk.Label(frme_venta_optimo,text=representarValores[i],bd=30,bg="#FFE4B5")]
        
        fila=0
        columna=0       
        for x in labelsOpt:
            x.grid(row=fila,column=columna) 
            columna+=1

        for j in range(len(representarValores)):
            labelsAlgo+=[tk.Label(frme_venta_algoritmo,text=representarValores[j],bd=30,bg="#FFE4B5")]
        
        fila=0
        columna=0       
        for y in labelsAlgo:
            y.grid(row=fila,column=columna) 
            columna+=1    
      

        scrollbarOptimo = tk.Scrollbar(frme_venta_optimo, orient=tk.VERTICAL, command=labelsOpt)
        scrollbarOptimo.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
        
        scrollbarAlgoritmo = tk.Scrollbar(frme_venta_algoritmo, orient=tk.VERTICAL, command=labelsAlgo)
        scrollbarAlgoritmo.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
        
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
            command=lambda: controller.show_frame(PaginaDebugger),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

    def acomodar(self,):
        pass

    def test(self):
        print(self.controller.fileContent)

    def optimo(self):
        self.simulador_optimo = Simulador("Optimo", self.controller.fileContent)
        self.simulador_optimo.correr_algoritmo()

    def aging(self):
        self.simulador_optimo = Simulador("Aging", self.controller.fileContent)
        self.simulador_optimo.correr_algoritmo()

    def lru(self):
        self.simulador_optimo = Simulador("LRU", self.controller.fileContent)
        self.simulador_optimo.correr_algoritmo()

    def random(self):
        self.simulador_optimo = Simulador("Random", self.controller.fileContent)
        self.simulador_optimo.correr_algoritmo()

    def secondchance(self):
        self.simulador_optimo = Simulador("SecondChance", self.controller.fileContent)
        self.simulador_optimo.correr_algoritmo()

class PaginaDebugger(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Para utilizar proximamente para ver prints del proceso")
        label.pack(padx=10, pady=10)
        switch_window_button = ttk.Button(
            self, text="De vuelta al simulador", command=lambda: controller.show_frame(PaginaSimulador)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)
