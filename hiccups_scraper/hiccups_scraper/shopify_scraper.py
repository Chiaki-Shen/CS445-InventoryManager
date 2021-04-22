import requests
import json
import pandas as pd


def get_bestware_products(output):
    #productlist = []

    for x in range(1, 50):

        url = 'https://bestwareshop.com/products.json?limit=250&page=' + str(x)
        r = requests.get(url)

        data = r.json()

        for item in data['products']:
            title = item['title']
            handle = item['handle']
            for variant in item['variants']:
                price = variant['price']
                quantity = variant['option1']
                sku = variant['sku']
                available = variant['available']

                product = {
                    'title': title.replace('?', ''),
                    'handle': 'https://bestwareshop.com/products/' + handle,
                    'price': price,
                    'sku': sku,
                    'quantity': quantity,
                    'available': available
                }

                output.append(product)
    #return productlist

# df = pd.DataFrame(productlist)
# df.to_csv('Bestware.csv')
# print('Proucts saved to Bestware.csv')