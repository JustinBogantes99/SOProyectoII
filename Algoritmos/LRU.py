from time import sleep
import random

class LRU:

    def __init__(self, simulador):
        self.simulador = simulador
        self.paginasMarcadas=[]

<<<<<<< Updated upstream
        self.listaAccesosBarajados=[[1,1,500]
        ,[3,6,128]
        ,[1,2,1024]
        ,[2,4,256]
        ,[2,5,512]
        ,[4,10,256]
        ,[1,3,512]
        ,[3,7,1024]
        ,[4,10,256]
        ,[3,8,512]
        ,[1,1,500]
        ,[2,5,512]
        ,[3,8,512]
        ,[3,9,512]
        ,[3,7,1024]
        ,[3,6,128]
        ,[1,2,1024]
        ,[2,4,256]
        ,[2,5,512]
        ,[4,10,256]
        ,[1,3,512]
        ,[3,7,1024]
        ,[4,10,256]
        ,[3,8,512]
        ,[1,1,500]
        ,[2,5,512]
        ,[3,8,512]
        ,[3,9,512]
        ,[3,7,1024]
        ]

        self.RAMSize=5
        self.RAMTotal=self.RAMSize*4
        self.RAMUtilizada=0
        self.VRAMUtilizada=len
        self.FragmentacionInternaLRU=0
        self.TiempoSimLRU=0
        self.TiempoTrashingLRU=0
        self.RAMLRU=[]
        self.VRAMLRU=[]
        self.mayores=[]
        self.VRAMUtilizada=len(self.VRAMLRU)*4
        self.paginasMarcadas=[]  #lista con las paginas y la cantidad de accesos a memoria necesarios antes de ser usada [accesos,[pagina]]

        self.agregarContadoresLRU() 
        self.run()

    # AQUI TIENE QUE IR TODA LA IMPLEMENTACION DE LOS METODOS PARA HACER FUNCIONAR EL ALGORITMO
    # NO CAMBIAR EL NOMBRE
    def simular(self):
        pass

    def calcularFragmentacionInternaLRU(self):
        self.FragmentacionInternaLRU=0
        for pagina in self.RAMLRU:
            self.FragmentacionInternaLRU= FragmentacionInternaLRU + ((4000-pagina[2])/1000)
        return self.FragmentacionInternaLRU
=======
    def calcularFragmentacionInternaOpt(self):
        self.FragmentacionInternaOpt=0
        for pagina in self.simulador.RAM:
            self.simulador.stats.FragmentacionInterna = self.simulador.stats.FragmentacionInterna + ((4000-pagina[2])/1000)
        return self.simulador.stats.FragmentacionInterna
>>>>>>> Stashed changes

    def calcularRAMUtilizadaYVRAM(self):
        self.simulador.stats.RAMUtilizada=len(self.simulador.RAM*4)
        self.simulador.stats.VRAMUtilizada = len(self.simulador.VRAM*4)
        
    def sacarMayorLRU(self):
        lista=[]
        for x in self.RAMLRU:
            lista+=[x[3]]
        self.valoMax=max(lista)
        return self.valoMax

    def run(self):
        print("Corriendo el print")
        while(len(self.simulador.varasBarajadas)>1):
            if len(self.simulador.RAM) < self.RAMSize:
                siguiente=self.simulador.varasBarajadas.pop(0)
                if self.simulador.RAM.count(siguiente)==0:
                    if self.simulador.VRAM.count(siguiente)>0:
                        self.simulador.VRAM.remove(siguiente)
                        self.simulador.RAM.append(siguiente)
                        self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+5
                        self.simulador.stats.TiempoTrashing = self.simulador.stats.TiempoTrashing+5
                    if len(self.RAM)!=0:
                        for pagina in self.RAM:
                            pagina.contador+=1
                    siguiente.contador+=1        
                    self.RAM.append(siguiente)
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1
                elif self.RAM.count(siguiente)!=0:
                    for pag in self.RAM:
                        if pag.pid == siguiente.pid:
                            pag.contador=0
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1

            if len(self.RAM) >= self.RAMSize:
                siguiente=self.simulador.varasBarajadas.pop(0)

                if self.RAM.count(siguiente)==0: 
                    mayor=self.sacarMayorLRU()
                    cont=0
                    for pagina in self.RAM:
                        if pagina.contador==mayor:
                            siguiente.contador+=1  

                            self.RAM[cont]=siguiente

                            self.VRAM.append(pagina)
                        cont+=1

                    if len(self.RAM)!=0:
                        for pagina in self.RAM:
                            pagina.contador+=1 


                elif self.RAM.count(siguiente)==0:
                    for pag in self.RAM:
                        if pag.PID==siguiente.PID:
                            pag.contador=0
                    self.simulador.stats.TiempoSimulado = self.simulador.stats.TiempoSimulado+1
1
