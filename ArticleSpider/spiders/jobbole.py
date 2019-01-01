# -*- coding: utf-8 -*-
import scrapy
import re

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://web.jobbole.com/94127/']

    def parse(self, response):
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


        # 通过 css选择器 提取字段
        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip().replace(' ·', '')
        praise_nums = response.css(".vote-post-up h10::text").extract()[0]

        fav_nums = response.css(".post-adds span:nth-child(2)::text").extract()[0]
        match_re = re.match(r".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)

        comment_nums = response.css(".post-adds a span::text").extract_first()
        match_re = re.match(r".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)

        content = response.css(".hentry").extract()[0]

        tag_list = response.css(".entry-meta-hide-on-mobile  a::text").extract()
        tag_list = [ele for ele in tag_list if not ele.strip().endswith("评论")]
        tag = ','.join(tag_list)

        pass
