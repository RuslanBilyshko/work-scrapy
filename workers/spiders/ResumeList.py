# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from workers.items import ResumeItem


class ResumeListSpider(scrapy.Spider):
    name = 'resumelist'
    # allowed_domains = ['www.work.ua']
    start_urls = [
        'https://www.work.ua/resumes-python-программист/?page=1',
    ]

    # rules = (
    #     Rule(LinkExtractor(allow='https://www.work.ua/resumes-python-программист/?page=*'), follow=True),
    #     Rule(LinkExtractor(allow='https://www.work.ua/resumes/*'), callback='parse_item'),
    # )

    def parse(self, response):
        resume_links = response.css('div.resume-link > h2 > a::attr(href)').extract()

        for link in resume_links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_item,
                dont_filter=True
            )

        next_page = response.xpath("//a[text()='Следующая']/@href").extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def parse_item(self, response):
        name = response.css('h1.cut-top::text').extract_first()

        if name != "Личные данные скрыты":
            Item = ResumeItem()

            url = response.url
            Item["id"] = url.split("/")[-2]
            Item['url'] = url
            Item['name'] = name

            data = response.css('.card-indent').extract_first()
            Item['data'] = ' '.join(data.split())

            yield Item