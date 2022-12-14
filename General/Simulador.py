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
    self.colorcitos = {}
    random.seed(self.seed)
    self.RAM = Memoria(100, self.seed)
    self.VRAM = Memoria(100, self.seed)
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

  def random_color(self):
    r = lambda: random.randint(0,255)
    color = '#%02X%02X%02X' % (r(),r(),r())
    return color

  def color(self, PID):
    if PID in self.colorcitos.keys():
      pass
    else:
      self.colorcitos[PID]=self.random_color()
    
  def correr_algoritmo(self):
    self.algoritmo.simular()
  
  def leer_txt(self):
    self.txt.pop(0)
    max_ptr=int(self.txt[-1][1])+1
    lista=[]
    for i in range(len(self.txt)):
      if int(self.txt[i][2])>4096:
        max_ptr,nuevos=self.agregarProcesos(max_ptr,self.txt[i])
        max_ptr+=1
        for proceso in nuevos:
          lista+=[proceso]
      else:
        lista+=[list(map(int, self.txt[i]))]
    self.ListadeAccesos=lista

  def agregarProcesos(self,max,proceso):
    max=int(max)
    memoria=int(proceso[2])//4096
    lista=[]
    cantidadMemoria=int(proceso[2])-(memoria*4096)
    for x in range(memoria):
      pag=[int(proceso[0]),max,4096]
      lista.append(pag)
      max+=1
    lista.append([int(proceso[0]),max,cantidadMemoria])
    return max,lista
  
  def crearBaraja(self):
    self.leer_txt()
    self.ListaAccesosBarajados= copy.deepcopy(self.ListadeAccesos)
    for x in range(0,len(self.ListaAccesosBarajados)*2):
      ran= random.randint(0,len(self.ListadeAccesos)-1)
      self.ListaAccesosBarajados.append(self.ListadeAccesos[ran])
    random.shuffle(self.ListaAccesosBarajados)
    for pagina in self.ListadeAccesos:
      self.color(pagina[0])
      nuevaPagina= Pagina()
      nuevaPagina.PID=pagina[0]
      nuevaPagina.Ptr=pagina[1]
      nuevaPagina.Size=pagina[2]
      nuevaPagina.Contador=0
      if self.tipoSimulador == "SecondChance":
        nuevaPagina.mark = False
      self.varasSinBarajar.append(nuevaPagina)

    print("Lista de Accesos Barajados")
    print(self.ListaAccesosBarajados)
    print('\n\n')

    for pagina in self.ListaAccesosBarajados:
      nuevaPagina= Pagina()
      nuevaPagina.PID=pagina[0]
      nuevaPagina.Ptr=pagina[1]
      nuevaPagina.Size=pagina[2]
      nuevaPagina.Contador=0
      if self.tipoSimulador == "SecondChance":
        nuevaPagina.mark = False
      self.varasBarajadas.append(nuevaPagina)