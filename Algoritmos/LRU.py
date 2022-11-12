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

    # Esto se tiene que llamar simular
    def simular(self):
        print("Corriendo el print")

        # Mientras haya algo por procesar
        while(len(self.simulador.varasBarajadas)>1):
            siguiente = self.simulador.varasBarajadas.pop(0)
            print("\n\n\n")
            print("---------------------")
            print("Iteración", len(self.simulador.varasBarajadas))
            print("Tomando la página PID", siguiente.PID, " Ptr", siguiente.Ptr)
            print("Actualmente la RAM tiene: \n\n")
            print(self.simulador.RAM.to_string())
            print("Actualmente la VRAM tiene: \n\n")
            print(self.simulador.VRAM.to_string())
            print("\n\n\n")
            # Si no se ha llenado la RAM
            if len(self.simulador.RAM.contenido) < 5:#self.simulador.RAMSize
                print("La RAM no está llena, metiendo un nuevo proceso")
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

            # Si la RAM esta llena
            else:
                print("La RAM está llena, intercambio de paginas activado")

                # Si la pagina no se encuentra en RAM
                if self.simulador.RAM.encontrar(siguiente.Ptr)==False:
                    print("No encontré la página en RAM")

                    # Si la página se encuentra en VRAM
                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        print("Encontré la página en VRAM")
                        # self.simulador.VRAM.contenido.remove(siguiente)
                        Paginamayor=self.sacarMayorLRU()
                        cont = 0
                        for pagina in self.simulador.RAM.contenido:
                            if pagina.Ptr==Paginamayor.Ptr:
                                siguiente.Contador = 0
                                self.simulador.RAM.contenido[cont]=siguiente
                                pagina.Contador = 0
                                self.simulador.VRAM.contenido.append(pagina)

                                for index, pagina in enumerate(self.simulador.VRAM.contenido):
                                    if pagina.Ptr == siguiente.Ptr:
                                        self.simulador.VRAM.contenido.pop(index)

                            cont+=1
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5

                    # La página no se encontro en VRAM - Hay que crearla
                    else:
                        print("No encontré la página en VRAM")
                        Paginamayor = self.sacarMayorLRU()
                        cont = 0
                        for pagina in self.simulador.RAM.contenido:
                            if pagina.Ptr==Paginamayor.Ptr:
                                siguiente.Contador = 0
                                self.simulador.RAM.contenido[cont]=siguiente
                                pagina.Contador = 0
                                self.simulador.VRAM.contenido.append(pagina)
                            cont+=1

 
                # La página se encontró en RAM (Aplicar LRU al mark)
                elif self.simulador.RAM.encontrar(siguiente.Ptr):
                    print("La página se encontró en RAM")
                    for pag in self.simulador.RAM.contenido:
                        if pag.Ptr==siguiente.Ptr:
                            pag.Contador=0
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

                # Hago las paginas mas viejas
                if len(self.simulador.RAM.contenido)!=0:
                    for pagina in self.simulador.RAM.contenido:
                        pagina.Contador+=1

        self.simulador.stats.PaginasEnMemoria= len(self.simulador.RAM.contenido)
        self.simulador.stats.PaginasEnDisco= len(self.simulador.VRAM.contenido)
        print("Tiempo total: ",self.simulador.stats.TiempoSimulado)
        print("Tiempo de Trashing: ",self.simulador.stats.TiempoTrashing)
        print("RAM utilizada: ", self.simulador.stats.RAMUtilizada)
        print("VRAM utilizada: ", self.simulador.stats.VRAMUtilizada)
        self.printMemorias()
