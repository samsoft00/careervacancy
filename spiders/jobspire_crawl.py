# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import log

import urllib

from career.items import CareerItem


class JobspireCrawlSpider(CrawlSpider):
    name = 'jobspire_crawl'
    allowed_domains = ['jobspire.com.ng']
    start_urls = ['http://www.jobspire.com.ng/job,vacancy-0,1,0.html']

    rules = (
        Rule(LinkExtractor(allow=r'/job,vacancy-[0-d+]0,1,0.html'), callback='parse_crawl_jobs', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_crawl_jobs(response)    

    def parse_crawl_jobs(self, response):
        i = CareerItem()

        #jobspire = Selector(text=response.body, type="html").xpath('//div[@class="boxsearch"]/div')
        log.msg(response.body)
        yield i


