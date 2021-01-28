# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def remove_unicode(value):
    #return value.replace(u"\u201c", '').replace(u"\u201d", '').replace(u"\2764", '').replace(u"\ufe0f").replace('\n', '')
    return bytes(value, 'utf-8').decode('unicode_escape')

class AirbnbScraperItem(scrapy.Item):
    
    listing_id = scrapy.Field()
    reviews_count = scrapy.Field()
    reviewer_ratings = scrapy.Field()
    

    
    
    
    



