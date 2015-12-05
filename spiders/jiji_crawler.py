# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import log

from bs4 import BeautifulSoup
import urllib

from career.items import CareerItem


class JijiCrawlerSpider(CrawlSpider):
    name = 'jiji_crawler'
    allowed_domains = ['jiji.ng']
    start_urls = ['http://jiji.ng/accounting-and-finance-jobs']

    rules = (
        Rule(LinkExtractor(allow=r'page[0-9]'), callback='parse_crawl_jobs', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_crawl_jobs(response)
        #yield scrapy.http.Request(response.url ,meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}, callback=self.parse_crawl_jobs)

    def parse_crawl_jobs(self, response):
        i = CareerItem()
        #html = urllib.urlopen('http://jiji.ng/jobs')
        #get_html = html.read()
        #bs = BeautifulSoup(get_html, 'html.parser')

        jobber = Selector(response).xpath('//div[@class="b-list-advert__item "]')

        for job in jobber :
        	log.msg(job)

        	yield i