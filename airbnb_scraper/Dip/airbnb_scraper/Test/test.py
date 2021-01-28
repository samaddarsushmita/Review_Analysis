import json
import collections

with open('23468602_Details.json') as json_file: 
       airbnb = json.load(json_file)
        

features =  airbnb.get('pdp_listing_detail').get('highlights') 

print(type(features),len(features))
highlight = ''

for i in range(0,len(features)):
    print(features[i])
    #print(feature.get('message'))
    highlight = highlight + features[i].get('message') + ' '
        
print('*******************'+highlight.strip()+'***************')

