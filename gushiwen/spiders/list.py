# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
# from gushiwen.utils import write_for_debug


class ListSpider(RedisSpider):
    name = 'list'
    allowed_domains = ['gushiwen.org']
    # redis_key = 'list_test' # just for debug

    custom_settings = {
        "ITEM_PIPELINES": {
            'gushiwen.pipelines.ListPipeline': 300
        },
    }

    def parse(self, response):
        # write_for_debug('list_debug.html', response.body)
        poem_urls = []

        for div in response.css('div.main3 div.left div.sons div.cont'):
            url = div.css('p a::attr(href)').extract_first()
            print url
            poem_urls.append(url)

        return {'poem_urls': poem_urls}
