import json
import collections

with open('seattle.json') as json_file: 
       airbnb = json.load(json_file)

reviews = airbnb[0]['detailed_reviews']

review_dict = collections.defaultdict(dict)
count = 0

for review in reviews:
    review_dict[count]['reviewer_name'] = review.get('reviewer').get('first_name')
    review_dict[count]['review_rating'] = review.get('rating')
    count = count + 1
    
print(count)


calendar_yr = airbnb[0]['calendar']

calendar = []

for month in calendar_yr:
    day_count = 0
    
    for day in month.get('days'):
        if(day.get('available')):
            day_count = day_count + 1
    
    calendar.append(day_count)
    
print(calendar)