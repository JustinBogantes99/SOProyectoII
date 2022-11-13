class Aging:

    def __init__(self, simulador):
        
        self.simulador = simulador
        self.vejezPaginas = []  #Corresponde al orden en el que las llamadas a las paginas se va realizando, L[0] = la más antigua.
        self.RAMSize = 6 # Pregunta, este valor de RAM no debería estar en la simulación?

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
        
        while(len(self.simulador.varasBarajadas) > 1): #Que sigan habiendo páginas pendientes de llamado

            if len(self.simulador.RAM.contenido) < self.RAMSize: #Que haya memoria RAM disponible VERIFICAR
                siguiente = self.simulador.varasBarajadas.pop(0) #Toma el proceso en "ejecución" de la lista barajada

                if siguiente not in self.simulador.RAM.contenido: #condición que indica que no se encuentra en memoria 

                    #if self.simulador.VRAM.contenido.count(siguiente) > 0: #condición que indica que se encuentra en el disco?.
                    #self.simulador.VRAM.contenido.remove(siguiente) #No me queda claro aún el uso de la Vram, entonces es como placeholer jaja 

                    self.simulador.RAM.contenido.append(siguiente)  #Ingresa a la memoria RAM
                        
                    self.vejezPaginas.append(siguiente[1]) #Lo añade a la lista de vejez dee páginas, queda de último en la lista, o sea es la página utilizada más jóven que las demás.

                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 5
                    self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing + 5

                #Cuando no se cumple la condición del IF significa que el proceso sí está en memoria, por lo tanto solamente se actualiza la lista de orden de las páginas utilizadas.
                #O sea se pone como la más jóven la que se está llamando, en este caso sería la que esté en "siguiente"
                self.vejezPaginas.remove(siguiente[1]) #Elimina el id de la página de la lista de Vejez,
                self.vejezPaginas.append(siguiente[1]) #Lo añade a la lista de vejez de páginas, queda de último en la lista, o sea es la página utilizada más jóven que las demás por su llamada reciente.

                #self.simulador.VRAM.contenido.remove(siguiente) ##No me queda claro aún el uso de la Vram, entonces es como placeholer jaja 
            
            #Cuando no existe memoria disponible en la RAM 
            #El id de página que se va a eliminar siempre va a ser el vejezPaginas[0] ya que es el más viejo al que se le dio uso. 
            for Pagina in self.simulador.RAM.contenido: #Recorre los procesos en RAM actuales para buscar el que cumpla con el id de página a eliminar.

                if Pagina[1] == self.vejezPaginas[0]:
                    self.simulador.RAM.contenido.remove(Pagina) #Quita la pagina que por el algoritmo debe salir
                    self.simulador.RAM.contenido.append(siguiente) #Agrega la nueva página a utilizar
                
                    self.vejezPaginas.remove(Pagina[1]) #Elimina el id de la página de la lista de Vejez que debe salir por el algoritmo
                    self.vejezPaginas.append(siguiente[1]) #Añade a la nueva página, como la más jóven de la lista de la vejez

                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado + 5 #costo de la ejecución por pagefault
                    self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing + 5 #costo de la ejecución por pagefault                    
                    

        




    # AQUI TIENE QUE IR TODA LA IMPLEMENTACION DE LOS METODOS PARA HACER FUNCIONAR EL ALGORITMO
    # NO CAMBIAR EL NOMBRE
    def simular(self):
        pass