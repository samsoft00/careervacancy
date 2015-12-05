# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CareerItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
    sponsor = scrapy.Field()
    description = scrapy.Field()
    # pass
