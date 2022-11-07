from os import path as path2
from cgitb import text
from glob import glob
from importlib.resources import path
from time import sleep
from tkinter import *
from tkinter import ttk
from unittest.mock import patch #Libreria para crear la interfaz grafica
from tkinter import messagebox
from tkinter import filedialog as fd
import tkinter as tk

import random
from PIL import Image,ImageTk

fileContent=[]

def validate_entry(text):
    return text.isdecimal()

def select_file():
    global FileNameLabel
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    lines=[]
    try:
        with fd.askopenfile(filetypes=filetypes) as f:
            FileNameLabel.config(text=f.name)
            lines = [line.rstrip('\n') for line in f]
    except:
        print("Error")
    listaProcesos=[]
    for x in range(len(lines)):
        listaProcesos+=[lines[x].split(", ")]
    fileContent=listaProcesos
    print(fileContent)

def ventana_iniciar(ventana):
    pass

    

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
ventana_principal.resizable(0,0)
img=ImageTk.PhotoImage(file="name.png")
imgbtn=ImageTk.PhotoImage(file="simu.png")  
LocalImg=Label(ventana_principal,image=img)
LocalImg.place(x=100,y=100)
open_button = ttk.Button(
        ventana_principal,
        text='Open Files',
        command=select_file
    )
open_button.place(x=350,y=380)
seedLabel=Label(ventana_principal,text="Por favor ingrese la semilla")
seedLabel.place(x=100,y=300)
seed_text=ttk.Entry(width = 20,validate="key",validatecommand=(ventana_principal.register(validate_entry), "%S"))
seed_text.place(x=260,y=300)
FileLabel=Label(ventana_principal,text="Seleccion el archivo a cargar")
FileLabel.place(x=100,y=380)
FileNameLabel=Label(ventana_principal,text="")
FileNameLabel.place(x=100,y=400)
btn_cargar=Button(ventana_principal,image=imgbtn,command=lambda:[ventana_iniciar(ventana_principal)],highlightthickness=1,bd=3)
btn_cargar.place(x=600,y=640)

ventana_principal.mainloop() 