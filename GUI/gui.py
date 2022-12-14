from .shared_imports import *

from .PaginaPrincipal import PaginaPrincipal
from .PaginaSimulador import PaginaSimulador

class Windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.fileContent = []
        self.algoritmo_escogido = ""
        self.seed = ""

        self.wm_title("Proyecto II: Sistemas Operativos")
        self.geometry("1600x1000+10+10")

        container = tk.Frame(self, height=300, width=300)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (PaginaPrincipal, PaginaSimulador):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PaginaPrincipal)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
