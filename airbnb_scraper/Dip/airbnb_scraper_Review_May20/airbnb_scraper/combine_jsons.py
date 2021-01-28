import json
import glob
import pandas
import numpy
from pathlib import Path 
import gender_guesser.detector as gender
d = gender.Detector()

dest = Path.cwd() / 'Combined_Jsons' / 'Combined_Reviews_Zero.csv.gz' # !!change everyday

src = Path.cwd() / 'Scraped_Listings_2'
files = src.glob('*.json')

reviews_day = pandas.DataFrame()

# day refers to the day in scrape_list.py goes b/w 0-7

for file in files:
    print(file)
    listing_count = 0
    with open(file) as json_file:
        listings = json.load(json_file)
        if(len(listings) == 0):
            continue
        for listing in listings:
            review_df = pandas.json_normalize(listing,'reviewer_ratings',['listing_id','reviews_count'])
            reviews_day = reviews_day.append(review_df, sort=True)
            listing_count = listing_count + 1
            
    print('Listing Count = ', listing_count)
    

cols = ['listing_id', 'reviews_count', 'reviewee_deleted', 'reviewee_first_name', 'reviewee_host_name', 'reviewee_id','reviewee_is_superhost', 'review_id', 'review_created_at', 'review_language', 'review_rating', 'review_comments', 'host_response', 'reviewer_deleted', 'reviewer_first_name', 'reviewer_host_name', 'reviewer_id', 'reviewer_is_superhost']

reviews_day = reviews_day[cols]
    
reviews_day.to_csv(dest, index = None, header=True, compression='gzip')
