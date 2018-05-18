# -*- coding: utf-8 -*-
import scrapy
import urlparse
from scrapy.http import Request
from pic.items import ArticleItem


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("#archive div.post")

        for post_node in post_nodes:

            post_url = post_node.css("div.post-thumb a::attr(href)").extract_first("")
            img_url = post_node.css("div.post-thumb img::attr(src)").extract_first("")

            yield Request(url=urlparse.urljoin(response.url, post_url),
                          meta={"front_image_url": img_url}, callback=self.parse_detail)
            next_url = response.css(".page-numbers:last-child::attr(href)").extract_first("")
            if next_url:
                yield Request(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        article_item = ArticleItem()
        title = response.css("div.entry-header h1::text").extract()
        img_url = response.meta.get('front_image_url', "")

        article_item['title'] = title
        article_item['image_urls'] = img_url
        yield article_item
