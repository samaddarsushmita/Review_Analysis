import glob
import pandas as pd
from pathlib import Path 


#src = Path(r'D:\Airbnb\Final_CSVs')
src = Path.cwd() / 'Compiled_CSVs'
dest = Path(r'D:\Airbnb\Compiled_CSVs')

listing_files = src.glob('*_Combined_Listings.csv.gz')

combined_listings = pd.DataFrame()

for file in listing_files:
    data = pd.read_csv(file, compression='gzip', error_bad_lines=False, dtype={'host_badge':str,'is_hotel': str,'localized_neighborhood':str,'license':str})
    data.drop_duplicates(subset='listing_id', keep='first', inplace=True)
    combined_listings = combined_listings.append(data, ignore_index = True)


print('Shape of Combined Listings 1 :',combined_listings.shape)
combined_listings.drop_duplicates(subset='listing_id', keep='last', inplace=True)
print('Shape of Combined Listings 2 :',combined_listings.shape)

print(combined_listings.groupby('search_location').size())
combined_listings.to_csv (dest / 'Combined_Listings.csv.gz', index = None, header=True, compression='gzip')



review_files = src.glob('*_Combined_Reviews.csv.gz')

rev_subset = ['listing_id','localized_city','review_comments','review_created_at','review_language','review_rating','reviewer_name','reviews_count']

combined_reviews = pd.DataFrame()

for file in review_files:
    data = pd.read_csv(file, compression='gzip', error_bad_lines=False)
    data.drop_duplicates(subset=rev_subset, keep='first', inplace=True)
    combined_reviews = combined_reviews.append(data, ignore_index = True)


print('Shape of Combined Reviews 1 :',combined_reviews.shape)
combined_reviews.drop_duplicates(subset=rev_subset, keep='last', inplace=True)
print('Shape of Combined Reviews 2 :',combined_reviews.shape)

print(combined_reviews.groupby('search_location').size())
combined_reviews.to_csv (dest / 'Combined_Reviews.csv.gz', index = None, header=True, compression='gzip')

