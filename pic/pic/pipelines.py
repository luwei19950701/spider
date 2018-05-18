# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import codecs
import json
import pymysql as db


class PicPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['image_urls']

        yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


class WebcrawlerScrapyPipeline(object):
    # @classmethod
    # def from_settings(cls, settings):
    #     '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
    #        2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
    #        3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
    #     config = pymysql.connect(host=settings['MYSQL_HOST'],
    #                              port=settings['MYSQL_PORT'],
    #                              user=settings['MYSQL_USER'],
    #                              password=settings['MYSQL_PASSWD'],
    #                              db=settings['MYSQL_DBNAME'],
    #                              charset='utf8mb4',
    #                              cursorclass=pymysql.cursors.DictCursor)
    #     connection = pymysql.connect(**config)
    #     return cls(connection)  # 相当于dbpool付给了这个类，self中可以得到

    def __init__(self):
        self.con = db.connect(user="root", passwd="123456", host="localhost", db="test_db", charset="utf8")
        self.cur = self.con.cursor()
        self.cur.execute('drop table douban_books')
        self.cur.execute(
            "create table douban_books(id int auto_increment primary key,title varchar(200),image_urls VARCHAR(200),image_paths varchar(200))")

    def process_item(self, item, spider):
        self.cur.execute(
            "insert into douban_books(id,title,image_urls,image_paths) values(NULL,%s,%s,%s)",
            (item['title'], item['image_urls'], item['image_paths']))
        self.con.commit()
        return item


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('img_file.json', 'w', encoding='utf-8')  # open file

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False)  # write in file
        self.file.write(lines)
        return item

    def spider_closed(self):
        self.file.close()  # close file
