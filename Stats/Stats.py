class Stats:
    def __init__(self):
        self.TiempoSimulado =0
        self.TiempoTrashing =0
        self.FragmentacionInterna=0
        self.RAMUtilizada =0
        self.VRAMUtilizada=0
        self.PaginasEnMemoria=0
        self.PaginasEnDisco=0

    def porcentajeTrashing(self):
        return (self.TiempoTrashing/self.TiempoSimulado)*100
        