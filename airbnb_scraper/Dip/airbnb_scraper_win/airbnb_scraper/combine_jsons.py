import json
import glob
import pandas
import numpy
from pathlib import Path 
import gender_guesser.detector as gender
d = gender.Detector()

#files = glob.glob(city+'/*.json')
'''
city = 'Miami_FL'
city = 'Dallas_TX'
city = 'Houston_TX'
city = 'Atlanta_GA'
city = 'Washington_DC'
city = 'Philadelphia_PA'
city = 'Boston_MA'
city = 'Phoenix_AZ'
city = 'Chicago_IL'
city = 'Denver_CO'
city = 'Seattle_WA'
city = 'San_Francisco_CA'
city = 'Tampa_FL'
city = 'New_York_NY'
city = 'Los_Angeles_CA'
city = 'Orlando_FL'
city = 'Fort_Lauderdale_FL'
city = 'San_Diego_CA'
city = 'Austin_TX'
city = 'Las_Vegas_NV'
city = 'Nashville_TN'
city = 'Palm_Springs_CA'
city = 'Jersey_City_NJ'
city = 'Panama_City_Beach_FL'
city = 'Salt_Lake_City_UT'
city = 'Kissimmee_FL'
city = 'Asheville_NC'
city = 'Scottsdale_AZ'
city = 'New_Orleans_LA'
city = 'San_Jose_CA'
city = 'Destin_FL'
city = 'Anaheim_CA'
city = 'Savannah_GA'
city = 'Portland_OR'
city = 'Honolulu_HI'
city = 'Charleston_SC'
city = 'Myrtle_Beach_SC'
city = 'Lake_Tahoe_CA'
'''


#city = 'Sarasota_FL'
city = 'Santa_Clarita_CA'




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

city_listings.to_csv(city+'/'+city+'_Combined_Listings.csv.gz', index = None, header=True, compression='gzip')
city_reviews.to_csv(city+'/'+city+'_Combined_Reviews.csv.gz', index = None, header=True, compression='gzip')

#city_listings.to_csv('Chicago_Combined_Listings.csv')
#city_reviews.to_csv('Chicago_Combined_Reviews.csv')
