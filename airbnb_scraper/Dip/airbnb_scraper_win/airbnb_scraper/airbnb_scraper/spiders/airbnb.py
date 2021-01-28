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



# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# *********************************************************************************************

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['www.airbnb.com']

    '''
    You don't have to override __init__ each time and can simply use self.parameter (See https://bit.ly/2Wxbkd9),
    but I find this way much more readable.
    '''
    
    def __init__(self, city='',price_lb='', price_ub='', *args,**kwargs):
        super(AirbnbSpider, self).__init__(*args, **kwargs)
        self.city = city
        self.price_lb = price_lb
        self.price_ub = price_ub

        
    def start_requests(self):
        
        '''Sends a scrapy request to the designated url price range

        Args:
        Returns:
        '''

        url = ('https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=false&currency=USD&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&items_per_grid=100&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&metadata_only=false'
              '&query={2}'            '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_version=1.2.6&search_type=section_navigation&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&timezone_offset=-240&version=1.7.0'                  
              '&price_min={0}&price_max={1}')
        new_url = url.format(self.price_lb, self.price_ub, self.city)
        
        if (int(self.price_lb)  >= 2500):
            #print('**********Above 2500*************')
            url = ('https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=false&currency=USD&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&items_per_grid=100&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&metadata_only=false'
              '&query={1}'         '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_version=1.2.6&search_type=section_navigation&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&timezone_offset=-240&version=1.7.0'                  
              '&price_min={0}')
            new_url = url.format(self.price_lb, self.city)

        yield scrapy.Request(url=new_url, callback=self.parse_id)
        
        
    def parse_id(self, response):
        
        '''Parses all the URLs/ids/available fields from the initial json object and stores into dictionary

        Args:
            response: Json object from explore_tabs
        Returns:
        '''
        
        # Fetch and Write the response data
        data = json.loads(response.body)

        # Return a List of all homes
        '''
        homes = data.get('explore_tabs')[0].get('sections')[0].get('listings')

        if homes is None:
            try: 
                homes = data.get('explore_tabs')[0].get('sections')[3].get('listings')
            except IndexError:
                try: 
                    homes = data.get('explore_tabs')[0].get('sections')[2].get('listings')
                except IndexError:
                    try: 
                        homes = data.get('explore_tabs')[0].get('sections')[1].get('listings')
                    except:
                        raise CloseSpider("No homes available in the city and price parameters")
		
        homes0 = data.get('explore_tabs')[0].get('sections')[0].get('listings')
        try: 
            homes1 = data.get('explore_tabs')[0].get('sections')[1].get('listings')
        except IndexError:
            homes1 = None
        try: 
            homes2 = data.get('explore_tabs')[0].get('sections')[2].get('listings')
        except IndexError:
            homes2 = None
        try: 
            homes3 = data.get('explore_tabs')[0].get('sections')[3].get('listings')
        except IndexError:
            homes3 = None
        
        homes = []
        
        if homes0 is not None:
            homes.extend(homes0)
        if homes1 is not None:
            homes.extend(homes1)
        if homes2 is not None:
            homes.extend(homes2)
        if homes3 is not None:
            homes.extend(homes3)
        if not homes:
                raise CloseSpider("No homes available in the city and price parameters")
		'''		
		
        homes = []
        sections = data.get('explore_tabs')[0].get('sections')
        for section in sections:
            section_homes = section.get('listings')
            if section_homes is not None:
                homes.extend(section_homes)
            	
        if not homes:
            raise CloseSpider("No homes available in the city and price parameters")
				
        base_url = 'https://www.airbnb.com/rooms/'
        data_dict = collections.defaultdict(dict) # Create Dictionary to put all currently available fields in

        for home in homes:
            room_id = str(home.get('listing').get('id'))
            url = base_url + str(home.get('listing').get('id'))
            #print('\n','*****     ',url,'     *****','\n')
            data_dict[room_id]['listing_id'] = room_id
            data_dict[room_id]['url'] = url
            data_dict[room_id]['price'] = home.get('pricing_quote').get('rate').get('amount')
            data_dict[room_id]['bathrooms'] = home.get('listing').get('bathrooms')
            data_dict[room_id]['bedrooms'] = home.get('listing').get('bedrooms')
            data_dict[room_id]['beds'] = home.get('listing').get('beds')
            data_dict[room_id]['host_languages1'] = home.get('listing').get('host_languages')
            data_dict[room_id]['is_business_travel_ready'] = home.get('listing').get('is_business_travel_ready')
            data_dict[room_id]['is_fully_refundable'] = home.get('listing').get('is_fully_refundable')
            data_dict[room_id]['is_new_listing'] = home.get('listing').get('is_new_listing')
            data_dict[room_id]['is_superhost'] = home.get('listing').get('is_superhost')
            data_dict[room_id]['lat'] = home.get('listing').get('lat')
            data_dict[room_id]['lng'] = home.get('listing').get('lng')
            data_dict[room_id]['localized_city'] = home.get('listing').get('localized_city')
            data_dict[room_id]['localized_neighborhood'] = home.get('listing').get('localized_neighborhood')
            data_dict[room_id]['listing_name'] = home.get('listing').get('name')
            data_dict[room_id]['person_capacity'] = home.get('listing').get('person_capacity')
            data_dict[room_id]['picture_count'] = home.get('listing').get('picture_count')
            data_dict[room_id]['reviews_count'] = home.get('listing').get('reviews_count')
            data_dict[room_id]['room_and_property_type'] = home.get('listing').get('room_and_property_type')
            data_dict[room_id]['star_rating'] = home.get('listing').get('star_rating')
            data_dict[room_id]['host_id'] = home.get('listing').get('user').get('id')
            data_dict[room_id]['avg_rating'] = home.get('listing').get('avg_rating')
            data_dict[room_id]['min_nights'] = home.get('listing').get('min_nights')
            data_dict[room_id]['max_nights'] = home.get('listing').get('max_nights')
            data_dict[room_id]['can_instant_book'] = home.get('pricing_quote').get('can_instant_book')
            data_dict[room_id]['monthly_price_factor'] = home.get('pricing_quote').get('monthly_price_factor')
            data_dict[room_id]['currency'] = home.get('pricing_quote').get('rate').get('currency')
            data_dict[room_id]['amt_w_service'] = home.get('pricing_quote').get('rate_with_service_fee').get('amount')
            data_dict[room_id]['rate_type'] = home.get('pricing_quote').get('rate_type')
            data_dict[room_id]['weekly_price_factor'] = home.get('pricing_quote').get('weekly_price_factor')
            data_dict[room_id]['host_verified_card'] = home.get('verified_card')
            if(home.get('verified_card')):
                data_dict[room_id]['host_badge'] = home.get('verified').get('badge_text')
            else:
                data_dict[room_id]['host_badge'] = ''
            


        # Iterate through dictionary of URLs in the single page to send a SplashRequest for each

        for room_id in data_dict:
            
            #pdp_url = 'https://www.airbnb.com/api/v2/pdp_listing_details/'+room_id+'?_format=for_rooms_show&_p3_impression_id=p3_1579795793_XqREBl3FbiNMjzS7&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&'
            
            pdp_url = 'https://www.airbnb.com/api/v2/pdp_listing_details/'+room_id+'?_format=for_rooms_show&currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20'
            #time.sleep(1)
            
            yield scrapy.Request(url=pdp_url, callback=self.parse_pdp,meta=data_dict.get(room_id))
		
                
		#After scraping entire listings page, check if more pages
        
        pagination_metadata = data.get('explore_tabs')[0].get('pagination_metadata')
        if pagination_metadata.get('has_next_page'):

            items_offset = pagination_metadata.get('items_offset')
            section_offset = pagination_metadata.get('section_offset')

            new_url = ('https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=false&currency=USD&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&items_per_grid=100&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&metadata_only=false'
                      '&query={4}' '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_version=1.2.6&search_type=section_navigation&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&timezone_offset=-240&version=1.7.0'
                      '&items_offset={0}&section_offset={1}&price_min={2}&price_max={3}')
            
            new_url = new_url.format(items_offset, section_offset, self.price_lb, self.price_ub, self.city)
            
            if (int(self.price_lb) >= 2500):
                #print('**********Above 2500*************')
                url = ('https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=false&currency=USD&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&items_per_grid=100&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&metadata_only=false'
                      '&query={3}' '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_version=1.2.6&search_type=section_navigation&selected_tab_id=home_tab&show_groupings=true&source=mc_search_bar&supports_for_you_v3=true&timezone_offset=-240&version=1.7.0'
                      '&items_offset={0}&section_offset={1}&price_min={2}')
            
                new_url = url.format(items_offset, section_offset, self.price_lb, self.city)
            
            # If there is a next page, update url and scrape from next page
            time.sleep(5)
            yield scrapy.Request(url=new_url, callback=self.parse_id)  
        
    def parse_pdp(self, response):
        
        # New Instance
        listing = AirbnbScraperItem()

        # Fill in fields for Instance from initial scrapy call
        listing['listing_id'] = str(response.meta['listing_id'])
        listing['url'] = response.meta['url']
        listing['room_and_property_type'] = response.meta['room_and_property_type']
        listing['listing_name'] = response.meta['listing_name']
        listing['price'] = response.meta['price']
        listing['currency'] = response.meta['currency']
        listing['amt_w_service'] = response.meta['amt_w_service']
        listing['rate_type'] = response.meta['rate_type']
        listing['person_capacity'] = response.meta['person_capacity']
        listing['bathrooms'] = response.meta['bathrooms']
        listing['bedrooms'] = response.meta['bedrooms']
        listing['beds'] = response.meta['beds']
        listing['lat'] = response.meta['lat']
        listing['lng'] = response.meta['lng']
        listing['localized_city'] = response.meta['localized_city']
        listing['localized_neighborhood'] = response.meta['localized_neighborhood']
        listing['picture_count'] = response.meta['picture_count']
        listing['reviews_count'] = response.meta['reviews_count']
        listing['star_rating'] = response.meta['star_rating']
        listing['avg_rating'] = response.meta['avg_rating']
        listing['min_nights'] = response.meta['min_nights']
        listing['max_nights'] = response.meta['max_nights']
        listing['can_instant_book'] = response.meta['can_instant_book']
        listing['is_business_travel_ready'] = response.meta['is_business_travel_ready']
        listing['is_fully_refundable'] = response.meta['is_fully_refundable']
        listing['is_new_listing'] = response.meta['is_new_listing']
        listing['monthly_price_factor'] = response.meta['monthly_price_factor']
        listing['weekly_price_factor'] = response.meta['weekly_price_factor']
        listing['host_id'] = str(response.meta['host_id'])
        listing['host_verified_card'] = response.meta['host_verified_card']
        listing['is_superhost'] = response.meta['is_superhost']
        listing['host_languages1'] = response.meta['host_languages1']
        listing['host_badge'] = response.meta['host_badge']
        
        # HOST INFORMATION & RATINGS
  

        #src = Path.cwd() / 'Raw_Jsons'
        #src = Path(r'D:\Airbnb\Raw_Jsons')
        src = Path(r'C:\\Users\soudi\Dropbox\Raw_Jsons')
        filename = str(listing['listing_id'])+'_Details.json'
        with open(src / filename, 'wb') as f:
            f.write(response.body)
        
        
        data = json.loads(response.body)
        
        # lat and lng are duplicates
        
        listing['host_id'] = data.get('pdp_listing_detail').get('primary_host').get('id')
        listing['host_name'] = data.get('pdp_listing_detail').get('primary_host').get('host_name')
        listing['host_identity_verified'] = data.get('pdp_listing_detail').get('primary_host').get('identity_verified')
        listing['host_languages2'] = data.get('pdp_listing_detail').get('primary_host').get('languages_as_string')
        listing['host_location'] = data.get('pdp_listing_detail').get('primary_host').get('location_long')
        listing['host_member_since'] = data.get('pdp_listing_detail').get('primary_host').get('member_since')
        listing['host_response_rate'] = data.get('pdp_listing_detail').get('primary_host').get('response_rate_without_na')
        listing['host_response_time'] = data.get('pdp_listing_detail').get('primary_host').get('response_time_without_na')
        
        #listing['min_nights'] = data.get('pdp_listing_detail').get('min_nights')
        listing['additional_hosts'] = data.get('pdp_listing_detail').get('additional_hosts')
        listing['room_type_category'] = data.get('pdp_listing_detail').get('room_type_category')
        listing['lat'] = data.get('pdp_listing_detail').get('lat')
        listing['lng'] = data.get('pdp_listing_detail').get('lng')
        
        listing['check_in_time'] = data.get('pdp_listing_detail').get('localized_check_in_time_window')
        listing['check_out_time'] = data.get('pdp_listing_detail').get('localized_check_out_time')
        listing['is_hotel'] = data.get('pdp_listing_detail').get('is_hotel')
        listing['license'] = data.get('pdp_listing_detail').get('license')

        listing['access_details'] = data.get('pdp_listing_detail').get('sectioned_description').get('access')
        listing['listing_description'] = data.get('pdp_listing_detail').get('sectioned_description').get('description')
        listing['house_rules'] = data.get('pdp_listing_detail').get('sectioned_description').get('house_rules')
        listing['interaction_w_host'] = data.get('pdp_listing_detail').get('sectioned_description').get('interaction')
        listing['neighborhood_overview'] = data.get('pdp_listing_detail').get('sectioned_description').get('neighborhood_overview')
        listing['notes_for_guests'] = data.get('pdp_listing_detail').get('sectioned_description').get('notes')
        listing['space_description'] = data.get('pdp_listing_detail').get('sectioned_description').get('space')
        listing['description_summary'] = data.get('pdp_listing_detail').get('sectioned_description').get('summary')
        listing['listing_transit'] = data.get('pdp_listing_detail').get('sectioned_description').get('transit')
        listing['localized_language_name'] = data.get('pdp_listing_detail').get('sectioned_description').get('localized_language_name')
                        
        try:
            features =  data.get('pdp_listing_detail').get('highlights')
            highlight = ''
            for feature in features:
                highlight = highlight + feature.get('message') + ' '
            listing['highlights'] = highlight.strip()
        except:
            listing['highlights'] = ''
        
        try: 
            listing['review_accuracy_percentage'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[0].get('percentage')
            listing['review_accuracy_localized_rating'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[0].get('localized_rating')
        except IndexError:
            listing['review_accuracy_percentage'] = -1
            listing['review_accuracy_localized_rating'] = -1
        try:
            listing['review_communication_percentage'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[1].get('percentage')
            listing['review_communication_localized_rating'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[1].get('localized_rating')
        except IndexError:
            listing['review_communication_percentage'] = -1
            listing['review_communication_localized_rating'] = -1
        try:
            listing['review_cleanliness_percentage'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[2].get('percentage')
            listing['review_cleanliness_localized_rating'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[2].get('localized_rating')
        except IndexError:
            listing['review_cleanliness_percentage'] = -1
            listing['review_cleanliness_localized_rating'] = -1
        try:
            listing['review_location_percentage'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[3].get('percentage')
            listing['review_location_localized_rating'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[3].get('localized_rating')
        except IndexError:
            listing['review_location_percentage'] = -1
            listing['review_location_localized_rating'] = -1
        try:
            listing['review_checkin_percentage'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[4].get('percentage')
            listing['review_checkin_localized_rating'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[4].get('localized_rating')
        except IndexError:
            listing['review_checkin_percentage'] = -1
            listing['review_checkin_localized_rating'] = -1
        try:
            listing['review_value_percentage'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[5].get('percentage')
            listing['review_value_localized_rating'] = data.get('pdp_listing_detail').get('review_details_interface').get('review_summary')[5].get('localized_rating')
        except IndexError:
            listing['review_value_percentage'] = -1
            listing['review_value_localized_rating']  = -1
        
        review_url = 'https://www.airbnb.com/api/v2/homes_pdp_reviews?&currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&listing_id='+str(listing['listing_id'])+'&_format=for_p3&limit='+str(listing['reviews_count'])+'&offset=0&order=language_country'
        #time.sleep(10)
        yield scrapy.Request(url=review_url, callback=self.parse_reviews,meta=listing)
        
  

    def parse_reviews(self, response):
        
        listing = AirbnbScraperItem()
                
        listing['listing_id'] = str(response.meta['listing_id'])
        listing['url'] = response.meta['url']
        listing['listing_name'] = response.meta['listing_name']
        listing['room_type_category'] = response.meta['room_type_category']
        listing['room_and_property_type'] = response.meta['room_and_property_type']
        listing['price'] = response.meta['price']
        listing['currency'] = response.meta['currency']
        listing['amt_w_service'] = response.meta['amt_w_service']
        listing['rate_type'] = response.meta['rate_type']
        listing['monthly_price_factor'] = response.meta['monthly_price_factor']
        listing['weekly_price_factor'] = response.meta['weekly_price_factor']
        listing['person_capacity'] = response.meta['person_capacity']
        listing['bathrooms'] = response.meta['bathrooms']
        listing['bedrooms'] = response.meta['bedrooms']
        listing['beds'] = response.meta['beds']
        listing['min_nights'] = response.meta['min_nights']
        listing['max_nights'] = response.meta['max_nights']
        listing['can_instant_book'] = response.meta['can_instant_book']
        listing['is_business_travel_ready'] = response.meta['is_business_travel_ready']
        listing['is_fully_refundable'] = response.meta['is_fully_refundable']
        listing['is_new_listing'] = response.meta['is_new_listing']

        # host info
       
        listing['host_id'] = str(response.meta['host_id'])
        listing['host_name'] = response.meta['host_name']
        listing['host_verified_card'] = response.meta['host_verified_card']
        listing['host_badge'] = response.meta['host_badge']
        listing['host_identity_verified'] = response.meta['host_identity_verified']  
        listing['is_superhost'] = response.meta['is_superhost']
        listing['host_languages1'] = response.meta['host_languages1']
        listing['host_languages2'] = response.meta['host_languages2']
        listing['host_location'] = response.meta['host_location']
        listing['host_member_since'] = response.meta['host_member_since']
        listing['host_response_rate'] = response.meta['host_response_rate']
        listing['host_response_time'] = response.meta['host_response_time']
        listing['additional_hosts'] = response.meta['additional_hosts']
        
        #listing_details
        
        listing['lat'] = response.meta['lat']
        listing['lng'] = response.meta['lng']
        listing['localized_city'] = response.meta['localized_city']
        listing['localized_neighborhood'] = response.meta['localized_neighborhood']
        listing['check_in_time'] = response.meta['check_in_time']
        listing['check_out_time'] = response.meta['check_out_time']
        listing['license'] = response.meta['license']
        listing['is_hotel'] = response.meta['is_hotel'] 
        listing['highlights'] = response.meta['highlights']
        listing['access_details'] = response.meta['access_details']
        listing['listing_description'] = response.meta['listing_description'] 
        listing['house_rules'] = response.meta['house_rules']
        listing['interaction_w_host'] = response.meta['interaction_w_host']
        listing['neighborhood_overview'] = response.meta['neighborhood_overview']
        listing['notes_for_guests'] = response.meta['notes_for_guests']
        listing['space_description'] = response.meta['space_description'] 
        listing['description_summary'] = response.meta['description_summary']
        listing['listing_transit'] = response.meta['listing_transit']
        listing['localized_language_name'] = response.meta['localized_language_name']

        #rating info
        
        listing['picture_count'] = response.meta['picture_count']
        listing['reviews_count'] = response.meta['reviews_count']
        listing['star_rating'] = response.meta['star_rating']
        listing['avg_rating'] = response.meta['avg_rating']
        listing['review_accuracy_percentage'] = response.meta['review_accuracy_percentage']
        listing['review_accuracy_localized_rating'] = response.meta['review_accuracy_localized_rating']
        listing['review_communication_percentage'] = response.meta['review_communication_percentage']
        listing['review_communication_localized_rating'] = response.meta['review_communication_localized_rating'] 
        listing['review_cleanliness_percentage'] = response.meta['review_cleanliness_percentage']
        listing['review_cleanliness_localized_rating'] = response.meta['review_cleanliness_localized_rating'] 
        listing['review_checkin_percentage'] = response.meta['review_checkin_percentage']
        listing['review_checkin_localized_rating'] = response.meta['review_checkin_localized_rating'] 
        listing['review_value_percentage'] = response.meta['review_value_percentage']
        listing['review_value_localized_rating'] = response.meta['review_value_localized_rating'] 
        listing['review_location_percentage'] = response.meta['review_location_percentage']
        listing['review_location_localized_rating'] = response.meta['review_location_localized_rating']
        
        data = json.loads(response.body)
        
        all_reviews = data.get('reviews')

        review_list = []
        for review in all_reviews:
            review_dict = collections.defaultdict(dict)
            review_dict['reviewer_name'] = review.get('reviewer').get('first_name')
            review_dict['review_rating']  = review.get('rating')
            raw_comment = review.get('comments')
            review_dict['review_comments']  = bytes(raw_comment, 'utf-8').decode('unicode_escape')
            review_dict['review_language']  = review.get('language')
            review_dict['review_created_at']  = review.get('created_at')
            review_list.append(review_dict)
            
        listing['reviewer_ratings'] = review_list
        
        calendar_url = 'https://www.airbnb.com/api/v2/homes_pdp_availability_calendar?&currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&listing_id='+str(listing['listing_id'])+'&month=3&year=2020&count=12'
        #time.sleep(10)
        yield scrapy.Request(url=calendar_url, callback=self.parse_calendar,meta=listing)
        
  

    def parse_calendar(self, response):
        
        listing = AirbnbScraperItem()
        
        listing['listing_id'] = str(response.meta['listing_id'])
        listing['url'] = response.meta['url']
        listing['listing_name'] = response.meta['listing_name']
        listing['room_type_category'] = response.meta['room_type_category']
        listing['room_and_property_type'] = response.meta['room_and_property_type']
        listing['price'] = response.meta['price']
        listing['currency'] = response.meta['currency']
        listing['amt_w_service'] = response.meta['amt_w_service']
        listing['rate_type'] = response.meta['rate_type']
        listing['monthly_price_factor'] = response.meta['monthly_price_factor']
        listing['weekly_price_factor'] = response.meta['weekly_price_factor']
        listing['person_capacity'] = response.meta['person_capacity']
        listing['bathrooms'] = response.meta['bathrooms']
        listing['bedrooms'] = response.meta['bedrooms']
        listing['beds'] = response.meta['beds']
        listing['min_nights'] = response.meta['min_nights']
        listing['max_nights'] = response.meta['max_nights']
        listing['can_instant_book'] = response.meta['can_instant_book']
        listing['is_business_travel_ready'] = response.meta['is_business_travel_ready']
        listing['is_fully_refundable'] = response.meta['is_fully_refundable']
        listing['is_new_listing'] = response.meta['is_new_listing']

        # host info
       
        listing['host_id'] = str(response.meta['host_id'])
        listing['host_name'] = response.meta['host_name']
        listing['host_verified_card'] = response.meta['host_verified_card']
        listing['host_badge'] = response.meta['host_badge']
        listing['host_identity_verified'] = response.meta['host_identity_verified']  
        listing['is_superhost'] = response.meta['is_superhost']
        listing['host_languages1'] = response.meta['host_languages1']
        listing['host_languages2'] = response.meta['host_languages2']
        listing['host_location'] = response.meta['host_location']
        listing['host_member_since'] = response.meta['host_member_since']
        listing['host_response_rate'] = response.meta['host_response_rate']
        listing['host_response_time'] = response.meta['host_response_time']
        listing['additional_hosts'] = response.meta['additional_hosts']
        
        #listing_details
        
        listing['lat'] = response.meta['lat']
        listing['lng'] = response.meta['lng']
        listing['localized_city'] = response.meta['localized_city']
        listing['localized_neighborhood'] = response.meta['localized_neighborhood']
        listing['check_in_time'] = response.meta['check_in_time']
        listing['check_out_time'] = response.meta['check_out_time']
        listing['license'] = response.meta['license']
        listing['is_hotel'] = response.meta['is_hotel'] 
        listing['highlights'] = response.meta['highlights']
        listing['access_details'] = response.meta['access_details']
        listing['listing_description'] = response.meta['listing_description'] 
        listing['house_rules'] = response.meta['house_rules']
        listing['interaction_w_host'] = response.meta['interaction_w_host']
        listing['neighborhood_overview'] = response.meta['neighborhood_overview']
        listing['notes_for_guests'] = response.meta['notes_for_guests']
        listing['space_description'] = response.meta['space_description'] 
        listing['description_summary'] = response.meta['description_summary']
        listing['listing_transit'] = response.meta['listing_transit']
        listing['localized_language_name'] = response.meta['localized_language_name']

        #rating info
        
        listing['picture_count'] = response.meta['picture_count']
        listing['reviews_count'] = response.meta['reviews_count']
        listing['star_rating'] = response.meta['star_rating']
        listing['avg_rating'] = response.meta['avg_rating']
        listing['review_accuracy_percentage'] = response.meta['review_accuracy_percentage']
        listing['review_accuracy_localized_rating'] = response.meta['review_accuracy_localized_rating']
        listing['review_communication_percentage'] = response.meta['review_communication_percentage']
        listing['review_communication_localized_rating'] = response.meta['review_communication_localized_rating'] 
        listing['review_cleanliness_percentage'] = response.meta['review_cleanliness_percentage']
        listing['review_cleanliness_localized_rating'] = response.meta['review_cleanliness_localized_rating'] 
        listing['review_checkin_percentage'] = response.meta['review_checkin_percentage']
        listing['review_checkin_localized_rating'] = response.meta['review_checkin_localized_rating'] 
        listing['review_value_percentage'] = response.meta['review_value_percentage']
        listing['review_value_localized_rating'] = response.meta['review_value_localized_rating'] 
        listing['review_location_percentage'] = response.meta['review_location_percentage']
        listing['review_location_localized_rating'] = response.meta['review_location_localized_rating']
        
        listing['reviewer_ratings'] = response.meta['reviewer_ratings']
        
        data = json.loads(response.body)
        
        calendar_yr = data.get('calendar_months')

        available = []

        for month in calendar_yr:
            day_count = 0

            for day in month.get('days'):
                if(day.get('available')):
                    day_count = day_count + 1

            available.append(day_count)
        
        listing['days_available_monthly'] = available
        
        cancel_policy_url = 'https://www.airbnb.com/api/v2/pdp_listing_booking_details?_format=for_web_dateless&currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id='+str(listing['listing_id'])
        #time.sleep(10)
        yield scrapy.Request(url=cancel_policy_url, callback=self.parse_cancel_policy,meta=listing)
        
        
        
    def parse_cancel_policy(self, response):
        
        listing = AirbnbScraperItem()
        
        listing['listing_id'] = str(response.meta['listing_id'])
        listing['url'] = response.meta['url']
        listing['listing_name'] = response.meta['listing_name']
        listing['room_type_category'] = response.meta['room_type_category']
        listing['room_and_property_type'] = response.meta['room_and_property_type']
        listing['price'] = response.meta['price']
        listing['currency'] = response.meta['currency']
        listing['amt_w_service'] = response.meta['amt_w_service']
        listing['rate_type'] = response.meta['rate_type']
        listing['monthly_price_factor'] = response.meta['monthly_price_factor']
        listing['weekly_price_factor'] = response.meta['weekly_price_factor']
        listing['person_capacity'] = response.meta['person_capacity']
        listing['bathrooms'] = response.meta['bathrooms']
        listing['bedrooms'] = response.meta['bedrooms']
        listing['beds'] = response.meta['beds']
        listing['min_nights'] = response.meta['min_nights']
        listing['max_nights'] = response.meta['max_nights']
        listing['can_instant_book'] = response.meta['can_instant_book']
        listing['is_business_travel_ready'] = response.meta['is_business_travel_ready']
        listing['is_fully_refundable'] = response.meta['is_fully_refundable']
        listing['is_new_listing'] = response.meta['is_new_listing']

        # host info
       
        listing['host_id'] = str(response.meta['host_id'])
        listing['host_name'] = response.meta['host_name']
        listing['host_verified_card'] = response.meta['host_verified_card']
        listing['host_badge'] = response.meta['host_badge']
        listing['host_identity_verified'] = response.meta['host_identity_verified']  
        listing['is_superhost'] = response.meta['is_superhost']
        listing['host_languages1'] = response.meta['host_languages1']
        listing['host_languages2'] = response.meta['host_languages2']
        listing['host_location'] = response.meta['host_location']
        listing['host_member_since'] = response.meta['host_member_since']
        listing['host_response_rate'] = response.meta['host_response_rate']
        listing['host_response_time'] = response.meta['host_response_time']
        listing['additional_hosts'] = response.meta['additional_hosts']
        
        #listing_details
        
        listing['lat'] = response.meta['lat']
        listing['lng'] = response.meta['lng']
        listing['localized_city'] = response.meta['localized_city']
        listing['localized_neighborhood'] = response.meta['localized_neighborhood']
        listing['check_in_time'] = response.meta['check_in_time']
        listing['check_out_time'] = response.meta['check_out_time']
        listing['license'] = response.meta['license']
        listing['is_hotel'] = response.meta['is_hotel'] 
        listing['highlights'] = response.meta['highlights']
        listing['access_details'] = response.meta['access_details']
        listing['listing_description'] = response.meta['listing_description'] 
        listing['house_rules'] = response.meta['house_rules']
        listing['interaction_w_host'] = response.meta['interaction_w_host']
        listing['neighborhood_overview'] = response.meta['neighborhood_overview']
        listing['notes_for_guests'] = response.meta['notes_for_guests']
        listing['space_description'] = response.meta['space_description'] 
        listing['description_summary'] = response.meta['description_summary']
        listing['listing_transit'] = response.meta['listing_transit']
        listing['localized_language_name'] = response.meta['localized_language_name']

        #rating info
        
        listing['picture_count'] = response.meta['picture_count']
        listing['reviews_count'] = response.meta['reviews_count']
        listing['star_rating'] = response.meta['star_rating']
        listing['avg_rating'] = response.meta['avg_rating']
        listing['review_accuracy_percentage'] = response.meta['review_accuracy_percentage']
        listing['review_accuracy_localized_rating'] = response.meta['review_accuracy_localized_rating']
        listing['review_communication_percentage'] = response.meta['review_communication_percentage']
        listing['review_communication_localized_rating'] = response.meta['review_communication_localized_rating'] 
        listing['review_cleanliness_percentage'] = response.meta['review_cleanliness_percentage']
        listing['review_cleanliness_localized_rating'] = response.meta['review_cleanliness_localized_rating'] 
        listing['review_checkin_percentage'] = response.meta['review_checkin_percentage']
        listing['review_checkin_localized_rating'] = response.meta['review_checkin_localized_rating'] 
        listing['review_value_percentage'] = response.meta['review_value_percentage']
        listing['review_value_localized_rating'] = response.meta['review_value_localized_rating'] 
        listing['review_location_percentage'] = response.meta['review_location_percentage']
        listing['review_location_localized_rating'] = response.meta['review_location_localized_rating']
        
        listing['reviewer_ratings'] = response.meta['reviewer_ratings']
        listing['days_available_monthly'] = response.meta['days_available_monthly']
        
        
        #src = Path.cwd() / 'Raw_Jsons'
        
        #src = Path(r'D:\Airbnb\Raw_Jsons')
        src = Path(r'C:\\Users\soudi\Dropbox\Raw_Jsons')
        filename = str(listing['listing_id'])+'_Cancellation_Policy.json'
        with open(src / filename, 'wb') as f:
            f.write(response.body)

        
        data = json.loads(response.body)
        
        try:
        
            listing['cancellation_policy_label'] = data.get('pdp_listing_booking_details')[0].get('cancellation_policy_label')

            cancel_policy_text = data.get('pdp_listing_booking_details')[0].get('p3_cancellation_section').get('title')+'.'
            subtitles = data.get('pdp_listing_booking_details')[0].get('p3_cancellation_section').get('subtitles')

            for subtitle in subtitles:
                cancel_policy_text = cancel_policy_text + ' '+ subtitle

            listing['cancellation_policy_id'] = data.get('pdp_listing_booking_details')[0].get('p3_cancellation_section').get('cancellation_policy_id')
            listing['cancellation_policy_text'] = cancel_policy_text
            listing['cancellation_policy_price_factor'] = data.get('pdp_listing_booking_details')[0].get('p3_cancellation_section').get('cancellation_policy_price_factor')
            
        except:
            try:
                listing['cancellation_policy_label'] = data.get('pdp_listing_booking_details')[1].get('cancellation_policy_label')

                cancel_policy_text = data.get('pdp_listing_booking_details')[1].get('p3_cancellation_section').get('title')+'.'
                subtitles = data.get('pdp_listing_booking_details')[1].get('p3_cancellation_section').get('subtitles')

                for subtitle in subtitles:
                    cancel_policy_text = cancel_policy_text + ' '+ subtitle

                listing['cancellation_policy_id'] = data.get('pdp_listing_booking_details')[1].get('p3_cancellation_section').get('cancellation_policy_id')
                listing['cancellation_policy_text'] = cancel_policy_text
                listing['cancellation_policy_price_factor'] = data.get('pdp_listing_booking_details')[1].get('p3_cancellation_section').get('cancellation_policy_price_factor')
            except:
                listing['cancellation_policy_label'] =''
                listing['cancellation_policy_id']=''
                listing['cancellation_policy_text']=''
                listing['cancellation_policy_price_factor']=''
                
        
        # Finally return the object
        yield listing

        