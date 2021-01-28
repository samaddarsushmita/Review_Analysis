import subprocess
import shutil
import time

city = "Miami"
state = "FL"

city_input=city+'%2C%20'+state+'%2C%20United%20States'

for interval in [5]:
    
    if(interval == 5):
        iter_start = 0
        iter_end = 15    
        
    elif(interval == 10):
        iter_start = 200
        iter_end = 350
        
    elif(interval == 25):
        iter_start = 350
        iter_end = 750
        
    elif(interval == 50):
        iter_start = 750
        iter_end = 1500
        
    else:
        iter_start = 1500
        iter_end = 2500
        
        
    for lower_bound in range(iter_start, iter_end, interval):
        
        upper_bound = lower_bound + interval
        
        json_file = city + '_' + state + '_' + str(lower_bound) + '_' + str(upper_bound) + '.json'
        log_file = city + '_' + state + '_' + str(lower_bound) + '_' + str(upper_bound) + '.log'
        
        scrape_cmd = 'scrapy crawl airbnb -o '+json_file+' -a city='+city_input+' -a price_lb='+str(lower_bound)+' -a price_ub='+str(upper_bound)+' -s LOG_FILE='+log_file
        
        subprocess.run(scrape_cmd, shell='True')
        shutil.move(json_file, city+'_'+state)
        shutil.move(log_file, city+'_'+state)
        time.sleep(15)
        
        
json_file = city + '_' + state + '_2500_10000.json'
log_file = city + '_' + state + '_2500_10000.log'
        
scrape_cmd = 'scrapy crawl airbnb -o '+json_file+' -a city='+city_input+' -a price_lb=2500 -a price_ub=10000 -s LOG_FILE='+log_file
        
subprocess.run(scrape_cmd, shell='True')
shutil.move(json_file, city+'_'+state)
shutil.move(log_file, city+'_'+state)
time.sleep(15)
        
        
        
        
        
        
