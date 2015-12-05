# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import log
from urlparse import urljoin

from FlaskApp.items import CareerItem


class Career24CrawlerSpider(CrawlSpider):
    name = 'career24_crawler'
    allowed_domains = ['careers24.com.ng']
    start_urls = ['http://www.careers24.com.ng/jobs/']

    rules = (
        Rule(LinkExtractor(allow=r'\?page=[0-9]'), callback='parse_crawl_jobs', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_crawl_jobs(response)

    def parse_crawl_jobs(self, response):
        i = CareerItem()
        job_categories = Selector(response).xpath('//div[@class="row job_search_wrapper"]')

        for category_link in job_categories :
            # self.category_name = str(category_link).split('/')[-2]
            # log.msg(category_link, log.INFO)

            base_url = 'http://www.careers24.com.ng'
            ext_url = str(category_link.xpath('div[@class="span6 job_search_content"]/h4/a/@href').extract()[0])
            main_url = urljoin(base_url, ext_url)

            i['url'] = main_url
            i['title'] = category_link.xpath('div[@class="span6 job_search_content"]/h4/a/text()').extract()[0]
            i['description'] = category_link.xpath('div[@class="span8 job_search_content job_search_summary"]/p/text()').extract()[0]
            i['category'] = category_link.xpath('div[@class="span6 job_search_content"]/p/text()').extract()[1]
            i['location'] = category_link.xpath('div[@class="span6 job_search_content"]/p/text()').extract()[0]
            i['sponsor'] = 'careers24.com.ng'
            # log.msg(i, log.INFO) 

            yield i


    def parse_item(self, response):
        i = CareerItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
