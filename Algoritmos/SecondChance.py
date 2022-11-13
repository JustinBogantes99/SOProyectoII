class SecondChance:
    def __init__(self, simulador):
        self.simulador = simulador


    def paging_bueno(self, pagina_a_ram):
        paging_not_done = True
        while paging_not_done:
            candidate = self.simulador.RAM.contenido.pop(0)
            if candidate.mark == True:
                candidate.mark = False
                self.simulador.RAM.contenido.append(candidate)
            else:
                self.simulador.VRAM.contenido.append(candidate)
                self.simulador.RAM.contenido.append(pagina_a_ram)
                paging_not_done = False
                break


    def simular(self):
        print("CorriendoSecondChance")
        while(len(self.simulador.varasBarajadas)>0):
            siguiente = self.simulador.varasBarajadas.pop(0)
            self.simulador.MMU.agregar(siguiente.PID,siguiente.Ptr,self.simulador.MMU.logicAddresCounter, len(self.simulador.RAM.contenido)-1, siguiente.mark, siguiente.Contador)

            # Si no se ha llenado la RAM
            if len(self.simulador.RAM.contenido) < 5: # self.simulador.RAMSize
                # La pagina no se encuentra en RAM
                if self.simulador.RAM.encontrar(siguiente.Ptr)==False:

                    # La pagina se encuentra en VRAM
                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        for index, pagina in enumerate(self.simulador.VRAM.contenido):
                            if pagina.Ptr == siguiente.Ptr:
                                pagina_a_ram = self.simulador.VRAM.contenido.pop(index)
                                break
                        self.paging_bueno(pagina_a_ram)

                    # La pagina no esta en VRAM - Metiendo a la RAM directamente
                    self.simulador.RAM.contenido.append(siguiente)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

                # La página se encontró en RAM - (Second Chance)
                elif self.simulador.RAM.encontrar(siguiente.Ptr)==True:
                    for index, pagina in enumerate(self.simulador.RAM.contenido):
                        if pagina.Ptr == siguiente.Ptr:
                            pagina.mark=True
                            temp = self.simulador.RAM.contenido.pop(index)
                            self.simulador.RAM.contenido.append(temp)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

            # Si la RAM esta llena - Page fault
            else:
                # Si la pagina no se encuentra en RAM
                if self.simulador.RAM.encontrar(siguiente.Ptr)==False:
                    
                    # Si la página se encuentra en VRAM
                    if self.simulador.VRAM.encontrar(siguiente.Ptr)==True:
                        for index, pagina in enumerate(self.simulador.VRAM.contenido):
                            if pagina.Ptr == siguiente.Ptr:
                                pagina_a_ram = self.simulador.VRAM.contenido.pop(index)
                                break
                        self.paging_bueno(pagina_a_ram)

                    # La página no se encontro en VRAM - Hay que crearla y hacer paging
                    else:
                        self.paging_bueno(siguiente) 

                # La página se encontró en RAM (Aplicar Second Chance)
                elif self.simulador.RAM.encontrar(siguiente.Ptr):
                    for index, pagina in enumerate(self.simulador.RAM.contenido):
                        if pagina.Ptr == siguiente.Ptr:
                            pagina.mark=True
                            temp = self.simulador.RAM.contenido.pop(index)
                            self.simulador.RAM.contenido.append(temp)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

