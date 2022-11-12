from time import sleep
import random
from operator import attrgetter
class LRU:

    def __init__(self, simulador):
        self.simulador = simulador
        self.paginasMarcadas=[]

    def calcularFragmentacionInternaOpt(self):
        self.FragmentacionInternaOpt=0
        for pagina in self.simulador.RAM:
            self.simulador.stats.FragmentacionInterna = self.simulador.stats.FragmentacionInterna + ((4000-pagina[2])/1000)
        return self.simulador.stats.FragmentacionInterna

    def calcularRAMUtilizadaYVRAM(self):
        self.simulador.stats.RAMUtilizada=len(self.simulador.RAM*4)
        self.simulador.stats.VRAMUtilizada = len(self.simulador.VRAM*4)
        
    def sacarMayorLRU(self):
        paginas=self.simulador.RAM.contenido
        max_attr = max(paginas, key=attrgetter('Contador'))
        return max_attr

    def printMemorias(self):
        ram="RAM-["
        vram="VRAM-["
        for pagina in self.simulador.RAM.contenido:
            ram=ram+str(pagina.Ptr)+","
        
        ram=ram+"]"
        for pagina in self.simulador.VRAM.contenido:
            vram=vram+str(pagina.Ptr)+","

        vram=vram+"]"

        print(ram)
        print(vram)

    def run(self):
        print("Corriendo el print")
        while(len(self.simulador.varasBarajadas)>1):
            if len(self.simulador.RAM.contenido) < 5:#self.simulador.RAMSize
                siguiente=self.simulador.varasBarajadas.pop(0)
                if self.simulador.RAM.encontrar(siguiente.Ptr)==False:
                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        self.simulador.VRAM.contenido.remove(siguiente)
                        self.simulador.RAM.contenido.append(siguiente)
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5

                    if len(self.simulador.RAM.contenido)!=0:
                        for pagina in self.simulador.RAM.contenido:
                            pagina.Contador+=1
                            
                    siguiente.Contador+=1        
                    self.simulador.RAM.contenido.append(siguiente)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

                elif self.simulador.RAM.encontrar(siguiente.Ptr)==True:
                    for pag in self.self.simulador.RAM.contenido:
                        if pag.Ptr == siguiente.Ptr:
                            pag.contador=0
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1
            
            if len(self.simulador.RAM.contenido) >= 5:
                siguiente=self.simulador.varasBarajadas.pop(0)
                if self.simulador.RAM.encontrar(siguiente.Ptr)==False: 

                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        #self.simulador.VRAM.contenido.remove(siguiente)
                        Paginamayor=self.sacarMayorLRU()
                        for pagina in self.simulador.RAM.contenido:
                            if pagina.Ptr==Paginamayor.Ptr:
                                siguiente.Contador+=1  
                                self.simulador.RAM.contenido[cont]=siguiente
                                self.simulador.VRAM.contenido.append(pagina)
                            cont+=1
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5

                    else:    
                        Paginamayor=self.sacarMayorLRU()
                        cont=0
                        for pagina in self.simulador.RAM.contenido:
                            if pagina.Ptr==Paginamayor.Ptr:
                                siguiente.Contador+=1  
                                self.simulador.RAM.contenido[cont]=siguiente
                                self.simulador.VRAM.contenido.append(pagina)
                            cont+=1
                    if len(self.simulador.RAM.contenido)!=0:
                        for pagina in self.simulador.RAM.contenido:
                            pagina.Contador+=1 

                elif self.simulador.RAM.encontrar(siguiente.Ptr):
                    for pag in self.simulador.RAM.contenido:
                        if pag.Ptr==siguiente.Ptr:
                            pag.Contador=0
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

        self.simulador.stats.PaginasEnMemoria= len(self.simulador.RAM.contenido)
        self.simulador.stats.PaginasEnDisco= len(self.simulador.VRAM.contenido)
        print("Tiempo total: ",self.simulador.stats.TiempoSimulado)
        print("Tiempo de Trashing: ",self.simulador.stats.TiempoTrashing)
        print("RAM utilizada: ", self.simulador.stats.RAMUtilizada)
        print("VRAM utilizada: ", self.simulador.stats.VRAMUtilizada)
        print("")
        self.printMemorias()

        
    def simular(self):
        self.run()
