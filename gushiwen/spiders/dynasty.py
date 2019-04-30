# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
# from gushiwen.utils import write_for_debug


class DynastySpider(Spider):
    name = 'dynasty'
    start_urls = ['https://www.gushiwen.org/shiwen/']

    custom_settings = {
        "ITEM_PIPELINES": {
            'gushiwen.pipelines.DynastyPipeline': 300
        },
    }

    def parse(self, response):
        # write_for_debug('dynasty_debug.html', response.body)
        return {
            'dynasty_links':
                response.css('div#type3 div.sright a::attr(href)').extract()
        }
