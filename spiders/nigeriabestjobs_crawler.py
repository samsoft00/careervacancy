# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule, XMLFeedSpider
from scrapy import log

from career.items import CareerItem


class NigeriabestjobsCrawlerSpider(XMLFeedSpider):
    name = 'nigeriabestjobs_crawler'
    allowed_domains = ['nigeriabestjobs.com']
    start_urls = ['http://www.nigeriabestjobs.com/feed/?post_type=job_listing']
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'


    def parse_node(self, response, node) :
        # jobs = Selector(response).xpath('//div[@class="mycase"]')

        # for job in jobs :
        i = CareerItem()

        i['url'] = node.select('link/text()').extract()[0]
        i['title'] = node.select('title/text()').extract()[0]
        description = node.select('description/text()').extract()[0]
        i['category'] = 'others'#node.select('category/text()').extract()[0]
        i['description'] = description

        if description.title().find('Lagos') > -1:
        	i['location'] = 'Lagos'#node.xpath('category/text()').extract()[1]
        elif description.title().find('Abuja') > -1:
            i['location'] = 'Abuja'
        elif description.title().find('Oyo') > -1:
            i['location'] = 'Oyo'
        else:
            i['location'] = 'Nigeria'
        i['sponsor'] = 'nigeriabestjobs.com'

        log.msg(i)

        yield i;

