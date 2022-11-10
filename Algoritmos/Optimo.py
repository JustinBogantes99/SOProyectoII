from time import sleep
import random

class Optimo:
    def __init__(self,Stats,Accesos, AccesosBarajados,MMU):
        self.ListadeAccesos=Accesos
        #=[[1,1,500]
        #,[1,2,1024]
        #,[1,3,512]
        #,[2,4,256]
        #,[2,5,512]
        #,[3,6,128]
        #,[3,7,1024]
        #,[3,8,512]
        #,[3,9,512]
       # ,[4,10,256]
        
        self.listaAccesosBarajados=AccesosBarajados#
        #[[1,1,500]
        #,[3,6,128]
        #,[1,2,1024]
        #,[2,4,256]
        #,[2,5,512]
        #,[4,10,256]
        #,[1,3,512]#
        #,[3,7,1024]
        #,[4,10,256]
        #,[3,8,512]
        #,[1,1,500]
        #,[2,5,512]
        #,[3,8,512]
        #,[3,9,512]
        #,[3,7,1024]
        #,[3,6,128]
        #,[1,2,1024]
       # ,[2,4,256]
        #,[2,5,512]
       # ,[4,10,256]
       # ,[1,3,512]
       # ,[3,7,1024]
       # ,[4,10,256]
      #  ,[3,8,512]
       # ,[1,1,500]
       # ,[2,5,512]
       # ,[3,8,512]
       # ,[3,9,512]
       # ,[3,7,1024]
       # ]

        #self.RAMSize=5
        #self.RAMTotal=self.RAMSize*4
        #self.RAMUtilizada=0
        #self.VRAMUtilizada=len
        #self.FragmentacionInternaOpt=0
        #self.TiempoSimOpt=0
        #self.TiempoTrashingOpt=0
        self.RAMOpt=[]
        self.VRAMOpt=[]
        #self.VRAMUtilizada=len(self.VRAMOpt)*4
        self.stats=Stats
        self.MMU=MMU
        self.paginasMarcadas=[]  #lista con las paginas y la cantidad de accesos a memoria necesarios antes de ser usada [accesos,[pagina]]
        for acceso in self.ListadeAccesos:
            self.paginasMarcadas.append([0,acceso])

        
        print(self.paginasMarcadas)
        self.optimo()



    #Calcula cuantos accesos a memoria faltan para que la paginas sea usada de nuevo
    def calcularAccesosfaltanttes(self):
            for x in range(len(self.ListadeAccesos)):
                contador=0
                for y in range(len(self.listaAccesosBarajados)):
                    if self.ListadeAccesos[x][1]!= self.listaAccesosBarajados[y][1]:
                        contador=contador+1
                    else:
                        break 
                self.paginasMarcadas[x][0]=contador

    #Devuelve la cantidad de accesoss faltantes para utilizar la pagina ptr       
    def getFaltantes(self, ptr):
        for y in range( len(self.paginasMarcadas)):
            if self.paginasMarcadas[y][1][1]==ptr:
                return self.paginasMarcadas[y][0]



    def calcularFragmentacionInternaOpt(self):
        self.FragmentacionInternaOpt=0
        for pagina in self.RAMOpt:
            self.stats.FragmentacionInterna = self.stats.FragmentacionInterna + ((4000-pagina[2])/1000)
        return self.stats.FragmentacionInterna

    def calcularRAMUtilizadaYVRAM(self):
        self.stats.RAMUtilizada=len(self.RAMOpt*4)
        self.stats.VRAMUtilizada = len(self.VRAMOpt*4)

    def optimo(self):
        while(len(self.listaAccesosBarajados)>1):
            if len(self.RAMOpt) < self.RAMSize:
                siguiente=self.listaAccesosBarajados.pop(0)
                if self.RAMOpt.count(siguiente)==0:
                    if self.VRAMOpt.count(siguiente)>0:
                        self.VRAMOpt.remove(siguiente)
                        self.RAMOpt.append(siguiente)
                        self.stats.TiempoSimulado = self.stats.TiempoSimulado+5
                        self.stats.TiempoTrashing = self.stats.TiempoTrashing+5

                    self.RAMOpt.append(siguiente)
                    self.stats.TiempoSimulado = self.stats.TiempoSimulado+1
                
                else:
                    self.stats.TiempoSimulado = self.stats.TiempoSimulado + 1

                sleep(2)

            if len(self.RAMOpt) >= self.RAMSize:
                siguiente= self.listaAccesosBarajados.pop(0)
                if self.RAMOpt.count(siguiente)==0:
                    maxIndx=0 #index de la pagina mas tardada
                    max=0 #accesos faltantes
                    for x in range(len(self.RAMOpt)):
                        accessosfaltantes = self.getFaltantes(self.RAMOpt[x][1])
                        if accessosfaltantes > max:
                            max = accessosfaltantes
                            maxIndx = x

                    siguiente= self.listaAccesosBarajados.pop(0)
                    if self.VRAMOpt.count(siguiente)>0:
                        self.VRAMOpt.remove(siguiente)
                    self.VRAMOpt.append(self.RAMOpt[maxIndx])
                    self.RAMOpt[maxIndx] = siguiente
                    self.stats.TiempoTrashing  = self.stats.TiempoTrashing  + 5
                    self.stats.TiempoSimulado = self.stats.TiempoSimulado + 6
                
                self.stats.TiempoSimulado = self.stats.TiempoSimulado + 1

                sleep(2)

            self.calcularAccesosfaltanttes()
            self.calcularFragmentacionInternaOpt()
            self.calcularRAMUtilizadaYVRAM()
            print("Tiempo total: ",self.stats.TiempoSimulado)
            print("Tiempo de Trashing: ",self.stats.TiempoTrashing)
            print("RAM utilizada: ", self.stats.RAMUtilizada)
            print("VRAM utilizada: ", self.stats.VRAMUtilizada)

            print("RAM-",self.RAMOpt)
            print("VRRAM-",self.VRAMOpt)
        return
