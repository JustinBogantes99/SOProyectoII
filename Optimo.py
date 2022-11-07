from time import sleep
import random
 
ListadeAccesos=[[1,1,500]
,[1,2,1024]
,[1,3,512]
,[2,4,256]
,[2,5,512]
,[3,6,128]
,[3,7,1024]
,[3,8,512]
,[3,9,512]
,[4,10,256]
]
listaAccesosBarajados=[[1,1,500]
,[3,6,128]
,[1,2,1024]
,[2,4,256]
,[2,5,512]
,[4,10,256]
,[1,3,512]
,[3,7,1024]
,[4,10,256]
,[3,8,512]
,[1,1,500]
,[2,5,512]
,[3,8,512]
,[3,9,512]
,[3,7,1024]
]


pRAM=[]
pVRAM=[]
paginasMarcadas=[]
for acceso in ListadeAccesos:
    paginasMarcadas.append([0,acceso])



def calcularAccesosfaltanttes():
        for x in range(len(ListadeAccesos)):
            contador=0
            for y in range(len(listaAccesosBarajados)):
                if ListadeAccesos[x][1]!= listaAccesosBarajados[y][1]:
                    contador=contador+1
                else:
                    break 
            paginasMarcadas[x][0]=contador

        
def getFaltantes(ptr):
    for y in range( len(paginasMarcadas)):
        if paginasMarcadas[y][1][1]==ptr:
            return paginasMarcadas[y][0]

def optimo():
    while(len(listaAccesosBarajados)>0):
        if len(pRAM)<15:
            pRAM.append(listaAccesosBarajados.pop(0))

        if len(pRAM)==15:
            max=0 #index de la pagina mas tardada
            for x in range(len(pRAM)):
                accessosfaltantes =getFaltantes(pRAM[x][1])
                if accessosfaltantes>max:
                    max= x

            pVRAM.append(pRAM[x])
            pRAM[x]=listaAccesosBarajados.pop(0)

        calcularAccesosfaltanttes()






    return



print(paginasMarcadas)