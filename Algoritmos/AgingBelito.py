from time import sleep
class AgingBelito:
    
    def __init__(self, simulador):
        self.simulador = simulador
        self.vejezPaginas = {}  #Corresponde al orden en el que las llamadas a las paginas se va realizando, L[0] = la más antigua.
    
    def getIndexMasViejo(self):
        for pagina in self.simulador.RAM.contenido:                            
            if pagina.PID == self.vejezPaginas[0].PID:
                return pagina
    
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

    def corrimientoDerecha(self,pagina): 
        tempDic = self.vejezPaginas
        #tempDic[var] = "0"+ bits[:7]
        print(pagina.Contador)


    def simular(self):
        
        while(len(self.simulador.varasBarajadas) > 0):
            siguiente = self.simulador.varasBarajadas.pop(0)
            if len(self.simulador.RAM.contenido) < self.simulador.RAM.RAMSize:
                if not self.simulador.RAM.encontrar(siguiente.Ptr):#si no esta en ram 
                    nuevaPagina = self.corrimientoDerecha(siguiente)
                    self.simulador.RAM.contenido.append(nuevaPagina)
                else:
                    #en este caso simplemente no hay corrimientos a la derecha 
                    pass
            else:
                #en caso de estar llena la ram 
                pass