import subprocess
import shutil
import time
from pathlib import Path 
#import glob
#from datetime import datetime
#import os


#start = 1
#end  = 327147

dest = Path.cwd() / 'Scraped_Listings'


day = 5 # run this from 0 to 5

for i in range (0,50):
    
    start = i*1000+1 + day*50000
    end = start+1000
    
    json_file = str(start) + '_' + str(end-1) + '.json'
    log_file = str(start) + '_' + str(end-1) + '.log'
    
    scrape_cmd = 'scrapy crawl airbnb -o '+json_file+' -a start='+str(start)+' -a end='+str(end)+' -s LOG_FILE='+log_file
    #print(scrape_cmd)
    
    subprocess.run(scrape_cmd, shell='True')
    shutil.move(json_file, dest)
    shutil.move(log_file, dest)
    time.sleep(60)

'''
day = 6

for i in range (0,27):
    
    start = i*1000+1 + day*50000
    end = start+1000
    
    json_file = str(start) + '_' + str(end-1) + '.json'
    log_file = str(start) + '_' + str(end-1) + '.log'
    
    scrape_cmd = 'scrapy crawl airbnb -o '+json_file+' -a start='+str(start)+' -a end='+str(end)+' -s LOG_FILE='+log_file
    #print(scrape_cmd)
    
    subprocess.run(scrape_cmd, shell='True')
    shutil.move(json_file, dest)
    shutil.move(log_file, dest)
    time.sleep(60)
    
start = 327001
end = 327147

json_file = str(start) + '_' + str(end-1) + '.json'
log_file = str(start) + '_' + str(end-1) + '.log'

scrape_cmd = 'scrapy crawl airbnb -o '+json_file+' -a start='+str(start)+' -a end='+str(end)+' -s LOG_FILE='+log_file
subprocess.run(scrape_cmd, shell='True')
shutil.move(json_file, dest)
shutil.move(log_file, dest)
'''