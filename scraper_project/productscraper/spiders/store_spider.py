import scrapy
import re

class TechSpider(scrapy.Spider):
    name = "tech"

    start_urls = [
        'https://www.sulpak.kz/f/smartfoniy/nur_sultan'
    ]

    def parse(self, response):
        for products in response.css('div.goods-tiles'):
            try:
                yield {
                    'title': re.sub('[^A-Za-z0-9 ]+', '', products.css('.title ::text').get().strip()),
                    'price': re.sub('[^A-Za-z0-9 ]+', '', products.css('div.price ::text').get().strip()),
                }
            except:
                yield {
                    'title': re.sub('[^A-Za-z0-9 ]+', '', products.css('.title ::text').get().strip()),
                    'price': 'NA',
                }

        next_page = response.css('a.next').attrib['href']
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
#     def start_requests(self):
#         yield SplashRequest(
#             url='https://www.technodom.kz/smartfony-i-gadzhety/smartfony-i-telefony/smartfony/f/brands/apple?page=1',
#             callback=self.parse,
#         )
        
#     def parse(self, response):
#         goods = response.css('div.ProductCard-Content::text')
#         i = 0
#         for good in goods:
#             print(f'{i}: {good}')
#             i += 1
#         # titles = response.css('h3.title ::text').getall()
#         # prices = response.css('div.price ::text').getall()
#         # for title, price in zip(titles, prices):
#         #     print(f'product: {title.strip()} price: {price}')
