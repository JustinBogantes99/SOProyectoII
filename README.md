# SOProyectoII
Proyecto II curso Sistemas operativos

## General

La carpeta general tiene el MMU y la Memoria (Para RAM y VRAM)

## Stats

Tiene la clase para manejar los stats de la simulación (tiempos, tamaños, espacios, etc)

## Algoritmos

Tiene los algoritmos C:

## GUI

En proceso de construcción. Se va a separar de main en su momento

## Funcionamiento civilizado

Se debe llamar a la clase Simulador y se le pasa por parametro el algoritmo que se quiere simular.

El simulador tiene el atributo algoritmo, pero el atributo algoritmo es una clase a la que se le pasa por parametro el simulador mismo.

El algoritmo tiene acceso a todos los atributos del simulador a partir del atributo simulador.

NO se tiene que cambiar nada desde la clase simulador. Todos los cambios se hacen desde la clase algoritmo.
