from pprint import pprint
class itemMMU:
    def __init__(self, pageID, processID, loaded, LAddres, MAddres, DAddres,mark,time):
        self.pageID = pageID#unico
        self.processID = processID
        self.loaded = loaded
        self.LAddres = LAddres
        self.MAddres = MAddres
        self.DAddres = DAddres
        self.color = "HEX" # dudoso
        self.time = time
        self.mark = mark

    def to_string(self):
        pprint(vars(self))