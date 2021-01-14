import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


class TechnodomTechSpider(scrapy.Spider):
    name = 'technodom_tech'
    allowed_domains = ['www.technodom.kz']
    start_urls = [
        'https://www.technodom.kz/smartfony-i-gadzhety/smartfony-i-telefony/smartfony',
        'https://www.technodom.kz/noutbuki-i-komp-jutery/noutbuki-i-aksessuary/noutbuki',
        'https://www.technodom.kz/noutbuki-i-komp-jutery/komplektujuschie/processory',
        'https://www.technodom.kz/noutbuki-i-komp-jutery/komplektujuschie/videokarty'
    ]

    count = 0

    def parse(self, response):
        # print(f'\n-------------------------\n{response.url}\n-------------------------\n')
        # count = 0
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        des_cap = options.to_capabilities()
        driver = webdriver.Chrome(
            executable_path='./chromedriver', options=options)

        driver.get(response.url)
        # driver = response.meta['driver']
        driver.implicitly_wait(30)

        button = driver.find_element_by_xpath(
            "//div[@class='VerifyCityModal__Actions']/descendant::p[1]")
        webdriver.ActionChains(driver).move_to_element(
            button).click(button).perform()
        driver.implicitly_wait(10)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='CategoryPagination-Arrow CategoryPagination-Arrow_direction_next']")))

        html = driver.page_source
        resp = Selector(text=html)

        products = resp.xpath("//a[@class='ProductCard-Content']")
        category = resp.xpath("//h1/text()").get()
        for product in products:
            title = product.xpath(".//h4/text()").get()
            price = product.xpath(".//descendant::data/text()").get()
            yield {
                'category': category,
                'title': title,
                'price': price
            }

        next_page = resp.xpath(
            "//a[@class='CategoryPagination-Arrow CategoryPagination-Arrow_direction_next']/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            driver.close()
            yield scrapy.Request(url=next_page_url, callback=self.parse)
            # yield SeleniumRequest(
            #     url=next_page_url,
            #     wait_time=20,
            #     # encoding='utf-8',
            #     # wait_until=EC.presence_of_element_located((By.XPATH, "//div[@class='ContentWrapper CategoryPage-Wrapper']")),
            #     wait_until=EC.presence_of_element_located((By.XPATH, "//a[@class='ProductCard-Content']")),
            #     callback=self.parse
            # )
        else:
            driver.close()

