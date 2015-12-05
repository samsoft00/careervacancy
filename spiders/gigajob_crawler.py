# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from urlparse import urljoin

from scrapy import log

from career.items import CareerItem


class GigajobCrawlerSpider(CrawlSpider):
    name = 'gigajob_crawler'
    allowed_domains = ['ng.gigajob.com']
    start_urls = ['http://ng.gigajob.com/All-jobs-in-Nigeria']

    rules = (
        Rule(LinkExtractor(allow=r'\?page=[0-9]'), callback='parse_crawl_jobs', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_crawl_jobs(response)

    def parse_crawl_jobs(self, response):
        i = CareerItem()

        gigajobs = Selector(response).xpath('//div[@class="dTableC vAlignM"]')

        log.msg(gigajobs)

        for jobs in gigajobs :
            base_url = 'http://ng.gigajob.com'
            i['url'] = urljoin(base_url, str(jobs.xpath('h3/a/@href').extract()[0]))
            i['title'] = jobs.xpath('h3/a/span/text()').extract()[0]
            i['description'] = jobs.xpath('span[@itemprop="description"]/text()').extract()[0]
            i['category'] = jobs.xpath('address[@class="fBold fsm"]/span/span/span/text()').extract()[0]
            i['location'] = str(jobs.xpath('address[@class="fBold fsm"]/span/span/span/text()').extract()[1]).split(',')[0]

            log.msg(i)

            yield i
