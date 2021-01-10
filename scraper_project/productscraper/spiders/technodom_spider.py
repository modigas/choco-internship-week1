import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from products.models import Product
from scraper_project.productscraper.items import ProductscraperItem


class TechnodomTechSpider(scrapy.Spider):
    name = 'technodom_tech'

    # allowed_domains = ['www.technodom.kz']
    # start_urls = [
    #               'https://www.technodom.kz/smartfony-i-gadzhety/smartfony-i-telefony/smartfony',
    #               'https://www.technodom.kz/noutbuki-i-komp-jutery/noutbuki-i-aksessuary/noutbuki',
    #               'https://www.technodom.kz/noutbuki-i-komp-jutery/komplektujuschie/processory',
    #               'https://www.technodom.kz/noutbuki-i-komp-jutery/komplektujuschie/videokarty'
    #              ]
    
    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://www.technodom.kz/smartfony-i-gadzhety/smartfony-i-telefony/smartfony',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        html = driver.page_source
        resp = Selector(text=html)
        products = resp.xpath("//a[@class='ProductCard-Content']")
        category = resp.xpath("//h1/text()").get()
        for product in products:
            title = product.xpath(".//h4/text()").get()
            price = product.xpath(".//descendant::data/text()").get()
            entry = Product(title = title, category = category, price = price, store = 'Technodom')
            entry.save()
            yield ProductscraperItem(
                title = title,
                price = price,
                category = category,
                store = 'Technodom'
            )

        next_page = resp.xpath("//a[@aria-label='Следующая страница']/@href").get()
        if next_page:
            next_page_url = f"https://www.technodom.kz{next_page}"
            yield SeleniumRequest(
                url=next_page_url,
                wait_time=20,
                # encoding='utf-8',
                # wait_until=EC.presence_of_element_located((By.XPATH, "//div[@class='ContentWrapper CategoryPage-Wrapper']")),
                wait_until=EC.presence_of_element_located((By.XPATH, "//a[@class='ProductCard-Content']")),
                callback=self.parse
            )

            

        

