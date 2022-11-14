from .Pagina import Pagina 

class Memoria:
    def __init__(self,RAMSIZE):
        self.contenido = []
        self.RAMSize= RAMSIZE
        self.FragmentacionInterna=0
        # item : Pagina

    
    def encontrar(self,ptr):
        for pagina in self.contenido:
            if pagina.Ptr==ptr:
                print("lo encontre")
                return True
        
        return False

    def calcularFragmentacionInterna(self):
        self.FragmentacionInternaOpt=0
        for pagina in self.contenido:
            self.FragmentacionInterna = self.FragmentacionInterna + ((4000-pagina.Size))
        return self.FragmentacionInterna

    def calcularMemoriaUtilizada(self):
        uRAM=len(self.contenido)*4000
        uVRAM= len(self.contenido)*4000

        return [uRAM,uVRAM]

    def calcularProcentajeRAM(self):
        
        return len(self.contenido)

    def calcularProcentajeRAM(self):
        VRAMutilizda= len(self.contenido)

        return (VRAMutilizda/self.RAMSize)*100

    def cantidadDeProcesos(self):
        procesos=[]
        for pag in self.contenido:
            if not pag.PID in procesos:
                procesos.append(pag.PID)
        
        return len(procesos)
            

    def to_string(self):
        for cont in self.contenido:
            cont.to_string()