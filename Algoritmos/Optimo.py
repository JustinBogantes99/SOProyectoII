from time import sleep
import random

class Optimo:
    def __init__(self, simulador):
        self.simulador = simulador
        self.paginasMarcadas=[]  #lista con las paginas y la cantidad de accesos a memoria necesarios antes de ser usada [accesos,[pagina]]
        self.RAMSize=6  #variable para determinar el tama;o de la ram
        self.hacerPaginasMarcadas()



    def hacerPaginasMarcadas(self):
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
        for pagina in self.simulador.RAM.contenido:
            self.simulador.stats.FragmentacionInterna = self.simulador.stats.FragmentacionInterna + ((4000-pagina.Size)/1000)
        return self.simulador.stats.FragmentacionInterna

    def calcularRAMUtilizadaYVRAM(self):
        self.simulador.stats.RAMUtilizada=len(self.simulador.RAM.contenido)*4
        self.simulador.stats.VRAMUtilizada = len(self.simulador.VRAM.contenido)*4

    def simular(self):
        print("CorriendoOptimo")
        while(len(self.simulador.varasBarajadas)>1):
            #sleep(2)
            siguiente=self.simulador.varasBarajadas.pop(0)

            # La RAM todavía no está llena
            if len(self.simulador.RAM.contenido) < self.RAMSize:

                # No se pudo encontrar la página en la RAM
                if not self.simulador.RAM.encontrar(siguiente.Ptr):
                    #self.simulador.VRAM.encontrar(siguiente.Ptr)==True  
                    #no seria cambiar a esto?

                    # La página se encontró en la VRAM
                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        print("VRAM NO FULL PAGE FAULT - TOMANDO PAGINA DE VRAM")
                        for index, pagina in enumerate(self.simulador.VRAM.contenido):
                            if pagina.Ptr == siguiente.Ptr:
                                self.simulador.VRAM.contenido.pop(index)
                                break
                        self.simulador.RAM.contenido.append(siguiente)
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5

                    # La pagina no esta en RAM, hay que agregarla sin paging
                    self.simulador.RAM.contenido.append(siguiente)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

                # La página se encontró en la RAM
                else:
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1
                #sleep(2)

            # La RAM está llena
            else:
                # La Pagina no está en la RAM
                if not self.simulador.RAM.encontrar(siguiente.Ptr):
                    print("PAGE FAULT - LA PAGINA NO ESTA EN LA RAM")
                    maxIndx=0 #index de la pagina mas tardada
                    max=0 #accesos faltantes
                    for x in range(len(self.simulador.RAM.contenido)):
                        accessosfaltantes = self.getFaltantes(self.simulador.RAM.contenido[x].Ptr)#que paso aca? porque es un [1]
                        if accessosfaltantes > max:
                            max = accessosfaltantes
                            maxIndx = x
                    # La página se encontró en la VRAM
                    print("REVISANDO")
                    print(siguiente.to_string())
                    print(self.simulador.VRAM.to_string())
                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        print("PAGE FAULT - TOMANDO PAGINA DE VRAM")
                        for index, pagina in enumerate(self.simulador.VRAM.contenido):
                            print("BUSCANDO PAGINA PARA ELIMINAR DE VRAM")
                            if pagina.Ptr == siguiente.Ptr:
                                print("ENCONTRE LA PAGINA QUE OCUPO ELIMINAR")
                                self.simulador.VRAM.contenido.pop(index)
                                break
                    self.simulador.VRAM.contenido.append(self.simulador.RAM.contenido[maxIndx])
                    self.simulador.RAM.contenido[maxIndx] = siguiente
                    self.simulador.stats.TiempoTrashing  = self.simulador.stats.TiempoTrashing  + 5
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 6

                # La página esta en la RAM
                else:
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1

                #sleep(2)

            self.calcularAccesosfaltanttes()
            self.calcularFragmentacionInternaOpt()
            self.calcularRAMUtilizadaYVRAM()
            self.simulador.stats.PaginasEnMemoria= len(self.simulador.RAM.contenido)
            self.simulador.stats.PaginasEnDisco= len(self.simulador.VRAM.contenido)

