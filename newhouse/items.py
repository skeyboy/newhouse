# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewhouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index = scrapy.Field()
    href = scrapy.Field()


class AreaModelItem(NewhouseItem):
    index = scrapy.Field()
    area = scrapy.Field()


class RailModelItem(NewhouseItem):
    rail = scrapy.Field()

class StationModelItem(NewhouseItem):
    href = scrapy.Field()
    station = scrapy.Field()


class HouseModelItem(NewhouseItem):

    name = scrapy.Field()
    img = scrapy.Field()
    price = scrapy.Field()
    em = scrapy.Field()
    state = scrapy.Field()
    kind = scrapy.Field()
    address = scrapy.Field()
    value_num = scrapy.Field()
    tel = scrapy.Field()
    href =  scrapy.Field()
    image_urls = scrapy.Field()

class HouseDetailModelItem(scrapy.Item):
    href = scrapy.Field()
    info = scrapy.Field()
    ping = scrapy.Field()
    stag = scrapy.Field()
    total_price = scrapy.Field()


