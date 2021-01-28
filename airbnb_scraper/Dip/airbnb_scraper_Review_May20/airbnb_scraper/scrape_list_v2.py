import subprocess
import shutil
import time
from pathlib import Path 
#import glob
#from datetime import datetime
#import os
'''
##### Listings with > 0 Previous Reviews ###########

#end  = 26205

dest = Path.cwd() / 'Scraped_Listings_2'


day = 0 

for i in range (0,26):
    
    start = i*1000+1 + day*50000
    end = start+1000
    
    json_file = str(start) + '_' + str(end-1) + '_v1.json'
    log_file = str(start) + '_' + str(end-1) + '_v1.log'
    
    scrape_cmd = 'scrapy crawl airbnb -o '+json_file+' -a start='+str(start)+' -a end='+str(end)+' -s LOG_FILE='+log_file
    #print(scrape_cmd)
    
    subprocess.run(scrape_cmd, shell='True')
    shutil.move(json_file, dest)
    shutil.move(log_file, dest)
    time.sleep(60)

start = 26001
end = 26205

json_file = str(start) + '_' + str(end-1) + '_v1.json'
log_file = str(start) + '_' + str(end-1) + '_v1.log'

scrape_cmd = 'scrapy crawl airbnb -o '+json_file+' -a start='+str(start)+' -a end='+str(end)+' -s LOG_FILE='+log_file
subprocess.run(scrape_cmd, shell='True')
shutil.move(json_file, dest)
shutil.move(log_file, dest)


'''
##### Listings with 0 Previous Reviews ###########

##### Remember to Change Source file in spider!!!!! #############

day = 0 

dest = Path.cwd() / 'Scraped_Listings_2'

for i in range (0,65):
    
    start = i*1000+1 + day*50000
    end = start+1000
    
    json_file = str(start) + '_' + str(end-1) + '_v2.json'
    log_file = str(start) + '_' + str(end-1) + '_v2.log'
    
    scrape_cmd = 'scrapy crawl airbnb -o '+json_file+' -a start='+str(start)+' -a end='+str(end)+' -s LOG_FILE='+log_file
    #print(scrape_cmd)
    
    subprocess.run(scrape_cmd, shell='True')
    shutil.move(json_file, dest)
    shutil.move(log_file, dest)
    time.sleep(60)

start = 65001
end = 65258

json_file = str(start) + '_' + str(end-1) + '_v2.json'
log_file = str(start) + '_' + str(end-1) + '_v2.log'

scrape_cmd = 'scrapy crawl airbnb -o '+json_file+' -a start='+str(start)+' -a end='+str(end)+' -s LOG_FILE='+log_file
subprocess.run(scrape_cmd, shell='True')
shutil.move(json_file, dest)
shutil.move(log_file, dest)
