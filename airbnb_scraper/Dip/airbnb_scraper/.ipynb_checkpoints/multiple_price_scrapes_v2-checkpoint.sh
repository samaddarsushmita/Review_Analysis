#!/bin/sh

SECONDS=0

#caffeinate -i long_running_script.sh
#CITY="New%20York%"
#Washington %2C %20 DC %2C %20 United %20 States

CITY="Austin"
STATE="TX"

CITY_INPUT="${CITY}%2C%20${STATE}%2C%20United%20States"


for interval in 5 10 25 50 100
do 
    #echo $interval
    
    if [ "$interval" -eq 5 ]
    then
      iter_start=0
      iter_end=195
         
    elif [ "$interval" -eq 10 ]
    then 
      iter_start=200
      iter_end=340
         
    elif [ "$interval" -eq 25 ]
    then 
      iter_start=350
      iter_end=725
    elif [ "$interval" -eq 50 ]
    then 
      iter_start=750
      iter_end=1450
      
    else 
      iter_start=1500
      iter_end=2400
    fi
    #echo $iter_start $iter_end $interval

   
    for var in `seq $iter_start $interval $iter_end`
    do

       lower_bound=$var
       upper_bound=`expr $var + $interval`


       json_file="${CITY}_${STATE}_${lower_bound}_${upper_bound}.json"
       log_file="${CITY}_${STATE}_${lower_bound}_${upper_bound}.log"

       #echo $CITY_INPUT $lower_bound $upper_bound
       # Run scraper on specific range

       scrapy crawl airbnb -o $json_file -a city=$CITY_INPUT -a price_lb=$lower_bound -a price_ub=$upper_bound -s LOG_FILE=$log_file

       mv $json_file $log_file "${CITY}_${STATE}"
       sleep 30s

       #echo -n "To continue, press [ENTER]:"
       #read

    done
done

#Above lb = 2500, ub does not matter

scrapy crawl airbnb -o $json_file -a city=$CITY_INPUT -a price_lb=2500 -a price_ub=10000 -s LOG_FILE=$log_file

mv "${CITY}_${STATE}_2000_10000.json" "${CITY}_${STATE}_2000_10000.log" "${CITY}_${STATE}"

duration=$SECONDS
echo "Time taken : $(($duration / 60)) minutes and $(($duration % 60)) seconds"
