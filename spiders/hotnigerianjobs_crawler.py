 # -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule, XMLFeedSpider
from scrapy.selector import Selector
from scrapy import log

from FlaskApp.items import CareerItem

class HotnigerianjobsCrawlerSpider(XMLFeedSpider):
    name = 'hotnigerianjobs_crawler'
    allowed_domains = ['hotnigerianjobs.com']
    start_urls = ['http://www.hotnigerianjobs.com/feed/rss.xml']

    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'    

    # rules = (
    #     Rule(LinkExtractor(allow=r'/Item'), callback='parse_item', follow=True),
    # )

    def __init__(self) :
        self.category_name = ''

    # def parse_start_url(self, response):
    #     return self.parse_crawl_jobs(response)


    # def parse_crawl_jobs(self, response):

    #     job_categories = Selector(response).xpath('//div[@class="cat_show"]/a/@href').extract()

    #     for category_link in job_categories :
    #         self.category_name = str(category_link).split('/')[-2]
    #         yield scrapy.http.Request(category_link, callback=self.parse_Jobs)


    def parse_node(self, response, node) :
        # jobs = Selector(response).xpath('//div[@class="mycase"]')

        # for job in jobs :
        i = CareerItem()

        i['url'] = node.select('link/text()').extract()[0]
        i['title'] = node.select('title/text()').extract()[0]
        i['description'] = node.select('description/text()').extract()[0]
        i['category'] = node.select('category/text()').extract()[0]
        i['location'] = node.xpath('category/text()').extract()[1]
        i['sponsor'] = 'hotnigerianjobs.com'

        log.msg(i)

        yield i;
