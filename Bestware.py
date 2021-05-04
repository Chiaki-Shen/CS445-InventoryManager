import os
import pandas as pd
import shopify_scraper

def get():

    productlist = []
    shopify_scraper.get_bestware_products(productlist)
    if os.path.exists("Bestware.csv"):
        os.remove("Bestware.csv")
        df = pd.DataFrame(productlist)
        df.to_csv('Bestware.csv')
        print('Proucts saved to Bestware.csv')