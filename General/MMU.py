from .itemMMU import itemMMU

class MMU:
    def __init__(self):
        self.listaDeCositas = {}
        # item : {pageid -> itemMMU}

    #llamar cuando entra por primera vez una pagina a memoria
    def agregar(self, pageID,processID,loaded,LAddres,MAddres,DAddres):
        item= itemMMU( pageID, processID, loaded, LAddres, MAddres, DAddres)
        self.listaDeCositas[pageID]=item

    #se llama cuando se pagina una pagina, de RAM a VRAM o viceversa
    def actualizar(self, key, loaded, MAddres, DAddres,mark,time):
        self.listaDeCositas[key].loaded=loaded
        self.listaDeCositas[key].loaded=MAddres
        self.listaDeCositas[key].loaded=DAddres
        self.listaDeCositas[key].loaded=mark
        self.listaDeCositas[key].loaded=time

    #Se llama cuando la siguiente pagina ya estaba en RAM
    def  actualizarAMarcadoYTiempo(self,key,mark,time):
        self.listaDeCositas[key].loaded=mark
        self.listaDeCositas[key].loaded=time

    def to_string(self):
     for key, value in self.listaDeCositas.items():
        print(key, value.to_string())

    