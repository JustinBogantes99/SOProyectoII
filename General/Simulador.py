from Algoritmos.Aging import Aging
from Algoritmos.LRU import LRU
from Algoritmos.Optimo import Optimo
from Algoritmos.Random import Random
from Algoritmos.SecondChance import SecondChance

from .Memoria import Memoria
from .MMU import MMU
from .itemMMU import itemMMU
from .Pagina import Pagina

from Stats.Stats import Stats

class Simulador:
  def __init__(self, tipoSimulador, txt):
    self.txt = txt
    self.varasBarajadas = []
    self.tipoSimulador = tipoSimulador
    self.ListadeAccesos = []
    self.ListaAccesosBarajados = []
    self.varasSinBarajar = []
    self.RAM = Memoria()
    self.VRAM = Memoria()
    self.MMU = MMU()
    self.stats = Stats()
    self.barajar()
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
    


  def barajar(self):
    self.ListadeAccesos=[[1,1,500]
    ,[1,2,1024]
    ,[1,3,512]
    ,[2,4,256]
    ,[2,5,512]
    ,[3,6,128]
    ,[3,7,1024]
    ,[3,8,512]
    ,[3,9,512]
    ,[4,10,256]
]
    self.ListaAccesosBarajados=[[1,1,500]
    ,[3,6,128]
    ,[3,9,512]
    ,[3,9,512]
    ,[1,1,500]
    ,[1,2,1024]
    ,[2,4,256]
    ,[2,4,256]
    ,[1,2,1024]
    ,[2,5,512]
    ,[4,10,256]
    ,[1,3,512]
    ,[1,3,512]
    ,[2,5,512]
    ,[3,7,1024]
    ,[4,10,256]
    ,[4,10,256]
    ,[3,8,512]
    ,[1,1,500]
    ,[2,5,512]
    ,[3,8,512]
    ,[3,9,512]
    ,[3,7,1024]
    ]

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

  def correr_algoritmo(self):
    self.algoritmo.simular()
  
  def leer_txt(self):
    pass

 # def barajar(self):
  #  pass
