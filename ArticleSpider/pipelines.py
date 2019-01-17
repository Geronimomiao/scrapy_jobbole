# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 此处主要是作数据存储
import codecs
import json
import MySQLdb
import MySQLdb.cursors

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

from ArticleSpider.models.es_types import ArticleType


# 定制自己的 pipelines 重载里面的方法
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for flag, value in results:
                # 这里你传进来时候就只有一张图片
                image_file_path = value['path']
            item["front_image_path"] = image_file_path
        # 因为还有下一个 pipeline 会对 item 进行处理
        return item


# 自定义 json 文件的导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        # codecs.open() 和 open() 区别 自动帮我们编码 省去了很多编码的繁杂工作
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 第二个参数 确保你能写入中文
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def sipder_closed(self, spider):
        self.file.close()



class JsonExporterPiple(object):
    # 调用 scrapy 提供的 jsonitemexporter 导出 json 文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def sipder_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticlespiderPipeline(object):
    # 此处数据处理的应该差不多了 此处应该将你的数据存到数据库
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self):
        # self.conn = MySQLdb.connect('host', 'user', 'password', 'dbname', charset='utf-8')
        self.conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='Geronimo1701', db='article_spider', use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    # 这里的插入是 同步的插入 可能会造成 插入的速度 小于 爬取的速度
    def process_item(self, item, spider):
        insert_sql = '''
            insert into article (title, url, create_date, fav_nums, url_object_id) values (%s, %s, %s ,%s, %s)
        '''
        list = [item["title"], item["url"], item["create_date"], item["fav_nums"], item["url_object_id"]]
        self.cursor.execute(insert_sql, list)
        self.conn.commit()
        return item


# 异步操作 mysql scrapy 框架提供的方法
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # scrapy 提供将 settings.py 值传进来
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            use_unicode=True,
            cursorclass = MySQLdb.cursors.DictCursor,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item

    def handle_error(self, failure):
        # 处理异步插入操作的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 具体插入逻辑
        insert_sql = '''
                    insert into article (title, url, create_date, fav_nums, url_object_id, tags, praise_nums, comment_nums, front_image_url, front_image_path) values (%s, %s, %s ,%s, %s, %s, %s, %s, %s, %s)
                '''
        list = [item["title"], item["url"], item["create_date"], item["fav_nums"], item["url_object_id"], item["tags"], item["praise_nums"], item["comment_nums"], item["front_image_url"][0], item["front_image_path"]]
        cursor.execute(insert_sql, list)
        # 此处无需 conn.commit scrapy 自动帮你提交了


class ElasticsearchPipeline(object):
    # 将数据写入到 es 中
    def process_item(self, item, spider):
        # 将item转化为es数据
        item.save_to_es()

        return item


