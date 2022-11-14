from time import sleep
class Aging:

    def __init__(self, simulador):
        
        self.simulador = simulador
        self.vejezPaginas = []  #Corresponde al orden en el que las llamadas a las paginas se va realizando, L[0] = la más antigua.


    def getIndexMasViejo(self):
        
        for pagina in self.simulador.RAM.contenido:                            
            if pagina.PID == self.vejezPaginas[0]:

                return pagina.index()

    def calcularFragmentacionInternaAging(self):
        self.fragmentacionInternaAging = 0

        for pagina in self.simulador.RAM:
            self.simulador.stats.FragmentacionInterna = self.simulador.stats.FragmentacionInterna + ((4000 - pagina.Size) / 1000)

        return self.simulador.stats.FragmentacionInterna

    def calcularRAMUtilizadayVRAM(self):
        self.simulador.stats.RAMUtilizada = len(self.simulador.RAM.contenido) * 4
        self.simulador.stats.VRAMUtilizada = len(self.simulador.VRAM.contenido) * 4

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

    

    def simular(self): #Considerar siempre que la competencia la hacen la vejez de las páginas, y que hay que cargar los procesos en RAM 
        
        while(len(self.simulador.varasBarajadas) > 0): #Que sigan habiendo páginas pendientes de llamado
            sleep(2)
            siguiente = self.simulador.varasBarajadas.pop(0) #Toma el proceso en "ejecución" de la lista barajada

            if len(self.simulador.RAM.contenido) < self.simulador.RAM.RAMSize: #Que haya memoria RAM disponible VERIFICAR
                siguiente = self.simulador.varasBarajadas.pop(0) #Toma el proceso en "ejecución" de la lista barajada
            print("---------------------")
            print("Iteración", len(self.simulador.varasBarajadas))
            print("Tomando la página PID", siguiente.PID, " Ptr", siguiente.Ptr)
            print("Actualmente la RAM tiene: \n\n")
            print(self.simulador.RAM.to_string())
            print("Actualmente la VRAM tiene: \n\n")
            print(self.simulador.VRAM.to_string())
            print("Actualmente la MMU tiene: \n\n")
            print(self.simulador.MMU.to_string())
            print("\n\n\n")
            print("\n\n\n")

            if len(self.simulador.RAM.contenido) < self.RAMSize: #Que haya memoria RAM disponible 
                
                if not self.simulador.RAM.encontrar(siguiente.Ptr): #Entra si no está dentro de la memoria RAM

                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True: #Entra si la pagina se encuentra en la memoria VRAM
                        print("VRAM NO FULL PAGE FAULT - TOMANDO PAGINA DE VRAM")

                        for index, pagina in enumerate(self.simulador.VRAM.contenido):
                           
                            if pagina.Ptr == siguiente.Ptr:
                                self.simulador.VRAM.contenido.pop(index)
                                break

                    #if siguiente not in self.simulador.RAM.contenido: #condición que indica que no se encuentra en memoria #Cambiar uso con función encontrar de
                    #if self.simulador.VRAM.contenido.count(siguiente) > 0: #condición que indica que se encuentra en el disco?.
                        
                        self.simulador.RAM.contenido.append(siguiente)#Ingresa a la memoria RAM
                            
                        self.vejezPaginas.append(siguiente.PID) #Lo añade a la lista de vejez de páginas, queda de último en la lista, o sea es la página utilizada más jóven que las demás.
                        index = siguiente.index()

                        if  siguiente.Ptr in self.simulador.MMU.listaDeCositas:
                            self.simulador.MMU.actualizar(siguiente.Ptr,False,index,None,"-","-")
                        else:
                            #Agregar la pagina a la mmu si no estaba en ram ni vram
                            self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter,index,"-","-")
                            self.simulador.MMU.actualizar(siguiente.Ptr,False,index,None,"-","-")
                        
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing + 5

                    self.simulador.RAM.contenido.append(siguiente)
                    #self.vejezPaginas.remove(siguiente[1]) #Elimina el id de la página de la lista de Vejez
                    self.vejezPaginas.append(siguiente.PID) #Lo añade a la lista de vejez de páginas, queda de último en la lista, o sea es la página utilizada más jóven que las demás por su llamada reciente.
                    self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter, len(self.simulador.RAM.contenido)-1, siguiente.mark, siguiente.Contador)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1
                
                #Aca solamente se actualiza la lista de vejez de las paginas, por lo que no se afecta la ram. 
                self.vejezPaginas.remove(siguiente.PID) #Elimina el id de la página de la lista de Vejez
                self.vejezPaginas.append(siguiente.PID) #Lo añade a la lista de vejez de páginas, queda de último en la lista, o sea es la página utilizada más jóven que las demás por su llamada reciente.
                self.simulador.MMU.actualizarAMarcadoYTiempo(siguiente.Ptr,siguiente.mark,siguiente.Contador)
                self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1

            #Cuando no existe memoria disponible en la RAM 
            #El id de página que se va a eliminar siempre va a ser el vejezPaginas[0] ya que es el más viejo al que se le dio uso. 
            else:

                if not self.simulador.RAM.encontrar(siguiente.Ptr): #No está en la RAM
                    print("PAGE FAULT - LA PAGINA NO ESTA EN LA RAM")
                
                    if self.simulador.VRAM.encontrar(siguiente.Ptr) == True: #Entra si la encuentra en la VRAM
                        
                        PIDdeLaMasViejaUsada = self.vejezPaginas[0] #Corresponde al PID de la pagina que se tiene que sacar de la RAM y meter al VRAM
                        for pagina in self.simulador.RAM.contenido: #Recorre RAM para sacarla y hacer espacio                             

                            if pagina.PID == PIDdeLaMasViejaUsada:

                                indexDeLaMasVieja = self.getIndexMasViejo() #Devuelve el index de la mas vieja, esto porque no se puede hacer por PID

                                self.simulador.VRAM.contenido.append(pagina) #Mete la que se va a sacar de RAM dentro de la VRAM
                                self.simulador.MMU.actualizar(self.simulador.RAM.contenido[indexDeLaMasVieja].Ptr,False,None,len(self.simulador.VRAM.contenido)-1,None,None)
                                self.simulador.RAM.contenido[indexDeLaMasVieja] = siguiente #Sustituye en RAM la que  salio de VRAM
                                self.simulador.VRAM.contenido.pop(siguiente) #Elimina de VRAM la que mando a RAM

                                index = siguiente.index()
                                if  siguiente.Ptr in self.simulador.MMU.listaDeCositas:
                                    self.simulador.MMU.actualizar(siguiente.Ptr,False,index,None,"-","-")
                                else:
                                #Agregar la pagina a la mmu si no estaba en ram ni vram
                                    self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter,index,"-","-")
                                    self.simulador.MMU.actualizar(siguiente.Ptr,False,index,None,"-","-")

                                #Actualiza la lista de vejez con los cambios hechos en VRAM y RAM
                                self.vejezPaginas.remove(PIDdeLaMasViejaUsada)
                                self.vejezPaginas.append(siguiente.PID)

                                self.simulador.stats.TiempoTrashing  = self.simulador.stats.TiempoTrashing  + 5
                                self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 6
                    
                    # La página no se encontro en VRAM - Hay que crearla
                    PIDdeLaMasViejaUsada = self.vejezPaginas[0] #Corresponde al PID de la pagina que se tiene que sacar de la RAM y meter al VRAM
                    for pagina in self.simulador.RAM.contenido: #Recorrer RAM para encontrarla

                        if pagina.PID == PIDdeLaMasViejaUsada: #La encuentra con esta condicion
                            indexDeLaMasVieja = self.getIndexMasViejo()
                            
                            self.simulador.VRAM.contenido.append(pagina)
                            self.simulador.RAM.contenido[indexDeLaMasVieja] = siguiente

                            #Actualiza la lista de vejez con los cambios hechos en VRAM y RAM
                            self.vejezPaginas.remove(PIDdeLaMasViejaUsada)
                            self.vejezPaginas.append(siguiente.PID)

            

                self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 1
                #Aca solamente se actualiza la lista de vejez de las paginas, por lo que no se afecta la ram. 
                self.simulador.MMU.actualizarAMarcadoYTiempo(siguiente.Ptr,siguiente.mark,siguiente.Contador)
                self.vejezPaginas.remove(siguiente.PID) #Elimina el id de la página de la lista de Vejez
                self.vejezPaginas.append(siguiente.PID) #Lo añade a la lista de vejez de páginas, queda de último en la lista, o sea es la página utilizada más jóven que las demás por su llamada reciente.


        self.simulador.stats.PaginasEnMemoria = len(self.simulador.RAM.contenido)
        self.simulador.stats.PaginasEnDisco = len(self.simulador.VRAM.contenido)
        memoriaUtilizada=self.simulador.RAM.calcularMemoriaUtilizada()
        self.simulador.stats.RAMUtilizada=memoriaUtilizada[0]
        self.simulador.stats.VRAMUtilizada = memoriaUtilizada[1]
        self.simulador.stats.FragmentacionInterna=self.simulador.RAM.calcularFragmentacionInterna()
        
        self.printMemorias()


    # AQUI TIENE QUE IR TODA LA IMPLEMENTACION DE LOS METODOS PARA HACER FUNCIONAR EL ALGORITMO
    # NO CAMBIAR EL NOMBRE
    