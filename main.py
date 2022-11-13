from GUI.gui import Windows
from General.Simulador import Simulador

def main():
    gui = Windows()
    gui.mainloop()

    # simulador_lru = Simulador("LRU", None)
    # simulador_lru.correr_algoritmo()

    # simulador_secondchance = Simulador("SecondChance", None)
    # simulador_secondchance.correr_algoritmo()

    # simulador_optimo = Simulador("Optimo", None)
    # simulador_optimo.correr_algoritmo()

    # simulador_aging = Simulador("Aging", None)
    # simulador_aging.correr_algoritmo()

    # simulador_random = Simulador("Random", None)
    # simulador_random.correr_algoritmo()


if __name__ == "__main__":
    main()
