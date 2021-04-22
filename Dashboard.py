from tkinter import *
from tkinter import ttk
import sqlite3

from matplotlib.figure import Figure
import matplotlib.patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# conn = sqlite3.connect('invetory.db')  # create a DB if there is not one
# c = conn.cursor()
# #c.execute("SELECT product_name, price FROM products;")
# product_labels = []
# prices = []
# records = c.fetchall()
# for r in records:
#     product_labels.append(r[0])
#     prices.append(r[1])

# fig = Figure()
# ax = fig.add_subplot(111)
# ax.set(title='Inventory')
# ax.pie(prices, radius=1, labels=product_labels, shadow=True)

# circle=matplotlib.patches.Circle((0,0), 0.7, color='white')
# ax.add_artist(circle)

# c.execute("SELECT product_name, quantity FROM products WHERE quantity <= 5;")
# records = c.fetchall()
# if records == None:
#     LowAlertString = "No alerts at the moment"
# else:
#     LowAlertString = "These items are low in stock: \n"
#     temp = ""
#     for r in records:
#         temp += ('{:40s} {:4.1f} \n').format(r[0], r[1])
#     print(temp)
#     LowAlertString += temp

def Dashboard(Tab):
    pass

    # labelframe = LabelFrame(Tab, text="Alerts")
    # labelframe.grid(column=1, row=0)
    # AlertLabels = Label(labelframe, text="LowAlertString")
    # AlertLabels.pack()


    # option_frame = ttk.Frame(Tab)
    # option_frame.grid(row=5, column=7, padx=20, pady=(10, 0))
    

    # chart1 = FigureCanvasTkAgg(fig,Tab)
    # chart1.get_tk_widget().grid(row=0,column=0)