# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

import re

from ArticleSpider.models.es_types import ArticleType


# 定义一些对字段处理的方法
def get_nums(value):
    match_re = re.match(r".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

def get_date(value):
    date = value.strip().replace(' ·', '')
    return date

def remove_comment_tags(value):
    # 去掉 tag 中提取掉评论
    if '评论,' in value:
        return ''
    else:
        return value

def return_value(value):
    return value

from elasticsearch_dsl.connections import connections
es = connections.create_connection(ArticleType._doc_type.using)

def gen_suggest(index, info_tuple):
    # 根据字符串 生成搜索建议 数组
    # 去重
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es中 analyze接口 分析字符串
            words = es.indices.analyze(index=index, analyzer='ik_max_word', params={'filter':["lowercase"]}, body=text)
            # 关键词 为一个字的 并无卵用
            analyzed_words = set([r["token"] for r in words['tokens'] if len(r["token"])>1])
            new_words = analyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})
    return suggests

# 定义字段的类 及 对字段处理的类
class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    # 自定义 itemLoader
    # output_processor 对要输出字段做处理
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    # scrapy.Field() 说明字段类型 Field means 任何类型
    # input_processor  对获取的字段进行预处理  MapCompose() 可以传处理的函数
    # output_processor = TakeFirst() 取第一个 输出的字段
    # 默认传进来 list 输出也是 list
    title = scrapy.Field()
    create_date = scrapy.Field(input_processor=MapCompose(get_date))
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    praise_nums = scrapy.Field()
    fav_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    comment_nums = scrapy.Field(input_processor=MapCompose(get_nums))
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(',')
    )
    content = scrapy.Field()
    # 此处 front_image_url 应为 list 否则 scrapy 图片下载器会抛异常
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    # 记录存放的本地路径
    front_image_path = scrapy.Field()

    def save_to_es(self):
        article = ArticleType()
        article.title = self['title']
        article.content = self["content"]
        article.front_image_url = self["front_image_url"]
        if "front_image_path" in self:
            article.front_image_path = self["front_image_path"]
        article.praise_nums = self["praise_nums"]
        article.fav_nums = self["fav_nums"]
        article.comment_nums = self["comment_nums"]
        article.url = self["url"]
        article.tags = remove_comment_tags(self["tags"])
        article.meta.id = self["url_object_id"]

        article.suggest = gen_suggest(ArticleType._doc_type.index, ((article.title, 10), (article.tags, 7)))
        article.save()

        return


