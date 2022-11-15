import tkinter as tk
from tkinter import ttk

recentWindow = tk.Tk()
recentWindow.geometry('800x300')

recentWindow.columnconfigure(0, weight=1)
recentWindow.rowconfigure(0, weight=1)

frmtreeborder = tk.LabelFrame(recentWindow,text='Recent')

frmtreeborder.columnconfigure(0, weight=1)
frmtreeborder.rowconfigure(0, weight=1)

colnames = [str(ii) for ii in range(20)]
tree = ttk.Treeview(frmtreeborder,columns=colnames,show='headings',
                    height=5,selectmode='extended')

for a in colnames:
    tree.column(a,width=85)
    tree.heading(a,text=a)

scrollbar = ttk.Scrollbar(recentWindow,orient=tk.HORIZONTAL,command=tree.xview)
tree.configure(xscrollcommand=scrollbar.set)

frmtreeborder.grid(column=0,row=0,sticky='nsew',padx=6,pady=6)
tree.grid(column=0,row=0,sticky='nsew',padx=6,pady=6)
scrollbar.grid(row=1,column=0,sticky='ew')

recentWindow.mainloop()