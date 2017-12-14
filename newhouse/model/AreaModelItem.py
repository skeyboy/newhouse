import scrapy

class AreaModelItem(scrapy.Item):
    area = scrapy.Field()
    href = scrapy.Field()
