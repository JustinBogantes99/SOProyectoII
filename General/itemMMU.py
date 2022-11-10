class itemMMU:
    def __init__(self, pageID, processID, loaded, LAddress, MAddres, DAddres):
        self.pageID = pageID
        self.processID = processID
        self.loaded = loaded
        self.LAddress = LAddress
        self.MAddres = MAddres
        self.DAddres = DAddres
        self.color = "HEX" # dudoso
        self.time = None
        self.mark = None