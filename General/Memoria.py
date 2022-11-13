from .Pagina import Pagina 

class Memoria:
    def __init__(self):
        self.contenido = []
        # item : Pagina

    
    def encontrar(self,ptr):
        for pagina in self.contenido:
            if pagina.Ptr==ptr:
                print("lo encontre")
                return True
        
        return False

    def to_string(self):
        for cont in self.contenido:
            cont.to_string()