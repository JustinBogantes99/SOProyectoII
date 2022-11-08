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
FragmentacionInternaLRU=0
TiempoSimLRU=0
TiempoTrashingLRU=0
RAMLRU=[]
VRAMLRU=[]
mayores=[]
VRAMUtilizada=len(VRAMLRU)*4
paginasMarcadas=[]  #lista con las paginas y la cantidad de accesos a memoria necesarios antes de ser usada [accesos,[pagina]]
for acceso in ListadeAccesos:
    paginasMarcadas.append([0,acceso])

def calcularFragmentacionInternaLRU():
    global FragmentacionInternaLRU
    FragmentacionInternaLRU=0
    for pagina in RAMLRU:
        FragmentacionInternaLRU= FragmentacionInternaLRU + ((4000-pagina[2])/1000)
    return FragmentacionInternaLRU

def calcularRAMUtilizadaYVRAM():
    global RAMUtilizada, VRAMUtilizada
    RAMUtilizada=len(RAMLRU*4)
    VRAMUtilizada = len(VRAMLRU*4)
    
def agregarContadoresLRU():
    global listaAccesosBarajados
    for x in listaAccesosBarajados:
        x+=[0]
    #print(listaAccesosBarajados)
    #print("-------------")
def sacarMayorLRU():
    global RAMLRU
    lista=[]
    for x in RAMLRU:
        lista+=[x[3]]
    valoMax=max(lista)
    return valoMax

def LRU():
    global TiempoSimLRU, TiempoTrashingLRU
      
    while(len(listaAccesosBarajados)>18):
        if len(RAMLRU)<RAMSize:
            siguiente=listaAccesosBarajados.pop(0)#[1,1,500]
            #print(siguiente)
            if RAMLRU.count(siguiente)==0:
                if VRAMLRU.count(siguiente)>0:
                    VRAMLRU.remove(siguiente)
                    RAMLRU.append(siguiente)
                    TiempoSimLRU=TiempoSimLRU+5#no me quedo claro que es
                    TiempoTrashingLRU=TiempoTrashingLRU+5#no me queda claro si en LRU hay Trashing
                if len(RAMLRU)!=0:
                    for pagina in RAMLRU:
                        pagina[3]+=1
                siguiente[3]+=1        
                RAMLRU.append(siguiente)
                TiempoSimLRU=TiempoSimLRU+1
            elif RAMLRU.count(siguiente)!=0:
                for pag in RAMLRU:
                    print("------------")
                    print(pag)
                    print("------------")
                    if pag==siguiente:
                        pag[3]=0
                TiempoSimLRU=TiempoSimLRU+1
        #print(RAMLRU)
        #print("------")
        if len(RAMLRU)>=RAMSize:
            siguiente= listaAccesosBarajados.pop(0)
            #print(siguiente) 
            if RAMLRU.count(siguiente)==0: 
                mayor=sacarMayorLRU()
                cont=0
                for pagina in RAMLRU:
                    if pagina[3]==mayor:
                        siguiente[3]+=1  
                        RAMLRU[cont]=siguiente
                        VRAMLRU.append(pagina)
                    cont+=1
                if len(RAMLRU)!=0:
                    for pagina in RAMLRU:
                        pagina[3]+=1    
            elif RAMLRU.count(siguiente)==0:
                for pag in RAMLRU:
                    print("------------")
                    print(pag)
                    print("------------")
                    if pag==siguiente:
                        pag[3]=0
                TiempoSimLRU=TiempoSimLRU+1
    #print("***************")
agregarContadoresLRU()   
LRU() 
print("-RAM-")
print(RAMLRU)
print("-VRAM-")
print(VRAMLRU)
