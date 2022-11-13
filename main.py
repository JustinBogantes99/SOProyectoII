from GUI.gui import Windows
from General.Simulador import Simulador

def main():
    # gui = Windows()
    # gui.mainloop()

    #simulador_optimo = Simulador("LRU", None)
    #simulador_optimo.correr_algoritmo()

    # simulador_optimo = Simulador("SecondChance", None)
    # simulador_optimo.correr_algoritmo()

    #simulador_optimo = Simulador("Optimo", None)
    #simulador_optimo.correr_algoritmo()

    simulador_optimo = Simulador("Random", None)
    simulador_optimo.correr_algoritmo()


if __name__ == "__main__":
    main()
