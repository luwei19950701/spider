# -*- coding: utf-8 -*-
import scrapy
from pic.items import PicItem

class PicSpider(scrapy.Spider):
    name = 'pic'
    allowed_domains = ['www.58pic.com']
    start_urls = ['http://www.58pic.com/webui/']

    def parse(self, response):
        pic_item = PicItem()
        img_nodes = response.css('div.topic-list')
        pic_item['href'] = img_nodes.css('a::attr(href)').extract()
        pic_item['src'] = img_nodes.css('img::attr(src)').extract()
        pic_item['title'] = img_nodes.css('span::text').extract()
        yield pic_item
