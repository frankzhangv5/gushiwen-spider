# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisSpider
from scrapy_splash import SplashRequest
import sys
import json
from gushiwen.utils import load_script, extract_text, eat_header_and_extract

reload(sys)
sys.setdefaultencoding('UTF-8')


class PoemSpider(RedisSpider):
    name = 'poem'
    allowed_domains = ['so.gushiwen.org']
    # redis_key = 'poem_test' # just for debug

    custom_settings = {
        'ITEM_PIPELINES': {
            'gushiwen.pipelines.PoemPipeline': 300
        },
        'SPLASH_URL': 'http://localhost:8050',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware':
                723,
            'scrapy_splash.SplashMiddleware':
                725,
            'scrapy.downloadermiddlewares.httpcompression.\
                HttpCompressionMiddleware':
                810
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        # 'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter'
    }

    def make_requests_from_url(self, url):
        return SplashRequest(
            url,
            self.parse_result,
            endpoint='execute',
            args={
                'lua_source': load_script('gushiwen/lua/poem.lua'),
                'wait': '0.15'
            },
            headers={'X-My-Header': 'value'},
            cache_args=['lua_source'])

    def parse_result(self, response):
        result = {}
        dict = json.loads(response.body)

        keys = [
            'poem_url', 'poem_name', 'poem_dynasty', 'poem_content',
            'like_count', 'poem_label', 'poet_name', 'translation',
            'annotation', 'appreciation', 'poet_url', 'poet_bio'
        ]
        for key in keys:
            result[key] = ''

        result['poem_url'] = response.url

        if 'translation' in dict:
            translation = extract_text(dict['translation'])
            # print translation
            result['translation'] = translation

        if 'annotation' in dict:
            annotation = extract_text(dict['annotation'])
            # print annotation
            result['annotation'] = annotation

        if 'appreciation' in dict:
            appreciation = eat_header_and_extract(dict['appreciation'])
            # print appreciation
            result['appreciation'] = appreciation

        if 'poem' in dict:
            poem_sel = Selector(text=dict['poem'])
            poem_name = poem_sel.css(
                'div.cont h1::text').extract_first().strip()
            poem_dynasty = poem_sel.xpath(
                '//div[@class="cont"]/p[@class="source"]/a[1]/text()'
            ).extract_first().strip()
            poet_name = poem_sel.xpath(
                '//div[@class="cont"]/p[@class="source"]/a[2]/text()'
            ).extract_first().strip()
            poem_content = poem_sel.xpath(
                '//div[@class="cont"]/div[@class="contson"]').extract_first()
            poem_content = extract_text(poem_content)
            like_count = poem_sel.xpath(
                '//div[@class="tool"]/div[@class="good"]/a/span/text()'
            ).extract_first().strip()
            poem_labels = poem_sel.xpath(
                '//div[@class="tag"]/a/text()').extract()
            label = ','.join(poem_labels)

            # print poem_name + '|' + poem_dynasty + '|' + poet_name + '|'
            # + poem_content + '|' + like_count + '|' + label
            result['poem_name'] = poem_name
            result['poem_dynasty'] = poem_dynasty
            result['poet_name'] = poet_name
            result['poem_content'] = poem_content
            result['like_count'] = like_count
            result['poem_label'] = label

        if 'poet' in dict:
            poet_sel = Selector(text=dict['poet'])
            poet_name = poet_sel.xpath(
                                    '//div[@class="cont"]/p[1]/a[1]/b/text()'
                                      ).extract_first().strip()
            poet_url = 'https://so.gushiwen.org' + poet_sel.xpath(
                '//div[@class="cont"]/p[1]/a[1]/@href').extract_first().strip()
            poet_bio = poet_sel.xpath(
                '//div[@class="cont"]/p[2]/text()').extract_first().strip()

            # print poet_name + '|' + poet_url + '|' + poet_bio
            result['poet_name'] = poet_name
            result['poet_url'] = poet_url
            result['poet_bio'] = poet_bio

        return result
