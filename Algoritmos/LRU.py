from time import sleep
import random

class LRU:

    def __init__(self):
        self.ListadeAccesos=[[1,1,500]
        ,[1,2,1024]
        ,[1,3,512]
        ,[2,4,256]
        ,[2,5,512]
        ,[3,6,128]
        ,[3,7,1024]
        ,[3,8,512]
        ,[3,9,512]
        ,[4,10,256]
        ]

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

    def calcularRAMUtilizadaYVRAM(self):
        self.RAMUtilizada=len(self.RAMLRU*4)
        self.VRAMUtilizada = len(self.VRAMLRU*4)
        
    def agregarContadoresLRU(self):
        for x in self.listaAccesosBarajados:
            x+=[0]

    def sacarMayorLRU(self):
        lista=[]
        for x in self.RAMLRU:
            lista+=[x[3]]
        self.valoMax=max(lista)
        return self.valoMax

    def run(self):
        print("Corriendo el print")
        while(len(self.listaAccesosBarajados)>18):
            if len(self.RAMLRU)<self.RAMSize:
                siguiente=self.listaAccesosBarajados.pop(0)#[1,1,500]
                if self.RAMLRU.count(siguiente)==0:
                    if self.VRAMLRU.count(siguiente)>0:
                        self.VRAMLRU.remove(siguiente)
                        self.RAMLRU.append(siguiente)
                        self.TiempoSimLRU = self.TiempoSimLRU+5 # no me quedo claro que es
                        self.TiempoTrashingLRU = self.TiempoTrashingLRU+5 # no me queda claro si en LRU hay Trashing
                    if len(self.RAMLRU)!=0:
                        for pagina in self.RAMLRU:
                            pagina[3]+=1
                    siguiente[3]+=1        
                    self.RAMLRU.append(siguiente)
                    self.TiempoSimLRU = self.TiempoSimLRU + 1
                elif self.RAMLRU.count(siguiente)!=0:
                    for pag in self.RAMLRU:
                        print("------------")
                        print(pag)
                        print("------------")
                        if pag==siguiente:
                            pag[3]=0
                    self.TiempoSimLRU = self.TiempoSimLRU + 1

            if len(self.RAMLRU) >= self.RAMSize:
                siguiente= self.listaAccesosBarajados.pop(0)

                if self.RAMLRU.count(siguiente)==0: 
                    mayor=self.sacarMayorLRU()
                    cont=0
                    for pagina in self.RAMLRU:
                        if pagina[3]==mayor:
                            siguiente[3]+=1  
                            self.RAMLRU[cont]=siguiente
                            self.VRAMLRU.append(pagina)
                        cont+=1
                    if len(self.RAMLRU)!=0:
                        for pagina in self.RAMLRU:
                            pagina[3]+=1    
                elif self.RAMLRU.count(siguiente)==0:
                    for pag in self.RAMLRU:
                        print("------------")
                        print(pag)
                        print("------------")
                        if pag==siguiente:
                            pag[3]=0
                    self.TiempoSimLRU = self.TiempoSimLRU+1
