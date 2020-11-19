# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3

class UkbookingsPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("bookings.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute(""" DROP TABLE IF EXISTS books_tb""")
        self.curr.execute("""create table books_tb(
                        Hotel_Name text,
                        Ratings text,
                        Hotels_reviews text,
                        image_link text
                         )""")

    def process_item(self, item, spider):
        self.store_db(item)
        print("Pipeline:" + item['hotel_name'][0])
        return item

    def store_db(self,item):
        self.curr.execute("""insert into books_tb values (?,?,?,?),"""(
            item['hotel_name'][0],
            item['hotel_rating'][0],
            item['hotel_review'][0],
            item['hotel_imagelink'][0]
        ))
        self.conn.commit()