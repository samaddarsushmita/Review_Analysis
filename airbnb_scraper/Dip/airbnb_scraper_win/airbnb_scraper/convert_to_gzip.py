import glob
import pandas as pd
from pathlib import Path 
import os
import gzip
import shutil

src = Path(r'D:\Airbnb\Compiled_CSVs')
listing_files = src.glob('*.csv')


for file in listing_files:
    base = os.path.basename(file.name)
    rename = os.path.splitext(base)[0]+'.csv.gz'
    with open(file, 'rb') as f_in:
        with gzip.open(src / rename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


'''
for file in listing_files:
    data = pd.read_csv(file, error_bad_lines=False, dtype={'host_badge':str,'is_hotel': str})
    base = os.path.basename(file.name)
    rename = os.path.splitext(base)[0]+'.csv.gz'
    print(base,rename)
    data.to_csv(src / rename, index = None, header=True, compression='gzip')
'''