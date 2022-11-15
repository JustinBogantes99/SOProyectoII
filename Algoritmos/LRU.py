from time import sleep
import random
from operator import attrgetter
class LRU:

    def __init__(self, simulador):
        self.simulador = simulador
        self.paginasMarcadas=[]
        self.logicAddresCounter=0 

    def calcularFragmentacionInternaLRU(self):
        self.FragmentacionInternaOpt=0
        for pagina in self.simulador.RAM:
            self.simulador.stats.FragmentacionInterna = self.simulador.stats.FragmentacionInterna + ((4096-pagina.Size)/1024)
        return self.simulador.stats.FragmentacionInterna

    def calcularRAMUtilizadaYVRAM(self):
        self.simulador.stats.RAMUtilizada=len(self.simulador.RAM.contenido)*4
        self.simulador.stats.VRAMUtilizada = len(self.simulador.VRAM.contenido)*4
        
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
        print("CorriendoLRU")
        print(self.simulador.varasBarajadas)
        # Mientras haya algo por procesar
        while(len(self.simulador.varasBarajadas)>0):
            siguiente = self.simulador.varasBarajadas.pop(0)

            # Si no se ha llenado la RAM
            if len(self.simulador.RAM.contenido) < self.simulador.RAM.RAMSize:#self.simulador.RAMSize

                if self.simulador.RAM.encontrar(siguiente.Ptr)==False:

                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        for index, pagina in enumerate(self.simulador.VRAM.contenido):
                            if pagina.Ptr == siguiente.Ptr:
                                self.simulador.VRAM.contenido.pop(index)
                                #self.simulador.MMU.actualizar(siguiente.Ptr,False,"-","-","-","-")
                        
                        self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter, len(self.simulador.RAM.contenido)-1, siguiente.mark, siguiente.Contador)
                        #self.simulador.MMU.actualizar(siguiente.Ptr,True,len(self.simulador.RAM.contenido)-1,"-","-",siguiente.Contador,"-")
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5

                    siguiente.Contador = 0      
                    self.simulador.RAM.contenido.append(siguiente)#key, loaded, MAddres, DAddres,mark,time
                    self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter, len(self.simulador.RAM.contenido)-1, siguiente.mark, siguiente.Contador)
                    #self.simulador.MMU.actualizar(siguiente.Ptr,True,len(self.simulador.RAM.contenido)-1,"-",siguiente.Contador,"-")
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+6

                elif self.simulador.RAM.encontrar(siguiente.Ptr)==True:
                    for pag in self.simulador.RAM.contenido:
                        if pag.Ptr == siguiente.Ptr:
                            pag.contador=0
                            self.simulador.MMU.actualizarAMarcadoYTiempo(pag.Ptr,pag.mark,pag.Contador)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

            # Si la RAM esta llena
            else:

                # Si la pagina no se encuentra en RAM
                if self.simulador.RAM.encontrar(siguiente.Ptr)==False:

                    # Si la página se encuentra en VRAM
                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        Paginamayor=self.sacarMayorLRU()
                        cont = 0
                        for pagina in self.simulador.RAM.contenido:
                            if pagina.Ptr==Paginamayor.Ptr:
                                siguiente.Contador = 0
                                #self.simulador.VRAM.contenido.append(pagina)#key, loaded, MAddres, DAddres,mark,time
                                self.simulador.VRAM.meter(pagina)
                                DAddres= self.simulador.VRAM.encontrar_direccion(self.simulador.RAM.contenido[cont].Ptr)
                                self.simulador.MMU.actualizar(self.simulador.RAM.contenido[cont].Ptr,False,"-",  DAddres,"-","-")
                                self.simulador.RAM.contenido[cont]=siguiente
                                self.simulador.MMU.actualizar(siguiente.Ptr,True,cont,"-",siguiente.Contador,"-")
                                pagina.Contador = 0
                                
                                

                                for index, pagina in enumerate(self.simulador.VRAM.contenido):
                                    if pagina.Ptr == siguiente.Ptr:
                                        #self.simulador.VRAM.contenido.pop(index)
                                        self.simulador.VRAM.sacar(index)

                            cont+=1
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+6
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5

                    # La página no se encontro en VRAM - Hay que crearla
                    else:
                        Paginamayor = self.sacarMayorLRU()
                        cont = 0
                        for pagina in self.simulador.RAM.contenido:
                            if pagina.Ptr==Paginamayor.Ptr:
                                siguiente.Contador = 0
                                #self.simulador.VRAM.contenido.append(pagina)
                                self.simulador.VRAM.meter(pagina)
                                DAddres= self.simulador.VRAM.encontrar_direccion(pagina.Ptr)
                                self.simulador.MMU.actualizar(self.simulador.RAM.contenido[cont].Ptr,False,"-",DAddres,"-","-")
                                self.simulador.RAM.contenido[cont]=siguiente
                                self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter, cont, siguiente.mark, siguiente.Contador)
                                pagina.Contador = 0
                                self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+6
                                self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5
                                
                    
                            cont+=1

 
                # La página se encontró en RAM (Aplicar LRU al mark)
                elif self.simulador.RAM.encontrar(siguiente.Ptr):
                    for pag in self.simulador.RAM.contenido:
                        if pag.Ptr==siguiente.Ptr:
                            pag.Contador=0
                            self.simulador.MMU.actualizarAMarcadoYTiempo(pag.Ptr,pag.Contador,"-")
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

            # Hago las paginas mas viejas
            if len(self.simulador.RAM.contenido)!=0:
                for pagina in self.simulador.RAM.contenido:
                    pagina.Contador+=1
                    self.simulador.MMU.actualizarAMarcadoYTiempo(pagina.Ptr,pagina.Contador,"-")
            sleep(1)
            self.simulador.stats.FragmentacionInterna=self.simulador.RAM.calcularFragmentacionInterna()
            memoriaUtilizada=self.simulador.RAM.calcularMemoriaUtilizada()
            self.simulador.stats.RAMUtilizada=self.simulador.RAM.calcularMemoriaUtilizada()
            self.simulador.stats.VRAMUtilizada = self.simulador.VRAM.calcularMemoriaUtilizada()
            self.simulador.stats.FragmentacionInterna=self.simulador.RAM.calcularFragmentacionInterna()
            self.simulador.stats.PaginasEnMemoria= len(self.simulador.RAM.contenido)
            self.simulador.stats.PaginasEnDisco= len(self.simulador.VRAM.contenido)
