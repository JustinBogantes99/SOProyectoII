from .Pagina import Pagina 
import uuid
import random

class Memoria:
    def __init__(self,RAMSIZE, seed):
        self.contenido = []
        self.direcciones_DAddres = {}
        self.RAMSize= RAMSIZE
        self.FragmentacionInterna=0
        random.seed(seed)
        # item : Pagina

    def random_uuid():
        uuid = uuid.UUID(bytes=bytes(random.getrandbits(8) for _ in range(16)), version=4)
        return str(uuid)[:4]

    def sacar(self, pagina):
        pass

    def meter(self, pagina):
        pass

    def encontrar_direccion(self, ptr):
        pass
    
    def encontrar(self,ptr):
        for pagina in self.contenido:
            if pagina.Ptr==ptr:
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

    def to_string(self):
        for cont in self.contenido:
            cont.to_string()