from time import sleep
import random

class Optimo:
    def __init__(self, simulador):
        self.simulador = simulador
        self.paginasMarcadas=[]  #lista con las paginas y la cantidad de accesos a memoria necesarios antes de ser usada [accesos,[pagina]]

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




    def simular(self):

        print("CorriendoOptimo")
        while(len(self.simulador.varasBarajadas)>0):
            siguiente=self.simulador.varasBarajadas.pop(0)

            '''print("\n\n\n")
            print("---------------------")
            print("Iteración", len(self.simulador.varasBarajadas))
            print("Tomando la página PID", siguiente.PID, " Ptr", siguiente.Ptr)
            print("Actualmente la RAM tiene: \n\n")
            print(self.simulador.RAM.to_string())
            print("Actualmente la VRAM tiene: \n\n")
            print(self.simulador.VRAM.to_string())
            print("Actualmente la MMU tiene: \n\n")
            print(self.simulador.MMU.to_string())
            print("\n\n\n")'''




            # La RAM todavía no está llena
            if len(self.simulador.RAM.contenido) <5:

                # No se pudo encontrar la página en la RAM
                if not self.simulador.RAM.encontrar(siguiente.Ptr):
                    #self.simulador.VRAM.encontrar(siguiente.Ptr)==True  
                    #no seria cambiar a esto?

                    # La página se encontró en la VRAM
                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        for index, pagina in enumerate(self.simulador.VRAM.contenido):
                            if pagina.Ptr == siguiente.Ptr:
                                self.simulador.VRAM.contenido.pop(index)
                                break

                        self.simulador.RAM.contenido.append(siguiente)
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5

                    # La pagina no esta en RAM, hay que agregarla sin paging
                    self.simulador.RAM.contenido.append(siguiente)
                    self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter,len(self.simulador.RAM.contenido)-1,"-","-")
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+6

                # La página se encontró en la RAM
                else:
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1
                #sleep(2)

            # La RAM está llena
            else:
                # La Pagina no está en la RAM
                if not self.simulador.RAM.encontrar(siguiente.Ptr):
                    maxIndx=0 #index de la pagina mas tardada
                    max=0 #accesos faltantes
                    for x in range(len(self.simulador.RAM.contenido)):
                        accessosfaltantes = self.getFaltantes(self.simulador.RAM.contenido[x].Ptr)#que paso aca? porque es un [1]
                        if accessosfaltantes > max:
                            max = accessosfaltantes
                            maxIndx = x
                    # La página se encontró en la VRAM
                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        for index, pagina in enumerate(self.simulador.VRAM.contenido):
                            if pagina.Ptr == siguiente.Ptr:
                                self.simulador.VRAM.contenido.pop(index)
                                break
                    
                    #self.simulador.VRAM.contenido.append(self.simulador.RAM.contenido[maxIndx])
                    self.simulador.VRAM.meter(self.simulador.RAM.contenido[maxIndx])
                    #actualizar valor en MMU de la pagina enviada a VRAM
                    DAddres= self.simulador.VRAM.encontrar_direccion(self.simulador.RAM.contenido[maxIndx].Ptr)
                    self.simulador.MMU.actualizar(self.simulador.RAM.contenido[maxIndx].Ptr,False,"-",DAddres,"-","-")

                    self.simulador.RAM.contenido[maxIndx] = siguiente
                    self.simulador.stats.TiempoTrashing  = self.simulador.stats.TiempoTrashing  + 5
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 6

                    if  siguiente.Ptr in self.simulador.MMU.listaDeCositas:
                        #self.simulador.MMU.actualizar(siguiente.Ptr,False,"-",len(self.simulador.VRAM.contenido)-1,"-","-")
                        self.simulador.MMU.actualizar(siguiente.Ptr,True,maxIndx,"-","-","-")
                    else:
                        #Agregar la pagina a la mmu si no estaba en ram ni vram
                        self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter,maxIndx,"-","-")

                # La página esta en la RAM
                else:
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1

               

            self.calcularAccesosfaltanttes()
            
            self.simulador.stats.FragmentacionInterna=self.simulador.RAM.calcularFragmentacionInterna()
          
            self.simulador.stats.RAMUtilizada=self.simulador.RAM.calcularMemoriaUtilizada()
            self.simulador.stats.VRAMUtilizada = self.simulador.VRAM.calcularMemoriaUtilizada()
            self.simulador.stats.FragmentacionInterna=self.simulador.RAM.calcularFragmentacionInterna()
            self.simulador.stats.PaginasEnMemoria= len(self.simulador.RAM.contenido)
            self.simulador.stats.PaginasEnDisco= len(self.simulador.VRAM.contenido)

            sleep(1)

