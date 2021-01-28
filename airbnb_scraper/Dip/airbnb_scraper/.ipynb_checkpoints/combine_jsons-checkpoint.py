import json
import glob
import pandas
import numpy
from pathlib import Path 
import gender_guesser.detector as gender
d = gender.Detector()


#files = glob.glob(city+'/*.json')

city = 'Miami_FL'
src = Path.cwd() / city
files = src.glob('*.json')

#files = Path.cwd().glob('*.json')
#city = 'Chicago_IL'

city_listings = pandas.DataFrame()
city_reviews = pandas.DataFrame()

listing_list = []

for file in files:
    print(file)
    listing_count = 0
    with open(file) as json_file:
        listings = json.load(json_file)
        if(len(listings) == 0):
            continue
        for listing in listings:
            additional_hosts = []
            for host in listing.get('additional_hosts'):
                additional_hosts.append(host.get('host_name'))
            listing['additional_hosts'] = additional_hosts
            review_df = pandas.io.json.json_normalize(listing,'reviewer_ratings',['localized_city','listing_id','reviews_count'])
            city_reviews = city_reviews.append(review_df, sort=True)
            listing.pop('reviewer_ratings')
            listing_list.append(listing)
            listing_count = listing_count + 1
            
    print('Listing Count = ', listing_count)
    
city_listings = pandas.DataFrame(listing_list)

city_listings['search_location'] = city
city_listings['host_name_has_space'] = numpy.where(city_listings['host_name'].str.contains(' ') , 1, 0)
city_listings['host_gender'] = city_listings['host_name'].apply(d.get_gender, 'usa')
city_listings.loc[city_listings['host_name_has_space'] == 1, 'host_gender'] = 'not_a_name'

city_reviews['search_location'] = city
city_reviews['reviewer_name_has_space'] = numpy.where(city_reviews['reviewer_name'].str.contains(' ') , 1, 0)
city_reviews['reviewer_gender'] = city_reviews['reviewer_name'].apply(d.get_gender, 'usa')
city_reviews.loc[city_reviews['reviewer_name_has_space'] == 1, 'reviewer_gender'] = 'not_a_name'

city_listings.to_csv(city+'/'+city+'_Combined_Listings.csv')
city_reviews.to_csv(city+'/'+city+'_Combined_Reviews.csv')

#city_listings.to_csv('Chicago_Combined_Listings.csv')
#city_reviews.to_csv('Chicago_Combined_Reviews.csv')
