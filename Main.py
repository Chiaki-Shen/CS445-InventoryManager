from tkinter import ttk
import tkinter as tk
from frontEnd_V0_3 import MainScreen


root = tk.Tk()
root.title('CECS 445 Inventory Manager By Team Boba')

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (1400 / 2)
y = (hs / 2) - (700 / 2)
root.geometry('%dx%d+%d+%d' % (1400, 700, x, y))

tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Main Tab")
tabControl.grid(row=0, column=0)

MainScreen(tab1,root)


style = ttk.Style(root)
style.theme_use("winnative")
style.configure('Treeview', rowheight=34)
style.configure("Treeview.Heading", foreground='green', background='light gray', relief="flat" ,font=("Helvetica",11,"bold"))
style.map('Treeview', background = [('selected','green')])

root.mainloop()

