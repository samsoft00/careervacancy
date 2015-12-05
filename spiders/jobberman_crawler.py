# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
import logging

from items import CareerItem
from utility import Utility

logging.basicConfig(filename='game.log', level=logging.DEBUG)

class JobbermanCrawlerSpider(CrawlSpider):
    name = 'jobberman_crawler'
    allowed_domains = ['jobberman.com']
    start_urls = ['http://www.jobberman.com/jobs-in-nigeria/?keywords=&job_level=']

    rules = (
        Rule(LinkExtractor(allow=r'\?page=(?:\b|-)([0-9]{1}|100)\b'), callback='parse_item', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        utility = Utility()
        jobs_link = Selector(response).xpath('//div[@class=" search-results clearfix"]')

        category = jobs_link.xpath('//p[@class="job-category"]/a/text()').extract()
        location = jobs_link.xpath('//p[@class="job-locatn"]/text()').extract()
        link = jobs_link.xpath('//div[@class="search-details-top-left"]/p[1]/a/@href').extract()

        for category, location, link1 in zip(category, location, link):#jobs_link:
            self.category = category#each_link.xpath('//p[@class="job-category"]/a/text()').extract()
            self.location = location#each_link.xpath('//p[@class="job-locatn"]/text()').extract()

            #Incase of list index out of range
            #try:
            #    link = each_link.xpath('//div[@class="search-details-top-left"]/p[1]/a/@href').extract()
            #except IndexError:
            #    link = each_link.xpath('//div[@class="search-details-top-left"]/p[1]/a/@href').extract()

            #if utility.convert_unicode_to_string(link).find('job-cities') != -1:
               # yield scrapy.http.Request(link, callback=self.parse_item)

            #check if url contain job-cities, class parse_item
            #logging.info(link1)

            yield scrapy.http.Request(link1, callback=self.parse_Jobberman)


    def parse_Jobberman(self, response):
        i = CareerItem()
        utility = Utility()

        i['url'] = response.url
        logging.info(response.url)
        try:
        	i['title'] = response.xpath('//div[@class="job-quick-sum"]/h1/text()').extract()[0]
        except IndexError:
        	i['title'] = response.xpath('//div[@class="job-quick-sum"]/h1/text()').extract()
        
        try:
        	description = response.xpath('//div[@class="job-details-main"]/p[2]/text()').extract()[0]
        except IndexError:
        	description = response.xpath('//div[@class="job-details-main"]/p[2]/text()').extract()
        
        i['description'] = utility.limit_length_of_string(description)#(description[:150] + '...') if len(description) > 150 else description
        i['category'] = utility.stringReplace(self.category, '/', ',')
        i['location'] = self.location #str(self.location).replace('/', ',')

        # try:
        # 	i['location'] = response.xpath('//div[@class="job-details-sidebar"]/p[7]/a/text()').extract()[0]
        # except IndexError:
        # 	i['location'] = response.xpath('//div[@class="job-details-sidebar"]/p[7]/a/text()').extract()

        # try:
        # 	i['category'] = str(response.xpath('//div[@class="job-details-sidebar"]/p[9]/a/text()').extract()[0]).replace('/', ',')
        # except IndexError:
        # 	i['category'] = str(response.xpath('//div[@class="job-details-sidebar"]/p[9]/a/text()').extract()).replace('/', ',')Onye

        i['sponsor'] = 'jobberman.com'
        #log.msg(i)
        yield i