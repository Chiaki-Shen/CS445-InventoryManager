from Vendors import vendors
from tkinter import *
from tkinter import ttk
import tkinter as tk
import sqlite3
from Dashboard import Dashboard
from frontEnd_V0_3 import MainScreen

running = True

def on_closing():
    running = False

root = tk.Tk()
root.title('CECS 445 Inventory Manager By Team Boba')

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (1400 / 2)
y = (hs / 2) - (700 / 2)
root.geometry('%dx%d+%d+%d' % (1400, 700, x, y))
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text="Main Tab")
tabControl.add(tab2, text="Dashboard")
tabControl.add(tab3, text="Vendors")
tabControl.grid(row=0, column=0)
MainScreen(tab1,root)
Dashboard(tab2)
vendors(tab3)

root.mainloop()

