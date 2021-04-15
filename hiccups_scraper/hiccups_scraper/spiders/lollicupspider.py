import scrapy

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

