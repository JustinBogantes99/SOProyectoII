from .Pagina import Pagina 
import uuid
import random

class Memoria:
    def __init__(self,RAMSIZE, seed):
        self.contenido = []
        self.direcciones_DAddres = {}
        self.RAMSize= RAMSIZE
        random.seed(seed)
        # item : Pagina

    def random_uuid(self):
        puuid = uuid.UUID(bytes=bytes(random.getrandbits(8) for _ in range(16)), version=4)
        return str(puuid)[:6]

    def sacar(self, index):
        pagina = self.contenido.pop(index)
        llave= None
        for key, value in self.direcciones_DAddres.items():
            if value == pagina.Ptr:
                llave=key
               
        
        del self.direcciones_DAddres[llave]
        return pagina

    def meter(self, pagina):
        self.contenido.append(pagina)
        key= self.random_uuid()
        self.direcciones_DAddres[key]=pagina.Ptr
        pass

    def encontrar_direccion(self, ptr):
        for key, value in self.direcciones_DAddres.items():
            if value==ptr:
                return key
        pass
    
    def encontrar(self,ptr):
        for pagina in self.contenido:
            if pagina.Ptr==ptr:
                return True
        
        return False

    def calcularFragmentacionInterna(self):
        FragmentacionInterna=0
        for pagina in self.contenido:
            FragmentacionInterna = FragmentacionInterna + ((4000-pagina.Size))
        return FragmentacionInterna

    def calcularMemoriaUtilizada(self):
        uRAM=len(self.contenido)*4000
      

        return uRAM

    def calcularProcentajeRAM(self):
        
        return len(self.contenido)

    def calcularProcentajeVRAM(self):
        VRAMutilizda= len(self.contenido)

        return (VRAMutilizda/self.RAMSize)*100

    def to_string(self):
        for cont in self.contenido:
            cont.to_string()