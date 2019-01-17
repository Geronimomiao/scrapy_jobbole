# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     es_types
   Description :   将爬虫爬到的数据 存入es中
   Author :       wsm
   date：          2019-01-17
-------------------------------------------------
   Change Activity:
                   2019-01-17:
-------------------------------------------------
"""
__author__ = 'wsm'
from datetime import datetime
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text, Integer

class ArticleType(Document):
    # 伯乐在线文章类型
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    url_object_id = Keyword()
    praise_nums = Integer()
    fav_nums = Integer()
    comment_nums = Integer()
    tags = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")
    front_image_url = Keyword()
    front_image_path = Keyword()


if __name__ == '__main__':
    pass