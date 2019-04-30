# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy_splash import SplashRequest
import sys
from gushiwen.utils import load_script, extract_text

reload(sys)
sys.setdefaultencoding('UTF-8')


class PoetSpider(RedisSpider):
    name = 'poet'
    allowed_domains = ['so.gushiwen.org']
    # redis_key = 'poet_test' # just for debug

    custom_settings = {
        'ITEM_PIPELINES': {
            'gushiwen.pipelines.PoetPipeline': 300
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
                'lua_source': load_script('gushiwen/lua/poet.lua'),
                'wait': '0.15'
            },
            cache_args=['lua_source'])

    def parse_result(self, response):
        result = {}
        keys = [
            'poet_name',
            'poet_url',
            'poet_bio',
            'like_count',
        ]
        for key in keys:
            result[key] = ''
        result['others'] = []
        result['poet_url'] = response.url

        poet_name = response.css(
            'div.sonspic div.cont h1 span b::text').extract_first().strip()
        # print poet_name
        result['poet_name'] = poet_name

        poet_bio = response.css(
            'div.sonspic div.cont p::text').extract_first().strip()
        # print poet_bio
        result['poet_bio'] = poet_bio

        like_count = response.css(
            'div.left div.sonspic div.tool div.good a span::text'
        ).extract_first().strip()
        # print like_count
        result['like_count'] = like_count

        for i, div in enumerate(response.css('div.sons div.contyishang')):
            if (i % 2 != 0):
                title = div.css('div h2 span::text').extract_first().strip()
                desc = extract_text(''.join(div.css('p').extract()))
                # print 'title : ' + title
                # print 'desc : ' + desc
                result['others'].append({'title': title, 'desc': desc})
        # print result['others']

        return result
