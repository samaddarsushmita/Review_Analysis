# -*- coding: utf-8 -*-
import json
import collections
import re
import numpy as np
import logging
import sys
import scrapy
import time
#from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
from airbnb_scraper.items import AirbnbScraperItem
from pathlib import Path 
import csv
from csv import reader
import gzip




# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# *********************************************************************************************

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['www.airbnb.com']
    
    
    def __init__(self, start='',end='', *args,**kwargs):
        super(AirbnbSpider, self).__init__(*args, **kwargs)
        self.start = start
        self.end = end

        
    def start_requests(self):
        
        with gzip.open(Path.cwd() /'Review_Scrape_List.csv.gz', 'rt',"encoding = 'utf-8'") as read_obj:
            csv_reader = csv.reader(read_obj)
            home_list = list(csv_reader)
            
            for i in range(int(self.start),int(self.end)):
                
                
                review_url = 'https://www.airbnb.com/api/v2/homes_pdp_reviews?&currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&listing_id='+str(home_list[i][0])+'&_format=for_p3&limit='+str(home_list[i][1])+'&offset=0&order=language_country'
                
                listing = AirbnbScraperItem()

                listing['listing_id'] = str(home_list[i][0])
                listing['reviews_count'] = home_list[i][1]

                yield scrapy.Request(url=review_url, callback=self.parse_reviews,meta=listing) 
                
                
    def parse_reviews(self, response):
        
        
        listing = AirbnbScraperItem()

        listing['listing_id'] = str(response.meta['listing_id'])
        listing['reviews_count'] = response.meta['reviews_count']
        
        
        data = json.loads(response.body)
        
        review_count = data.get('metadata').get('reviews_count')
        
        #print('Parse Review function:', review_count, listing['reviews_count'])
        
        if(review_count > int(listing['reviews_count'])):
            listing['reviews_count'] = str(review_count)
            
            review_url = 'https://www.airbnb.com/api/v2/homes_pdp_reviews?&currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&listing_id='+str(listing['listing_id'])+'&_format=for_p3&limit='+str(review_count)+'&offset=0&order=language_country'
            
            yield scrapy.Request(url=review_url, callback=self.parse_reviews,meta=listing) 
            
        listing['reviews_count'] = review_count
        
        all_reviews = data.get('reviews')

        review_list = []
        for review in all_reviews:
            
            review_dict = collections.defaultdict(dict)
            
            review_dict['review_id']  = review.get('id')
            review_dict['review_rating']  = review.get('rating')
            raw_comment = review.get('comments')
            review_dict['review_comments']  = bytes(raw_comment, 'utf-8').decode('unicode_escape')
            review_dict['review_language']  = review.get('language')
            review_dict['review_created_at']  = review.get('created_at')
            review_dict['host_response']  = review.get('response')

            review_dict['reviewee_deleted'] = review.get('reviewee').get('deleted')
            review_dict['reviewee_first_name'] = review.get('reviewee').get('first_name')
            review_dict['reviewee_host_name'] = review.get('reviewee').get('host_name')
            review_dict['reviewee_id'] = review.get('reviewee').get('id')
            review_dict['reviewee_is_superhost'] = review.get('reviewee').get('is_superhost')
            
            review_dict['reviewer_deleted'] = review.get('reviewer').get('deleted')
            review_dict['reviewer_first_name'] = review.get('reviewer').get('first_name')
            review_dict['reviewer_host_name'] = review.get('reviewer').get('host_name')
            review_dict['reviewer_id'] = review.get('reviewer').get('id')
            review_dict['reviewer_is_superhost'] = review.get('reviewer').get('is_superhost')
            
            review_list.append(review_dict)
            
        listing['reviewer_ratings'] = review_list
        
        #src = Path(r'D:\Airbnb\Raw_Jsons')
        src = Path.cwd() / 'Review_Jsons'
        filename = str(listing['listing_id'])+'_Reviews.json'
        with open(src / filename, 'wb') as f:
            f.write(response.body)
            
        yield listing
        