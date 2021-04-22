from hiccups_scraper.hiccups_scraper.shopify_scraper import get_bestware_products
import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter as tk
from typing import Counter
import webbrowser
import threading
import time

bestware_products = []


def thread(name, productbox):
    
    print("thread {} started".format(name))
    while True:
        
        get_bestware_products(bestware_products)
        for i in productbox.get_children():
            productbox.delete(i)
        for i in range(1000):
            productbox.insert('', 'end', text=bestware_products[i]['title'], values=(bestware_products[i]['handle'], bestware_products[i]['price']))
        time.sleep(1)
        bestware_products.clear()
        
    

def openwebpage(url):
    webbrowser.open(url)

def vendors(tab):
    
    productbox = ttk.Treeview(tab, columns=("Name", "URL", "Price"))
    productbox.grid(row=1, column=0)
    
    productbox.heading("#0", text=" Name")
    productbox.heading("#1", text=" URL")
    productbox.heading("#2", text=" Price")

    x = threading.Thread(target=thread, args=("new thread", productbox))
    x.daemon = True
    x.start()

    conn = sqlite3.connect('Hiccups.db')  # create a DB if there is not one
    c = conn.cursor()
    c.execute('''SELECT 
                SKU,
                CASE
                    WHEN LENGTH(prodDesc) > 50 THEN
                        substr(prodDesc, 1, 50) || "..."
                    ELSE
                        prodDesc
                    END shortProdDesc,
                    
                unitsInStock,
                productURL
            FROM products
            WHERE unitsInStock == 0
            LIMIT 20 ;''')

    data = c.fetchall()
    

    button = ttk.Button(tab, text=data[0][0], command=lambda: openwebpage(data[0][3]))
    button.grid(column=0, row=0)
    
    items = []
