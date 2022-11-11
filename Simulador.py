from Algoritmos.Aging import Aging
from Algoritmos.LRU import LRU
from Algoritmos.Optimo import Optimo
from Algoritmos.Random import Random
from Algoritmos.SecondChance import SecondChance

from General.Memoria import Memoria
from General.MMU import MMU
from Stats.Stats import Stats

from General.itemMMU import itemMMU
from General.Pagina import Pagina

class Simulador:
  def __init__(self, tipoSimulador,txt):
    self.varasBarajadas = None
    self.varasSinBarajar = None
    self.RAM = Memoria()
    self.VRAM = Memoria()
    self.MMU = MMU()
    self.stats = Stats()
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
  
  def leer_txt(self):
    pass

  def barajar(self):
    pass
