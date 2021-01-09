# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from itemadapter import ItemAdapter


class ProductscraperPipeline:

    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'modigas'
        password = 'modigas'
        database = 'productsdb'
        self.connection = psycopg2.connect(
            host = hostname,
            user = username,
            password = password,
            dbname = database
        )
        self.cur = self.connection.cursor()
    
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute(
            '''
            insert into products_product(title,category,price,store)
            values(%s,%s,%s,%s)
            ''',
            (item.get('title'), item.get('category'), item.get('price'), item.get('store'))
            
            # (item['title'], item['category'], item['price'], item['store'])
        )
        self.connection.commit()
        item.save()
        return item
