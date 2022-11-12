from .Pagina import Pagina 

class Memoria:
    def __init__(self):
        self.contenido = []
        # item : Pagina

    
    def encontrar(self,ptr):
        for pagina in self.contenido:
            if pagina.Ptr==ptr:
                return True
        
        return False