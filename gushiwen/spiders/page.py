# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider


class PageSpider(RedisCrawlSpider):
    name = 'page'
    allowed_domains = ['gushiwen.org']
    # redis_key = 'page_test'

    rules = [
        # follow all links
        Rule(
            LinkExtractor(restrict_css=('div.pagesright a.amore')),
            callback='parse_page',
            follow=True)
    ]

    custom_settings = {
        "ITEM_PIPELINES": {
            'gushiwen.pipelines.PagePipeline': 300
        },
    }

    def parse_page(self, response):
        return {
            'link':
                response.css('div.pagesright a.amore::attr(href)'
                            ).extract_first()
        }
