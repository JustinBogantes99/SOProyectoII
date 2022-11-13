from Algoritmos.Aging import Aging
from Algoritmos.LRU import LRU
from Algoritmos.Optimo import Optimo
from Algoritmos.Random import Random
from Algoritmos.SecondChance import SecondChance
import copy
from .Memoria import Memoria
from .MMU import MMU
from .itemMMU import itemMMU
from .Pagina import Pagina
import random
from Stats.Stats import Stats

class Simulador:
  def __init__(self, tipoSimulador, txt, seed):
    self.seed = seed
    self.txt = txt
    self.varasBarajadas = []
    self.tipoSimulador = tipoSimulador
    self.ListadeAccesos = []
    self.ListaAccesosBarajados = []
    self.varasSinBarajar = []
    random.seed(self.seed)
    self.RAM = Memoria(100)
    self.VRAM = Memoria(100)
    self.MMU = MMU()
    self.stats = Stats()
    self.crearBaraja()
    if tipoSimulador == "LRU":
      self.algoritmo = LRU(self)
    if tipoSimulador == "Optimo":
      self.algoritmo = Optimo(self)
    if tipoSimulador == "Random":
      self.algoritmo = Random(self)
    if tipoSimulador == "SecondChance":
      self.algoritmo = SecondChance(self)
    if tipoSimulador == "Aging":
      self.algoritmo = Aging(self)
    
  def correr_algoritmo(self):
    self.algoritmo.simular()
  
  def leer_txt(self):
    self.txt.pop(0)
    lista=[]
    for i in range(len(self.txt)):
      lista+=[list(map(int, self.txt[i]))]
    print("\n\n\n")
    print("Lista enteros") 
    print(lista)
    self.ListadeAccesos=lista
  
  def crearBaraja(self):
    self.leer_txt()
    self.ListaAccesosBarajados= copy.deepcopy(self.ListadeAccesos)
    for x in range(0,50):
      ran= random.randint(0,len(self.ListadeAccesos)-1)
      self.ListaAccesosBarajados.append(self.ListadeAccesos[ran])
    random.shuffle(self.ListaAccesosBarajados)
    print("\n\n\n")
    print("Lista barajada")
    print(self.ListaAccesosBarajados)
    print("\n\n\n")
    
    for pagina in self.ListadeAccesos:
      nuevaPagina= Pagina()
      nuevaPagina.PID=pagina[0]
      nuevaPagina.Ptr=pagina[1]
      nuevaPagina.Size=pagina[2]
      nuevaPagina.Contador=0
      if self.tipoSimulador == "SecondChance":
        nuevaPagina.mark = False
      self.varasSinBarajar.append(nuevaPagina)

    for pagina in self.ListaAccesosBarajados:
      nuevaPagina= Pagina()
      nuevaPagina.PID=pagina[0]
      nuevaPagina.Ptr=pagina[1]
      nuevaPagina.Size=pagina[2]
      nuevaPagina.Contador=0
      if self.tipoSimulador == "SecondChance":
        nuevaPagina.mark = False
      self.varasBarajadas.append(nuevaPagina)      

    print("baraje")
    print(len(self.varasBarajadas))
    pass