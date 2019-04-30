# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis
import MySQLdb
import json
from gushiwen.utils import join_url
from gushiwen import settings

rds = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


class DynastyPipeline(object):

    def process_item(self, item, spider):
        if 'dynasty_links' in item:
            for link in item['dynasty_links']:
                url = join_url(link)
                # print url
                rds.lpush('page:start_urls', url)
                rds.lpush('list:start_urls', url)

    pass


class PagePipeline(object):

    def process_item(self, item, spider):
        if 'link' in item:
            url = join_url(item['link'])
            # print url
            rds.lpush('list:start_urls', url)

    pass


class ListPipeline(object):

    def process_item(self, item, spider):
        if 'poem_urls' in item:
            for url in item['poem_urls']:
                # print url
                rds.lpush('poem:start_urls', url)

    pass


class PoemPipeline(object):

    def __init__(self):
        self.connect = MySQLdb.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True,
            port=settings.MYSQL_PORT)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # print item.keys()
        if item['poet_url'] is not None:
            rds.lpush('poet:start_urls', item['poet_url'])

        try:
            self.cursor.execute("""select * from poem where poem_name = %s""",
                                (item['poem_name'],))
            repetition = self.cursor.fetchone()

            if repetition:
                pass
            else:
                self.cursor.execute(
                    """insert into poem(poem_url, poem_name, poem_dynasty,
                        poem_content, poem_label, like_count, translation,
                            annotation, appreciation, poet_name, poet_bio,
                                poet_url) values
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                        item['poem_url'],
                        item['poem_name'],
                        item['poem_dynasty'],
                        item['poem_content'],
                        item['poem_label'],
                        item['like_count'],
                        item['translation'],
                        item['annotation'],
                        item['appreciation'],
                        item['poet_name'],
                        item['poet_bio'],
                        item['poet_url'],
                    ))
                self.connect.commit()
        except Exception as error:
            print 'PoemPipeline error:'
            print error

    def spider_closed(self, spider):
        self.cursor.close()
        self.connect.close()


class PoetPipeline(object):

    def __init__(self):
        self.connect = MySQLdb.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True,
            port=settings.MYSQL_PORT)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # print item.keys()
        try:
            self.cursor.execute("""select * from poet where poet_name = %s""",
                                (item['poet_name'],))

            repetition = self.cursor.fetchone()

            if repetition:
                pass
            else:
                self.cursor.execute(
                    """insert into poet(poet_url, poet_name, poet_bio, like_count, others)
                    values(%s, %s, %s, %s, %s)""", (
                        item['poet_url'],
                        item['poet_name'],
                        item['poet_bio'],
                        item['like_count'],
                        json.dumps(item['others'], ensure_ascii=False),
                    ))
                self.connect.commit()
        except Exception as error:
            print 'PoetPipeline error:'
            print error

    def spider_closed(self, spider):
        self.cursor.close()
        self.connect.close()
