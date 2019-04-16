# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebsiteScanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GenecopoeiaaScanItem(scrapy.Item):
    url = scrapy.Field()
    code = scrapy.Field()
    response_url = scrapy.Field()