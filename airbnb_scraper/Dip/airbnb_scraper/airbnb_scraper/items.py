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
    url = scrapy.Field()
    listing_name = scrapy.Field(input_processor=MapCompose(remove_unicode))
    room_type_category = scrapy.Field()
    room_and_property_type = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    amt_w_service = scrapy.Field()
    rate_type = scrapy.Field()
    monthly_price_factor = scrapy.Field()
    weekly_price_factor = scrapy.Field()
    person_capacity = scrapy.Field()
    bathrooms = scrapy.Field()
    bedrooms = scrapy.Field()
    beds = scrapy.Field()
    min_nights = scrapy.Field()
    max_nights = scrapy.Field()
    can_instant_book = scrapy.Field()
    is_business_travel_ready = scrapy.Field()
    is_fully_refundable = scrapy.Field()
    is_new_listing = scrapy.Field()
    
# host info
    
    host_id = scrapy.Field()
    host_name = scrapy.Field()
    host_verified_card = scrapy.Field()
    host_badge = scrapy.Field()
    host_identity_verified = scrapy.Field()
    is_superhost = scrapy.Field()
    host_languages1 = scrapy.Field()
    host_languages2 = scrapy.Field()
    host_location = scrapy.Field()
    host_member_since = scrapy.Field()
    host_response_rate = scrapy.Field()
    host_response_time = scrapy.Field()
    additional_hosts = scrapy.Field()
    
# listing_details
    
    lat = scrapy.Field()
    lng = scrapy.Field()
    localized_city = scrapy.Field()
    localized_neighborhood = scrapy.Field()
    check_in_time = scrapy.Field()
    check_out_time = scrapy.Field()
    license = scrapy.Field()
    is_hotel = scrapy.Field()
    highlights = scrapy.Field(input_processor=MapCompose(remove_unicode))
    access_details = scrapy.Field(input_processor=MapCompose(remove_unicode))
    listing_description = scrapy.Field(input_processor=MapCompose(remove_unicode))
    house_rules = scrapy.Field(input_processor=MapCompose(remove_unicode))
    interaction_w_host = scrapy.Field(input_processor=MapCompose(remove_unicode))
    neighborhood_overview = scrapy.Field(input_processor=MapCompose(remove_unicode))
    notes_for_guests = scrapy.Field(input_processor=MapCompose(remove_unicode))
    space_description = scrapy.Field(input_processor=MapCompose(remove_unicode))
    description_summary = scrapy.Field(input_processor=MapCompose(remove_unicode))
    listing_transit = scrapy.Field()
    localized_language_name = scrapy.Field()
    
# rating info
    
    picture_count = scrapy.Field()
    reviews_count = scrapy.Field()
    star_rating = scrapy.Field()
    avg_rating = scrapy.Field()
    review_accuracy_percentage = scrapy.Field()
    review_accuracy_localized_rating = scrapy.Field()
    review_communication_percentage = scrapy.Field()
    review_communication_localized_rating = scrapy.Field()
    review_cleanliness_percentage = scrapy.Field()
    review_cleanliness_localized_rating = scrapy.Field()
    review_checkin_percentage = scrapy.Field()
    review_checkin_localized_rating = scrapy.Field()
    review_value_percentage = scrapy.Field()
    review_value_localized_rating = scrapy.Field()
    review_location_percentage = scrapy.Field()
    review_location_localized_rating = scrapy.Field()
    
# detailed review, calendar, cancellation
    
    reviewer_ratings = scrapy.Field()
    days_available_monthly = scrapy.Field()
    cancellation_policy_label = scrapy.Field()
    cancellation_policy_id = scrapy.Field()
    cancellation_policy_text = scrapy.Field(input_processor=MapCompose(remove_unicode))
    cancellation_policy_price_factor = scrapy.Field()


    
    
    
    



