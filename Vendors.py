from hiccups_scraper.hiccups_scraper.shopify_scraper import get_bestware_products
import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter as tk
from typing import Counter
import webbrowser
import threading
import time
import os
from twisted.internet import reactor
import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess

class LollicupSpider(scrapy.Spider):
    name = 'lollicup'
    start_urls = ['https://lollicupstore.com/all-categories/food-beverages.html?product_list_limit=all',
                  'https://lollicupstore.com/all-categories/restaurant-supplies.html?product_list_limit=all',
                  'https://lollicupstore.com/all-categories/general-supplies.html?product_list_limit=all']

    def parse(self, response):
        for products in response.css('div.product-info'):
            yield {
                'name': products.css('a.product-item-link::text').get().replace('\n', ''),
                'price': products.css('span.price::text').get().replace('$', ''),
                'link': products.css('a.product-item-link').attrib['href'],
            }

bestware_products = []
lollicup_products = []


def bestware_thread(name, productbox):
    
    print("thread {} started".format(name))
    while True:
        
        get_bestware_products(bestware_products)
        for i in productbox.get_children():
            productbox.delete(i)
        for i in range(1000):
            productbox.insert('', 'end', text=bestware_products[i]['title'], values=(bestware_products[i]['handle'], bestware_products[i]['price']))
        time.sleep(1)
        bestware_products.clear()
        
def lollicup_thread(output_list):
    if os.path.exists("lollicup_products.csv"):
        os.remove("lollicup_products.csv")
    c = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0',
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'lollicup_products.csv',
})
    c.crawl(LollicupSpider)
    c.start()

    df = pd.read_csv("lollicup_products.csv", delimiter=',')
    for x in df.values:
        output_list.append(tuple(x))

def openwebpage(url):
    webbrowser.open(url)

def vendors(tab):
    
    BestWareTable = ttk.Treeview(tab, columns=("Name", "URL", "Price"))
    BestWareTable.grid(row=1, column=0)
    
    BestWareTable.heading("#0", text=" Name")
    BestWareTable.heading("#1", text=" URL")
    BestWareTable.heading("#2", text=" Price")

    LollicupTable = ttk.Treeview(tab, columns=("Name", "URL", "Price"))
    LollicupTable.grid(row=2, column=0)
    
    LollicupTable.heading("#0", text=" Name")
    LollicupTable.heading("#1", text=" URL")
    LollicupTable.heading("#2", text=" Price")

    #starts the thread that pulls info from bestware
    x = threading.Thread(target=bestware_thread, args=("new thread", BestWareTable))
    x.daemon = True
    x.start()

    #starts thread that pulls the info from the lollicup store
    lollicup_thread(lollicup_products)
    for i in range(1000):
            LollicupTable.insert('', 'end', text=lollicup_products[i][0], values=(lollicup_products[i][2], lollicup_products[i][1]))

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
