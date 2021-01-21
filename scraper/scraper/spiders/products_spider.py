import scrapy
import json
from scraper.scraper import scrape_urls
from datetime import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scraper.scraper.items import ScraperItem
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.selector import Selector
from selenium import webdriver
from .urls import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class StoreSpider(scrapy.Spider):
    """
    Scrapy spider that scrapes data from www.mechta.kz using JSON
    """
    name = 'mechta_tech'
    allowed_domains = ['www.mechta.kz']
    start_urls = MECHTA_URLS
    store_name = 'MECHTA'

    def parse(self, response):
        datas = response.xpath('//body/descendant::text()').get()
        url = response.url
        json_response = None
        try:
            json_response = json.loads(datas.encode('utf-8'))
        except BaseException:
            while True:
                try:
                    ind_start = datas.index('<ifr')
                    ind_end = datas.index(r'<\/iframe>')
                    chunk = datas[ind_start:ind_end + len(r'<\/iframe>')]
                    datas = datas.replace(chunk, '')
                except BaseException:
                    break
            json_response = json.loads(datas.encode('utf-8'))

        dict = {}
        for el in url[url.index('?')+1:].split('&'):
            temp = el.split('=')
            dict[temp[0]] = temp[1]

        product = json_response['data']['ITEMS']
        total_items = int(json_response['data']['ALL_ITEMS'])
        curr_page = json_response['data']['PAGE_NUMBER']
        category = dict['section']
        max_pages = total_items // 18 + 1
        curr_date = datetime.now()

        for elem in product:
            title = elem['NAME']
            price = elem['PRICE']['PRICE']
            loader = ItemLoader(item=ScraperItem(), response=response)
            loader.default_output_processor = TakeFirst()
            loader.add_value('title', title)
            loader.add_value('price', price)
            loader.add_value('category', category)
            loader.add_value('storeName', self.store_name)
            loader.add_value('dateAndTime', curr_date)
            yield loader.load_item()

        if int(curr_page) < max_pages:
            to_replace = 'page_num=' + str(curr_page)
            replace_with = 'page_num=' + str(int(curr_page) + 1)
            next_page = url.replace(to_replace, replace_with)
            yield scrapy.Request(url=next_page, callback=self.parse)


class BasicSpiderShopWW(scrapy.Spider):
    """
    Scrapy spider that scrapes data from www.shop.kz using XPATH
    """
    name = 'shopww_tech'
    allowed_domains = ['www.shop.kz']
    start_urls = SHOPWW_URLS
    store_name = 'WHITE WIND'

    def parse(self, response):
        category = response.xpath(
            "//div[@class='bx-breadcrumb']/descendant::span[2]/text()").get()
        products = response.xpath("//div[@class='bx_catalog_item double']")
        for product in products:
            title = product.xpath('.//descendant::a/@title').get()
            price = product.xpath(
                ".//descendant::span[@class='bx-more-price-text']/text()").get()
            if price:
                loader = ItemLoader(item=ScraperItem(), response=response)
                loader.default_output_processor = TakeFirst()
                decomp = response.url.split('shop.kz')
                curr_date = datetime.now()
                loader.add_value('title', title)
                if isinstance(price, str):
                    loader.add_value('price', scrape_urls.strPriceToNum(price))
                elif isinstance(price, int):
                    loader.add_value('price', price)
                loader.add_value('category', decomp[1].split('/')[1])
                # loader.add_value('category', category)
                loader.add_value('storeName', self.store_name)
                loader.add_value('dateAndTime', curr_date)
                yield loader.load_item()

        next_page = response.xpath("//li[@class='bx-pag-next']/a/@href").get()
        next_page_url = f"https://www.shop.kz{next_page}"

        if next_page:
            yield scrapy.Request(url=next_page_url, callback=self.parse)


class BasicSpiderSulpak(scrapy.Spider):
    """
    Scrapy spider that scrapes data from www.sulpak.kz using XPATH
    """
    name = 'sulpak_tech'
    allowed_domains = ['www.sulpak.kz']
    start_urls = SULPAK_URLS
    store_name = 'SULPAK'

    def parse(self, response):
        products = response.xpath("//div[@class='goods-tiles']")
        for product in products:
            title = product.xpath(
                'normalize-space(.//descendant::h3/text())').get()
            price = product.xpath(
                ".//descendant::div[@class='price']/span/text()").get()
            if price:
                loader = ItemLoader(item=ScraperItem(), response=response)
                loader.default_output_processor = TakeFirst()
                decomp = response.url.split('/f')

                curr_date = datetime.now()
                loader.add_value('title', title)
                if isinstance(price, str):
                    loader.add_value('price', scrape_urls.strPriceToNum(price))
                elif isinstance(price, int):
                    loader.add_value('price', price)
                loader.add_value('category', decomp[1].split('/')[1])
                loader.add_value('storeName', self.store_name)
                loader.add_value('dateAndTime', curr_date)
                yield loader.load_item()

        next_page = response.xpath("//a[@class='next']/@href").get()
        next_page_url = f"https://www.sulpak.kz{next_page}"

        if next_page:
            yield scrapy.Request(url=next_page_url, callback=self.parse)


class SeleniumSpiderTechnodom(scrapy.Spider):
    """
    Scrapy spider that scrapes data from dynamic website www.technodom.kz using Selenium and geckodriver
    """
    name = 'technodom_tech'
    allowed_domains = ['www.technodom.kz']
    start_urls = TECHNODOM_URLS
    count = 0
    store_name = 'TECHNODOM'

    def parse(self, response):
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')

        # des_cap = options.to_capabilities()
        # driver = webdriver.Firefox(
        #     executable_path='./geckodriver', firefox_options=options)
        driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.FIREFOX)
        driver.get(response.url)
        driver.implicitly_wait(30)

        button = driver.find_element_by_xpath(
            "//div[@class='VerifyCityModal__Actions']/descendant::p[1]")
        webdriver.ActionChains(driver).move_to_element(
            button).click(button).perform()
        driver.implicitly_wait(10)
        element = WebDriverWait(
            driver,
            10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "//a[@class='CategoryPagination-Arrow CategoryPagination-Arrow_direction_next']")))

        html = driver.page_source
        resp = Selector(text=html)

        products = resp.xpath("//a[@class='ProductCard-Content']")
        category = resp.xpath("//h1/text()").get()
        for product in products:
            loader = ItemLoader(item=ScraperItem(), response=response)
            loader.default_output_processor = TakeFirst()
            title = product.xpath(".//h4/text()").get()
            price = product.xpath(".//descendant::data/text()").get()
            loader.add_value('title', title)
            if isinstance(price, str):
                loader.add_value('price', scrape_urls.strPriceToNum(price))
            elif isinstance(price, int):
                loader.add_value('price', price)
            loader.add_value('storeName', self.store_name)
            loader.add_value('dateAndTime', datetime.now())
            loader.add_value('category', response.url.split('/')[-1])
            yield loader.load_item()

        next_page = resp.xpath(
            "//a[@class='CategoryPagination-Arrow CategoryPagination-Arrow_direction_next']/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            driver.close()
            yield scrapy.Request(url=next_page_url, callback=self.parse)
        else:
            driver.close()
