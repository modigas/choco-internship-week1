import scrapy
import json

class MechtaTechSpider(scrapy.Spider):
    name = 'mechta_tech'
    allowed_domains = ['www.mechta.kz']
    start_urls = ['https://www.mechta.kz/api/main/catalog_new/index.php?section=noutbuki&page_num=1&catalog=true&page_element_count=18',
                  'https://www.mechta.kz/api/main/catalog_new/index.php?section=smartfony&page_num=1&catalog=true&page_element_count=18',
                  'https://www.mechta.kz/api/main/catalog_new/index.php?section=processor&page_num=1&catalog=true&page_element_count=18',
                  'https://www.mechta.kz/api/main/catalog_new/index.php?section=videokarta&page_num=1&catalog=true&page_element_count=18']

    max_page_number = 1

    def parse(self, response):
        datas = response.xpath('//body/descendant::text()').get()
        JSON = None        
        try:
            JSON = json.loads(datas.encode('utf-8'))
        except:
            while True:
                try:
                    ind_start = datas.index('<ifr')
                    ind_end = datas.index('<\/iframe>')
                    chunk = datas[ind_start:ind_end+len('<\/iframe>')]
                    datas = datas.replace(chunk, '')
                except:
                    break
            JSON = json.loads(datas.encode('utf-8'))
            
        product = JSON['data']['ITEMS']
        total_items = int(JSON['data']['ALL_ITEMS'])
        curr_page = JSON['data']['PAGE_NUMBER']
        category = product[0]["METRICS"]["CATEGORY"]
        max_pages = total_items//18 + 1       
        
        for elem in product:
            title = elem['NAME']
            price = elem['PRICE']['PRICE']
            yield {
                'title'    : title,
                'price'    : price,
                'category' : category
            }

        if int(curr_page) <= max_pages:
            to_replace = 'page_num=' + str(curr_page)
            replace_with = 'page_num=' + str(int(curr_page) + 1)
            next_page = response.url.replace(to_replace, replace_with)
            yield scrapy.Request(url=next_page, callback=self.parse)

        