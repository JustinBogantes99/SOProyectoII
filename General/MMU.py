from .itemMMU import itemMMU

class MMU:
    def __init__(self):
        self.listaDeCositas = {}
        self.logicAddresCounter=0
        # item : {pageid -> itemMMU}

    #llamar cuando entra por primera vez una pagina a memoria
    def agregar(self,processID,ptr,LAddres,MAddres,mark,time):
        item= itemMMU( ptr, processID,True,LAddres,MAddres,"-",mark,time)#pageID unico ptr
        if ptr in self.listaDeCositas:
            pass
        else:
            self.listaDeCositas[ptr]=item
            self.logicAddresCounter=self.logicAddresCounter+1

    #se llama cuando se pagina una pagina, de RAM a VRAM o viceversa
    
    def actualizar(self, key, loaded, MAddres, DAddres,mark,time):
        
        self.listaDeCositas[key].loaded=loaded
        self.listaDeCositas[key].MAddres=MAddres
        self.listaDeCositas[key].DAddres=DAddres
        self.listaDeCositas[key].mark=mark
        self.listaDeCositas[key].time=time

    #Se llama cuando la siguiente pagina ya estaba en RAM
    def  actualizarAMarcadoYTiempo(self,key,mark,time):
        self.listaDeCositas[key].mark=mark
        self.listaDeCositas[key].time=time

    def to_string(self):
     for key, value in self.listaDeCositas.items():
        print(key, value.to_string())

    