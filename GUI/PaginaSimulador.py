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
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        label = tk.Label(self, text="Simulador")
        label.pack(padx=10)

        self.frame_ram=tk.LabelFrame(self, text="RAM-OPT")
        self.frame_ram.place(x=25,y=40)

        self.frame_vram=tk.LabelFrame(self, text="RAM-ALG")
        self.frame_vram.place(x=100,y=40)

        frame_opt=tk.LabelFrame(self, text="Algoritmo óptimo")
        frame_opt.place(x=180,y=40)

        frame_algoritmo=tk.LabelFrame(self, text="Algoritmo escogido")
        frame_algoritmo.place(x=870,y=40)

        self.frame_stats_opt=tk.LabelFrame(self, text="Estadísticas óptimo")
        self.frame_stats_opt.place(x=180,y=740)

        self.frame_stats=tk.LabelFrame(self, text="Algoritmo Escogido")
        self.frame_stats.place(x=870,y=740)

        #self.canvas_ram = tk.Canvas(frame_ram, bg="green", width=50, height=700)
        #self.canvas_ram.pack()

        #self.canvas_vram = tk.Canvas(self.frame_vram, bg="green", width=50, height=700)
        #self.canvas_vram.pack()

        self.canvas_mmu_opt = tk.Canvas(frame_opt, bg="blue", height=600, width=300)
        self.canvas_mmu_opt.pack()

        self.canvas_mmu = tk.Canvas(frame_algoritmo, bg="blue", height=600, width=650)
        self.canvas_mmu.pack()

        #self.canvas_stats_opt = tk.Canvas(frame_stats_opt, bg="yellow", height=150, width=650)
        #self.canvas_stats_opt.pack()

        #self.canvas_stats = tk.Canvas(frame_stats, bg="yellow", height=150, width=650)
        #self.canvas_stats.pack()


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

        self.opt = ttk.Treeview(self.canvas_mmu_opt, height=30,selectmode ='none')

        sb1 = Scrollbar(self.canvas_mmu_opt, orient=VERTICAL)
        sb1.pack(side=RIGHT, fill=Y)
        self.opt.config(yscrollcommand=sb1.set)
        sb1.config(command=self.opt.yview)

        self.alg = ttk.Treeview(self.canvas_mmu, height=30,selectmode ='none')

        sb2 = Scrollbar(self.canvas_mmu, orient=VERTICAL)
        sb2.pack(side=RIGHT, fill=Y)
        self.alg.config(yscrollcommand=sb2.set)
        sb2.config(command=self.alg.yview)

        self.tram = ttk.Treeview(self.frame_ram, height=50, selectmode ='none')

        sb3 = Scrollbar(self.frame_ram, orient=VERTICAL)
        sb3.pack(side=RIGHT, fill=Y)
        self.tram.config(yscrollcommand=sb3.set)
        sb3.config(command=self.tram.yview)

        self.tvram = ttk.Treeview(self.frame_vram, height=50, selectmode ='none')

        sb4 = Scrollbar(self.frame_vram, orient=VERTICAL)
        sb4.pack(side=RIGHT, fill=Y)
        self.tvram.config(yscrollcommand=sb4.set)
        sb4.config(command=self.tvram.yview)

        self.tstatsopt = ttk.Treeview(self.frame_stats_opt, height=7, selectmode ='none')

        sb5 = Scrollbar(self.frame_stats_opt, orient=VERTICAL)
        sb5.pack(side=RIGHT, fill=Y)
        self.tstatsopt.config(yscrollcommand=sb5.set)
        sb5.config(command=self.tstatsopt.yview)

        self.tstats = ttk.Treeview(self.frame_stats, height=7, selectmode ='none')

        sb6 = Scrollbar(self.frame_stats, orient=VERTICAL)
        sb6.pack(side=RIGHT, fill=Y)
        self.tstats.config(yscrollcommand=sb6.set)
        sb6.config(command=self.tstats.yview)

        self.opt['columns'] = ("Ptr", "PID", "LOADED", "L-ADDR", "M-ADDR", "D-ADDR", "LOADED-T", "Mark")
        self.alg['columns'] = ("Ptr", "PID", "LOADED", "L-ADDR", "M-ADDR", "D-ADDR", "LOADED-T", "Mark")
        self.tram['columns'] = ("Ptr")
        self.tvram['columns'] = ("Ptr")
        self.tstatsopt['columns'] = ("Estadistica", "Valor")
        self.tstats['columns'] = ("Estadistica", "Valor")
        self.tram.column("#0", width=0)
        self.tram.column("Ptr", anchor=CENTER, width=50)
        self.tram.heading("Ptr", text="Ptr", anchor=CENTER)
        self.tram.pack()

        self.tstatsopt.column("#0", width=0)
        self.tstatsopt.column("Estadistica", anchor=CENTER, width=300)
        self.tstatsopt.heading("Estadistica", text="Stat", anchor=CENTER)
        self.tstatsopt.column("Valor", anchor=CENTER, width=300)
        self.tstatsopt.heading("Valor", text="#", anchor=CENTER)
        self.tstatsopt.pack()

        self.tstats.column("#0", width=0)
        self.tstats.column("Estadistica", anchor=CENTER, width=300)
        self.tstats.heading("Estadistica", text="Stat", anchor=CENTER)
        self.tstats.column("Valor", anchor=CENTER, width=300)
        self.tstats.heading("Valor", text="#", anchor=CENTER)
        self.tstats.pack()


        self.tvram.column("#0", width=0)
        self.tvram.column("Ptr", anchor=CENTER, width=50)
        self.tvram.heading("Ptr", text="Ptr", anchor=CENTER)
        self.tvram.pack()


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
        self.opt.pack(expand=True, fill="both")

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
        for item in self.opt.get_children():
            self.opt.delete(item)
        for item in self.alg.get_children():
            self.alg.delete(item)
        for item in self.tram.get_children():
            self.tram.delete(item)
        for item in self.tvram.get_children():
            self.tvram.delete(item)
        for item in self.tstatsopt.get_children():
            self.tstatsopt.delete(item)
        for item in self.tstats.get_children():
            self.tstats.delete(item)


        if not self.simulador_optimo == None:
            self.tstatsopt.insert('', 'end', values=("Tiempo Simulado",self.simulador_optimo.stats.TiempoSimulado))
            self.tstatsopt.insert('', 'end', values=("Tiempo Trashing",self.simulador_optimo.stats.TiempoTrashing))
            self.tstatsopt.insert('', 'end', values=("Fragmentacion Interna",self.simulador_optimo.stats.FragmentacionInterna))
            self.tstatsopt.insert('', 'end', values=("RAM Utilizada",self.simulador_optimo.stats.RAMUtilizada))
            self.tstatsopt.insert('', 'end', values=("VRAM Utilizados",self.simulador_optimo.stats.VRAMUtilizada))
            self.tstatsopt.insert('', 'end', values=("Paginas en Memoria",self.simulador_optimo.stats.PaginasEnMemoria))
            self.tstatsopt.insert('', 'end', values=("Paginas en Disco",self.simulador_optimo.stats.PaginasEnDisco))
            for pag in self.simulador_optimo.RAM.contenido:
                self.tram.insert('', 'end', values=(pag.Ptr), tags=(pag.PID))
            for item in self.simulador_optimo.MMU.listaDeCositas.items():
                item = item[1]
                self.opt.insert('', 'end', values=(item.pageID, 
                                                    item.processID, 
                                                    item.loaded, 
                                                    item.LAddres, 
                                                    item.MAddres, 
                                                    item.DAddres, 
                                                    item.time, 
                                                    item.mark ), tags=(item.processID))
            for pag in self.simulador.varasSinBarajar:
                self.tram.tag_configure(pag.PID, background=self.simulador.colorcitos[pag.PID])
                self.opt.tag_configure(pag.PID, background=self.simulador.colorcitos[pag.PID])                                       
        if not self.simulador == None:
            self.tstats.insert('', 'end', values=("Tiempo Simulado",self.simulador.stats.TiempoSimulado))
            self.tstats.insert('', 'end', values=("Tiempo Trashing",self.simulador.stats.TiempoTrashing))
            self.tstats.insert('', 'end', values=("Fragmentacion Interna",self.simulador.stats.FragmentacionInterna))
            self.tstats.insert('', 'end', values=("RAM Utilizada",self.simulador.stats.RAMUtilizada))
            self.tstats.insert('', 'end', values=("VRAM Utilizados",self.simulador.stats.VRAMUtilizada))
            self.tstats.insert('', 'end', values=("Paginas en Memoria",self.simulador.stats.PaginasEnMemoria))
            self.tstats.insert('', 'end', values=("Paginas en Disco",self.simulador.stats.PaginasEnDisco))
            for pag in self.simulador.RAM.contenido:
                self.tvram.insert('', 'end', values=(pag.Ptr), tags=(pag.PID))
            for item in self.simulador.MMU.listaDeCositas.items():
                item = item[1]
                self.alg.insert('', 'end', values=(item.pageID, 
                                                    item.processID, 
                                                    item.loaded, 
                                                    item.LAddres, 
                                                    item.MAddres, 
                                                    item.DAddres, 
                                                    item.time, 
                                                    item.mark ), tags=(item.processID))
            for pag in self.simulador.varasSinBarajar:
                self.tvram.tag_configure(pag.PID, background=self.simulador.colorcitos[pag.PID])
                self.alg.tag_configure(pag.PID, background=self.simulador.colorcitos[pag.PID])

        self.sim = self.parent.after(500, self.draw)

    def correr_simulacion(self):
        print("AYUDAME JESUS")
        print(self.controller.fileContent)
        self.tmp = copy.deepcopy(self.controller.fileContent)
        if self.controller.algoritmo_escogido == "Aging":
            self.tAging.start()
        if self.controller.algoritmo_escogido == "LRU":
            self.tLRU.start()
        if self.controller.algoritmo_escogido == "Second Chance":
            self.tSecondChance.start()
        if self.controller.algoritmo_escogido == "Random":
            self.tRandom.start()
        self.tOptimo.start()


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

