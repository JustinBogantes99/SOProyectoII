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

RAMSize=5
RAMTotal=RAMSize*4
RAMUtilizada=0
VRAMUtilizada=len
FragmentacionInternaOpt=0
TiempoSimOpt=0
TiempoTrashingOpt=0
RAMOpt=[]
VRAMOpt=[]
VRAMUtilizada=len(VRAMOpt)*4
paginasMarcadas=[]  #lista con las paginas y la cantidad de accesos a memoria necesarios antes de ser usada [accesos,[pagina]]
for acceso in ListadeAccesos:
    paginasMarcadas.append([0,acceso])



#Calcula cuantos accesos a memoria faltan para que la paginas sea usada de nuevo
def calcularAccesosfaltanttes():
        for x in range(len(ListadeAccesos)):
            contador=0
            for y in range(len(listaAccesosBarajados)):
                if ListadeAccesos[x][1]!= listaAccesosBarajados[y][1]:
                    contador=contador+1
                else:
                    break 
            paginasMarcadas[x][0]=contador

#Devuelve la cantidad de accesoss faltantes para utilizar la pagina ptr       
def getFaltantes(ptr):
    for y in range( len(paginasMarcadas)):
        if paginasMarcadas[y][1][1]==ptr:
            return paginasMarcadas[y][0]



def calcularFragmentacionInternaOpt():
    global FragmentacionInternaOpt
    FragmentacionInternaOpt=0
    for pagina in RAMOpt:
        FragmentacionInternaOpt= FragmentacionInternaOpt + ((4000-pagina[2])/1000)
    return FragmentacionInternaOpt

def calcularRAMUtilizadaYVRAM():
    global RAMUtilizada, VRAMUtilizada
    RAMUtilizada=len(RAMOpt*4)
    VRAMUtilizada = len(VRAMOpt*4)

def optimo():
    global TiempoSimOpt, TiempoTrashingOpt
    while(len(listaAccesosBarajados)>1):
        if len(RAMOpt)<RAMSize:
            siguiente=listaAccesosBarajados.pop(0)
            if RAMOpt.count(siguiente)==0:
                if VRAMOpt.count(siguiente)>0:
                    VRAMOpt.remove(siguiente)
                    RAMOpt.append(siguiente)
                    TiempoSimOpt=TiempoSimOpt+5
                    TiempoTrashingOpt=TiempoTrashingOpt+5

                RAMOpt.append(siguiente)
                TiempoSimOpt=TiempoSimOpt+1
            
            else:
                TiempoSimOpt=TiempoSimOpt+1



            sleep(2)

        if len(RAMOpt)>=RAMSize:
            siguiente= listaAccesosBarajados.pop(0)
            if RAMOpt.count(siguiente)==0:
                maxIndx=0 #index de la pagina mas tardada
                max=0 #accesos faltantes
                for x in range(len(RAMOpt)):
                    accessosfaltantes =getFaltantes(RAMOpt[x][1])
                    if accessosfaltantes>max:
                        max= accessosfaltantes
                        maxIndx=x

                siguiente= listaAccesosBarajados.pop(0)
                if VRAMOpt.count(siguiente)>0:
                    VRAMOpt.remove(siguiente)
                VRAMOpt.append(RAMOpt[maxIndx])
                RAMOpt[maxIndx]=siguiente
                TiempoTrashingOpt=TiempoTrashingOpt+5
                TiempoSimOpt=TiempoSimOpt+6
            
            TiempoSimOpt=TiempoSimOpt+1

            sleep(2)

        calcularAccesosfaltanttes()
        calcularFragmentacionInternaOpt()
        calcularRAMUtilizadaYVRAM()
        print("Tiempo total: ",TiempoSimOpt)
        print("Tiempo de Trashing: ",TiempoTrashingOpt)
        print("RAM utilizada: ", RAMUtilizada)
        print("VRAM utilizada: ", VRAMUtilizada)

        print("RAM-",RAMOpt)
        print("VRRAM-",VRAMOpt)
    return



print(paginasMarcadas)
optimo()