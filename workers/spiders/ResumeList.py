# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from workers.items import ResumeListItem


class ResumeListSpider(scrapy.Spider):
    name = 'resumelist'
    allowed_domains = ['https://www.work.ua']
    start_urls = [
        'https://www.work.ua/resumes-python-программист/?page=1',
    ]

    rules = (
        Rule(LinkExtractor(allow=('page=\d+$',)), follow=True),
    )

    def parse(self, response):
        # Неправильно извлекалось
        # hxs = Selector(response=response)
        # all = hxs.css('div.resume-link')

        # Так правильно извлекается, но мне кажеться както не пофеншую
        # и не соответствует примерам из докуменации
        all_text_list = response.css('div.resume-link').extract()
        all = [Selector(text=x) for x in all_text_list]

        for field in all:
            name = field.xpath('//div/b/text()').extract_first()
            Item = ResumeListItem()
            Item['name'] = name
            # print(name)
            yield Item
