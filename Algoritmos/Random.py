import random
from time import sleep
class Random:
    def __init__(self, simulador):
        self.simulador = simulador
        self.RAMSize=6 
        pass
    
    def calcularFragmentacionInternaOpt(self):
        self.FragmentacionInternaOpt=0
        for pagina in self.simulador.RAM.contenido:
            self.simulador.stats.FragmentacionInterna = self.simulador.stats.FragmentacionInterna + ((4000-pagina.Size)/1000)
        return self.simulador.stats.FragmentacionInterna

    def calcularRAMUtilizadaYVRAM(self):
        self.simulador.stats.RAMUtilizada=len(self.simulador.RAM.contenido)*4
        self.simulador.stats.VRAMUtilizada = len(self.simulador.VRAM.contenido)*4
    
    
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

   
    # AQUI TIENE QUE IR TODA LA IMPLEMENTACION DE LOS METODOS PARA HACER FUNCIONAR EL ALGORITMO
    # NO CAMBIAR EL NOMBRE

    def simular(self):
        
        while(len(self.simulador.varasBarajadas)>1):
            if len(self.simulador.RAM.contenido) < self.RAMSize:
                siguiente=self.simulador.varasBarajadas.pop(0)
                if self.simulador.RAM.encontrar(siguiente.Ptr):
                    print("esta")
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1
                
                else:

                    print("no esta")
                    if self.simulador.VRAM.contenido.count(siguiente)>0:
                        self.simulador.VRAM.contenido.remove(siguiente)
                        self.simulador.RAM.contenido.append(siguiente)
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5

                    self.simulador.RAM.contenido.append(siguiente)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

                sleep(2)

            if len(self.simulador.RAM.contenido) >= self.RAMSize:
                siguiente= self.simulador.varasBarajadas.pop(0)
                elegido=random.randint(0,len(self.simulador.RAM.contenido)-1)
                if self.simulador.RAM.encontrar(siguiente.Ptr):
                    print("esta")
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1
                    
                    
                
                else:
                    if self.simulador.VRAM.encontrar(siguiente.Ptr):
                        self.simulador.VRAM.contenido.remove(siguiente)
                    self.simulador.VRAM.contenido.append(self.simulador.RAM.contenido[elegido])
                    self.simulador.RAM.contenido[elegido] = siguiente
                    self.simulador.stats.TiempoTrashing  = self.simulador.stats.TiempoTrashing  + 5
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 6

                sleep(2)

            
            self.calcularFragmentacionInternaOpt()
            self.calcularRAMUtilizadaYVRAM()
            self.simulador.stats.PaginasEnMemoria= len(self.simulador.RAM.contenido)
            self.simulador.stats.PaginasEnDisco= len(self.simulador.VRAM.contenido)
            print("Tiempo total: ",self.simulador.stats.TiempoSimulado)
            print("Tiempo de Trashing: ",self.simulador.stats.TiempoTrashing)
            print("RAM utilizada: ", self.simulador.stats.RAMUtilizada)
            print("VRAM utilizada: ", self.simulador.stats.VRAMUtilizada)
            self.printMemorias()

        pass
