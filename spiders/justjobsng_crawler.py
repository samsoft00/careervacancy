# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from scrapy.selector import Selector

from career.items import CareerItem


class JustjobsngCrawlerSpider(CrawlSpider):
    name = 'justjobsng_crawler'
    allowed_domains = ['justjobsng.com']
    start_urls = ['http://www.justjobsng.com']

    rules = (
        Rule(LinkExtractor(allow=r'/page/1'), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        i = CareerItem()
        each_jobs = Selector(response).xpath('//div[@id="h_jobs1"]')

        log.msg(response)
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        yield i
