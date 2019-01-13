# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import re

from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts']

    # 收集 伯乐在线 所以 404 的 url 以及 404 页面数
    # 不写这行代码 会自动过滤 404 页面
    handle_httpstatus_list = [404]

    def __init__(self):
        self.fail_urls = []
        # 将 定义的 函数 和 信号 绑定到一起
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        # 当 spider 结束 后 将 fail_urls 拼成 字符串 存到 stats 中
        self.crawler.stats.set_value('failed_urls', ','.join(self.fail_urls))


    def parse(self, response):
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value('failed_url')

        '''
        1. 获取文章列表页中 文章 url 并交给 scrapy 进行解析
        2. 获取下一页 url 交给 scrapy 进行处理
        '''

        # 获取文章列表页中 文章 url 并交给 scrapy 进行解析
        post_nodes = response.css('#archive .post-thumb a')
        for post_node in post_nodes:
            # 如果提取到的 href 不带域名
            # response.url + post_url 或用如下方法
            # yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": ''}, callback=self.parse_detail, dont_filter=True)
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")

            # urljoin 如果传的 url 没域名 会自动从 response 中获取 url 进行拼接  如果获取的 url 有域名 则直接保存
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail, dont_filter=True)


        # 获取下一页 url 交给 scrapy 进行处理
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()

        # 通过 css选择器 提取字段
        # title = response.css(".entry-header h1::text").extract()[0]
        # create_date = response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip().replace(' ·', '')
        # praise_nums = response.css(".vote-post-up h10::text").extract()[0]

        # fav_nums = response.css(".post-adds span:nth-child(2)::text").extract()[0]
        # match_re = re.match(r".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     # 如果没有匹配到数字 给一个默认值
        #     fav_nums = 0

        # comment_nums = response.css(".post-adds a span::text").extract_first()
        # match_re = re.match(r".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0

        # content = response.css(".hentry").extract()[0]

        # tag_list = response.css(".entry-meta-hide-on-mobile  a::text").extract()
        # tag_list = [ele for ele in tag_list if not ele.strip().endswith("评论")]
        # tags = ','.join(tag_list)

        # 获取图片信息
        # 取传入信息的默认值 防止未取到 设置默认 ‘’
        # 文章封面图
        # front_image_url = response.meta.get('front_image_url', '')

        # 此处下标从1开始
        # /html/body/div[1]/div[3]/div[1]/h1
        # // *[ @ id = "post-95521"] / div[1] / h1
        # re1_selector = response.xpath("/html/head/title")
        # re2_selector = response.xpath('//*[@id="post-95521"]/div[1]/h1')
        # re3_selector = response.xpath('//*[@class="entry-header"]/h1/text()')

        # 通过 xpath 提取字段
        # title = response.xpath('//*[@class="entry-header"]/h1/text()')
        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace(' ·', '')
        # praise_nums = response.xpath('//span[contains(@class, "vote-post-up")]/h10/text()').extract()[0]
        #
        # fav_nums = response.xpath('//span[contains(@class, "bookmark-btn")]/text()').extract()[0]
        # match_re = re.match(r".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        #
        # comment_nums = response.xpath('//a[contains(@href, "#article-comment")]/span/text()').extract()[0]
        # match_re = re.match(r".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = match_re.group(1)
        #
        # content = response.xpath('//div[contains(@class, "hentry")]').extract()[0]
        #
        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag_list = [ele for ele in tag_list if not ele.strip().endswith("评论")]
        # tag  = ','.join(tag_list)

        # article_item["title"] = title
        # article_item["url"] = response.url
        # article_item["url_object_id"] = get_md5(response.url)
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["praise_nums"] = praise_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["tags"] = tags
        # article_item["content"] = content
        # article_item["front_image_url"] = [front_image_url]

        # 通过 item_loader 加载 item 便于项目后期维护
        # 用 scrapy 提供的 loader
        # item_loader = ItemLoader(item=JobBoleArticleItem(), response=response)
        # 用自定义的 loader

        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_css('create_date', ".entry-meta-hide-on-mobile::text")
        item_loader.add_css('praise_nums', '.vote-post-up h10::text')
        item_loader.add_css('fav_nums', '.post-adds span:nth-child(2)::text')
        item_loader.add_css('comment_nums', '.post-adds a span::text')
        item_loader.add_css('tags', '.entry-meta-hide-on-mobile  a::text')
        item_loader.add_css('content', '.hentry')
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", response.meta.get('front_image_url', ''))
        # item_loader.add_xpath()

        # 默认取出的所有 item 对象都是一个 list
        article_item = item_loader.load_item()

        yield article_item
