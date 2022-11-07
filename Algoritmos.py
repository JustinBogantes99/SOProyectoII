from time import sleep
import random

paginas=[1,2,3,4,5,6]
Paginacion=[]
listaPaginas={1:3,2:1,2:3,4:0,5:0,6:0}
contGlobalPag=0
LeastUsedCont=0
#[1,-,-] [1,2,-] [1,2,3] 
#print(listaPaginas.keys())

def crearPrimerasPaginas():
    global paginas,contGlobalPag,LeastUsedCont,Paginacion
    contPag=0
    dictPag=[]
    while contGlobalPag!=3:
        while contPag!=3:
            if len(dictPag)!=3:
                if contGlobalPag==0:
                    if len(dictPag)==0:
                        dictPag+=[{paginas[contGlobalPag]:LeastUsedCont}]
                    if len(dictPag)==2:
                        dictPag+=[{'':LeastUsedCont}]   
                    else:                
                        dictPag+=[{'':LeastUsedCont}]
                elif contGlobalPag==1:
                    cont=0
                    while cont!=2:
                        dictPag+=[{paginas[cont]:LeastUsedCont}]
                        cont+=1
                    dictPag+=[{'':LeastUsedCont}]
                else:
                    cont=0
                    while cont!=3:
                        dictPag+=[{paginas[cont]:LeastUsedCont}]
                        cont+=1
                        LeastUsedCont+=1     
            contPag+=1 
        contGlobalPag+=1 
        Paginacion+=[dictPag]   
        contPag=0
        dictPag=[]
    print(Paginacion)

def crearPaginas():
    global paginas,contGlobalPag,LeastUsedCont,Paginacion
    print(Paginacion)
    print(paginas[contGlobalPag])
    
crearPrimerasPaginas() 
crearPaginas()      