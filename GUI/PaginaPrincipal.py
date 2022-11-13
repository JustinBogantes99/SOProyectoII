from .shared_imports import *

from .PaginaSimulador import PaginaSimulador

class PaginaPrincipal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        # Cargar imagenes a utilizar
        self.img_titulo = ImageTk.PhotoImage(file="Assets/name.png")
        self.img_empezar = ImageTk.PhotoImage(file="Assets/simu.png")

        algoritmos_paging = ["", "Aging", "LRU", "Random", "Second Chance"]
        
        

        # Declarar componentes
        label_titulo = tk.Label(self, image=self.img_titulo)
        label_semilla = tk.Label(self, text="Por favor ingrese la semilla")
        self.input_seed = ttk.Entry(self, width=20, validate="key", validatecommand=(
            self.register(self.validate_entry), "%S"))

        
        label_dropdown = tk.Label(self, text="Seleccion un algoritmo")
        text_dropdown = tk.StringVar(self)
        text_dropdown.set(algoritmos_paging[0])
        self.dropdown_algoritmos = tk.OptionMenu(self, text_dropdown, *algoritmos_paging, command=self.callback)

        label_archivo = tk.Label(self, text="Seleccion el archivo a cargar")
        self.label_nombre_archivo = tk.Label(self, text="")
        button_archivo = ttk.Button(
            self,
            text='Importar archivo',
            command=self.select_file
        )

        button_empezar = ttk.Button(
            self, image=self.img_empezar, command=self.continuar)

        

        # Ubicación de los componentes
        label_titulo.place(x=100, y=100)

        label_semilla.place(x=100, y=300)
        self.input_seed.place(x=300, y=300)

        label_dropdown.place(x=100, y=400)
        self.dropdown_algoritmos.place(x=300, y=400)

        label_archivo.place(x=100, y=500)
        self.label_nombre_archivo.place(x=100, y=500)
        button_archivo.place(x=300, y=500)

        button_empezar.place(x=600, y=640)

    def continuar(self):
        if self.input_seed.get() == '' or self.controller.algoritmo_escogido == '' or self.label_nombre_archivo['text'] == '':
            self.open_popup()
        else:
            self.controller.seed = self.input_seed.get()
            self.controller.show_frame(PaginaSimulador)

    def open_popup(self):
        top= tk.Toplevel(self.parent)
        top.geometry('750x250')
        top.title("Error")
        tk.Label(top, text= "Debe declarar un seed, un algoritmo y un archivo", font=('Mistral 18 bold')).place(x=150,y=80)

    def callback(self, item):
        self.controller.algoritmo_escogido = item

    def validate_entry(self, text):
        return text.isdecimal()


    def select_file(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        lines = []
        try:
            with fd.askopenfile(filetypes=filetypes) as f:
                self.label_nombre_archivo.config(text=f.name)
                lines = [line.rstrip('\n') for line in f]
        except Exception as e:
            print(e)
        listaProcesos = []
        for x in range(len(lines)):
            listaProcesos += [lines[x].split(", ")]
        self.controller.fileContent = listaProcesos
        print(self.controller.fileContent)
