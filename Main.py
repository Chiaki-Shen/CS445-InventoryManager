'''from Vendors import vendors'''
from tkinter import ttk
import tkinter as tk
from frontEnd_V0_3 import MainScreen
'''from report import plot'''
from tkinter import *

root = tk.Tk()
root.title('CECS 445 Inventory Manager By Team Boba')

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (1400 / 2)
y = (hs / 2) - (1000 / 2)
root.geometry('%dx%d+%d+%d' % (1400, 1000, x, y))
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)


tabControl.add(tab1, text="Main Tab")
tabControl.add(tab2, text="Monthly Reports")
tabControl.grid(row=0, column=0)
MainScreen(tab1,root)
'''plot(tab2)'''
style = ttk.Style(root)
style.theme_use("winnative")
style.configure('Treeview', rowheight=34)
style.configure("Treeview.Heading", foreground='green', background='light gray', relief="flat" ,font=("Helvetica",11,"bold"))

'''global selected
selected = False
def cut_text(e):
    global selected
    if my_text.secletion_get():
        selected = my_text.secletion_get()
        my_text.delete("sel.first", "sel.last")

def copy_text(e):
    global selected
    if my_text.secletion_get():
        selected = my_text.secletion_get()

def paste_text(e):
    if selected:
        position = my_text.index(INSERT)
        my_text.insert(position, selected)

root.bing('<Control-Key-x>', cut_text)
root.bing('<Control-Key-c>', copy_text)
root.bing('<Control-Key-v>', paste_text)'''
root.mainloop()

