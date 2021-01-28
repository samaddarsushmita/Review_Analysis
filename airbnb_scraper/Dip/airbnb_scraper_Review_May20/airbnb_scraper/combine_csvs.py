import glob
import pandas as pd
from pathlib import Path 


#src = Path(r'D:\Airbnb\Final_CSVs')
src = Path.cwd() / 'Combined_Jsons'
dest = src

review_files = src.glob('*.csv.gz')

#rev_subset = ['listing_id', 'reviews_count', 'reviewee_deleted', 'reviewee_first_name', 'reviewee_host_name', 'reviewee_id','reviewee_is_superhost', 'review_id', 'review_created_at', 'review_language', 'review_rating', 'review_comments', 'host_response', 'reviewer_deleted', 'reviewer_first_name', 'reviewer_host_name', 'reviewer_id', 'reviewer_is_superhost']

combined_reviews = pd.DataFrame()

for file in review_files:
    print(file)
    data = pd.read_csv(file, compression='gzip', error_bad_lines=False)
    print('Shape : ',data.shape)
    data.drop_duplicates(keep='first', inplace=True)
    print('Shape : ',data.shape)
    combined_reviews = combined_reviews.append(data, ignore_index = True)
    

print('Shape of Combined Reviews 1 : ',combined_reviews.shape)
combined_reviews.drop_duplicates(keep='first', inplace=True)
print('Shape of Combined Reviews 2 :',combined_reviews.shape)

#print(combined_reviews.groupby('search_location').size())
combined_reviews.to_csv (dest / 'Combined_Reviews_May20.csv.gz', index = None, header=True, compression='gzip')

