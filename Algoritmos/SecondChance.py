class SecondChance:
    def __init__(self):
        pass

    def marks(self, x, arr, second_chance, paginas):
        for i in range(paginas):
              
            if arr[i] == x:
                second_chance[i] = True
                return True
          
        return False
      
    def paging(self, x, arr, second_chance, paginas, pointer):
        while(True):
            if not second_chance[pointer]:
                arr[pointer] = x

                return (pointer+1)%paginas

            second_chance[pointer] = False
              
            pointer = (pointer + 1) % paginas
      
    def simular(self, reference_string, paginas):
          
        pointer = 0
        pf = 0
        arr = [0]*paginas
        for s in range(paginas):
            arr[s] = -1

        second_chance = [False]*paginas
        Str = reference_string.split(' ')
          
        l = len(Str)
          
        for i in range(l):
            x = Str[i]

            if not self.marks(x,arr,second_chance,paginas):
                pointer = self.paging(x,arr,second_chance,paginas,pointer)
                pf += 1

    def simular_real(self):
        while(len(self.simulador.varasBarajadas)>1):
            siguiente = self.simulador.varasBarajadas.pop(0)

            # Si no se ha llenado la RAM
            if len(self.simulador.RAM.contenido) < 5: # self.simulador.RAMSize
                print("La RAM no está llena, metiendo un nuevo proceso")
                # La pagina no se encuentra en RAM
                if self.simulador.RAM.encontrar(siguiente.Ptr)==False:
                    # La pagina se encuentra en VRAM
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

                # La página se encontró en RAM
                elif self.simulador.RAM.encontrar(siguiente.Ptr)==True:
                    for pag in self.self.simulador.RAM.contenido:
                        if pag.Ptr == siguiente.Ptr:
                            pag.contador=0
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

            # Si la RAM esta llena
            else:
                # Si la pagina no se encuentra en RAM
                if self.simulador.RAM.encontrar(siguiente.Ptr)==False:
                    
                    # Si la página se encuentra en VRAM
                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        pass

                    # La página no se encontro en VRAM - Hay que crearla
                    else:
                        pass
                # La página se encontró en RAM (Aplicar LRU al mark)
                elif self.simulador.RAM.encontrar(siguiente.Ptr):
                    pass
