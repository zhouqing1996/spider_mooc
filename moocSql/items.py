# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoocsqlItem(scrapy.Item):
    # id = scrapy.Field()
    courseName = scrapy.Field()
    courseName_English = scrapy.Field()
    schoolName = scrapy.Field()
    language = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
