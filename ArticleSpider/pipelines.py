# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 此处主要是作数据存储

from scrapy.pipelines.images import ImagesPipeline

# 定制自己的 pipelines 重载里面的方法
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for flag, value in results:
            # 这里你传进来时候就只有一张图片
            image_file_path = value['path']
        item["front_image_path"] = image_file_path
        # 因为还有下一个 pipeline 会对 item 进行处理
        return item


class ArticlespiderPipeline(object):
    # 此处数据处理的应该差不多了 此处应该将你的数据存到数据库
    def process_item(self, item, spider):
        return item

# 保存 json 文件
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
