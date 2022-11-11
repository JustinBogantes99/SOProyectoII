from time import sleep
import random

class Optimo:
    def __init__(self, simulador):
        self.simulador = simulador
        self.paginasMarcadas=[]  #lista con las paginas y la cantidad de accesos a memoria necesarios antes de ser usada [accesos,[pagina]]
        self.RamSize=6  #variable para determinar el tama;o de la ram
        for acceso in self.simulador.varasSinBarajar: 
            self.paginasMarcadas.append([0,acceso])

    #Calcula cuantos accesos a memoria faltan para que la paginas sea usada de nuevo
    def calcularAccesosfaltanttes(self):
            for x in range(len(self.simulador.varasSinBarajar)):
                contador=0
                for y in range(len(self.simulador.varasBarajadas)):
                    if self.simulador.varasSinBarajar[x].Ptr != self.simulador.varasBarajadas[y].Ptr:
                        contador=contador+1
                    else:
                        break 
                self.paginasMarcadas[x][0]=contador

    #Devuelve la cantidad de accesoss faltantes para utilizar la pagina ptr       
    def getFaltantes(self, ptr):
        for y in range( len(self.paginasMarcadas)):
            if self.paginasMarcadas[y][1].Ptr ==ptr:
                return self.paginasMarcadas[y][0]



    def calcularFragmentacionInternaOpt(self):
        self.FragmentacionInternaOpt=0
        for pagina in self.simulador.RAM:
            self.simulador.stats.FragmentacionInterna = self.simulador.stats.FragmentacionInterna + ((4000-pagina[2])/1000)
        return self.simulador.stats.FragmentacionInterna

    def calcularRAMUtilizadaYVRAM(self):
        self.simulador.stats.RAMUtilizada=len(self.simulador.RAM*4)
        self.simulador.stats.VRAMUtilizada = len(self.simulador.VRAM*4)

    def simular(self):
        while(len(self.simulador.varasBarajadas)>1):
            if len(self.simulador.RAM) < self.RAMSize:
                siguiente=self.simulador.varasBarajadas.pop(0)
                if self.simulador.RAM.count(siguiente)==0:
                    if self.simulador.VRAM.count(siguiente)>0:
                        self.simulador.VRAM.remove(siguiente)
                        self.simulador.RAM.append(siguiente)
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5

                    self.simulador.RAM.append(siguiente)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1
                
                else:
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1

                sleep(2)

            if len(self.simulador.RAM) >= self.RAMSize:
                siguiente= self.simulador.varasBarajadas.pop(0)
                if self.simulador.RAM.count(siguiente)==0:
                    maxIndx=0 #index de la pagina mas tardada
                    max=0 #accesos faltantes
                    for x in range(len(self.simulador.RAM)):
                        accessosfaltantes = self.getFaltantes(self.simulador.RAM[x][1])
                        if accessosfaltantes > max:
                            max = accessosfaltantes
                            maxIndx = x

                    siguiente= self.simulador.varasBarajadas.pop(0)
                    if self.simulador.VRAM.count(siguiente)>0:
                        self.simulador.VRAM.remove(siguiente)
                    self.simulador.VRAM.append(self.simulador.RAM[maxIndx])
                    self.simulador.RAM[maxIndx] = siguiente
                    self.simulador.stats.TiempoTrashing  = self.simulador.stats.TiempoTrashing  + 5
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 6
                
                self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1

                sleep(2)

            self.calcularAccesosfaltanttes()
            self.calcularFragmentacionInternaOpt()
            self.calcularRAMUtilizadaYVRAM()
            self.simulador.stats.PaginasEnMemoria= len(self.simulador.RAM)
            self.simulador.stats.PaginasEnDisco= len(self.simulador.VRAM)
            print("Tiempo total: ",self.simulador.stats.TiempoSimulado)
            print("Tiempo de Trashing: ",self.simulador.stats.TiempoTrashing)
            print("RAM utilizada: ", self.simulador.stats.RAMUtilizada)
            print("VRAM utilizada: ", self.simulador.stats.VRAMUtilizada)

            print("RAM-",self.simulador.RAM)
            print("VRRAM-",self.simulador.VRAM)
        return
