#!/bin/sh

SECONDS=0

#CITY="New%20York%"
#Washington %2C %20 DC %2C %20 United %20 States

CITY="Austin"
STATE="TX"

CITY_INPUT="${CITY}%2C%20${STATE}%2C%20United%20States"


for var in `seq 0 10 190`
do

   lower_bound=$var
   upper_bound=`expr $var + 10`


   json_file="${CITY}_${STATE}_${lower_bound}_${upper_bound}.json"
   log_file="${CITY}_${STATE}_${lower_bound}_${upper_bound}.log"

   echo $json_file
   # Run scraper on specific range

   #scrapy crawl airbnb -o $json_file -a city=$CITY -a price_lb=$lower_bound -a price_ub=$upper_bound -s LOG_FILE=$log_file
   #scrapy crawl airbnb -o $json_file -a city=$CITY_INPUT -a price_lb=$lower_bound -a price_ub=$upper_bound -s LOG_FILE=$log_file
   
   #mv $json_file $log_file $CITY
   #sleep 120s
   
   #echo -n "To continue, press [ENTER]:"
   #read

done

for var in `seq 200 25 475`
do

   lower_bound=$var
   upper_bound=`expr $var + 25`


   json_file="${CITY}_${STATE}_${lower_bound}_${upper_bound}.json"
   log_file="${CITY}_${STATE}_${lower_bound}_${upper_bound}.log"

   echo $json_file
   # Run scraper on specific range

   #scrapy crawl airbnb -o $json_file -a city=$CITY -a price_lb=$lower_bound -a price_ub=$upper_bound -s LOG_FILE=$log_file
   #scrapy crawl airbnb -o $json_file -a city=$CITY_INPUT -a price_lb=$lower_bound -a price_ub=$upper_bound -s LOG_FILE=$log_file
   
   #mv $json_file $log_file $CITY
   #sleep 120s
   
   #echo -n "To continue, press [ENTER]:"
   #read

done

for var in `seq 500 100 1000`
do

   lower_bound=$var
   upper_bound=`expr $var + 100`


   json_file="${CITY}_${STATE}_${lower_bound}_${upper_bound}.json"
   log_file="${CITY}_${STATE}_${lower_bound}_${upper_bound}.log"

   echo $json_file
   # Run scraper on specific range

   #scrapy crawl airbnb -o $json_file -a city=$CITY -a price_lb=$lower_bound -a price_ub=$upper_bound -s LOG_FILE=$log_file
   #scrapy crawl airbnb -o $json_file -a city=$CITY_INPUT -a price_lb=$lower_bound -a price_ub=$upper_bound -s LOG_FILE=$log_file
   
   #mv $json_file $log_file $CITY
   #sleep 120s
   
   #echo -n "To continue, press [ENTER]:"
   #read

done

duration=$SECONDS
echo "Time taken : $(($duration / 60)) minutes and $(($duration % 60)) seconds"
