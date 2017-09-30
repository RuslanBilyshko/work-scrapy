# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from workers.items import WorkerItem


class ResumeListSpider(scrapy.Spider):
    name = 'resumelist'
    allowed_domains = ['https://www.work.ua']
    start_urls = [
        'https://www.work.ua/resumes-python-программист/?page=1',
    ]

    # start_urls = ['https://www.work.ua/resumes/4286599/']

    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths="//a[text()='Следующая']"), follow=True, callback='parse_next'),
    # )

    def parse(self, response):
        # count = int(response.xpath('//nav/ul/li/a/text()').extract()[2])
        # pages = []

        # for p in range(2, count + 1):
        #     pages.append('https://www.work.ua/resumes-python-программист/?page={0}'.format(p))

        # print(pages)

        # for next_page in pages:
        #     yield response.follow(next_page, self.parse)

        next_page = response.xpath("//a[text()='Следующая']/@href").extract_first()

        # for next_page in response.xpath("//a[text()='Следующая']").extract_first():
        #     yield response.follow(next_page, self.parse)

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)



    def parse_next(self, response, next_page):
        yield response.follow(response, next_page)
