# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

import re

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



