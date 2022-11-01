from os import path as path2
from cgitb import text
from glob import glob
from importlib.resources import path
from multiprocessing.connection import wait
from time import sleep
from tkinter import *
from tkinter import ttk
from unittest.mock import patch #Libreria para crear la interfaz grafica
from tkinter import messagebox
from tkinter import filedialog as fd
import random

fileContent=[]

def validate_entry(text):
    return text.isdecimal()

def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    lines=[]
    with fd.askopenfile(filetypes=filetypes) as f:
        lines = [line.rstrip('\n') for line in f]
    
    listaProcesos=[]
    for x in range(len(lines)):
        listaProcesos+=[lines[x].split(", ")]
    print(listaProcesos)

def ventana_iniciar(ventana):
    global txt_charge, mensajeCargado
    frme_venta_iniciar=Frame(ventana,width=750,height=695,bg="#FFE4B5")
    frme_venta_iniciar.place(x=0,y=0)
    mensajeCargado=Label(ventana,text="",bd=10,bg="#FFE4B5")
    mensajeCargado.place(x=470,y=635)

    open_button = ttk.Button(
        ventana,
        text='Open Files',
        command=select_file
    )
    open_button.place(x=470,y=635)
    seed_text=ttk.Entry(width = 20,validate="key",validatecommand=(ventana.register(validate_entry), "%S"))
    seed_text.place(x=340,y=645)
    btn_cargar=Button(ventana,text="Iniciar Simulacion",command=lambda:[ ],highlightthickness=1,bd=3,activebackground="khaki1")
    btn_cargar.place(x=220,y=640)

def cargar(ventana):
    global txt_charge, mensajeCargado
    if(isinstance(txt_charge.get(), str)):
        lines = open(txt_charge.get(),"r")
        for line in lines:
            mensajeCargado['text'] = line
    else:
        mensajeCargado['text'] = "No se ha encontrado el .txt"
    ventana.update()
        
ventana_principal=Tk()  
ventana_principal.title("Memory")     
ventana_principal.geometry("1400x720+280+0")
ventana_principal.config(bg="#FFE4B5")
ventana_principal.resizable(0,0)
ventana_iniciar(ventana_principal)
ventana_principal.mainloop() 