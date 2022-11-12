from time import sleep
import random

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
        lista=[]
        for x in self.RAMLRU:
            lista+=[x[3]]
        self.valoMax=max(lista)
        return self.valoMax

    def run(self):
        print("Corriendo el print")
        while(len(self.simulador.varasBarajadas)>1):
            if len(self.simulador.RAM) < self.RAMSize:
                siguiente=self.simulador.varasBarajadas.pop(0)
                if self.simulador.RAM.count(siguiente)==0:
                    if self.simulador.VRAM.count(siguiente)>0:
                        self.simulador.VRAM.remove(siguiente)
                        self.simulador.RAM.append(siguiente)
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5
                    if len(self.RAM)!=0:
                        for pagina in self.RAM:
                            pagina.contador+=1
                    siguiente.contador+=1        
                    self.RAM.append(siguiente)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1
                elif self.RAM.count(siguiente)!=0:
                    for pag in self.RAM:
                        if pag.pid == siguiente.pid:
                            pag.contador=0
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

            if len(self.RAM) >= self.RAMSize:
                siguiente=self.simulador.varasBarajadas.pop(0)

                if self.RAM.count(siguiente)==0: 
                    mayor=self.sacarMayorLRU()
                    cont=0
                    for pagina in self.RAM:
                        if pagina.contador==mayor:
                            siguiente.contador+=1  

                            self.RAM[cont]=siguiente

                            self.VRAM.append(pagina)
                        cont+=1

                    if len(self.RAM)!=0:
                        for pagina in self.RAM:
                            pagina.contador+=1 


                elif self.RAM.count(siguiente)==0:
                    for pag in self.RAM:
                        if pag.PID==siguiente.PID:
                            pag.contador=0
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1
        self.simulador.stats.PaginasEnMemoria= len(self.simulador.RAM)
        self.simulador.stats.PaginasEnDisco= len(self.simulador.VRAM)
        print("Tiempo total: ",self.simulador.stats.TiempoSimulado)
        print("Tiempo de Trashing: ",self.simulador.stats.TiempoTrashing)
        print("RAM utilizada: ", self.simulador.stats.RAMUtilizada)
        print("VRAM utilizada: ", self.simulador.stats.VRAMUtilizada)

        print("RAM-",self.simulador.RAM)
        print("VRRAM-",self.simulador.VRAM)

        
    def simular(self):
        self.run(self)
