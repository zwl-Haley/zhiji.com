# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhijiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    address = scrapy.Field()
    user_id = scrapy.Field()
    images = scrapy.Field()
    sex = scrapy.Field()
    age = scrapy.Field()
    income = scrapy.Field()
    introduction = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    education = scrapy.Field()
    marriage = scrapy.Field()
    qq = scrapy.Field()
    head_img = scrapy.Field()
    weixin_num = scrapy.Field()

    # member = scrapy.Field()