import pprint
from sre_parse import TYPE_FLAGS
import sys
from time import sleep
from .shared_imports import *
from General.Simulador import Simulador
import random
import threading
import numpy as np
from tkinter import *
import copy

class PaginaSimulador(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Aqui va el simulador con las tablas")
        label.pack(padx=10)

        frame_memoria=tk.Frame(self, width=1400, height=200)
        frame_memoria.place(x=25,y=30)

        frame_opt=tk.Frame(self,  height=600, width=650)
        frame_opt.place(x=25,y=220)

        frame_algoritmo=tk.Frame(self, height=600, width=650)
        frame_algoritmo.place(x=775,y=220)

        frame_stats_opt=tk.Frame(self,height=150, width=650)
        frame_stats_opt.place(x=25,y=850)

        frame_stats=tk.Frame(self,height=150, width=650)
        frame_stats.place(x=775,y=850)

        self.canvas_memory = tk.Canvas(frame_memoria, bg="green", width=1400, height=175)
        self.canvas_memory.pack()

        self.canvas_mmu_opt = tk.Canvas(frame_opt, bg="blue", height=600, width=650)
        self.canvas_mmu_opt.pack()

        self.canvas_mmu = tk.Canvas(frame_algoritmo, bg="blue", height=600, width=650)
        self.canvas_mmu.pack()

        self.canvas_stats_opt = tk.Canvas(frame_stats_opt, bg="yellow", height=150, width=650)
        self.canvas_stats_opt.pack()

        self.canvas_stats = tk.Canvas(frame_stats, bg="yellow", height=150, width=650)
        self.canvas_stats.pack()

        self.label_test = tk.Label(self.canvas_stats_opt, text="Buenas")
        self.label_test.place(x=10,y=10)

        self.controller = controller
        self.tmp = []
        self.tamanio=(len(self.controller.fileContent)-1)+(len(self.controller.fileContent)*2)
        self.sim = None
        self.parent = parent
        self.simulador_optimo = None
        self.simulador = None

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

        self.opt = ttk.Treeview(self.canvas_mmu_opt, selectmode ='none')
        sb = Scrollbar(self.canvas_mmu_opt, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)

        self.opt.config(yscrollcommand=sb.set)
        sb.config(command=self.opt.yview)

        self.alg = ttk.Treeview(self.canvas_mmu, selectmode ='none')

        sb = Scrollbar(self.canvas_mmu, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)

        self.alg.config(yscrollcommand=sb.set)
        sb.config(command=self.alg.yview)

        self.opt['columns'] = ("Ptr", "PID", "LOADED", "L-ADDR", "M-ADDR", "D-ADDR", "LOADED-T", "Mark")
        self.alg['columns'] = ("Ptr", "PID", "LOADED", "L-ADDR", "M-ADDR", "D-ADDR", "LOADED-T", "Mark")

        self.opt.column("#0", width=0)
        self.opt.column("Ptr", anchor=CENTER, width=80)
        self.opt.column("PID", anchor=CENTER, width=80)
        self.opt.column("LOADED", anchor=CENTER, width=80)
        self.opt.column("L-ADDR", anchor=CENTER, width=80)
        self.opt.column("M-ADDR", anchor=CENTER, width=80)
        self.opt.column("D-ADDR", anchor=CENTER, width=80)
        self.opt.column("LOADED-T", anchor=CENTER, width=80)
        self.opt.column("Mark", anchor=CENTER, width=80)

        self.opt.heading("#0",text='')
        self.opt.heading("Ptr", text="Ptr", anchor=CENTER)
        self.opt.heading("PID", text="PID", anchor=CENTER)
        self.opt.heading("LOADED", text="LOADED", anchor=CENTER)
        self.opt.heading("L-ADDR", text="L-ADDR", anchor=CENTER)
        self.opt.heading("M-ADDR", text="M-ADDR", anchor=CENTER)
        self.opt.heading("D-ADDR", text="D-ADDR", anchor=CENTER)
        self.opt.heading("LOADED-T", text="LOADED-T", anchor=CENTER)
        self.opt.heading("Mark", text="Mark", anchor=CENTER)
        self.opt.pack()

        self.alg.column("#0", width=0)
        self.alg.column("Ptr", anchor=CENTER, width=80)
        self.alg.column("PID", anchor=CENTER, width=80)
        self.alg.column("LOADED", anchor=CENTER, width=80)
        self.alg.column("L-ADDR", anchor=CENTER, width=80)
        self.alg.column("M-ADDR", anchor=CENTER, width=80)
        self.alg.column("D-ADDR", anchor=CENTER, width=80)
        self.alg.column("LOADED-T", anchor=CENTER, width=80)
        self.alg.column("Mark", anchor=CENTER, width=80)

        self.alg.heading("#0",text='')
        self.alg.heading("Ptr", text="Ptr", anchor=CENTER)
        self.alg.heading("PID", text="PID", anchor=CENTER)
        self.alg.heading("LOADED", text="LOADED", anchor=CENTER)
        self.alg.heading("L-ADDR", text="L-ADDR", anchor=CENTER)
        self.alg.heading("M-ADDR", text="M-ADDR", anchor=CENTER)
        self.alg.heading("D-ADDR", text="D-ADDR", anchor=CENTER)
        self.alg.heading("LOADED-T", text="LOADED-T", anchor=CENTER)
        self.alg.heading("Mark", text="Mark", anchor=CENTER)
        self.alg.pack()
        self.draw()



    def draw(self):
        self.label_test.config(text = str(random.randint(0,5)))
        for item in self.opt.get_children():
            self.opt.delete(item)
        for item in self.alg.get_children():
            self.alg.delete(item)

        if not self.simulador_optimo == None:
            for item in self.simulador_optimo.MMU.listaDeCositas.items():
                item = item[1]
                self.opt.insert('', 'end', values=(item.pageID, 
                                                    item.processID, 
                                                    item.loaded, 
                                                    item.LAddres, 
                                                    item.MAddres, 
                                                    item.DAddres, 
                                                    item.time, 
                                                    item.mark ))
        if not self.simulador == None:
            for item in self.simulador.MMU.listaDeCositas.items():
                item = item[1]
                self.alg.insert('', 'end', values=(item.pageID, 
                                                    item.processID, 
                                                    item.loaded, 
                                                    item.LAddres, 
                                                    item.MAddres, 
                                                    item.DAddres, 
                                                    item.time, 
                                                    item.mark ))
        

        self.sim = self.parent.after(500, self.draw)

    def correr_simulacion(self):
        print("AYUDAME JESUS")
        print(self.controller.fileContent)
        self.tmp = copy.deepcopy(self.controller.fileContent)
        self.tOptimo.start()
        if self.controller.algoritmo_escogido == "Aging":
            self.tAging.start()
        if self.controller.algoritmo_escogido == "LRU":
            self.tLRU.start()
        if self.controller.algoritmo_escogido == "Second Chance":
            self.tSecondChance.start()
        if self.controller.algoritmo_escogido == "Random":
            self.tRandom.start()


    def optimo(self):
        self.simulador_optimo = Simulador("Optimo", self.controller.fileContent, self.controller.seed)
        self.simulador_optimo.correr_algoritmo()

    def aging(self):
        self.simulador = Simulador("Aging", self.tmp, self.controller.seed)
        self.simulador.correr_algoritmo()

    def lru(self):
        self.simulador = Simulador("LRU", self.tmp, self.controller.seed)
        self.simulador.correr_algoritmo()

    def random(self):
        self.simulador = Simulador("Random", self.tmp, self.controller.seed)
        self.simulador.correr_algoritmo()

    def secondchance(self):
        self.simulador = Simulador("SecondChance", self.tmp, self.controller.seed)
        self.simulador.correr_algoritmo()

