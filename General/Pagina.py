from pprint import pprint
class Pagina:
    def __init__(self):
        self.PID = None
        self.Ptr = None
        self.Size = None
        self.Contador=None
      
    def to_string(self):
        pprint(vars(self)) 
