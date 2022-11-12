from pprint import pprint
class itemMMU:
    def __init__(self, pageID, processID, loaded, LAddres, MAddres, DAddres):
        self.pageID = pageID
        self.processID = processID
        self.loaded = loaded
        self.LAddres = LAddres
        self.MAddres = MAddres
        self.DAddres = DAddres
        self.color = "HEX" # dudoso
        self.time = None
        self.mark = None

    def to_string(self):
        pprint(vars(self))