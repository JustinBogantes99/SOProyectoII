import random
from time import sleep
class Random:
    def __init__(self, simulador):
        self.simulador = simulador
        self.logicAddresCounter=0
        random.seed(self.simulador.seed)
        pass
    
    def calcularRAMUtilizadaYVRAM(self):
        self.simulador.stats.RAMUtilizada=len(self.simulador.RAM.contenido)*4096
        self.simulador.stats.VRAMUtilizada = len(self.simulador.VRAM.contenido)*4096
    
    
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
        print("CorriendoRandom")
        while(len(self.simulador.varasBarajadas)>1):
            siguiente=self.simulador.varasBarajadas.pop(0)

 
            if len(self.simulador.RAM.contenido) < self.simulador.RAM.RAMSize:
                if self.simulador.RAM.encontrar(siguiente.Ptr):
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1
                else:
                    self.simulador.RAM.contenido.append(siguiente)
                    #Actualizar MMU                   
                    self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter,len(self.simulador.RAM.contenido)-1,"-","-")

           
                        

                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+6
                #sleep(2)

            #RAM LLENA
            else:
                elegido=random.randint(0,len(self.simulador.RAM.contenido)-1)
                if self.simulador.RAM.encontrar(siguiente.Ptr):
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1
                else:
                    if self.simulador.VRAM.encontrar(siguiente.Ptr):
                        for index, pagina in enumerate(self.simulador.VRAM.contenido):
                            if pagina.Ptr == siguiente.Ptr:
                                #self.simulador.VRAM.contenido.pop(index)
                                self.simulador.VRAM.sacar(index)

                    #self.simulador.VRAM.contenido.append(self.simulador.RAM.contenido[elegido])
                    self.simulador.VRAM.meter(self.simulador.RAM.contenido[elegido])
                    #self.simulador.MMU.actualizar(self.simulador.RAM.contenido[elegido].Ptr,False,"-",len(self.simulador.RAM.contenido)-1,"-","-")
                    #self.simulador.MMU.actualizar (self.simulador.RAM.contenido[elegido].Ptr,"-","-",len(self.simulador.VRAM.contenido)-1,"-","-")

                    #actualizar la pagina que va a la VRAM
                    DAddres= self.simulador.VRAM.encontrar_direccion(self.simulador.RAM.contenido[elegido].Ptr)
                    self.simulador.MMU.actualizar(self.simulador.RAM.contenido[elegido].Ptr,False,"-",DAddres,"-","-")

                    self.simulador.RAM.contenido[elegido] = siguiente
                    self.simulador.stats.TiempoTrashing  = self.simulador.stats.TiempoTrashing  + 5
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 6
                    #actualizar pagina que pasa de la VRAM a la RAM
                    if  siguiente.Ptr in self.simulador.MMU.listaDeCositas:
                        #self.simulador.MMU.actualizar(siguiente.Ptr,False,"-",len(self.simulador.VRAM.contenido)-1,"-","-")
                        self.simulador.MMU.actualizar(siguiente.Ptr,True,elegido,"-","-","-")
                    else:
                        #Agregar la pagina a la mmu si no estaba en ram ni vram
                        self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter,elegido,"-","-")
                     

                #sleep(2)

            sleep(1)
            
            self.simulador.stats.FragmentacionInterna=self.simulador.RAM.calcularFragmentacionInterna()
            self.simulador.stats.RAMUtilizada=self.simulador.RAM.calcularMemoriaUtilizada()
            self.simulador.stats.VRAMUtilizada = self.simulador.VRAM.calcularMemoriaUtilizada()
            self.simulador.stats.FragmentacionInterna=self.simulador.RAM.calcularFragmentacionInterna()
            self.simulador.stats.PaginasEnMemoria= len(self.simulador.RAM.contenido)
            self.simulador.stats.PaginasEnDisco= len(self.simulador.VRAM.contenido)
           # print("Tiempo total: ",self.simulador.stats.TiempoSimulado)
           # print("Tiempo de Trashing: ",self.simulador.stats.TiempoTrashing)
            #print("RAM utilizada: ", self.simulador.stats.RAMUtilizada)
           # print("VRAM utilizada: ", self.simulador.stats.VRAMUtilizada)

   

        pass
