#!/bin/sh

for var in `seq 0 100 800`
do

   lower_bound=$var
   upper_bound=`expr $var + 500`

   # Fixed Variables
   
   #CITY="New%20York%"
   #DATA_LOCATION="New_York"
   
   CITY="Seattle"
   CONJUNCTION="_"
   FORMAT=".json"
   DATA_LOCATION="Seattle"

   filename="$lower_bound$CONJUNCTION$upper_bound$FORMAT"

   # Run scraper on specific range
   scrapy crawl airbnb -o $filename -a city=$CITY -a price_lb=$lower_bound -a price_ub=$upper_bound
   mv $filename $DATA_LOCATION

done


