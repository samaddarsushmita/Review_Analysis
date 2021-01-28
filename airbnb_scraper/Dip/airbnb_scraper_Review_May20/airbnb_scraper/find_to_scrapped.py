import glob
import pandas as pd
from pathlib import Path 


src = Path.cwd() / 'Combined_Jsons'

all_scrapped = pd.read_csv( src / 'Combined_Reviews_May20.csv.gz', compression='gzip', error_bad_lines=False)

print('Shape of All Scrapped:',all_scrapped.shape)

for index, col in enumerate(all_scrapped.columns): 
    print(index, col)
    
already_scrapped = pd.DataFrame(all_scrapped, columns=["listing_id","reviews_count"])
print(already_scrapped.shape)
already_scrapped.drop_duplicates(keep = 'first', inplace = True)
print(already_scrapped.shape)

already_scrapped.to_csv(src /'Already_Scraped.csv.gz', index=False, header=True, compression='gzip')


all_listings = pd.read_csv( src / 'Review_Scrape_List.csv.gz', compression='gzip', error_bad_lines=False)
print('Shape of All Listings:',all_listings.shape)
all_listings.drop_duplicates(keep = 'first', inplace = True)
print('Shape of All Listings:',all_listings.shape)

to_scrape = all_listings[~all_listings["listing_id"].isin(already_scrapped["listing_id"])]
print('Shape of To Scrape:',to_scrape.shape)
to_scrape.to_csv(src /'To_Scrape.csv.gz', index=False, header=True, compression='gzip')
